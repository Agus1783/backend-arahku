# import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import engine
from app.models.models import Base
from app.routers.auth_router import router as auth_router
from app.routers.career_router import router as career_router
from app.routers.predict_router import router as predict_router
from app.routers.question_router import router as question_router
from app.routers.recommendation_router import (
    router as recommendation_router,
)
from app.routers.response_router import router as response_router
from app.routers.session_router import router as session_router
from app.routers.user_router import router as user_router

Base.metadata.create_all(bind=engine)
# Load env
_ = load_dotenv()

app = FastAPI(
    title="ArahKu API",
    description="Backend API untuk platform rekomendasi karir ArahKu",
    version="1.0.0",
)

# Frontend URL

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception,
):

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
        },
    )


# Register routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(question_router)
app.include_router(session_router)
app.include_router(response_router)
app.include_router(predict_router)
app.include_router(recommendation_router)
app.include_router(career_router)


# Root Endpoint
@app.get("/")
def root():
    return {"message": "ArahKu Backend API Running"}


# Health Check
@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/db-test")
def db_test():
    try:
        connection = engine.connect()
        connection.close()
        return {"message": "Database connected"}
    except Exception as e:
        return {"error": str(e)}
