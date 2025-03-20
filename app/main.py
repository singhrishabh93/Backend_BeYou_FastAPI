from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models.routers import affirmation

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

# Include routers
app.include_router(affirmation.router)

@app.get("/")
async def root():
    return {"message": "Welcome to BeYou API"}