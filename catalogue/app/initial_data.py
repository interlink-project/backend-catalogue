import asyncio
import json
import logging
import ntpath
import os
import shutil
from distutils.dir_util import copy_tree
from pathlib import Path

import requests
from slugify import slugify
from sqlalchemy import MetaData

from app import crud, models, schemas
from app.config import settings
from app.general.db.session import SessionLocal
from app.messages import set_logging_disabled

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# in start-dev.sh and start-prod.sh it is made a git clone of https://github.com/interlink-project/interlinkers-data/

class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def move_file(origin, destination):
    # print(f"Copying from {origin} to {destination}")
    shutil.copy(origin, destination)


def get_snapshots(origin, dest):
    # create directory in static for its files and clean if has contents
    static_path = Path(dest)
    shutil.rmtree(static_path, ignore_errors=True)
    static_path.mkdir(parents=True, exist_ok=True)

    # get snapshots folder content and move them to static folder
    snapshots_folder = str(origin) + "/snapshots"
    static_snapshots_folder = dest + "/snapshots"

    if os.path.isdir(snapshots_folder):
        fol = static_snapshots_folder.replace("/app", "")
        snapshots = [
            f"{fol}/{file}" for file in os.listdir(snapshots_folder) if file.endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))]
        copy_tree(snapshots_folder, static_snapshots_folder)

        print(snapshots)
        return snapshots
    return []


def get_logotype(logotype_path, origin, dest):
    # create directory in static for its files and clean if has contents
    file_path = path_leaf(logotype_path)
    filename, file_extension = os.path.splitext(file_path)
    ori = str(origin) + "/" + file_path
    dst = f"{dest}/logotype{file_extension}"
    move_file(ori, dst)
    print(dst)
    return dst.replace("/app", "")


