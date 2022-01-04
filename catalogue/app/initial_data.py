import json
import logging

import requests

from app import crud, schemas
from app.general.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main() -> None:
    logger.info("Creating initial data")
    db = SessionLocal()
    with open('app/general/init_data/interlinkers.json') as json_file:
        interlinkers_data = json.load(json_file)
        for interlinker in interlinkers_data:
            name = interlinker["name"]
            backend = interlinker["backend"]
            init_asset_id = None
            if interlinker["type"] == "KN":
                path = interlinker["path"]

                files_data = {'file': ("demoooo.docx", open(path, "rb"))}
                print(files_data)
                response = requests.post(
                    f"http://{backend}/api/v1/assets/", files=files_data)
                
                print(f"RESPUESTA PARA {backend}")
                files_data = response.json()
                print(files_data)
                init_asset_id = files_data["_id"]
            
            # I don´t know why sometimes a tuple that contains InterlinkerVersionCreate instance is created
            crud.interlinker.create(
                db=db,
                interlinker=schemas.InterlinkerCreate(**{
                    "name": name,
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam lacus sapien, dapibus fringilla dolor sit amet, bibendum aliquam massa. Duis nec faucibus nunc. In sit amet vulputate justo. In dictum turpis eu dolor posuere vehicula. Sed turpis risus, vestibulum sed aliquam id, tempus nec dolor. Nulla facilisi. Suspendisse tempor pulvinar dignissim. Nulla dui ante, finibus in bibendum vel, dignissim nec risus. Nullam gravida nisi quis purus porttitor, sed hendrerit ante tristique. Donec eget augue vitae purus vehicula vehicula non sit amet lacus. Quisque porta nisi pharetra, fringilla felis id, porta arcu. Mauris vel elementum tortor. Ut sed magna id enim finibus molestie eu vitae leo. Mauris at sem elit. Fusce viverra accumsan orci et feugiat. Mauris ullamcorper molestie massa ac faucibus. Integer sit amet tellus tortor. Vivamus bibendum at libero at aliquet. Proin consectetur, erat et vulputate tincidunt, tortor quam euismod elit, id efficitur sem sapien tempus dolor. Aliquam a molestie risus. Nunc rutrum rutrum felis, in malesuada dolor porttitor nec. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nunc condimentum porta magna sed pharetra. In non quam dolor.",
                    "logotype": "string",
                    "published": True,
                    "keywords": [],
                    "documentation": "<>string</>",
                    "SOC_type": "A11",
                    "nature": "SW" if interlinker["type"] == "SW" else "KN",
                    "problemdomains": [],
                    "backend": backend,
                    "init_asset_id": init_asset_id
                    }
                ),
            )
    
    db.close()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
