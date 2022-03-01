from typing import Any, List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.general import deps
import requests

router = APIRouter()

@router.get("", response_model=List[schemas.KnowledgeInterlinkerOut])
def list_knowledgeinterlinkers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Optional[dict] = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve knowledge interlinkers.
    """
    return crud.interlinker.get_multi_knowledgeinterlinkers(db, skip=skip, limit=limit)

@router.post("/{id}/instantiate")
def instantiate_knowledgeinterlinker(
    *,
    id: str,
    db: Session = Depends(deps.get_db),
    current_user: dict = Depends(deps.get_current_active_user),
    token: str = Depends(deps.get_current_active_token),
) -> Any:
    """
    Instantiate knowledge interlinker
    Sends a post to the clone URI
    """
    if not crud.interlinker.can_create(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # TODO: check if interlinker can clone
    interlinker = crud.interlinker.get_knowledgeinterlinker(db=db, id=id)
    if not interlinker:
        raise HTTPException(status_code=404, detail="Knowledge interlinker not found")

    try:
        external_info = requests.post(interlinker.internal_link + "/clone", headers={
            "Authorization": "Bearer " + token
        }).json()
    except:
        external_info = requests.post(interlinker.link + "/clone", headers={
            "Authorization": "Bearer " + token
        }).json()
    return external_info


@router.get("/{id}/external")
def read_knowledgeinterlinker_external_asset(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
    token: str = Depends(deps.get_current_active_token),
) -> Any:
    """
    Get asset of interlinker by interlinker ID.
    """
    interlinker = crud.interlinker.get_knowledgeinterlinker(db=db, id=id)
    if not interlinker:
        raise HTTPException(status_code=404, detail="Knowledge interlinker not found")

    try:
        return requests.get(interlinker.internal_link, headers={
            "Authorization": "Bearer " + token
        }).json()
    except:
        return requests.get(interlinker.link, headers={
            "Authorization": "Bearer " + token
        }).json()