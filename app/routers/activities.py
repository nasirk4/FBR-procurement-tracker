from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import ProcurementActivity
from app.dependencies import get_db

router = APIRouter(redirect_slashes=False)

@router.get("")
def get_activities(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    activities = db.query(ProcurementActivity).offset(skip).limit(limit).all()
    return activities

@router.get("/{activity_no}")
def get_activity(activity_no: str, db: Session = Depends(get_db)):
    activity = db.query(ProcurementActivity).filter(ProcurementActivity.activity_no == activity_no).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity
