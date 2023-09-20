import uuid
from typing import Any, List, Optional

import requests
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.general import deps

router = APIRouter()


@router.get("", response_model=Page[schemas.SoftwareInterlinkerOut])
async def list_softwareinterlinkers(
    db: Session = Depends(deps.get_db),
    current_user: Optional[dict] = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve software interlinkers.
    """
    return await crud.interlinker.get_multi_softwareinterlinkers(db)

@router.get("/{name}", response_model=schemas.SoftwareInterlinkerOut)
async def read_softwareinterlinkers(
    *,
    db: Session = Depends(deps.get_db),
    name: str,
    current_user: Optional[dict] = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve software interlinkers.
    """
    return await crud.interlinker.get_softwareinterlinker_by_service_name(db,name)

