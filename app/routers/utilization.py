from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Utilization, GlobalSetting
from app.schemas import UtilizationCreate, UtilizationResponse
from app.dependencies import get_db
from decimal import Decimal

router = APIRouter(redirect_slashes=False)

def get_total_funds_released(db: Session):
    setting = db.query(GlobalSetting).filter(GlobalSetting.key == "total_funds_released").first()
    return float(setting.value) if setting else 0

@router.get("", response_model=list[UtilizationResponse])
def get_utilization(db: Session = Depends(get_db)):
    records = db.query(Utilization).order_by(Utilization.year, Utilization.quarter).all()
    total_released = get_total_funds_released(db)
    cumulative = 0
    result = []
    for r in records:
        cumulative += r.funds_utilized
        percentage = (cumulative / Decimal(total_released) * Decimal(100)) if total_released else Decimal(0)
        result.append({
            "id": r.id,
            "year": r.year,
            "quarter": r.quarter,
            "funds_utilized": float(r.funds_utilized),
            "cumulative_utilized": cumulative,
            "percentage": round(percentage, 2),
            "notes": r.notes
        })
    return result

@router.post("")
def create_utilization(util: UtilizationCreate, db: Session = Depends(get_db)):
    existing = db.query(Utilization).filter_by(year=util.year, quarter=util.quarter).first()
    if existing:
        raise HTTPException(400, "Data for this quarter already exists")
    new = Utilization(**util.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new

@router.patch("/{util_id}")
def update_utilization(util_id: int, util: UtilizationCreate, db: Session = Depends(get_db)):
    record = db.query(Utilization).filter(Utilization.id == util_id).first()
    if not record:
        raise HTTPException(404, "Not found")
    for field, value in util.dict().items():
        setattr(record, field, value)
    db.commit()
    return record

@router.delete("/{util_id}")
def delete_utilization(util_id: int, db: Session = Depends(get_db)):
    record = db.query(Utilization).filter(Utilization.id == util_id).first()
    if not record:
        raise HTTPException(404, "Not found")
    db.delete(record)
    db.commit()
    return {"message": "Deleted"}