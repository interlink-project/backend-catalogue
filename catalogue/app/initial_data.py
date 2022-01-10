import json
import logging

import requests

from app import crud, schemas
from app.general.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

interlinkers = [
    {
        "name": "Skeleton to guide the description of the main aim of the collaborative project",
        "nature": "KN",
        "backend": "googledrive",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam lacus sapien, dapibus fringilla dolor sit amet, bibendum aliquam massa. Duis nec faucibus nunc. In sit amet vulputate justo. In dictum turpis eu dolor posuere vehicula. Sed turpis risus, vestibulum sed aliquam id, tempus nec dolor. Nulla facilisi. Suspendisse tempor pulvinar dignissim. Nulla dui ante, finibus in bibendum vel, dignissim nec risus. Nullam gravida nisi quis purus porttitor, sed hendrerit ante tristique. Donec eget augue vitae purus vehicula vehicula non sit amet lacus. Quisque porta nisi pharetra, fringilla felis id, porta arcu. Mauris vel elementum tortor. Ut sed magna id enim finibus molestie eu vitae leo. Mauris at sem elit. Fusce viverra accumsan orci et feugiat. Mauris ullamcorper molestie massa ac faucibus. Integer sit amet tellus tortor. Vivamus bibendum at libero at aliquet. Proin consectetur, erat et vulputate tincidunt, tortor quam euismod elit, id efficitur sem sapien tempus dolor. Aliquam a molestie risus. Nunc rutrum rutrum felis, in malesuada dolor porttitor nec. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nunc condimentum porta magna sed pharetra. In non quam dolor.",
        "logo": "/static/demodata/interlinkers/knowledge/doc.png",
        "images": [],
        "keywords": "skeleton;aim;project",
        "path": "static/demodata/interlinkers/knowledge/skeleton_to_guide_the_description_of_the_main_aim_of_the_collaborative_project.docx",
    },
    {
        "name": "Collaborative editor",
        "nature": "SW",
        "backend": "etherwrapper",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam lacus sapien, dapibus fringilla dolor sit amet, bibendum aliquam massa. Duis nec faucibus nunc. In sit amet vulputate justo. In dictum turpis eu dolor posuere vehicula. Sed turpis risus, vestibulum sed aliquam id, tempus nec dolor. Nulla facilisi. Suspendisse tempor pulvinar dignissim. Nulla dui ante, finibus in bibendum vel, dignissim nec risus. Nullam gravida nisi quis purus porttitor, sed hendrerit ante tristique. Donec eget augue vitae purus vehicula vehicula non sit amet lacus. Quisque porta nisi pharetra, fringilla felis id, porta arcu. Mauris vel elementum tortor. Ut sed magna id enim finibus molestie eu vitae leo. Mauris at sem elit. Fusce viverra accumsan orci et feugiat. Mauris ullamcorper molestie massa ac faucibus. Integer sit amet tellus tortor. Vivamus bibendum at libero at aliquet. Proin consectetur, erat et vulputate tincidunt, tortor quam euismod elit, id efficitur sem sapien tempus dolor. Aliquam a molestie risus. Nunc rutrum rutrum felis, in malesuada dolor porttitor nec. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nunc condimentum porta magna sed pharetra. In non quam dolor.",
        "logo": "/static/demodata/interlinkers/etherpad/logo.jpeg",
        "images": ["/static/demodata/interlinkers/etherpad/screenshot.png"],
        "keywords": "collaborative;document;editor;etherpad",
    },
    {
        "name": "File manager",
        "nature": "SW",
        "backend": "filemanager",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam lacus sapien, dapibus fringilla dolor sit amet, bibendum aliquam massa. Duis nec faucibus nunc. In sit amet vulputate justo. In dictum turpis eu dolor posuere vehicula. Sed turpis risus, vestibulum sed aliquam id, tempus nec dolor. Nulla facilisi. Suspendisse tempor pulvinar dignissim. Nulla dui ante, finibus in bibendum vel, dignissim nec risus. Nullam gravida nisi quis purus porttitor, sed hendrerit ante tristique. Donec eget augue vitae purus vehicula vehicula non sit amet lacus. Quisque porta nisi pharetra, fringilla felis id, porta arcu. Mauris vel elementum tortor. Ut sed magna id enim finibus molestie eu vitae leo. Mauris at sem elit. Fusce viverra accumsan orci et feugiat. Mauris ullamcorper molestie massa ac faucibus. Integer sit amet tellus tortor. Vivamus bibendum at libero at aliquet. Proin consectetur, erat et vulputate tincidunt, tortor quam euismod elit, id efficitur sem sapien tempus dolor. Aliquam a molestie risus. Nunc rutrum rutrum felis, in malesuada dolor porttitor nec. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nunc condimentum porta magna sed pharetra. In non quam dolor.",
        "logo": "/static/demodata/interlinkers/filemanager/logo.png",
        "images": ["/static/demodata/interlinkers/filemanager/screenshot.jpeg"],
        "keywords": "static;file;manager",
    },
    {
        "name": "Forum",
        "nature": "SW",
        "backend": "forum",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam lacus sapien, dapibus fringilla dolor sit amet, bibendum aliquam massa. Duis nec faucibus nunc. In sit amet vulputate justo. In dictum turpis eu dolor posuere vehicula. Sed turpis risus, vestibulum sed aliquam id, tempus nec dolor. Nulla facilisi. Suspendisse tempor pulvinar dignissim. Nulla dui ante, finibus in bibendum vel, dignissim nec risus. Nullam gravida nisi quis purus porttitor, sed hendrerit ante tristique. Donec eget augue vitae purus vehicula vehicula non sit amet lacus. Quisque porta nisi pharetra, fringilla felis id, porta arcu. Mauris vel elementum tortor. Ut sed magna id enim finibus molestie eu vitae leo. Mauris at sem elit. Fusce viverra accumsan orci et feugiat. Mauris ullamcorper molestie massa ac faucibus. Integer sit amet tellus tortor. Vivamus bibendum at libero at aliquet. Proin consectetur, erat et vulputate tincidunt, tortor quam euismod elit, id efficitur sem sapien tempus dolor. Aliquam a molestie risus. Nunc rutrum rutrum felis, in malesuada dolor porttitor nec. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nunc condimentum porta magna sed pharetra. In non quam dolor.",
        "logo": "/static/demodata/interlinkers/forum/logo.png",
        "images": [],
        "keywords": "forum;chat;conversation;discussion",
    },
    {
        "name": "Google Drive",
        "nature": "SW",
        "backend": "googledrive",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam lacus sapien, dapibus fringilla dolor sit amet, bibendum aliquam massa. Duis nec faucibus nunc. In sit amet vulputate justo. In dictum turpis eu dolor posuere vehicula. Sed turpis risus, vestibulum sed aliquam id, tempus nec dolor. Nulla facilisi. Suspendisse tempor pulvinar dignissim. Nulla dui ante, finibus in bibendum vel, dignissim nec risus. Nullam gravida nisi quis purus porttitor, sed hendrerit ante tristique. Donec eget augue vitae purus vehicula vehicula non sit amet lacus. Quisque porta nisi pharetra, fringilla felis id, porta arcu. Mauris vel elementum tortor. Ut sed magna id enim finibus molestie eu vitae leo. Mauris at sem elit. Fusce viverra accumsan orci et feugiat. Mauris ullamcorper molestie massa ac faucibus. Integer sit amet tellus tortor. Vivamus bibendum at libero at aliquet. Proin consectetur, erat et vulputate tincidunt, tortor quam euismod elit, id efficitur sem sapien tempus dolor. Aliquam a molestie risus. Nunc rutrum rutrum felis, in malesuada dolor porttitor nec. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nunc condimentum porta magna sed pharetra. In non quam dolor.",
        "logo": "/static/demodata/interlinkers/googledrive/logo.png",
        "images": ["/static/demodata/interlinkers/googledrive/sheets.png", "/static/demodata/interlinkers/googledrive/docs.png", "/static/demodata/interlinkers/googledrive/slides.png"],
        "keywords": "document;share;edit;slide;collaboration",
    }
]

