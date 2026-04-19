from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db

router = APIRouter()

@router.get("/quarterly")
def quarterly_report(db: Session = Depends(get_db)):
    return {"report_type": "ADB Quarterly", "status": "placeholder - will be expanded"}

@router.get("/awards")
def contract_awards_report(db: Session = Depends(get_db)):
    return {"report_type": "WB Contract Awards", "status": "placeholder"}

@router.get("/vfm")
def value_for_money_report(db: Session = Depends(get_db)):
    return {"report_type": "Value for Money Analysis", "status": "placeholder"}

@router.get("/ppra")
def ppra_compliance_report(db: Session = Depends(get_db)):
    return {"report_type": "PPRA Compliance", "status": "placeholder"}
