# FBR Procurement Activity Tracker
**BRD, SRS & Roadmap**  
**(Final Consolidated Version – April 2026)**

## 1. Business Requirements Document (BRD)

### 1.1 Executive Summary
The FBR Procurement Activity Tracker is a secure web-based system to monitor RFB and INDV procurement activities, post-award deliverables, and generate reports for WB, ADB, and GoP/PPRA.

### 1.2 Business Objectives
- Single source of truth for procurement activities
- Track full milestones and deliverables
- Generate donor-compliant reports (WB, ADB, PPRA)
- Enforce 2FA and role-based access
- Support Value-for-Money analysis

### 1.3 Key Business Rules
- `actual_submission_date` can be before `due_date`
- All dates must be ≥ `contract_date` (award date)
- Full audit trail for every change

## 2. SRS Summary
- Backend: FastAPI + SQLAlchemy
- Frontend: HTML + Tailwind + Chart.js
- Auth: Firebase with 2FA
- Reporting: Quarterly, Contract Awards, VfM, PPRA

## 3. Roadmap
Phase 1: Database & Import  
Phase 2: Backend + Validation  
Phase 3: Frontend + Reports  
Phase 4: Deployment

**Document Version**: Final