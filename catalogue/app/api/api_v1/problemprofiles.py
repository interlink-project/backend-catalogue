from typing import Any, List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.general import deps
from app.exceptions import CrudException
router = APIRouter()

def user_get_locale():
    return "es"

@router.get("/", response_model=List[schemas.ProblemProfileOut])
def list_problemprofiles(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Optional[dict] = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve problemprofiles.
    """
    if not crud.problemprofile.can_list(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    problemprofiles = crud.problemprofile.get_multi(db, skip=skip, limit=limit)
    return problemprofiles


@router.post("/", response_model=schemas.ProblemProfileOut)
def create_problemprofile(
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
        problemprofile = crud.problemprofile.create(db=db, problemprofile=problemprofile_in)
        return problemprofile
    except CrudException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}", response_model=schemas.ProblemProfileOut)
def update_problemprofile(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
    problemprofile_in: schemas.ProblemProfilePatch,
    current_user: dict = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an problemprofile.
    """
    problemprofile = crud.problemprofile.get(db=db, id=id)
    if not problemprofile:
        raise HTTPException(status_code=404, detail="ProblemProfile not found")
    if not crud.problemprofile.can_update(current_user, problemprofile):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    problemprofile = crud.problemprofile.update(db=db, db_obj=problemprofile, obj_in=problemprofile_in)
    return problemprofile


@router.get("/{id}", response_model=schemas.ProblemProfileOut)
def read_problemprofile(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: Optional[dict] = Depends(deps.get_current_user),
) -> Any:
    """
    Get problemprofile by ID.
    """
    problemprofile = crud.problemprofile.get(db=db, id=id)
    if not problemprofile:
        raise HTTPException(status_code=404, detail="ProblemProfile not found")
    if not crud.problemprofile.can_read(current_user, problemprofile):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return problemprofile

@router.get("/get_by_name/{name}", response_model=schemas.ProblemProfileOut)
def read_problemprofile(
    *,
    db: Session = Depends(deps.get_db),
    name: str,
) -> Any:
    """
    Get problemprofile by ID.
    """
    problemprofile = crud.problemprofile.get_by_name(db=db, name=name)
    if not problemprofile:
        raise HTTPException(status_code=404, detail="ProblemProfile not found")
    return problemprofile


@router.delete("/{id}", response_model=schemas.ProblemProfileOut)
def delete_problemprofile(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: dict = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an problemprofile.
    """
    problemprofile = crud.problemprofile.get(db=db, id=id)
    if not problemprofile:
        raise HTTPException(status_code=404, detail="ProblemProfile not found")
    if not crud.problemprofile.can_remove(current_user, problemprofile):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    crud.problemprofile.remove(db=db, id=id)
    return None