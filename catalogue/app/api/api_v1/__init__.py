from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from app.api.api_v1 import (
    interlinkers,
    problemprofiles,
    knowledgeinterlinkers,
    softwareinterlinkers,
    rating
)


api_router = APIRouter()

api_router.include_router(interlinkers.router,
                          prefix="/interlinkers", tags=["artefacts"])
api_router.include_router(knowledgeinterlinkers.router,
                          prefix="/knowledgeinterlinkers", tags=["artefacts"])
api_router.include_router(softwareinterlinkers.router,
                          prefix="/softwareinterlinkers", tags=["artefacts"])                         
api_router.include_router(problemprofiles.router,
                          prefix="/problemprofiles", tags=["problemprofiles"])
api_router.include_router(rating.router,
                          prefix="/ratings", tags=["social"])

@api_router.get("/")
def main():
    return RedirectResponse(url="/api/v1/interlinkers")
