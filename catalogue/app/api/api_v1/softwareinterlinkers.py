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
def list_softwareinterlinkers(
    db: Session = Depends(deps.get_db),
    current_user: Optional[dict] = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve software interlinkers.
    """
    return crud.interlinker.get_multi_softwareinterlinkers(db)


@router.get("/integrated", response_model=List[schemas.SoftwareInterlinkerOut])
def list_softwareinterlinkers(
    db: Session = Depends(deps.get_db),
    current_user: Optional[dict] = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve software interlinkers.
    """
    return crud.interlinker.get_multi_internally_integrated_softwareinterlinkers(db)
