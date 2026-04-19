from sqlalchemy.orm import Session
from app.dependencies import SessionLocal
from app.models import ProcurementActivity
from datetime import date

def create_sample_data():
    db = SessionLocal()
    try:
        # Clear existing data
        db.query(ProcurementActivity).delete()
        
        sample_activities = [
            ProcurementActivity(
                activity_no="PK-FBR-2026-001",
                title="Supply of IT Equipment for FBR Regional Offices",
                wing="IT Wing",
                type="RFB",
                status="Evaluation",
                contract_date=date(2026, 3, 15),
                estimated_cost=45000000,
                award_method="NCB"
            ),
            ProcurementActivity(
                activity_no="PK-FBR-2026-002",
                title="Consultancy for Digital Transformation",
                wing="Policy Wing",
                type="INDV",
                status="Contract Signed",
                contract_date=date(2026, 2, 28),
                estimated_cost=12500000,
                award_method="QCBS"
            )
        ]
        
        db.add_all(sample_activities)
        db.commit()
        print(f"✅ {len(sample_activities)} sample activities created successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
