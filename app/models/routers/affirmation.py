from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.affirmation import Affirmation, AffirmationCreate, AffirmationInDB
from app.database import db
from bson import ObjectId
from datetime import datetime

router = APIRouter(
    prefix="/affirmations",
    tags=["affirmations"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Affirmation])
async def get_affirmations():
    affirmations = await db.affirmations.find().to_list(1000)
    return affirmations

@router.get("/{affirmation_id}", response_model=Affirmation)
async def get_affirmation(affirmation_id: str):
    affirmation = await db.affirmations.find_one({"id": affirmation_id})
    if affirmation is None:
        raise HTTPException(status_code=404, detail="Affirmation not found")
    return affirmation

@router.post("/", response_model=Affirmation, status_code=status.HTTP_201_CREATED)
async def create_affirmation(affirmation: AffirmationCreate):
    new_affirmation = AffirmationInDB(
        text=affirmation.text,
        category=affirmation.category
    )
    
    affirmation_dict = new_affirmation.model_dump()
    result = await db.affirmations.insert_one(affirmation_dict)
    
    created_affirmation = await db.affirmations.find_one({"_id": result.inserted_id})
    return created_affirmation