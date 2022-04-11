from typing import Any, List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from app import crud, models, schemas
from app.general import deps
import requests

router = APIRouter()

@router.get("", response_model=Page[schemas.ExternalKnowledgeInterlinkerOut])
async def list_externalinterlinkers(
    db: Session = Depends(deps.get_db),
    current_user: Optional[dict] = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve external interlinkers.
    """
    return await crud.interlinker.get_multi_externalknowledgeinterlinkers(db)