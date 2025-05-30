from fastapi import APIRouter, Depends, status, HTTPException
from app.services.level import LevelService
from app.schemas.level import LevelCreate, LevelUpdate, LevelResponse, LevelWithQuestionsResponse
from app.middleware.auth import verify_token
from typing import List, Dict

router = APIRouter(
    prefix="/levels",
    tags=["levels"],
)

@router.post("", response_model=LevelResponse, status_code=status.HTTP_201_CREATED)
async def create_level(
    level_data: LevelCreate,
    payload: dict = Depends(verify_token),
    level_service: LevelService = Depends()
):
    """
    Create a new level
    """
    return await level_service.create_level(level_data)

@router.get("", response_model=List[LevelResponse])
async def get_all_levels(
    payload: dict = Depends(verify_token),
    level_service: LevelService = Depends()
):
    """
    Get all levels
    """
    return await level_service.get_all_levels()

@router.get("/history", response_model=List[LevelWithQuestionsResponse])
async def get_user_level_history(
    payload: dict = Depends(verify_token),
    level_service: LevelService = Depends()
):
    """
    Get user's level history with detailed question data - all levels lower than the user's current checkpoint
    """
    user_email = payload.get("sub")
    if not user_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token: user email not found in payload"
        )
    return await level_service.get_user_level_history(user_email)

@router.get("/{level_id}", response_model=LevelResponse)
async def get_level(
    level_id: int,
    payload: dict = Depends(verify_token),
    level_service: LevelService = Depends()
):
    """
    Get a specific level by ID
    """
    return await level_service.get_level(level_id)

@router.put("/{level_id}", response_model=LevelResponse)
async def update_level(
    level_id: int,
    level_data: LevelUpdate,
    payload: dict = Depends(verify_token),
    level_service: LevelService = Depends()
):
    """
    Update a level
    """
    return await level_service.update_level(level_id, level_data)

@router.delete("/{level_id}", status_code=status.HTTP_200_OK)
async def delete_level(
    level_id: int,
    payload: dict = Depends(verify_token),
    level_service: LevelService = Depends()
):
    """
    Delete a level
    """
    return await level_service.delete_level(level_id)

@router.post("/{level_id}/questions/{question_id}", response_model=LevelResponse)
async def add_question_to_level(
    level_id: int,
    question_id: str,
    payload: dict = Depends(verify_token),
    level_service: LevelService = Depends()
):
    """
    Add a question to a level
    """
    return await level_service.add_question_to_level(level_id, question_id)

@router.delete("/{level_id}/questions/{question_id}", response_model=LevelResponse)
async def remove_question_from_level(
    level_id: int,
    question_id: str,
    payload: dict = Depends(verify_token),
    level_service: LevelService = Depends()
):
    """
    Remove a question from a level
    """
    return await level_service.remove_question_from_level(level_id, question_id)