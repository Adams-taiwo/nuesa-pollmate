from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.routers import (
    admins as admins_router,
    auth as auth_router,
    candidates as candidates_router
)
from contextlib import asynccontextmanager
from app.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting server ...")
    await init_db()
    yield

app = FastAPI(
    title="NUESA PollMate",
    description="A secure e-voting platform for FUTMinna student elections",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory for saving uploaded files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(auth_router.router,)
app.include_router(admins_router.router,)
app.include_router(candidates_router.router,)
