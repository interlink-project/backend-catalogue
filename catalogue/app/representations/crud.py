from sqlalchemy.orm import Session

from app.general.utils.CRUDBase import CRUDBase
from app.models import Representation
from app.schemas import RepresentationCreate, RepresentationPatch


class CRUDRepresentation(CRUDBase[Representation, RepresentationCreate, RepresentationPatch]):
    def create(self, db: Session, *, representation: RepresentationCreate) -> Representation:
        db_obj = Representation(
            knowledgeinterlinker_id=representation.knowledgeinterlinker_id,
            instructions=representation.instructions,
            form=representation.form,
            language=representation.language,
            format=representation.format,
            genesis_asset_id=representation.genesis_asset_id,
            softwareinterlinker_id=representation.softwareinterlinker_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

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

exportCrud = CRUDRepresentation(Representation)
