
from app.general.db.session import SessionLocal
from app import crud
import requests

status_dict = {}

def set_interlinkers_status() -> None:
    with SessionLocal() as db:
        for interlinker in crud.interlinker.get_multi(db=db):
            done = []
            try:
                id = interlinker.backend
                if id not in done:
                    last_status = status_dict[id] if id in status_dict else None
                    
                    current_status = "off"
                    try:
                        data = requests.get(f"http://{interlinker.backend}/healthcheck/").json()
                        current_status = "on" if data else "off"
                    except Exception as e:
                        print(str(e))
                        pass
                    print(f"{interlinker.name} - {current_status}")
                    if (last_status == "off" and current_status == "on") or (last_status == "on" and current_status == "off"):
                        current_status = "dangling"
                    
                    status_dict[id] = {
                        "name": interlinker.name,
                        "status": current_status
                    }
                    done.append(id)
            except Exception as e:
                print(str(e))

def get_interlinker_status(interlinker_id):
    return status_dict[interlinker_id]