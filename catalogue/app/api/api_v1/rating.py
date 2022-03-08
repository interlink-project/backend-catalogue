import uuid
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.exceptions import CrudException
from app.general import deps

router = APIRouter()

@router.post("", response_model=schemas.RatingOut)
def create_rating(
    *,
    db: Session = Depends(deps.get_db),
    rating_in: schemas.RatingCreate,
    current_user: dict = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new rating.
    """
    if not crud.rating.can_create(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    try:
        return crud.rating.create(db=db, rating=rating_in, user_id=current_user["sub"])
    except CrudException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}", response_model=schemas.RatingOut)
def update_rating(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    rating_in: schemas.RatingPatch,
    current_user: dict = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an rating.
    """
    rating = crud.rating.get(db=db, id=id)
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    if not crud.rating.can_update(current_user, rating):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    rating = crud.rating.update(db=db, db_obj=rating, obj_in=rating_in)
    return rating


@router.get("/{id}", response_model=schemas.RatingOut)
def read_rating(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: Optional[dict] = Depends(deps.get_current_user),
) -> Any:
    """
    Get rating by ID.
    """
    rating = crud.rating.get(db=db, id=id)
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    if not crud.rating.can_read(current_user, rating):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return rating


@router.delete("/{id}", response_model=schemas.RatingOut)
def delete_rating(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: dict = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an rating.
    """
    rating = crud.rating.get(db=db, id=id)
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    if not crud.rating.can_remove(current_user, rating):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    crud.rating.remove(db=db, id=id)
    return None
