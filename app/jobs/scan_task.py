from app.jobs.base_task import BaseTask

class ScanTask(BaseTask):
    def __init__(self, schedule_id: str, user_scan_id: str):
        self.schedule_id = schedule_id
        self.user_scan_id = user_scan_id

    def execute(self):
        print(f"🔍 Executing ScanTask: schedule_id={self.schedule_id}, user_scan_id={self.user_scan_id}")