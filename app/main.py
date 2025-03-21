import os
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .models.routers import affirmation
from .database import db, client

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="BeYou API",
    description="API for BeYou affirmations",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def root():
    """Root endpoint, also used for healthcheck by Railway"""
    return {"message": "Welcome to BeYou API", "status": "online"}

@app.get("/health")
async def health_check():
    """Health check endpoint to verify database connection"""
    try:
        # Test MongoDB connection
        if db and client:
            client.admin.command('ping')
            return {"status": "healthy", "database": "connected"}
        else:
            return JSONResponse(
                content={"status": "unhealthy", "database": "not initialized"}, 
                status_code=500
            )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            content={"status": "unhealthy", "error": str(e)}, 
            status_code=500
        )

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    """Middleware to check MongoDB connection before handling requests"""
    if request.url.path in ['/', '/health']:
        # Skip DB check for healthcheck endpoints
        return await call_next(request)
    
    try:
        if not db:
            return JSONResponse(
                content={"detail": "Database connection not available"}, 
                status_code=503
            )
        
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Error in middleware: {str(e)}")
        return JSONResponse(
            content={"detail": str(e)}, 
            status_code=500
        )

# Include routers
app.include_router(affirmation.router)