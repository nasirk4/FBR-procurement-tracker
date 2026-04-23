from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routers import activities, deliverables, dashboard, reports, dashboard_advanced, utilization, plans
from app.models import Base
from app.dependencies import engine

# Create the FastAPI app first
app = FastAPI(title="FBR Procurement Tracker")

# Register routers
app.include_router(dashboard_advanced.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(utilization.router, prefix="/api/utilization", tags=["utilization"])
app.include_router(activities.router, prefix="/api/activities", tags=["activities"])
app.include_router(deliverables.router, prefix="/api/deliverables", tags=["deliverables"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])
app.include_router(plans.router, prefix="/api", tags=["plans"])

# Serve static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="frontend", html=False), name="static")

# Serve the main HTML file at the root
@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
