from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.models import Base
from app.dependencies import engine
from app.routers import activities, deliverables, dashboard, reports, utilization, dashboard_advanced, plans

app = FastAPI(title="FBR Procurement Activity Tracker")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")

app.include_router(activities.router, prefix="/api/activities", tags=["activities"])
app.include_router(deliverables.router, prefix="/api/deliverables", tags=["deliverables"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])
app.include_router(utilization.router, prefix="/api/utilization", tags=["utilization"])
app.include_router(dashboard_advanced.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(plans.router, prefix="/api", tags=["plans"])

@app.get("/api/health")
async def health():
    return {"status": "ok", "message": "FBR Procurement Tracker is running"}

# Serve index.html at root
@app.get("/", response_class=FileResponse)
async def root():
    return FileResponse("frontend/index.html")
