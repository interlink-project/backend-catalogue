from sqlalchemy.orm import Session

from app import models
from app.general.utils.CRUDBase import CRUDBase
from app.problemprofiles.crud import exportCrud as problemprofilesCrud

from .models import TreeItemMetadata, TreeItemTypes
from .schemas import TreeItemCreate, TreeItemPatch
from app.messages import log
from fastapi.encoders import jsonable_encoder

def recursive_check(id, obj):
    if hasattr(obj, "prerequisites"):
        for pre in obj.prerequisites:
            if id == pre.id:
                raise Exception("Circular prerequisite")
            return recursive_check(id, pre)
    return

class CRUDTreeItemMetadata(CRUDBase[TreeItemMetadata, TreeItemCreate, TreeItemPatch]):
    async def create(self, db: Session, *, obj_in: TreeItemCreate, commit : bool = True) -> TreeItemMetadata:
        data = obj_in.dict()
        problemprofiles_string_list = data.get("problemprofiles", []) or []
        del data["problemprofiles"]
        
        db_obj = TreeItemMetadata(**data)
        db.add(db_obj)
        if commit:
            db.commit()
            db.refresh(db_obj)
        
        for id in problemprofiles_string_list:
            if pp := await problemprofilesCrud.get(db=db, id=id):
                db_obj.problemprofiles.append(pp)

        return db_obj

    async def update(
        self,
        db: Session,
        *,
        db_obj: TreeItemMetadata,
        obj_in: TreeItemPatch
    ) -> TreeItemMetadata:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for id in update_data.get("problemprofiles", []):
            if problem := await problemprofilesCrud.get(db=db, id=id):
                db_obj.problemprofiles.append(problem)
        del update_data["problemprofiles"]
        
        for field, value in update_data.items():
            if hasattr(db_obj, field) and value != getattr(db_obj, field):
                print("Updating", field)
                setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        await log({
            "model": self.modelName,
            "action": "UPDATE",
            "id": db_obj.id
        })
        db.refresh(db_obj)
        return db_obj

    async def add_prerequisite(self, db: Session, treeitem: TreeItemMetadata, prerequisite: TreeItemMetadata, commit : bool = True) -> TreeItemMetadata:
        if treeitem == prerequisite:
            raise Exception("Same object")

        recursive_check(treeitem.id, prerequisite)
        treeitem.prerequisites.append(prerequisite)
        if commit:
            db.commit()
            db.refresh(treeitem)
        return treeitem

    # CRUD Permissions
    def can_create(self, user):
        return True

    def can_list(self, user):
        return True

    def can_read(self, user, object):
        return True

    def can_update(self, user, object):
        return True

    def can_remove(self, user, object):
        return True

exportCrud = CRUDTreeItemMetadata(TreeItemMetadata)