def main() -> None:
    logger.info("Creating initial data")
    db = SessionLocal()
    for interlinker in interlinkers:
        nature = interlinker["nature"]
        name = interlinker["name"]
        backend = interlinker["backend"]
        description = interlinker["description"]
        logo = interlinker["logo"]
        keywords = interlinker["keywords"]
        images = interlinker["images"]
        init_asset_id = None

        if crud.interlinker.get_by_name(db=db, name=name):
            return
        try:
            if nature == "KN":
                path = interlinker["path"]
                files_data = {'file': ("demoooo.docx", open(path, "rb"))}
                print(files_data)
                response = requests.post(
                    f"http://{backend}/api/v1/assets/", files=files_data)
                
                print(f"RESPUESTA PARA {backend}")
                files_data = response.json()
                print(files_data)
                init_asset_id = files_data["_id"]
            
            print(images)
            # I don´t know why sometimes a tuple that contains InterlinkerVersionCreate instance is created
            crud.interlinker.create(
                db=db,
                interlinker=schemas.InterlinkerCreate(**{
                    "name": name,
                    "description": description,
                    "logotype": logo,
                    "images": images,
                    "published": True,
                    "keywords": keywords,
                    "documentation": "<>string</>",
                    "SOC_type": "A11",
                    "nature": nature,
                    "problemdomains": [],
                    "backend": backend,
                    "init_asset_id": init_asset_id
                    }
                ),
            )
        except Exception as e:
            print(str(e))
            pass

    db.close()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
