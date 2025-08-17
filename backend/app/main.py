from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .api.routers import (
    admins as admins_router,
    auth as auth_router,
    candidates as candidates_router
)
from .core.config import Settings

settings = Settings()

app = FastAPI(
    title="NUESA PollMate",
    description="A secure e-voting platform for FUTMinna student elections",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory for serving uploaded files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(auth_router.router, prefix="/api/v1/auth")
app.include_router(admins_router.router, prefix="/api/v1/admin")
app.include_router(candidates_router.router, prefix="/api/v1/candidates")
