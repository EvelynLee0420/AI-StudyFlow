import datetime
import json  # 用於儲存和載入使用者資料 (可以替換為資料庫)

class User:
    """使用者類別，儲存使用者的個人資訊和學習習慣。"""
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.learning_habits = {}  # 例如：偏好的筆記格式、專注時長等
        self.study_preferences = {} # 例如：希望加強的科目、題型
        self.notes = {}           # 儲存筆記，key 可以是科目或主題
        self.study_schedule = {}  # 儲存學習進度計畫

    def update_learning_habits(self, habit, value):
        """更新使用者的學習習慣。"""
        self.learning_habits[habit] = value

    def update_study_preferences(self, preference, value):
        """更新使用者的學習偏好。"""
        self.study_preferences[preference] = value

    def add_note(self, subject, content):
        """新增筆記。"""
        if subject not in self.notes:
            self.notes[subject] = []
        self.notes[subject].append({"timestamp": datetime.datetime.now().isoformat(), "content": content})

    def get_notes_by_subject(self, subject):
        """取得特定科目的所有筆記。"""
        return self.notes.get(subject, [])

    def add_study_task(self, task, deadline, details=None):
        """新增學習任務到排程。"""
        self.study_schedule[task] = {"deadline": deadline, "details": details, "completed": False}

    def mark_task_completed(self, task):
        """標記學習任務為已完成。"""
        if task in self.study_schedule:
            self.study_schedule[task]["completed"] = True

    def get_upcoming_tasks(self):
        """取得未來的學習任務。"""
        upcoming_tasks = {}
        now = datetime.datetime.now()
        for task, details in self.study_schedule.items():
            deadline_dt = datetime.datetime.fromisoformat(details['deadline'])
            if not details['completed'] and deadline_dt > now:
                upcoming_tasks[task] = details
        return upcoming_tasks

    def to_dict(self):
        """將使用者資料轉換為字典，方便儲存。"""
        return {
            "user_id": self.user_id,
            "name": self.name,
            "learning_habits": self.learning_habits,
            "study_preferences": self.study_preferences,
            "notes": self.notes,
            "study_schedule": self.study_schedule
        }

    @staticmethod
    def from_dict(data):
        """從字典建立使用者物件。"""
        user = User(data['user_id'], data['name'])
        user.learning_habits = data.get('learning_habits', {})
        user.notes = data.get('notes', {})
        user.study_schedule = data.get('study_schedule', {})
        return user

class NoteOrganizer:
    """筆記整理器類別，負責處理筆記的統整和結構化。"""
    def summarize_note(self, note_content):
        """使用 AI 模型總結筆記內容 (這裡只是 placeholder)。"""
        # TODO: 整合 AI 模型進行筆記摘要
        return f"【AI摘要】{note_content[:50]}..."

    def structure_note(self, note_content):
        """使用 AI 模型將筆記結構化 (這裡只是 placeholder)。"""
        # TODO: 整合 AI 模型進行筆記結構化，例如提取關鍵字、建立層級結構
        return {"main_points": [note_content[:30], note_content[30:60]], "keywords": [note_content[:10], note_content[20:30]]}

    def generate_knowledge_map(self, structured_notes):
        """根據結構化筆記產生知識結構圖 (這裡只是 placeholder)。"""
        # TODO: 實作知識結構圖的生成邏輯，可能需要圖形資料庫或視覺化函式庫
        return {"nodes": list(structured_notes.keys()), "edges": []}

class StudyScheduler:
    """學習排程器類別，負責根據使用者需求和學習習慣安排進度。"""
    def plan_schedule(self, user, available_time, focused_time, important_subjects, exam_date=None, subjects_per_day=2):
        """根據使用者提供的資訊規劃學習進度。"""
        schedule = {}
        # 確保 available_time 不是空的
        if not available_time:
            print("警告：沒有可用的讀書時間。")
            return schedule

        if not important_subjects:
            print("警告：沒有重要的科目。")
            return schedule

        daily_schedule = {}
        for day, hours in available_time.items():
            daily_schedule[day] = []
            if hours > 0:
                if subjects_per_day > len(important_subjects):
                    subjects_per_day = len(important_subjects)
                time_per_subject = hours / subjects_per_day
                for i in range(subjects_per_day):
                    subject_index = (list(available_time.keys()).index(day) + i) % len(important_subjects)
                    subject = important_subjects[subject_index]
                    daily_schedule[day].append({subject: time_per_subject})
            else:
                 daily_schedule[day].append({"休息": 0})

        schedule = daily_schedule

        if exam_date:
            days_until_exam = (datetime.datetime.strptime(exam_date, '%Y-%m-%d') - datetime.datetime.now()).days
            schedule['複習'] = {"start_day": f"考前 {days_until_exam} 天"}
        return schedule

    def suggest_review_schedule(self, notes):
        """根據筆記內容建議複習進度 (這裡只是 placeholder)。"""
        # TODO: 實作根據筆記內容和時間戳記建議複習的邏輯
        review_items = {}
        for subject, note_list in notes.items():
            # 簡單地建議複習最近的筆記
            if note_list:
                latest_note_time = max(n['timestamp'] for n in note_list)
                review_items[subject] = f"建議複習 {datetime.datetime.fromisoformat(latest_note_time).strftime('%Y-%m-%d')} 的筆記"
        return review_items

