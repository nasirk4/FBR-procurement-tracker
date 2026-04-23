from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db
from app.models import ProcurementPlan
from app.schemas import PlanCreate, PlanResponse

router = APIRouter(
    prefix="/plans",
    tags=["plans"],
    redirect_slashes=False
)

@router.get("", response_model=List[PlanResponse])
def get_plans(db: Session = Depends(get_db)):
    """Get all procurement plans"""
    plans = db.query(ProcurementPlan).all()
    return plans

@router.post("", response_model=PlanResponse)
def create_plan(plan: PlanCreate, db: Session = Depends(get_db)):
    """Create a new procurement plan"""
    db_plan = ProcurementPlan(**plan.dict())
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan