from typing import Any, List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.general import deps
from app.exceptions import CrudException
router = APIRouter()


@router.get("", response_model=List[schemas.InterlinkerOut])
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
    return crud.interlinker.get_multi(db, skip=skip, limit=limit, search=search)


@router.post("/by_problem_profiles", response_model=List[schemas.InterlinkerOut])
def list_interlinkers_by_problem_profiles(
    problems: List[str],
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Optional[dict] = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve interlinkers.
    """
    interlinkers = crud.interlinker.get_by_problem_profiles(db, skip=skip, limit=limit, problem_profiles=problems)
    return interlinkers


@router.post("", response_model=schemas.InterlinkerOut)
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
    try:
        interlinker = crud.interlinker.create(db=db, interlinker=interlinker_in)
        return interlinker
    except CrudException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}", response_model=schemas.InterlinkerOut)
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


@router.get("/{id}", response_model=schemas.InterlinkerOut)
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

@router.get("/get_by_name/{name}", response_model=schemas.InterlinkerOut)
def read_interlinker(
    *,
    db: Session = Depends(deps.get_db),
    name: str,
    locale: str = "en"
) -> Any:
    """
    Get interlinker by ID.
    """
    interlinker = crud.interlinker.get_by_name(db=db, name=name)
    if not interlinker:
        raise HTTPException(status_code=404, detail="Interlinker not found")
    return interlinker


@router.delete("/{id}", response_model=schemas.InterlinkerOut)
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

@router.get("/{id}/related", response_model=List[schemas.InterlinkerOut])
def related_interlinkers(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
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
    return crud.interlinker.get_by_problem_profiles(db=db, exclude=[interlinker.id], problem_profiles=[pr.id for pr in interlinker.problemprofiles], skip=skip, limit=limit)
    # return crud.interlinker.get_related(db=db, interlinker=interlinker, skip=skip, limit=limit)
