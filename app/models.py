from sqlalchemy import Column, Integer, String, Date, DateTime, JSON, ForeignKey, Numeric, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ProcurementActivity(Base):
    __tablename__ = "procurement_activities"
    id = Column(Integer, primary_key=True, index=True)
    activity_no = Column(String, unique=True, index=True)
    title = Column(String)
    wing = Column(String)
    type = Column(String)                    # RFB or INDV
    status = Column(String)
    wb_nol_date = Column(Date, nullable=True)
    contract_date = Column(Date, nullable=True)
    estimated_cost = Column(Numeric(12,2), nullable=True)
    award_method = Column(String, nullable=True)
    publication_date = Column(Date, nullable=True)
    milestones = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    contract_value = Column(Numeric(12,2), nullable=True)   # actual signed contract value

class ContractDeliverable(Base):
    __tablename__ = "contract_deliverables"
    id = Column(Integer, primary_key=True, index=True)
    contract_number = Column(String, ForeignKey("procurement_activities.activity_no"), index=True)
    deliverable_name = Column(String)
    description = Column(Text)
    due_date = Column(Date)
    actual_submission_date = Column(Date, nullable=True)
    approval_date = Column(Date, nullable=True)
    payment_due = Column(Numeric(12,2), default=0)
    payment_released = Column(Numeric(12,2), default=0)
    status = Column(String, default="Pending")

class AuditLog(Base):
    __tablename__ = "audit_log"
    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String)
    action = Column(String)
    table_name = Column(String)
    record_id = Column(Integer)
    old_values = Column(JSON, nullable=True)
    new_values = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Utilization(Base):
    __tablename__ = "utilization"
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=False)  # 1,2,3,4
    percentage = Column(Numeric(5,2), nullable=False)  # e.g., 85.50
    resources_used = Column(String, nullable=True)    # optional description
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ProcurementPlan(Base):
    __tablename__ = "procurement_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    reference_no = Column(String, nullable=True)
    category = Column(String, nullable=True)
    amount_usd = Column(Float, nullable=True)
    method = Column(String, nullable=True)
    wing = Column(String, nullable=True)
    planned_start = Column(Date, nullable=True)
    planned_end = Column(Date, nullable=True)
    

    def __repr__(self):
        return f"<ProcurementPlan {self.name}>"