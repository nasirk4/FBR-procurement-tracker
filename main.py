from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routers import activities, deliverables, dashboard, reports, dashboard_advanced, utilization, plans, settings
from app.models import Base
from app.dependencies import engine


import logging
import re

# ---------- Suppress scanner noise ----------
class SuppressScannerFilter(logging.Filter):
    def filter(self, record):
        msg = record.getMessage()
        # Block HEAD requests to hidden directories
        if 'HEAD' in msg and re.search(r'HEAD /\.(aws|ada|ssh|midway|env|git|config|well-known)/', msg):
            return False
        return True

# Apply to uvicorn access logger (if already configured)
for logger_name in ["uvicorn.access", "uvicorn.error"]:
    logger = logging.getLogger(logger_name)
    logger.addFilter(SuppressScannerFilter())

# --------------------------------------------

# Create the FastAPI app first
app = FastAPI(title="FBR Procurement Tracker")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(dashboard_advanced.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(utilization.router, prefix="/api/utilization", tags=["utilization"])
app.include_router(activities.router, prefix="/api/activities", tags=["activities"])
app.include_router(deliverables.router, prefix="/api/deliverables", tags=["deliverables"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])
app.include_router(plans.router, prefix="/api/plans", tags=["plans"])
app.include_router(settings.router, prefix="/api/settings", tags=["settings"])


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

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("frontend/favicon.ico")
