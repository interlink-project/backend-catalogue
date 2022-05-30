from typing import Any, List, Optional, Union

from app.coproductionschemas.schemas import *
from app.interlinkers.schemas import *
from app.problemprofiles.schemas import *
from app.publicservices.schemas import *
from app.ratings.schemas import *
from app.treeitems.schemas import *

class ArtefactOutFull(ArtefactOut):
    pass

class PublicServiceOutFull(ArtefactOutFull, PublicServiceOut):
    pass


class ProblemProfileOutFull(ProblemProfileOut):
    pass

class RatingOutFull(RatingOut):
    pass


class TreeItemOutFull(TreeItemOut):
    problemprofiles: List[ProblemProfileOut]
    children: List["TreeItemOutFull"]

TreeItemOutFull.update_forward_refs()

class CoproductionSchemaOutFull(CoproductionSchemaOut):
    treeitems: List[TreeItemOutFull] = []
