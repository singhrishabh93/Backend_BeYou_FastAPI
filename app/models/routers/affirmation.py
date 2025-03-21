import logging
from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.affirmation import Affirmation, AffirmationCreate, AffirmationInDB
from app.database import db
from datetime import datetime

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/affirmations",
    tags=["affirmations"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Affirmation])
async def get_affirmations():
    try:
        if not db:
            logger.error("Database connection not available")
            raise HTTPException(
                status_code=503, 
                detail="Database connection not available"
            )
            
        logger.info("Fetching affirmations")
        affirmations = await db.affirmations.find().to_list(1000)
        logger.info(f"Found {len(affirmations)} affirmations")
        return affirmations
    except Exception as e:
        logger.error(f"Error fetching affirmations: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch affirmations: {str(e)}"
        )

@router.get("/{affirmation_id}", response_model=Affirmation)
async def get_affirmation(affirmation_id: str):
    try:
        if not db:
            logger.error("Database connection not available")
            raise HTTPException(
                status_code=503, 
                detail="Database connection not available"
            )
            
        affirmation = await db.affirmations.find_one({"id": affirmation_id})
        if affirmation is None:
            logger.warning(f"Affirmation with ID {affirmation_id} not found")
            raise HTTPException(status_code=404, detail="Affirmation not found")
            
        return affirmation
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching affirmation {affirmation_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch affirmation: {str(e)}"
        )

@router.post("/", response_model=Affirmation, status_code=status.HTTP_201_CREATED)
async def create_affirmation(affirmation: AffirmationCreate):
    try:
        if not db:
            logger.error("Database connection not available")
            raise HTTPException(
                status_code=503, 
                detail="Database connection not available"
            )
            
        new_affirmation = AffirmationInDB(
            text=affirmation.text,
            category=affirmation.category
        )
        
        affirmation_dict = new_affirmation.model_dump()
        logger.info(f"Creating new affirmation: {affirmation_dict}")
        
        result = await db.affirmations.insert_one(affirmation_dict)
        
        created_affirmation = await db.affirmations.find_one({"_id": result.inserted_id})
        logger.info(f"Created affirmation with ID: {created_affirmation.get('id')}")
        
        return created_affirmation
    except Exception as e:
        logger.error(f"Error creating affirmation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create affirmation: {str(e)}"
        )