from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import ContractDeliverable, ProcurementActivity
from datetime import date
from app.dependencies import get_db

router = APIRouter(redirect_slashes=False)

def validate_deliverable_dates(db: Session, deliverable_data: dict, contract_number: str):
    activity = db.query(ProcurementActivity).filter(ProcurementActivity.activity_no == contract_number).first()
    if not activity or not activity.contract_date:
        raise HTTPException(status_code=400, detail="Contract award date not found. Please set contract_date first.")
    
    award_date = activity.contract_date

    if deliverable_data.get("due_date") and deliverable_data["due_date"] < award_date:
        raise HTTPException(status_code=400, detail=f"Due date cannot be before award date ({award_date})")
    
    if deliverable_data.get("actual_submission_date") and deliverable_data["actual_submission_date"] < award_date:
        raise HTTPException(status_code=400, detail=f"Actual submission date cannot be before award date ({award_date})")
    
    if deliverable_data.get("approval_date") and deliverable_data["approval_date"] < award_date:
        raise HTTPException(status_code=400, detail=f"Approval date cannot be before award date ({award_date})")
    
    return True

@router.get("")
def get_all_deliverables(db: Session = Depends(get_db)):
    return db.query(ContractDeliverable).all()

@router.post("/")
def create_deliverable(deliverable: dict, db: Session = Depends(get_db)):
    validate_deliverable_dates(db, deliverable, deliverable["contract_number"])
    new_deliverable = ContractDeliverable(**deliverable)
    db.add(new_deliverable)
    db.commit()
    db.refresh(new_deliverable)
    return new_deliverable
