from typing import Any, List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.general import deps
from app.exceptions import CrudException
import requests

router = APIRouter()

def user_get_locale():
    return "es"

@router.get("", response_model=List[schemas.RepresentationOut])
def list_representations(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Optional[dict] = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve representations.
    """
    if not crud.representation.can_list(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    representations = crud.representation.get_multi(db, skip=skip, limit=limit)
    return representations

@router.post("", response_model=schemas.RepresentationOut)
def create_representation(
    *,
    db: Session = Depends(deps.get_db),
    representation_in: schemas.RepresentationCreate,
    current_user: dict = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new representation.
    """
    if not crud.representation.can_create(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    try:
        representation = crud.representation.create(db=db, representation=representation_in)
        return representation
    except CrudException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{id}/clone")
def clone_representation(
    *,
    id: str,
    db: Session = Depends(deps.get_db),
    current_user: dict = Depends(deps.get_current_active_user),
    token: str = Depends(deps.get_current_active_token),
) -> Any:
    """
    Clone representation.
    """
    if not crud.representation.can_create(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    representation = crud.representation.get(db=db, id=id)
    if not representation:
        raise HTTPException(status_code=404, detail="Representation not found")

    external_info = requests.post(representation.link + "/clone", headers={
        "Authorization": "Bearer " + token
    }).json()
    return external_info

@router.put("/{id}", response_model=schemas.RepresentationOut)
def update_representation(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    representation_in: schemas.RepresentationPatch,
    current_user: dict = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an representation.
    """
    representation = crud.representation.get(db=db, id=id)
    if not representation:
        raise HTTPException(status_code=404, detail="Representation not found")
    if not crud.representation.can_update(current_user, representation):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    representation = crud.representation.update(db=db, db_obj=representation, obj_in=representation_in)
    return representation


@router.get("/{id}", response_model=schemas.RepresentationOut)
def read_representation(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: Optional[dict] = Depends(deps.get_current_user),
) -> Any:
    """
    Get representation by ID.
    """
    representation = crud.representation.get(db=db, id=id)
    if not representation:
        raise HTTPException(status_code=404, detail="Representation not found")
    if not crud.representation.can_read(current_user, representation):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return representation


@router.get("/external/{id}")
def read_external_asset(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
    token: str = Depends(deps.get_current_active_token),
) -> Any:
    """
    Get asset of representation by representation ID.
    """
    representation = crud.representation.get(db=db, id=id)
    if not representation:
        raise HTTPException(status_code=404, detail="Representation not found")
    return requests.get(representation.link, headers={
        "Authorization": "Bearer " + token
    }).json()

@router.delete("/{id}", response_model=schemas.RepresentationOut)
def delete_representation(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: dict = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an representation.
    """
    representation = crud.representation.get(db=db, id=id)
    if not representation:
        raise HTTPException(status_code=404, detail="Representation not found")
    if not crud.representation.can_remove(current_user, representation):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    crud.representation.remove(db=db, id=id)
    return None