from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.routes import routes_law
from app.services import database
from app.models import models_law
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handle application startup and shutdown events.
    This replaces the deprecated on_event("startup").
    """
    print("Application startup... creating database tables.")
    async with database.engine.begin() as conn:
        await conn.run_sync(models_law.Base.metadata.create_all)
    print("Database tables checked/created.")
    yield
    print("Application shutdown")

app = FastAPI(
    title="Indian Law Blog Generator AI",
    description="An AI-powered service to generate blogs on Indian legal topics.",
    version="1.0.0",
    lifespan=lifespan
)

# ADDED: http://localhost:5173 to the list below
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-legalmate.vercel.app/", 
        "http://127.0.0.1:5173", 
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_law.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Indian Law Blog Generator AI"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)