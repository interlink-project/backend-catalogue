from sqlalchemy.orm import Session

from app import crud
from app.schemas import InterlinkerCreate, InterlinkerPatch
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def test_create_interlinker(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    interlinker_in = InterlinkerCreate(title=title, description=description)
    user = create_random_user(db)
    interlinker = crud.interlinker.create_with_owner(db=db, obj_in=interlinker_in, owner_id=user.id)
    assert interlinker.title == title
    assert interlinker.description == description
    assert interlinker.owner_id == user.id


def test_get_interlinker(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    interlinker_in = InterlinkerCreate(title=title, description=description)
    user = create_random_user(db)
    interlinker = crud.interlinker.create_with_owner(db=db, obj_in=interlinker_in, owner_id=user.id)
    stored_interlinker = crud.interlinker.get(db=db, id=interlinker.id)
    assert stored_interlinker
    assert interlinker.id == stored_interlinker.id
    assert interlinker.title == stored_interlinker.title
    assert interlinker.description == stored_interlinker.description
    assert interlinker.owner_id == stored_interlinker.owner_id


def test_update_interlinker(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    interlinker_in = InterlinkerCreate(title=title, description=description)
    user = create_random_user(db)
    interlinker = crud.interlinker.create_with_owner(db=db, obj_in=interlinker_in, owner_id=user.id)
    description2 = random_lower_string()
    interlinker_update = InterlinkerPatch(description=description2)
    interlinker2 = crud.interlinker.update(db=db, db_obj=interlinker, obj_in=interlinker_update)
    assert interlinker.id == interlinker2.id
    assert interlinker.title == interlinker2.title
    assert interlinker2.description == description2
    assert interlinker.owner_id == interlinker2.owner_id


def test_delete_interlinker(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    interlinker_in = InterlinkerCreate(title=title, description=description)
    user = create_random_user(db)
    interlinker = crud.interlinker.create_with_owner(db=db, obj_in=interlinker_in, owner_id=user.id)
    interlinker2 = crud.interlinker.remove(db=db, id=interlinker.id)
    interlinker3 = crud.interlinker.get(db=db, id=interlinker.id)
    assert interlinker3 is None
    assert interlinker2.id == interlinker.id
    assert interlinker2.title == title
    assert interlinker2.description == description
    assert interlinker2.owner_id == user.id
