from typing import List, Optional

from app.interlinkers.schemas import *
from app.publicservices.schemas import *
from app.functionalities.schemas import *
from app.problemdomains.schemas import *
from app.ratings.schemas import *
from app.questioncomments.schemas import *


class ArtefactOutFull(ArtefactOut):
    questioncomments: List[QuestionCommentOut]


class PublicServiceOutFull(ArtefactOutFull, PublicServiceOut):
    pass


class ProblemDomainOutFull(ProblemDomainOut):
    pass


class FunctionalityOutFull(FunctionalityOut):
    pass


class QuestionCommentOutFull(QuestionCommentOut):
    pass


class RatingOutFull(RatingOut):
    pass
