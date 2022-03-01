from typing import Any, List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.general import deps
import requests

router = APIRouter()

@router.get("", response_model=List[schemas.SoftwareInterlinkerOut])
def list_softwareinterlinkers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Optional[dict] = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve software interlinkers.
    """
    return crud.interlinker.get_multi_softwareinterlinkers(db, skip=skip, limit=limit)

@router.get("/integrated", response_model=List[schemas.SoftwareInterlinkerOut])
def list_softwareinterlinkers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Optional[dict] = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve software interlinkers.
    """
    return crud.interlinker.get_multi_integrated_softwareinterlinkers(db, skip=skip, limit=limit)
