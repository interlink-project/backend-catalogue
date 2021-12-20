from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from app.api.api_v1 import (
    interlinkers
)


api_router = APIRouter()

api_router.include_router(interlinkers.router,
                          prefix="/interlinkers", tags=["artefacts"])

@api_router.get("/")
def main():
    return RedirectResponse(url="/api/v1/interlinkers")
