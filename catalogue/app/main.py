from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_pagination import add_pagination
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette_context import context, plugins
from starlette_context.middleware import ContextMiddleware

from app.api.api_v1 import api_router
from app.config import settings
from app.middleware import LanguagePlugin, UserPlugin
from app.kpis import init

middleware = [
    Middleware(
        ContextMiddleware,
        plugins=(
            plugins.RequestIdPlugin(),
            plugins.CorrelationIdPlugin(),
            UserPlugin(),
            LanguagePlugin()
        )
    )
]
app = FastAPI(
    title=settings.PROJECT_NAME, docs_url="/docs", openapi_url=f"{settings.API_V1_STR}/openapi.json", root_path=settings.BASE_PATH, middleware=middleware
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        # allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/")
def main():
    return RedirectResponse(url=f"{settings.BASE_PATH}/docs")

@app.get("/kpis")
async def kpis():
    return await init()

@app.get("/healthcheck")
def healthcheck():
    return True

app.include_router(api_router, prefix=settings.API_V1_STR)

###################
# Staticfiles
###################

app.mount("/static", StaticFiles(directory="static"), name="static")

###################
# Tasks
###################

# from fastapi_utils.tasks import repeat_every
# from app.status import set_interlinkers_status
#
# @app.on_event("startup")
# @repeat_every(seconds=5)
# async def task_set_interlinkers_status() -> None:
#     print("Setting interlinkers status")
#     set_interlinkers_status()

# PAGINATION
add_pagination(app)