async def create_interlinker(db, metadata_path, software=False, externalsoftware=False, knowledge=False, externalknowledge=False):
    error = False
    ####################
    # COMMON
    ####################
    str_metadata_path = str(metadata_path)
    with open(str_metadata_path) as json_file:
        data = json.load(json_file)

    name = data["name_translations"]["en"]
    print(f"\n{bcolors.OKBLUE}Processing {bcolors.ENDC}{bcolors.BOLD}{name}{bcolors.ENDC}")

    existing_interlinker = await crud.interlinker.get_by_name(db=db, name=name)
    if (existing_interlinker):
        print(f"\t{bcolors.WARNING}Already in the database{bcolors.ENDC}. UPDATING")

    # parent folder where metadata.json is located
    folder = metadata_path.parents[0]
    slug = slugify(name)
    str_static_path = f'/app/static/{slug}'
    data["snapshots"] = get_snapshots(folder, str_static_path)
    data["logotype"] = get_logotype(
        data["logotype"], folder, str_static_path) if "logotype" in data else None

    # get instructions file contents if IS FILE PATH
    for key, value in data["instructions_translations"].items():
        if not "http" in value:
            filename = path_leaf(value)
            with open(str(folder) + "/" + filename, 'r') as f:
                data["instructions_translations"][key] = f.read()

    if software:
        # set nature
        data["nature"] = "softwareinterlinker"
        data = {**data, **data["integration"]}
        data = {**data, **data["integration"]["capabilities"]}
        data = {**data, **data["integration"]["capabilities_translations"]}
        del data["integration"]

        # create interlinker
        if existing_interlinker:
            interlinker = await crud.interlinker.update(
                db=db,
                db_obj=existing_interlinker,
                obj_in=schemas.SoftwareInterlinkerPatch(**data),
            )
        else:
            interlinker = await crud.interlinker.create(
                db=db,
                interlinker=schemas.SoftwareInterlinkerCreate(**data),
            )


    if externalknowledge:
        data["nature"] = "externalknowledgeinterlinker"

        if existing_interlinker:
            interlinker = await crud.interlinker.update(
                db=db,
                db_obj=existing_interlinker,
                obj_in=schemas.ExternalKnowledgeInterlinkerPatch(**data),
            )
        else:
            interlinker = await crud.interlinker.create(
            db=db,
            interlinker=schemas.ExternalKnowledgeInterlinkerCreate(**data),
        )

        
    if externalsoftware:
         # set nature
        data["nature"] = "externalsoftwareinterlinker"

        if existing_interlinker:
            interlinker = await crud.interlinker.update(
                db=db,
                db_obj=existing_interlinker,
                obj_in=schemas.ExternalSoftwareInterlinkerPatch(**data),
            )
        else:
            interlinker = await crud.interlinker.create(
                db=db,
                interlinker=schemas.ExternalSoftwareInterlinkerCreate(**data),
            )

    if knowledge:
        # get file contents in file and send to the software interlinker
        service = data["softwareinterlinker"]
        softwareinterlinker = await crud.interlinker.get_softwareinterlinker_by_service_name(db=db, service_name=service)
        if not softwareinterlinker:
            print(f"\t{bcolors.FAIL}there is no {service} softwareinterlinker{bcolors.ENDC}")
            return

        try:
            print(f"\tis {service} supported knowledge interlinker")

            #TODO: if softwareinterlinker != existing_interlinker.softwareinterlinker => delete asset
            genesis_asset_id_translations = {}
            for key, value in data["file_translations"].items():
                filename = path_leaf(value)
                short_filename, file_extension = os.path.splitext(filename)

                if "json" in file_extension:
                    with open(str(folder) + "/" + filename, 'r') as f:
                        response = requests.post(
                            f"http://{service}/assets", data=f.read()).json()
                else:
                    filedata = open(str(folder) + "/" + filename, "rb").read()
                    # TODO: hash filedata and check if already exists
                    name_for_file = data["name_translations"][key]
                    files_data = {
                        'file': (name_for_file + file_extension, filedata)}
                    response = requests.post(
                        f"http://{service}/assets", files=files_data).json()

                print(f"{key} ANSWER FOR {service}")
                print(response)
                data["softwareinterlinker_id"] = softwareinterlinker.id
                genesis_asset_id_translations[key] = response["id"] if "id" in response else response["_id"]
            
            data["genesis_asset_id_translations"] = genesis_asset_id_translations
            if existing_interlinker:
                interlinker : models.KnowledgeInterlinker = await crud.interlinker.update(
                    db=db,
                    db_obj=existing_interlinker,
                    obj_in=schemas.KnowledgeInterlinkerPatch(**data),
                )
                if interlinker.genesis_asset_id_translations != genesis_asset_id_translations:
                    raise Exception(f"{interlinker.genesis_asset_id_translations} no es igual a {genesis_asset_id_translations}")
            else:
                interlinker : models.KnowledgeInterlinker = await crud.interlinker.create(
                    db=db,
                    interlinker=schemas.KnowledgeInterlinkerCreate(**data),
                )

        except Exception as e:
            error = True
            print(f"\t{bcolors.FAIL}{str(e)}{bcolors.ENDC}")
        if not error:
            verb = "Created" if not existing_interlinker else "Updated"
            print(f"\t{bcolors.OKGREEN}{verb} successfully!{bcolors.ENDC}")

async def create_problemprofile(db, problem):
    id = problem["id"]
    if pp := await crud.problemprofile.get(
        db=db,
        id=id
    ):
        print(f"\t{bcolors.WARNING}{id} already in the database{bcolors.ENDC}. UPDATING")
        await crud.problemprofile.update(
            db=db,
            db_obj=pp,
            obj_in=schemas.ProblemProfilePatch(**problem)
        )
        return
    await crud.problemprofile.create(
        db=db,
        obj_in=schemas.ProblemProfileCreate(**problem)
    )
    print(f"\t{bcolors.OKGREEN}Problem profile {id} created successfully!{bcolors.ENDC}")


