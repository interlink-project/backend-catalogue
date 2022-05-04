import uuid
from typing import Any, List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Page
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.exceptions import CrudException
from app.general import deps
from app.locales import get_language

router = APIRouter()


@router.get("", response_model=Page[schemas.InterlinkerOut])
async def list_interlinkers(
    nature: Optional[List[str]] = Query(None),
    rating: Optional[int] = Query(None),
    creator: Optional[List[str]] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(deps.get_db),
    current_user: Optional[dict] = Depends(deps.get_current_user),
    language: str = Depends(get_language)
) -> Any:
    """
    Retrieve interlinkers.
    """
    return await crud.interlinker.get_multi(db, search=search, rating=rating, natures=nature, creator=creator, language=language)


@router.post("/by_problemprofiles", response_model=Page[schemas.InterlinkerOut])
async def list_interlinkers_by_problemprofiles(
    problemprofiles: List[str],
    db: Session = Depends(deps.get_db),
    current_user: Optional[dict] = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve interlinkers.
    """
    return await crud.interlinker.get_by_problemprofiles(db, problemprofiles=problemprofiles)


@router.post("", response_model=schemas.InterlinkerOut)
async def create_interlinker(
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
        interlinker = await crud.interlinker.create(db=db, interlinker=interlinker_in)
        return interlinker
    except CrudException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}", response_model=schemas.InterlinkerOut)
async def update_interlinker(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
    interlinker_in: schemas.InterlinkerPatch,
    current_user: dict = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an interlinker.
    """
    interlinker = await crud.interlinker.get(db=db, id=id)
    if not interlinker:
        raise HTTPException(status_code=404, detail="Interlinker not found")
    if not crud.interlinker.can_update(current_user, interlinker):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return await crud.interlinker.update(db=db, db_obj=interlinker, obj_in=interlinker_in)


@router.get("/{id}", response_model=schemas.InterlinkerOut)
async def read_interlinker(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: Optional[dict] = Depends(deps.get_current_user),
) -> Any:
    """
    Get interlinker by ID.
    """
    interlinker = await crud.interlinker.get(db=db, id=id)
    if not interlinker:
        raise HTTPException(status_code=404, detail="Interlinker not found")
    if not crud.interlinker.can_read(current_user, interlinker):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return interlinker

@router.get("/get_by_name/{name}", response_model=schemas.InterlinkerOut)
async def read_interlinker_by_name(
    *,
    db: Session = Depends(deps.get_db),
    name: str,
) -> Any:
    """
    Get interlinker by name.
    """
    interlinker = await crud.interlinker.get_by_name(db=db, name=name)
    if not interlinker:
        raise HTTPException(status_code=404, detail="Interlinker not found")
    return interlinker


@router.delete("/{id}", response_model=schemas.InterlinkerOut)
async def delete_interlinker(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: dict = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an interlinker.
    """
    interlinker = await crud.interlinker.get(db=db, id=id)
    if not interlinker:
        raise HTTPException(status_code=404, detail="Interlinker not found")
    if not crud.interlinker.can_remove(current_user, interlinker):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    await crud.interlinker.remove(db=db, id=id)
    return None

@router.get("/{id}/related", response_model=Page[schemas.InterlinkerOut])
async def related_interlinkers(
    id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: Optional[dict] = Depends(deps.get_current_user),
) -> Any:
    """
    Get interlinker by ID.
    """
    interlinker = await crud.interlinker.get(db=db, id=id)
    if not interlinker:
        raise HTTPException(status_code=404, detail="Interlinker not found")
    if not crud.interlinker.can_read(current_user, interlinker):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return await crud.interlinker.get_by_problemprofiles(db=db, exclude=[interlinker.id], problemprofiles=[pr.id for pr in interlinker.problemprofiles])
