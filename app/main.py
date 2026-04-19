from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials
from app.routers import activities, deliverables, dashboard, reports

app = FastAPI(title="FBR Procurement Activity Tracker")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Firebase (you will add service-account.json later)
# cred = credentials.Certificate("service-account.json")
# firebase_admin.initialize_app(cred)

app.include_router(activities.router, prefix="/api/activities", tags=["activities"])
app.include_router(deliverables.router, prefix="/api/deliverables", tags=["deliverables"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])

@app.get("/api/health")
async def health():
    return {"status": "ok", "message": "FBR Procurement Tracker is running"}
