from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import ProcurementActivity, ContractDeliverable, Utilization
from app.dependencies import get_db
from datetime import date

router = APIRouter(redirect_slashes=False)

@router.get("/advanced")
def get_advanced_stats(db: Session = Depends(get_db)):
    # 1. Cost of activities under procurement (not yet contracted)
    under_procurement = db.query(func.sum(ProcurementActivity.estimated_cost)).filter(
        ProcurementActivity.contract_date.is_(None),
        ProcurementActivity.status != "Cancelled"
    ).scalar() or 0

    # 2. Total contract value of signed contracts (contract_date exists)
    #    Use actual contract_value if available, else estimated_cost
    signed_activities = db.query(ProcurementActivity).filter(
        ProcurementActivity.contract_date.isnot(None)
    ).all()
    total_contract_value = sum(
        (act.contract_value or act.estimated_cost or 0) for act in signed_activities
    )

    # 3. Activities in the pipeline (from Plans – we don't have plans yet, use activities with status 'Planning')
    pipeline_activities = db.query(ProcurementActivity).filter(
        ProcurementActivity.status == "Planning"
    ).count()

    # 4. Total individual consultants engaged (INDV activities with contract_date)
    consultants_engaged = db.query(ProcurementActivity).filter(
        ProcurementActivity.type == "INDV",
        ProcurementActivity.contract_date.isnot(None)
    ).count()

    # 5. Utilization over time – return latest 8 quarters for chart
    util_data = db.query(Utilization).order_by(Utilization.year.desc(), Utilization.quarter.desc()).limit(8).all()
    utilization = [{"year": u.year, "quarter": u.quarter, "percentage": u.percentage} for u in util_data]
    utilization.reverse()  # oldest first for chart

    return {
        "under_procurement_cost": under_procurement,
        "total_contract_value": total_contract_value,
        "pipeline_activities": pipeline_activities,
        "consultants_engaged": consultants_engaged,
        "utilization": utilization
    }