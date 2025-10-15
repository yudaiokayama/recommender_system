class MockFetcher:
    """
    ManagerAPIのダミー。
    ローカルテスト用に固定のデータを返す。
    """
    def get_student_profile(self, student_id):
        print(f"Fetching profile for student: {student_id}")
        return {'student_id': student_id, 'name': 'Dummy Student'}

    def get_candidate_problems(self, student_id):
        print(f"Fetching candidate problems for student: {student_id}")
        return [{'id': 'problem_1'}, {'id': 'problem_2'}, {'id': 'problem_3'}]

class MockStorage:
    """
    Redis/Postgresのダミー。
    ローカルテスト用に何もしないか、printするだけ。
    """
    def get_recent_events(self, student_id):
        print(f"Getting recent events for student: {student_id}")
        return []

    def push_event(self, event):
        print(f"Received event: {event}")
        # In a real scenario, this would write to Redis/DB.
        pass
