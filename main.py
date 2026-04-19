from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routers import activities, deliverables, dashboard, reports
from app.models import Base
from app.dependencies import engine

app = FastAPI(title="FBR Procurement Tracker")

# Mount the frontend folder
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Include routers
app.include_router(activities.router, prefix="/api/activities", tags=["activities"])
app.include_router(deliverables.router, prefix="/api/deliverables", tags=["deliverables"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])

@app.get("/api/health")
async def health():
    return {"status": "ok", "message": "FBR Procurement Tracker is running"}

# Root route - redirect to frontend
@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
