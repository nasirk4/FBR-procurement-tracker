from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import ProcurementActivity
from app.dependencies import get_db
from app.schemas import ActivityCreate

router = APIRouter()

@router.get("")
def get_activities(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    activities = db.query(ProcurementActivity).offset(skip).limit(limit).all()
    return activities

@router.post("")
def create_activity(activity: ActivityCreate, db: Session = Depends(get_db)):
    existing = db.query(ProcurementActivity).filter(ProcurementActivity.activity_no == activity.activity_no).first()
    if existing:
        raise HTTPException(status_code=400, detail="Activity number already exists")

    new_activity = ProcurementActivity(
        activity_no=activity.activity_no,
        title=activity.title,
        wing=activity.wing,
        type=activity.type,
        status=activity.status,
        wb_nol_date=activity.wb_nol_date,
        contract_date=activity.contract_date,
        estimated_cost=activity.estimated_cost,
        award_method=activity.award_method,
        publication_date=activity.publication_date,
        milestones=activity.milestones
    )
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    return new_activity
