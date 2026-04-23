from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import ContractDeliverable, ProcurementActivity
from datetime import date, datetime
from app.dependencies import get_db
from app.schemas import DeliverableCreate

router = APIRouter(redirect_slashes=False)

def parse_date(val):
    """Convert string or date to date object."""
    if val is None:
        return None
    if isinstance(val, date):
        return val
    if isinstance(val, str):
        return datetime.strptime(val, "%Y-%m-%d").date()
    raise ValueError("Invalid date format")

def validate_deliverable_dates(db: Session, data: dict, contract_number: str):
    activity = db.query(ProcurementActivity).filter(ProcurementActivity.activity_no == contract_number).first()
    if not activity or not activity.contract_date:
        raise HTTPException(status_code=400, detail="Contract award date not found. Please set contract_date first.")
    
    award_date = activity.contract_date

    due = parse_date(data.get("due_date"))
    if due and due < award_date:
        raise HTTPException(status_code=400, detail=f"Due date cannot be before award date ({award_date})")
    
    actual = parse_date(data.get("actual_submission_date"))
    if actual and actual < award_date:
        raise HTTPException(status_code=400, detail=f"Actual submission date cannot be before award date ({award_date})")
    
    approval = parse_date(data.get("approval_date"))
    if approval and approval < award_date:
        raise HTTPException(status_code=400, detail=f"Approval date cannot be before award date ({award_date})")
    
    return True

@router.get("")
def get_all_deliverables(db: Session = Depends(get_db)):
    return db.query(ContractDeliverable).all()

@router.post("")
def create_deliverable(deliverable: DeliverableCreate, db: Session = Depends(get_db)):
    # Convert Pydantic model to dict
    data = deliverable.dict()
    validate_deliverable_dates(db, data, deliverable.contract_number)
    new_deliverable = ContractDeliverable(**data)
    db.add(new_deliverable)
    db.commit()
    db.refresh(new_deliverable)
    return new_deliverable