class Personalizer:
    """個人化調整器類別，根據使用者習慣調整筆記格式和學習進度。"""
    def adjust_note_format(self, note_content, preferred_format):
        """根據使用者偏好調整筆記格式 (這裡只是簡單的範例)。"""
        if preferred_format == "bullet_points":
            return "- " + "\n- ".join(note_content.split('\n'))
        elif preferred_format == "mind_map_keywords":
            # TODO: 更複雜的格式轉換
            structured_note = NoteOrganizer().structure_note(note_content) # 創建 NoteOrganizer 的實例
            if structured_note and 'keywords' in structured_note:
                return f"【關鍵字】{', '.join(structured_note['keywords'])}"
            else:
                return "【關鍵字】 無"
        return note_content

    def adjust_schedule(self, study_schedule, user_habits):
        """根據使用者習慣調整學習進度 (這裡只是簡單的範例)。"""
        adjusted_schedule = study_schedule.copy()
        if user_habits.get("preferred_study_time") == "morning":
            for day, subjects in adjusted_schedule.items():
                if day != '複習':  # 確保我們不在處理複習的特殊情況
                    for item in subjects:
                        for subject, time in item.items():
                            adjusted_schedule[day] = [{"[早上] " + k: v for k, v in item.items()} for item in subjects]
                else:
                    adjusted_schedule[day] = f"[早上] {adjusted_schedule[day]}"
        return adjusted_schedule

