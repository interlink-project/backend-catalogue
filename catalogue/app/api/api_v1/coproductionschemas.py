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


@router.get("", response_model=Page[schemas.CoproductionSchemaOutFull])
async def list_coproductionschemas(
    rating: Optional[int] = Query(None),
    creator: Optional[List[str]] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(deps.get_db),
    language: Session = Depends(get_language),
    current_user: Optional[dict] = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve coproductionschemas.
    """
    return await crud.coproductionschema.get_multi(db, search=search, rating=rating, language=language, creator=creator)

@router.get("/public", response_model=List[schemas.CoproductionSchemaOutFull])
async def public_coproductionschemas(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve public coproductionschemas.
    """
    return await crud.coproductionschema.get_public(db, skip=skip, limit=limit)


@router.post("", response_model=schemas.CoproductionSchemaOut)
async def create_coproductionschema(
    *,
    db: Session = Depends(deps.get_db),
    coproductionschema_in: schemas.CoproductionSchemaCreate,
    current_user: dict = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new coproductionschema.
    """
    if not crud.coproductionschema.can_create(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    try:
        return await crud.coproductionschema.create(db=db, obj_in=coproductionschema_in)
    except CrudException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}", response_model=schemas.CoproductionSchemaOut)
async def update_coproductionschema(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
    coproductionschema_in: schemas.CoproductionSchemaPatch,
    current_user: dict = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an coproductionschema.
    """
    coproductionschema = await crud.coproductionschema.get(db=db, id=id)
    if not coproductionschema:
        raise HTTPException(status_code=404, detail="CoproductionSchema not found")
    if not crud.coproductionschema.can_update(current_user, coproductionschema):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    coproductionschema = await crud.coproductionschema.update(db=db, db_obj=coproductionschema, obj_in=coproductionschema_in)
    return coproductionschema


@router.get("/{id}", response_model=schemas.CoproductionSchemaOutFull)
async def read_coproductionschema(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: Optional[dict] = Depends(deps.get_current_user),
) -> Any:
    """
    Get coproductionschema by ID.
    """
    coproductionschema = await crud.coproductionschema.get(db=db, id=id)
    # for i in coproductionschema.phasemetadatas:
    #     print(i.prerequisites_ids)
    if not coproductionschema:
        raise HTTPException(status_code=404, detail="CoproductionSchema not found")
    if not crud.coproductionschema.can_read(current_user, coproductionschema):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return coproductionschema

@router.get("/get_by_name/{name}", response_model=schemas.CoproductionSchemaOut)
async def read_coproductionschema(
    *,
    db: Session = Depends(deps.get_db),
    name: str,
) -> Any:
    """
    Get coproductionschema by ID.
    """
    coproductionschema = await crud.coproductionschema.get_by_name(db=db, name=name)
    if not coproductionschema:
        raise HTTPException(status_code=404, detail="CoproductionSchema not found")
    return coproductionschema


@router.delete("/{id}", response_model=schemas.CoproductionSchemaOut)
async def delete_coproductionschema(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: dict = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an coproductionschema.
    """
    coproductionschema = await crud.coproductionschema.get(db=db, id=id)
    if not coproductionschema:
        raise HTTPException(status_code=404, detail="CoproductionSchema not found")
    if not crud.coproductionschema.can_remove(current_user, coproductionschema):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    await crud.coproductionschema.remove(db=db, id=id)
    return None