async def create_coproductionschema(db, schema_data):
    name = schema_data["name_translations"]["en"]
    if (sc := await crud.coproductionschema.get_by_name(db=db, locale="en", name=name)):
        print(f"\t{bcolors.WARNING}{name} already in the database{bcolors.ENDC}. UPDATING")
        SCHEMA = await crud.coproductionschema.update(
            db=db,
            db_obj=sc,
            obj_in=schemas.CoproductionSchemaPatch(
                **schema_data, is_public=True
            )
        )
    else:
        SCHEMA = await crud.coproductionschema.create(
        db=db,
        obj_in=schemas.CoproductionSchemaCreate(
            **schema_data, is_public=True
        )
    )

    print(f"{bcolors.OKBLUE}## Processing {bcolors.ENDC}{name}{bcolors.OKBLUE}")     
    for i in SCHEMA.children:
        await crud.treeitems.remove(db=db, id=i.id)
    
    items_resume = {}
    phase_data: dict
    for phase_data in schema_data["phases"]:
        db_phase = await crud.treeitems.create(
            db=db,
            obj_in=schemas.TreeItemCreate(
                **phase_data,
                coproductionschema_id=SCHEMA.id,
                type=models.TreeItemTypes.phase
            )
        )
        items_resume[phase_data["id"]] = {
            "db_id": db_phase.id,
            "prerequisites": phase_data.get("prerequisites", [])
        }

        objective_data: dict
        for objective_data in phase_data["objectives"]:
            db_objective = await crud.treeitems.create(
                db=db,
                obj_in=schemas.TreeItemCreate(
                    **objective_data,
                    parent_id=db_phase.id,
                    type=models.TreeItemTypes.objective
                )
            )
            items_resume[objective_data["id"]] = {
                "db_id": db_objective.id,
                "prerequisites": objective_data.get("prerequisites", [])
            }

            task_data: dict
            for task_data in objective_data["tasks"]:
                sum = list(task_data["problemprofiles"]) + \
                    list(objective_data["problemprofiles"])
                del task_data["problemprofiles"]
                db_task = await crud.treeitems.create(
                    db=db,
                    obj_in=schemas.TreeItemCreate(
                        **task_data,
                        parent_id=db_objective.id,
                        type=models.TreeItemTypes.task,
                        problemprofiles=list(set(sum))
                    )
                )
                items_resume[task_data["id"]] = {
                    "db_id": db_task.id,
                    "prerequisites": task_data.get("prerequisites", [])
                }

    for key, resume in items_resume.items():
        db_treeitem = await crud.treeitems.get(db=db, id=resume["db_id"])
        for prerequisite_id in resume["prerequisites"]:
            if (ref := prerequisite_id.get("item", None)):
                db_prerequisite = await crud.treeitems.get(
                    db=db, id=items_resume[ref]["db_id"])

                print(db_prerequisite, "is a prerequisite for", db_treeitem)
                await crud.treeitems.add_prerequisite(db=db, treeitem=db_treeitem, prerequisite=db_prerequisite)


async def init():
    db = SessionLocal()
    set_logging_disabled(True)

    try:
        # create problem profiles
        with open("/app/interlinkers-data/problemprofiles/problemprofiles.json") as json_file:
            for problem in json.load(json_file):
                await create_problemprofile(db, problem)

        # create coproduction schemas
        # data = requests.get("https://raw.githubusercontent.com/interlink-project/interlinkers-data/master/all.json").json()
        with open("/app/interlinkers-data/all.json") as json_file:
            data = json.load(json_file)
            for schema_data in data["schemas"]:
                await create_coproductionschema(db, schema_data)

        # create external interlinkers first
        for metadata_path in Path("/app/interlinkers-data/interlinkers").glob("externalsoftware/**/metadata.json"):
            await create_interlinker(db, metadata_path, externalsoftware=True)
        
        for metadata_path in Path("/app/interlinkers-data/interlinkers").glob("externalknowledge/**/metadata.json"):
            await create_interlinker(db, metadata_path, externalknowledge=True)

        # create software interlinkers first
        for metadata_path in Path("/app/interlinkers-data/interlinkers").glob("software/**/metadata.json"):
            await create_interlinker(db, metadata_path, software=True)

        # then knowledge interlinkers
        for metadata_path in Path("/app/interlinkers-data/interlinkers").glob("knowledge/**/metadata.json"):
            await create_interlinker(db, metadata_path, knowledge=True)

    except Exception as e:
        raise e
        
    db.close()

if __name__ == "__main__":
    logger.info("Creating initial data")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init())
    logger.info("Initial data created")
    