class SmartNoteApp:
    """智慧筆記助手應用程式的核心類別。"""
    def __init__(self):
        self.users = {}
        self.note_organizer = NoteOrganizer() # 創建 NoteOrganizer 的實例
        self.study_scheduler = StudyScheduler() # 創建 StudyScheduler 的實例
        self.personalizer = Personalizer()   # 創建 Personalizer 的實例
        self.data_file = "user_data.json" # 用於簡單儲存使用者資料

    def register_user(self, user_id, name):
        """註冊新使用者。"""
        if user_id not in self.users:
            self.users[user_id] = User(user_id, name)
            self.save_data()
            return self.users[user_id]
        return self.users[user_id]

    def get_user(self, user_id):
        """取得使用者物件。"""
        return self.users.get(user_id)

    def process_voice_note(self, user_id, audio_data):
        """處理語音筆記 (這裡只是 placeholder)。"""
        # TODO: 整合語音辨識技術將音訊轉為文字
        transcribed_text = f"【語音轉文字】{audio_data[:80]}..."
        subject = input("請輸入筆記的科目：")
        self.add_note(user_id, subject, transcribed_text)

    def add_note(self, user_id, subject, content):
        """新增筆記。"""
        user = self.get_user(user_id)
        if user:
            user.add_note(subject, content)
            self.save_data()

    def get_notes(self, user_id, subject):
        """取得特定使用者的特定科目筆記。"""
        user = self.get_user(user_id)
        return user.get_notes_by_subject(subject) if user else []

    def summarize_note(self, user_id, subject):
        """總結特定使用者的特定科目筆記 (這裡只總結最新的)。"""
        user = self.get_user(user_id)
        if user and user.get_notes_by_subject(subject):
            latest_note = user.get_notes_by_subject(subject)[-1]['content']
            return self.note_organizer.summarize_note(latest_note)
        return "沒有相關筆記。"

    def get_structured_note(self, user_id, subject):
        """取得特定使用者特定科目結構化後的筆記 (這裡只結構化最新的)。"""
        user = self.get_user(user_id)
        if user and user.get_notes_by_subject(subject):
            latest_note = user.get_notes_by_subject(subject)[-1]['content']
            return self.note_organizer.structure_note(latest_note)
        return "沒有相關筆記。"

    def plan_study_schedule(self, user_id, available_time, focused_time, important_subjects, exam_date=None, subjects_per_day=2):
        """為使用者規劃學習進度。"""
        user = self.get_user(user_id)
        if user:
            schedule = self.study_scheduler.plan_schedule(user, available_time, focused_time, important_subjects, exam_date, subjects_per_day)
            user.study_schedule = schedule
            self.save_data()
            return schedule
        return {}

    def get_study_schedule(self, user_id):
        """取得使用者的學習進度。"""
        user = self.get_user(user_id)
        return user.study_schedule if user else {}

    def get_upcoming_tasks(self, user_id):
        """取得使用者即將到來的學習任務。"""
        user = self.get_user(user_id)
        return user.get_upcoming_tasks() if user else {}

    def get_review_suggestions(self, user_id):
        """取得使用者的複習建議。"""
        user = self.get_user(user_id)
        return self.study_scheduler.suggest_review_schedule(user.notes) if user else {}

    def update_learning_habits(self, user_id, habit, value):
        """更新使用者的學習習慣。"""
        user = self.get_user(user_id)
        if user:
            user.update_learning_habits(habit, value)
            self.save_data()

    def update_study_preferences(self, user_id, preference, value):
        """更新使用者的學習偏好。"""
        user = self.get_user(user_id)
        if user:
            user.update_study_preferences(preference, value)
            self.save_data()

    def adjust_note_format(self, user_id, subject, preferred_format):
        """根據使用者偏好調整特定科目筆記的格式 (這裡只調整最新的)。"""
        user = self.get_user(user_id)
        if user and user.get_notes_by_subject(subject):
            latest_note_index = len(user.get_notes_by_subject(subject)) - 1
            original_content = user.get_notes_by_subject(subject)[latest_note_index]['content']
            formatted_content = self.personalizer.adjust_note_format(original_content, preferred_format)
            user.get_notes_by_subject(subject)[latest_note_index]['content'] = formatted_content
            self.save_data()
            return formatted_content
        return "沒有相關筆記。"

    def adjust_study_schedule(self, user_id):
        """根據使用者習慣調整學習進度。"""
        user = self.get_user(user_id)
        if user:
            adjusted_schedule = self.personalizer.adjust_schedule(user.study_schedule, user.learning_habits)
            user.study_schedule = adjusted_schedule
            self.save_data()
            return adjusted_schedule
        return {}

    def save_data(self):
        """將使用者資料儲存到檔案 (簡單的資料持久化)。"""
        data = {user_id: user.to_dict() for user_id, user in self.users.items()}
        try:
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"儲存資料失敗: {e}")

    def load_data(self):
        """從檔案載入使用者資料。"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.users = {user_id: User.from_dict(user_data) for user_id, user_data in data.items()}
        except FileNotFoundError:
            print("使用者資料檔案未找到，將創建一個新的。")
            self.users = {}
        except json.JSONDecodeError:
            print("使用者資料檔案格式錯誤，將創建一個新的。")
            self.users = {}

    def get_user_available_time(self):
        """獲取使用者一周每天可用的讀書時間。"""
        available_time = {}
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for day in days:
            while True:
                try:
                    hours = int(input(f"請輸入您{day}可用的讀書時數："))
                    if 0 <= hours <= 24:
                        available_time[day] = hours
                        break
                    else:
                        print("請輸入 0 到 24 之間的有效時數。")
                except ValueError:
                    print("輸入無效，請輸入一個數字。")
        return available_time

    def get_study_time_for_subject(self, available_time, important_subjects):
        """
        Calculates the study time for each subject based on available time and number of subjects.

        Args:
            available_time (dict): A dictionary representing the available time for each day of the week.
            important_subjects (list): A list of important subjects.

        Returns:
            dict: A dictionary containing the study time for each subject, распределенное по дням.
                  Если important_subjects пуст, возвращает словарь с нулевым временем для каждого дня.
        """
        study_time_per_subject = {}
        if not important_subjects:
            for day in available_time:
                study_time_per_subject[day] = 0
            return study_time_per_subject

        total_available_time = sum(available_time.values())
        hours_per_subject = total_available_time / len(important_subjects)

        for day, hours in available_time.items():
            # Distribute time, ensuring no negative values
            study_time_per_subject[day] = min(hours, hours_per_subject)

        return study_time_per_subject
    
# --- 測試程式 ---
if __name__ == "__main__":
    app = SmartNoteApp()
    app.load_data() # 載入已儲存的資料

    # 註冊一個新使用者
    user1 = app.register_user("student123", "小明")
    print(f"註冊使用者：{user1.name} (ID: {user1.user_id})")

    # 新增筆記
    app.add_note("student123", "數學", "今天學了微積分的基本定理，需要多練習相關題目。")
    app.add_note("student123", "數學", "複習了三角函數的公式。")
    app.add_note("student123", "物理", "學習了牛頓三大運動定律。")  # 新增物理筆記
    app.add_note("student123", "英文", "學習了現在完成式的用法。")  # 新增英文筆記

    # 取得數學筆記
    math_notes = app.get_notes("student123", "數學")
    print("\n數學筆記：")
    for note in math_notes:
        print(f"- {note['timestamp']}: {note['content']}")

    # 總結最新的數學筆記
    summary = app.summarize_note("student123", "數學")
    print(f"\n最新數學筆記摘要：{summary}")

    # 取得結構化後的最新筆記
    structured_note_math = app.get_structured_note("student123", "數學") # 取得數學結構化筆記
    print(f"\n最新數學筆記結構：{structured_note_math}")
    structured_note_physics = app.get_structured_note("student123", "物理") # 取得物理結構化筆記
    print(f"\n最新物理筆記結構：{structured_note_physics}")
    structured_note_english = app.get_structured_note("student123", "英文") # 取得英文結構化筆記
    print(f"\n最新英文筆記結構：{structured_note_english}")

    # 更新學習習慣
    app.update_learning_habits("student123", "preferred_note_format", "bullet_points")
    app.update_learning_habits("student123", "preferred_study_time", "morning")

    # 調整最新數學筆記的格式
    formatted_note = app.adjust_note_format("student123", "數學", "bullet_points")
    print(f"\n調整格式後的最新數學筆記：\n{formatted_note}")

    # 獲取使用者可用的讀書時間
    available_time = app.get_user_available_time()

    # 規劃學習進度
    # available_time = {"Monday": 1, "Tuesday": 2, "Wednesday": 4, "Thursday": 1, "Friday": 2, "Saturday": 3, "Sunday": 4}
    focused_time = 60 # 分鐘
    important_subjects = ["數學", "英文", "物理"]
    exam_date = "2025-06-15"
    subjects_per_day = int(input("請問您偏好一天學習幾個科目？ (1-3): "))
    study_schedule = app.plan_study_schedule("student123", available_time, focused_time, important_subjects, exam_date, subjects_per_day)
    print("\n初始學習進度：")
    for day, subjects in study_schedule.items():
        if day != '複習':
            print(f"{day}:")
            for item in subjects:
                for subject, time in item.items():
                    print(f"  {subject}: {time:.1f} 小時")
        else:
            print(f"{day}: {subjects['start_day']}")

    # 取得調整後的學習進度
    adjusted_schedule = app.adjust_study_schedule("student123")
    print("\n調整後的學習進度：")
    for day, subjects in adjusted_schedule.items():
        if day != '複習':
            print(f"{day}:")
            for item in subjects:
                for subject, time in item.items():
                    print(f"  {subject}: {time:.1f} 小時")
        else:
            print(f"{day}: {subjects['start_day']}")

    # 取得即將到來的任務
    upcoming_tasks = app.get_upcoming_tasks("student123")
    print("\n即將到來的任務：")
    if upcoming_tasks:
        for task, details in upcoming_tasks.items():
            print(f"{task}: Deadline - {datetime.datetime.fromisoformat(details['deadline']).strftime('%Y-%m-%d %H:%M')}, Details - {details['details']}")
    else:
        print("沒有即將到來的任務。")

    # 取得複習建議
    review_suggestions = app.get_review_suggestions("student123")
    print("\n複習建議：")
    for subject, suggestion in review_suggestions.items():
        print(f"{subject}: {suggestion}")

    # 測試語音筆記 (需要使用者輸入)
    # audio_data = "今天天氣晴朗，我們學習了如何使用語音辨識技術來記錄筆記，這節課非常有趣。"
    # app.process_voice_note("student123", audio_data)
    # print("\n語音筆記已處理。")

    # 再次取得數學筆記，確認語音筆記是否成功加入
    math_notes_after_voice = app.get_notes("student123", "數學")
    print("\n數學筆記 (包含語音筆記)：")
    for note in math_notes_after_voice:
        print(f"- {note['timestamp']}: {note['content']}")

    app.save_data()  # 保存資料
