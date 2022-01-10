from fastapi import FastAPI
from fastapi.responses import RedirectResponse, HTMLResponse
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1 import api_router
from app.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME, docs_url="/docs", openapi_url=f"{settings.API_V1_STR}/openapi.json", root_path=settings.BASE_PATH
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


app.include_router(api_router, prefix=settings.API_V1_STR)



@app.get("/")
def main():
    return RedirectResponse(url=f"{settings.BASE_PATH}/docs")


@app.get("/healthcheck/")
def healthcheck():
    return True

###################
# we need this to save temporary code & state in session (authentication)
###################
#from app.general.authentication import AuthMiddleware
#from starlette.middleware.sessions import SessionMiddleware
#app.add_middleware(SessionMiddleware, secret_key="some-random-string")
#app.add_middleware(AuthMiddleware)

###################
# Staticfiles
###################

from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")

###################
# Tasks and sockets
###################

from fastapi_utils.tasks import repeat_every
from app.status import set_interlinkers_status, status_dict
import json
from fastapi import WebSocket, WebSocketDisconnect, Depends
from app.general import deps
from app.sockets import manager

@app.on_event("startup")
@repeat_every(seconds=5)
async def task_set_interlinkers_status() -> None:
    print("Setting interlinkers status")
    last_status = status_dict
    set_interlinkers_status()
    if (last_status != status_dict):
        print("UPDATED STATUS")
        data = {
            "event": "NEW_STATUS",
            "payload": status_dict
        }
        await manager.broadcast(json.dumps(data))

@app.get("/interlinkers_status/")
async def status():
    data = {
        "event": "NEW_STATUS",
        "payload": status_dict
    }
    await manager.broadcast(json.dumps(data))
    return status_dict

@app.websocket("/connect/")
async def websocket_endpoint(
    websocket: WebSocket,
    current_user: str = Depends(deps.get_current_user_socket)
):
    user_id = current_user["email"]
    await manager.connect(websocket)
    print(f"Client #{user_id} connected")
    data = {
        "event": "NEW_STATUS",
        "payload": status_dict
    }
    await manager.send_personal_message(json.dumps(data), websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        
        print(f"Client #{user_id} disconnected")
        await manager.broadcast(f"Client #{user_id} disconnected")