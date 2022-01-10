from typing import Any, List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.general import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.InterlinkerOutFull])
def list_interlinkers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    search: str = "",
    current_user: Optional[dict] = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve interlinkers.
    """
    if not crud.interlinker.can_list(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    interlinkers = crud.interlinker.get_multi(db, skip=skip, limit=limit, search=search)
    return interlinkers


@router.post("/", response_model=schemas.InterlinkerOutFull)
def create_interlinker(
    *,
    db: Session = Depends(deps.get_db),
    interlinker_in: schemas.InterlinkerCreate,
    current_user: dict = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new interlinker.
    """
    if not crud.interlinker.can_create(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    interlinker = crud.interlinker.create(db=db, interlinker=interlinker_in)
    return interlinker


@router.put("/{id}", response_model=schemas.InterlinkerOutFull)
def update_interlinker(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
    interlinker_in: schemas.InterlinkerPatch,
    current_user: dict = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an interlinker.
    """
    interlinker = crud.interlinker.get(db=db, id=id)
    if not interlinker:
        raise HTTPException(status_code=404, detail="Interlinker not found")
    if not crud.interlinker.can_update(current_user, interlinker):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    interlinker = crud.interlinker.update(db=db, db_obj=interlinker, obj_in=interlinker_in)
    return interlinker


@router.get("/{id}", response_model=schemas.InterlinkerOutFull)
def read_interlinker(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: Optional[dict] = Depends(deps.get_current_user),
) -> Any:
    """
    Get interlinker by ID.
    """
    interlinker = crud.interlinker.get(db=db, id=id)
    if not interlinker:
        raise HTTPException(status_code=404, detail="Interlinker not found")
    if not crud.interlinker.can_read(current_user, interlinker):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return interlinker

@router.get("/get_by_name/{name}", response_model=schemas.InterlinkerOutFull)
def read_interlinker(
    *,
    db: Session = Depends(deps.get_db),
    name: str,
) -> Any:
    """
    Get interlinker by ID.
    """
    interlinker = crud.interlinker.get_by_name(db=db, name=name)
    if not interlinker:
        raise HTTPException(status_code=404, detail="Interlinker not found")
    return interlinker


@router.delete("/{id}", response_model=schemas.InterlinkerOutFull)
def delete_interlinker(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: dict = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an interlinker.
    """
    interlinker = crud.interlinker.get(db=db, id=id)
    if not interlinker:
        raise HTTPException(status_code=404, detail="Interlinker not found")
    if not crud.interlinker.can_remove(current_user, interlinker):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    crud.interlinker.remove(db=db, id=id)
    return None