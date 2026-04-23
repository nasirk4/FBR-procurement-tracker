from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Utilization
from app.schemas import UtilizationCreate, UtilizationUpdate
from app.dependencies import get_db

router = APIRouter(redirect_slashes=False)

@router.get("")
def get_all_utilization(db: Session = Depends(get_db)):
    return db.query(Utilization).order_by(Utilization.year, Utilization.quarter).all()

@router.post("")
def add_utilization(util: UtilizationCreate, db: Session = Depends(get_db)):
    existing = db.query(Utilization).filter_by(year=util.year, quarter=util.quarter).first()
    if existing:
        raise HTTPException(400, "Utilization for this quarter already exists")
    new_util = Utilization(**util.dict())
    db.add(new_util)
    db.commit()
    db.refresh(new_util)
    return new_util

@router.patch("/{util_id}")
def update_utilization(util_id: int, update: UtilizationUpdate, db: Session = Depends(get_db)):
    util = db.query(Utilization).filter(Utilization.id == util_id).first()
    if not util:
        raise HTTPException(404, "Not found")
    for field, value in update.dict(exclude_unset=True).items():
        setattr(util, field, value)
    db.commit()
    return util

@router.delete("/{util_id}")
def delete_utilization(util_id: int, db: Session = Depends(get_db)):
    util = db.query(Utilization).filter(Utilization.id == util_id).first()
    if not util:
        raise HTTPException(404, "Not found")
    db.delete(util)
    db.commit()
    return {"message": "Deleted"}