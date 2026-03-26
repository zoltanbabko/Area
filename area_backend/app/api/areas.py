from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.area import Area
from app.api.dependencies import get_current_user
from app.core.scheduler import add_timer_job, remove_timer_job

router = APIRouter(prefix="/areas", tags=["areas"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _handle_scheduler_update(area: Area, need_update: bool):
    if not need_update:
        return

    is_timer = area.action.startswith("timer.")

    if is_timer:
        if area.is_active:
            add_timer_job(area)
        else:
            remove_timer_job(area.id)
    else:
        remove_timer_job(area.id)


@router.post("/")
def create_area(area: dict, user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not area.get("name") or not area.get("action") or not area.get("reaction"):
        raise HTTPException(status_code=400, detail="Missing required fields")

    new_area = Area(
        user_id=user.id,
        name=area["name"],
        action=area["action"],
        reaction=area["reaction"],
        action_params=area.get("action_params", {}),
        reaction_params=area.get("reaction_params", {}),
        is_active=True
    )
    db.add(new_area)
    db.commit()
    db.refresh(new_area)

    if new_area.action.startswith("timer."):
        add_timer_job(new_area)

    return new_area


@router.get("/")
def list_areas(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Area).filter(Area.user_id == user.id).all()


@router.get("/{area_id}")
def get_area(area_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    area = db.query(Area).filter(Area.id == area_id, Area.user_id == user.id).first()
    if not area:
        raise HTTPException(status_code=404, detail="Area not found")
    return area


@router.delete("/{area_id}")
def delete_area(area_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    area = db.query(Area).filter(Area.id == area_id, Area.user_id == user.id).first()
    if not area:
        raise HTTPException(status_code=404, detail="Area not found")

    if area.action.startswith("timer."):
        remove_timer_job(area.id)

    db.delete(area)
    db.commit()
    return {"status": "deleted", "id": area_id}


@router.patch("/{area_id}")
def update_area(area_id: int, payload: dict, user=Depends(get_current_user), db: Session = Depends(get_db)):
    area = db.query(Area).filter(Area.id == area_id, Area.user_id == user.id).first()
    if not area:
        raise HTTPException(status_code=404, detail="Area not found")

    updatable_fields = [
        "name", "is_active", "action", "reaction",
        "action_params", "reaction_params"
    ]

    for field in updatable_fields:
        if field in payload:
            setattr(area, field, payload[field])

    db.commit()
    db.refresh(area)

    scheduler_triggers = ["is_active", "action", "action_params"]
    need_job_update = any(key in payload for key in scheduler_triggers)

    _handle_scheduler_update(area, need_job_update)

    return area
