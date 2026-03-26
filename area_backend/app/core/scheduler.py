from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import not_
from app.database import SessionLocal
from app.models.area import Area
from app.core.hook_engine import execute_area

scheduler = BackgroundScheduler()


def poll_areas():
    db = SessionLocal()
    areas = db.query(Area).filter(
        Area.is_active,
        not_(Area.action.like("timer.%"))
    ).all()

    area_ids = [area.id for area in areas]
    db.close()

    for area_id in area_ids:
        execute_area(area_id)


def restore_timer_jobs():
    db = SessionLocal()
    timer_areas = db.query(Area).filter(
        Area.is_active,
        Area.action.like("timer.%")
    ).all()

    for area in timer_areas:
        add_timer_job(area)

    db.close()


def add_timer_job(area):
    seconds = 60

    if area.action == "timer.every_minute":
        seconds = 60
    elif area.action == "timer.every_hour":
        seconds = 3600
    elif area.action == "timer.every_day":
        seconds = 86400
    elif area.action == "timer.custom_interval":
        seconds = int(area.action_params.get("interval", 60))
        if seconds < 10:
            seconds = 10

    job_id = f"area_{area.id}"

    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)

    scheduler.add_job(
        execute_area,
        "interval",
        seconds=seconds,
        args=[area.id],
        id=job_id,
        replace_existing=True
    )
    print(f"[SCHEDULER] Job added for Area {area.id} (Interval: {seconds}s)")


def remove_timer_job(area_id):
    job_id = f"area_{area_id}"
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
        print(f"[SCHEDULER] Job removed for Area {area_id}")


def start_scheduler():
    scheduler.add_job(poll_areas, "interval", seconds=30)
    restore_timer_jobs()
    scheduler.start()
