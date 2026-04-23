from pydantic import BaseModel
from datetime import date
from typing import Optional, Dict, Any

class ActivityCreate(BaseModel):
    activity_no: str
    title: str
    wing: str
    type: str                    # "RFB" or "INDV"
    status: Optional[str] = "Planning"
    wb_nol_date: Optional[date] = None
    contract_date: Optional[date] = None
    estimated_cost: Optional[float] = None
    award_method: Optional[str] = None
    publication_date: Optional[date] = None
    milestones: Dict[str, Any] = {}   # All other fields from Excel

class DeliverableCreate(BaseModel):
    contract_number: str
    deliverable_name: str
    description: Optional[str] = None
    due_date: date
    actual_submission_date: Optional[date] = None
    approval_date: Optional[date] = None
    payment_due: float = 0.0
    payment_released: Optional[float] = 0.0
    status: Optional[str] = "Pending"

class UtilizationCreate(BaseModel):
    year: int
    quarter: int
    percentage: float
    resources_used: Optional[str] = None
    notes: Optional[str] = None

class UtilizationUpdate(BaseModel):
    percentage: Optional[float] = None
    resources_used: Optional[str] = None
    notes: Optional[str] = None

class PlanCreate(BaseModel):
    name: str
    reference_no: Optional[str] = None
    category: Optional[str] = None
    amount_usd: Optional[float] = None
    method: Optional[str] = None
    wing: Optional[str] = None
    planned_start: Optional[date] = None
    planned_end: Optional[date] = None
    

class PlanResponse(PlanCreate):
    id: int

    class Config:
        from_attributes = True