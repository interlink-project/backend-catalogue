
from app.general.db.session import SessionLocal
from app import crud, schemas
import requests

status_dict = {}

def set_interlinkers_status() -> None:
    with SessionLocal() as db:
        for interlinker in crud.interlinker.get_multi_softwareinterlinkers(db=db):
            try:
                id = interlinker.id
                last_status = status_dict[id] if id in status_dict else None

                print(interlinker.name)
                current_status = "off"
                try:
                    data = requests.get(f"http://{interlinker.backend}/healthcheck/").json()
                    current_status = "on" if data else "off"
                except Exception as e:
                    # print(str(e))
                    pass
                # print(f"{interlinker.name} - {current_status}")
                if (last_status == "off" and current_status == "on") or (last_status == "on" and current_status == "off"):
                    current_status = "dangling"
                
                if current_status != interlinker.status:
                    setattr(interlinker, "status", current_status)
                    db.add(interlinker)
                    db.commit()
                    db.refresh(interlinker)
                    
            except Exception as e:
                print(str(e))