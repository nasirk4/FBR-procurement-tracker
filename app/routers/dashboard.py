from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import ProcurementActivity, ContractDeliverable
from app.dependencies import get_db

router = APIRouter()

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_activities = db.query(ProcurementActivity).count()
    total_deliverables = db.query(ContractDeliverable).count()
    
    return {
        "total_activities": total_activities,
        "total_deliverables": total_deliverables,
        "message": "Dashboard stats - more KPIs will be added in next phase"
    }
