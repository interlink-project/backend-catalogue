from typing import Any, List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.general import deps
from app.exceptions import CrudException
router = APIRouter()

@router.get("", response_model=List[schemas.ProblemProfileOut])
async def list_problemprofiles(
    db: Session = Depends(deps.get_db),
    current_user: Optional[dict] = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve problemprofiles.
    """
    if not crud.problemprofile.can_list(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return await crud.problemprofile.get_multi(db)

@router.get("/ids", response_model=list)
async def ids_list_problemprofiles(
    db: Session = Depends(deps.get_db),
    current_user: Optional[dict] = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve problemprofiles ids.
    """
    problemprofiles = [problemprofile.id for problemprofile in await crud.problemprofile.get_multi(db)]
    return problemprofiles

@router.post("", response_model=schemas.ProblemProfileOut)
async def create_problemprofile(
    *,
    db: Session = Depends(deps.get_db),
    problemprofile_in: schemas.ProblemProfileCreate,
    current_user: dict = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new problemprofile.
    """
    if not crud.problemprofile.can_create(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    try:
        return await crud.problemprofile.create(db=db, obj_in=problemprofile_in)
    except CrudException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}", response_model=schemas.ProblemProfileOut)
async def update_problemprofile(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    problemprofile_in: schemas.ProblemProfilePatch,
    current_user: dict = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an problemprofile.
    """
    problemprofile = await crud.problemprofile.get(db=db, id=id)
    if not problemprofile:
        raise HTTPException(status_code=404, detail="ProblemProfile not found")
    if not crud.problemprofile.can_update(current_user, problemprofile):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return await crud.problemprofile.update(db=db, db_obj=problemprofile, obj_in=problemprofile_in)


@router.get("/{id}", response_model=schemas.ProblemProfileOut)
async def read_problemprofile(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: Optional[dict] = Depends(deps.get_current_user),
) -> Any:
    """
    Get problemprofile by ID.
    """
    problemprofile = await crud.problemprofile.get(db=db, id=id)
    if not problemprofile:
        raise HTTPException(status_code=404, detail="ProblemProfile not found")
    if not crud.problemprofile.can_read(current_user, problemprofile):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return problemprofile


@router.get("/get_by_name/{name}", response_model=schemas.ProblemProfileOut)
async def read_problemprofile(
    *,
    db: Session = Depends(deps.get_db),
    name: str,
    locale: str
) -> Any:
    """
    Get problemprofile by ID.
    """
    problemprofile = await crud.problemprofile.get_by_name(db=db, name=name, locale=locale)
    if not problemprofile:
        raise HTTPException(status_code=404, detail="ProblemProfile not found")
    return problemprofile


@router.delete("/{id}", response_model=schemas.ProblemProfileOut)
async def delete_problemprofile(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: dict = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an problemprofile.
    """
    problemprofile = await crud.problemprofile.get(db=db, id=id)
    if not problemprofile:
        raise HTTPException(status_code=404, detail="ProblemProfile not found")
    if not crud.problemprofile.can_remove(current_user, problemprofile):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    await crud.problemprofile.remove(db=db, id=id)
    return None