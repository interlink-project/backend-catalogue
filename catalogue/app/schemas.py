from typing import Any, List, Optional, Union

from app.coproductionschemas.schemas import *
from app.integrations.schemas import *
from app.interlinkers.schemas import *
from app.problemprofiles.schemas import *
from app.publicservices.schemas import *
from app.questioncomments.schemas import *
from app.ratings.schemas import *

class ArtefactOutFull(ArtefactOut):
    questioncomments: List[QuestionCommentOut]


class PublicServiceOutFull(ArtefactOutFull, PublicServiceOut):
    pass


class ProblemProfileOutFull(ProblemProfileOut):
    pass


class QuestionCommentOutFull(QuestionCommentOut):
    pass


class RatingOutFull(RatingOut):
    pass


class TaskMetadataOutFull(TaskMetadataOut):
    problemprofiles: List[ProblemProfileOut]
    prerequisites_ids: List[uuid.UUID]

    @validator('prerequisites_ids', pre=True)
    def prerequisites_ids_to_list(cls, v):
        return list(v)

class ObjectiveMetadataOutFull(ObjectiveMetadataOut):
    taskmetadatas: List[TaskMetadataOutFull] = []
    prerequisites_ids: List[uuid.UUID]

    @validator('prerequisites_ids', pre=True)
    def prerequisites_ids_to_list(cls, v):
        return list(v)

class PhaseMetadataOutFull(PhaseMetadataOut):
    objectivemetadatas: List[ObjectiveMetadataOutFull] = []
    prerequisites_ids: List[uuid.UUID]

    @validator('prerequisites_ids', pre=True)
    def prerequisites_ids_to_list(cls, v):
        return list(v)

class CoproductionSchemaOutFull(CoproductionSchemaOut):
    phasemetadatas: List[PhaseMetadataOutFull] = []
