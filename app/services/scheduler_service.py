from apscheduler.schedulers.background import BackgroundScheduler

from app.jobs.scan_task import ScanTask
from app.models.user_scan_schedules import ScheduleType
from app.repositories.unit_of_work import UnitOfWork
from app.schemas.user_schedule_create import ScheduleCreate

scheduler = BackgroundScheduler(timezone="UTC")
scheduler.start()

class ScheduleService:

    def start_scheduler(self, schedule: ScheduleCreate):
        try:
            args = [str(schedule.id), str(schedule.user_scan_id)]
            job_id = str(schedule.id)

            if schedule.schedule_type == ScheduleType.date:
                scheduler.add_job(
                    self.run_scan_task,
                    trigger="date",
                    run_date=schedule.run_date,
                    args=args,
                    id=job_id,
                    name=schedule.name,
                )
            elif schedule.schedule_type == ScheduleType.interval:
                scheduler.add_job(
                    self.run_scan_task,
                    trigger="interval",
                    seconds=schedule.interval_seconds or 0,
                    minutes=schedule.interval_minutes or 0,
                    hours=schedule.interval_hours or 0,
                    args=args,
                    id=job_id,
                    name=schedule.name,
                )
            elif schedule.schedule_type == ScheduleType.cron:
                scheduler.add_job(
                    self.run_scan_task,
                    trigger="cron",
                    second=schedule.cron_second or "0",
                    minute=schedule.cron_minute or "0",
                    hour=schedule.cron_hour or "*",
                    day=schedule.cron_day or "*",
                    month=schedule.cron_month or "*",
                    day_of_week=schedule.cron_day_of_week or "*",
                    args=args,
                    id=job_id,
                    name=schedule.name,
                )
        except Exception as e:
            print(f"Error starting scheduler: {e}")

    def load_schedules_from_db(self, uow: UnitOfWork):
        schedules = uow.schedule_repo.get_all_enabled()
        for schedule in schedules:
            self.start_scheduler(schedule)

    def run_scan_task(self, schedule_id: str, user_scan_id: str):
        task = ScanTask(schedule_id, user_scan_id)
        task.execute()