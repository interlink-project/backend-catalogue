import json
import logging

import requests

from app import crud, schemas
from app.general.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

interlinkers = [
    {
        "name": "Collaborative editor",
        "nature": "SW",
        "backend": "etherwrapper",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam lacus sapien, dapibus fringilla dolor sit amet, bibendum aliquam massa. Duis nec faucibus nunc. In sit amet vulputate justo. In dictum turpis eu dolor posuere vehicula. Sed turpis risus, vestibulum sed aliquam id, tempus nec dolor. Nulla facilisi. Suspendisse tempor pulvinar dignissim. Nulla dui ante, finibus in bibendum vel, dignissim nec risus. Nullam gravida nisi quis purus porttitor, sed hendrerit ante tristique. Donec eget augue vitae purus vehicula vehicula non sit amet lacus. Quisque porta nisi pharetra, fringilla felis id, porta arcu. Mauris vel elementum tortor. Ut sed magna id enim finibus molestie eu vitae leo. Mauris at sem elit. Fusce viverra accumsan orci et feugiat. Mauris ullamcorper molestie massa ac faucibus. Integer sit amet tellus tortor. Vivamus bibendum at libero at aliquet. Proin consectetur, erat et vulputate tincidunt, tortor quam euismod elit, id efficitur sem sapien tempus dolor. Aliquam a molestie risus. Nunc rutrum rutrum felis, in malesuada dolor porttitor nec. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nunc condimentum porta magna sed pharetra. In non quam dolor.",
        "logo": "/static/demodata/interlinkers/etherpad/logo.jpeg",
        "images": ["/static/demodata/interlinkers/etherpad/screenshot.png"],
        "keywords": "collaborative;document;editor;etherpad",
        "deletable": True,
        "updatable": True,
        "clonable": True
    },
    {
        "name": "File manager",
        "nature": "SW",
        "backend": "filemanager",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam lacus sapien, dapibus fringilla dolor sit amet, bibendum aliquam massa. Duis nec faucibus nunc. In sit amet vulputate justo. In dictum turpis eu dolor posuere vehicula. Sed turpis risus, vestibulum sed aliquam id, tempus nec dolor. Nulla facilisi. Suspendisse tempor pulvinar dignissim. Nulla dui ante, finibus in bibendum vel, dignissim nec risus. Nullam gravida nisi quis purus porttitor, sed hendrerit ante tristique. Donec eget augue vitae purus vehicula vehicula non sit amet lacus. Quisque porta nisi pharetra, fringilla felis id, porta arcu. Mauris vel elementum tortor. Ut sed magna id enim finibus molestie eu vitae leo. Mauris at sem elit. Fusce viverra accumsan orci et feugiat. Mauris ullamcorper molestie massa ac faucibus. Integer sit amet tellus tortor. Vivamus bibendum at libero at aliquet. Proin consectetur, erat et vulputate tincidunt, tortor quam euismod elit, id efficitur sem sapien tempus dolor. Aliquam a molestie risus. Nunc rutrum rutrum felis, in malesuada dolor porttitor nec. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nunc condimentum porta magna sed pharetra. In non quam dolor.",
        "logo": "/static/demodata/interlinkers/filemanager/logo.png",
        "images": ["/static/demodata/interlinkers/filemanager/screenshot.jpeg"],
        "keywords": "static;file;manager",
        "deletable": True,
        "updatable": False,
        "clonable": True
    },
    {
        "name": "Forum",
        "nature": "SW",
        "backend": "forum",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam lacus sapien, dapibus fringilla dolor sit amet, bibendum aliquam massa. Duis nec faucibus nunc. In sit amet vulputate justo. In dictum turpis eu dolor posuere vehicula. Sed turpis risus, vestibulum sed aliquam id, tempus nec dolor. Nulla facilisi. Suspendisse tempor pulvinar dignissim. Nulla dui ante, finibus in bibendum vel, dignissim nec risus. Nullam gravida nisi quis purus porttitor, sed hendrerit ante tristique. Donec eget augue vitae purus vehicula vehicula non sit amet lacus. Quisque porta nisi pharetra, fringilla felis id, porta arcu. Mauris vel elementum tortor. Ut sed magna id enim finibus molestie eu vitae leo. Mauris at sem elit. Fusce viverra accumsan orci et feugiat. Mauris ullamcorper molestie massa ac faucibus. Integer sit amet tellus tortor. Vivamus bibendum at libero at aliquet. Proin consectetur, erat et vulputate tincidunt, tortor quam euismod elit, id efficitur sem sapien tempus dolor. Aliquam a molestie risus. Nunc rutrum rutrum felis, in malesuada dolor porttitor nec. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nunc condimentum porta magna sed pharetra. In non quam dolor.",
        "logo": "/static/demodata/interlinkers/forum/logo.png",
        "images": [],
        "keywords": "forum;chat;conversation;discussion",
        "deletable": True,
        "updatable": True,
        "clonable": True
    },
    {
        "name": "Google Drive",
        "nature": "SW",
        "backend": "googledrive",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam lacus sapien, dapibus fringilla dolor sit amet, bibendum aliquam massa. Duis nec faucibus nunc. In sit amet vulputate justo. In dictum turpis eu dolor posuere vehicula. Sed turpis risus, vestibulum sed aliquam id, tempus nec dolor. Nulla facilisi. Suspendisse tempor pulvinar dignissim. Nulla dui ante, finibus in bibendum vel, dignissim nec risus. Nullam gravida nisi quis purus porttitor, sed hendrerit ante tristique. Donec eget augue vitae purus vehicula vehicula non sit amet lacus. Quisque porta nisi pharetra, fringilla felis id, porta arcu. Mauris vel elementum tortor. Ut sed magna id enim finibus molestie eu vitae leo. Mauris at sem elit. Fusce viverra accumsan orci et feugiat. Mauris ullamcorper molestie massa ac faucibus. Integer sit amet tellus tortor. Vivamus bibendum at libero at aliquet. Proin consectetur, erat et vulputate tincidunt, tortor quam euismod elit, id efficitur sem sapien tempus dolor. Aliquam a molestie risus. Nunc rutrum rutrum felis, in malesuada dolor porttitor nec. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nunc condimentum porta magna sed pharetra. In non quam dolor.",
        "logo": "/static/demodata/interlinkers/googledrive/logo.png",
        "images": ["/static/demodata/interlinkers/googledrive/sheets.png", "/static/demodata/interlinkers/googledrive/docs.png", "/static/demodata/interlinkers/googledrive/slides.png"],
        "keywords": "document;share;edit;slide;collaboration",
        "deletable": True,
        "updatable": False,
        "clonable": True
    },
    {
        "name": "Survey",
        "nature": "SW",
        "backend": "survey",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam lacus sapien, dapibus fringilla dolor sit amet, bibendum aliquam massa. Duis nec faucibus nunc. In sit amet vulputate justo. In dictum turpis eu dolor posuere vehicula. Sed turpis risus, vestibulum sed aliquam id, tempus nec dolor. Nulla facilisi. Suspendisse tempor pulvinar dignissim. Nulla dui ante, finibus in bibendum vel, dignissim nec risus. Nullam gravida nisi quis purus porttitor, sed hendrerit ante tristique. Donec eget augue vitae purus vehicula vehicula non sit amet lacus. Quisque porta nisi pharetra, fringilla felis id, porta arcu. Mauris vel elementum tortor. Ut sed magna id enim finibus molestie eu vitae leo. Mauris at sem elit. Fusce viverra accumsan orci et feugiat. Mauris ullamcorper molestie massa ac faucibus. Integer sit amet tellus tortor. Vivamus bibendum at libero at aliquet. Proin consectetur, erat et vulputate tincidunt, tortor quam euismod elit, id efficitur sem sapien tempus dolor. Aliquam a molestie risus. Nunc rutrum rutrum felis, in malesuada dolor porttitor nec. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nunc condimentum porta magna sed pharetra. In non quam dolor.",
        "logo": "/static/demodata/interlinkers/survey/logo.png",
        "images": ["/static/demodata/interlinkers/survey/screenshot.png"],
        "keywords": "survey;question;voting",
        "deletable": True,
        "updatable": True,
        "clonable": True
    },
    {
        "name": "Skeleton to guide the description of the main aim of the collaborative project",
        "nature": "KN",
        "softwareinterlinker": "googledrive",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam lacus sapien, dapibus fringilla dolor sit amet, bibendum aliquam massa. Duis nec faucibus nunc. In sit amet vulputate justo. In dictum turpis eu dolor posuere vehicula. Sed turpis risus, vestibulum sed aliquam id, tempus nec dolor. Nulla facilisi. Suspendisse tempor pulvinar dignissim. Nulla dui ante, finibus in bibendum vel, dignissim nec risus. Nullam gravida nisi quis purus porttitor, sed hendrerit ante tristique. Donec eget augue vitae purus vehicula vehicula non sit amet lacus. Quisque porta nisi pharetra, fringilla felis id, porta arcu. Mauris vel elementum tortor. Ut sed magna id enim finibus molestie eu vitae leo. Mauris at sem elit. Fusce viverra accumsan orci et feugiat. Mauris ullamcorper molestie massa ac faucibus. Integer sit amet tellus tortor. Vivamus bibendum at libero at aliquet. Proin consectetur, erat et vulputate tincidunt, tortor quam euismod elit, id efficitur sem sapien tempus dolor. Aliquam a molestie risus. Nunc rutrum rutrum felis, in malesuada dolor porttitor nec. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nunc condimentum porta magna sed pharetra. In non quam dolor.",
        "logo": "/static/demodata/interlinkers/knowledge/doc.png",
        "images": [],
        "keywords": "skeleton;aim;project",
        "path": "static/demodata/interlinkers/knowledge/skeleton_to_guide_the_description_of_the_main_aim_of_the_collaborative_project.docx",
    },
]


