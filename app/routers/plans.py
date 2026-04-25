from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db
from app.models import ProcurementPlan
from app.schemas import PlanCreate, PlanResponse, PlanUpdate

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

@router.patch("/{plan_id}")
def update_plan(plan_id: int, update: PlanUpdate, db: Session = Depends(get_db)):
    plan = db.query(ProcurementPlan).filter(ProcurementPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(404, "Plan not found")
    for field, value in update.dict(exclude_unset=True).items():
        setattr(plan, field, value)
    db.commit()
    return plan

@router.delete("/{plan_id}")
def delete_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(ProcurementPlan).filter(ProcurementPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(404, "Plan not found")
    db.delete(plan)
    db.commit()
    return {"message": "Deleted"}

@router.get("/{plan_id}")
def get_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(ProcurementPlan).filter(ProcurementPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(404, "Plan not found")
    return plan