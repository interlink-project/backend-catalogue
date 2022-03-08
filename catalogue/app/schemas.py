from typing import List, Optional

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


class IntegrationOutFull(IntegrationOut):
    pass