def main() -> None:
    logger.info("Creating initial data")
    db = SessionLocal()
    for interlinker in interlinkers:
        nature = interlinker["nature"]
        name = interlinker["name"]
        description = interlinker["description"]
        logo = interlinker["logo"]
        keywords = interlinker["keywords"]
        images = interlinker["images"]

        if crud.interlinker.get_by_name(db=db, name=name):
            return
        try:
            data_dict = {
                "name": name,
                "description": description,
                "logotype": logo,
                "images": images,
                "published": True,
                "keywords": keywords,
                "documentation": """
                        # Dillinger
                        ## _The Last Markdown Editor, Ever_

                        Dillinger is a cloud-enabled, mobile-ready, offline-storage compatible,
                        AngularJS-powered HTML5 Markdown editor.

                        - Type some Markdown on the left
                        - See HTML in the right
                        - ✨Magic ✨

                        ## Features

                        - Import a HTML file and watch it magically convert to Markdown
                        - Drag and drop images (requires your Dropbox account be linked)
                        - Import and save files from GitHub, Dropbox, Google Drive and One Drive
                        - Drag and drop markdown and HTML files into Dillinger
                        - Export documents as Markdown, HTML and PDF
                        """,
                "problemdomains": [],
                "functionalities": [],
                # Interlinker
                "constraints": [],
                "regulations": [],
            }
            if nature == "KN":
                path = interlinker["path"]
                files_data = {'file': ("demo.docx", open(path, "rb"))}
                
                backend = interlinker["softwareinterlinker"]
                softwareinterlinker = crud.interlinker.get_softwareinterlinker_by_backend(db=db, backend=backend)
                
                response = requests.post(
                    f"http://{backend}/api/v1/assets/", files=files_data)

                print(f"RESPUESTA PARA {backend}")
                files_data = response.json()
                print(files_data)

                data_dict["nature"] = "knowledgeinterlinker"
                data_dict["softwareinterlinker_id"] = softwareinterlinker.id
                data_dict["genesis_asset_id"] = files_data["_id"]
                schema = schemas.KnowledgeInterlinkerCreate(**data_dict)

            else:
                data_dict["nature"] = "softwareinterlinker"
                data_dict["backend"] = interlinker["backend"]
                data_dict["assets_deletable"] = interlinker["deletable"]
                data_dict["assets_updatable"] = interlinker["updatable"]
                data_dict["assets_clonable"] = interlinker["clonable"]
                schema = schemas.SoftwareInterlinkerCreate(**data_dict)
            # I don´t know why sometimes a tuple that contains InterlinkerVersionCreate instance is created
            crud.interlinker.create(
                db=db,
                interlinker=schema,
            )
        except Exception as e:
            print(str(e))
            pass

    db.close()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
