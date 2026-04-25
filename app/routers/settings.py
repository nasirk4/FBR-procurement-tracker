from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import GlobalSetting
from app.schemas import GlobalFundsSet
from app.dependencies import get_db

router = APIRouter(redirect_slashes=False)

@router.get("/total_funds_released")
def get_total_funds_released(db: Session = Depends(get_db)):
    setting = db.query(GlobalSetting).filter(GlobalSetting.key == "total_funds_released").first()
    if not setting:
        return {"total_funds_released": 0}
    return {"total_funds_released": float(setting.value)}

@router.post("/total_funds_released")
def set_total_funds_released(data: GlobalFundsSet, db: Session = Depends(get_db)):
    setting = db.query(GlobalSetting).filter(GlobalSetting.key == "total_funds_released").first()
    if setting:
        setting.value = str(data.total_funds_released)
    else:
        setting = GlobalSetting(key="total_funds_released", value=str(data.total_funds_released))
        db.add(setting)
    db.commit()
    return {"total_funds_released": data.total_funds_released}