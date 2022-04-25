import json
import logging
import ntpath
import os
import shutil
from distutils.dir_util import copy_tree
from pathlib import Path

import requests
from pydantic import BaseModel, parse_obj_as
from slugify import slugify

from app import crud, schemas
from app.general.db.session import SessionLocal
import asyncio
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

    if await crud.interlinker.get_by_name(db=db, name=name):
        print(f"\t{bcolors.WARNING}Already in the database{bcolors.ENDC}")
        return

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
        # create interlinker
        interlinker = await crud.interlinker.create(
            db=db,
            interlinker=schemas.SoftwareInterlinkerCreate(**data),
        )

        if "integration" in data:
            integrationData = data["integration"]
            integrationData["softwareinterlinker_id"] = interlinker.id
            integrationData = {**integrationData, **data["integration"]["capabilities"]}
            integrationData = {**integrationData, **
                            data["integration"]["capabilities_translations"]}
        
            await crud.integration.create(
                db=db,
                obj_in=parse_obj_as(schemas.IntegrationCreate, integrationData)
            )

    if externalknowledge:
        data["nature"] = "externalknowledgeinterlinker"
        interlinker = await crud.interlinker.create(
            db=db,
            interlinker=schemas.ExternalKnowledgeInterlinkerCreate(**data),
        )
    if externalsoftware:
         # set nature
        data["nature"] = "externalsoftwareinterlinker"
        interlinker = await crud.interlinker.create(
            db=db,
            interlinker=schemas.ExternalSoftwareInterlinkerCreate(**data),
        )

    if knowledge:
        # get file contents in file and send to the software interlinker
        service = data["softwareinterlinker"]
        softwareinterlinker = await crud.interlinker.get_softwareinterlinker_by_service_name(
            db=db, service_name=service)
        if not softwareinterlinker:
            print(f"\t{bcolors.FAIL}there is no {service} softwareinterlinker")
            return

        try:
            print(f"\tis {service} supported knowledge interlinker")

            for key, value in data["file_translations"].items():
                filename = path_leaf(value)
                short_filename, file_extension = os.path.splitext(filename)

                if "json" in file_extension:
                    with open(str(folder) + "/" + filename, 'r') as f:
                        response = requests.post(
                            f"http://{service}/assets", data=f.read()).json()
                else:
                    files_data = {
                        'file': (name + file_extension, open(str(folder) + "/" + filename, "rb").read())}
                    response = requests.post(
                        f"http://{service}/assets", files=files_data).json()

                print(f"ANSWER FOR {service}")
                print(response)
                data["softwareinterlinker_id"] = softwareinterlinker.id
                if not "genesis_asset_id_translations" in data:
                    data["genesis_asset_id_translations"] = {}
                data["genesis_asset_id_translations"][key] = response["id"] if "id" in response else response["_id"]

            await crud.interlinker.create(
                db=db,
                interlinker=schemas.KnowledgeInterlinkerCreate(**data)
            )

        except Exception as e:
            error = True
            print(f"\t{bcolors.FAIL}{str(e)}{bcolors.ENDC}")
        if not error:
            print(f"\t{bcolors.OKGREEN}Created successfully!{bcolors.ENDC}")

async def create_problemprofiles(db):
    with open("/app/interlinkers-data/problemprofiles.json") as json_file:
        for problem in json.load(json_file):
            id = problem["id"]
            if not await crud.problemprofile.get(
                db=db,
                id=id
            ):
                await crud.problemprofile.create(
                    db=db,
                    obj_in=schemas.ProblemProfileCreate(**problem)
                )
                print(f"\t{bcolors.OKGREEN}Problem profile {id} successfully!{bcolors.ENDC}")


async def create_coproductionschemas(db):
    if (sc := await crud.coproductionschema.get_by_name(db=db, locale="en", name="Default schema")):
        await crud.coproductionschema.remove(db=db, id=sc.id)
        print("Schema removed")

    if (sc := await crud.coproductionschema.get_by_name(db=db, locale="en", name="hackathon")):
        await crud.coproductionschema.remove(db=db, id=sc.id)
        print("Schema removed")
        
    data = requests.get(
        "https://raw.githubusercontent.com/interlink-project/interlinkers-data/master/all.json").json()
    # with open("/app/interlinkers-data/all.json") as json_file:
    #     data = json.load(json_file)

    for schema_data in data["schemas"]:
        name = schema_data["name_translations"]["en"]
        print(f"{bcolors.OKBLUE}## PROCESSING {bcolors.ENDC}{name}{bcolors.OKBLUE}")
        SCHEMA = await crud.coproductionschema.create(
            db=db,
            obj_in=schemas.CoproductionSchemaCreate(
                **schema_data, is_public=True
            )
        )
        phases_resume = {}
        phase_data: dict
        for phase_data in schema_data["phases"]:
            phase_data["coproductionschema_id"] = SCHEMA.id

            db_phase = await crud.phasemetadata.create(
                db=db,
                phasemetadata=schemas.PhaseMetadataCreate(
                    **phase_data
                )
            )
            phases_resume[phase_data["reference"]] = {
                "id": db_phase.id,
                "prerequisites": phase_data.get("prerequisites", [])
            }

            objectives_resume = {}
            objective_data: dict
            for objective_data in phase_data["objectives"]:
                objective_data["phasemetadata_id"] = db_phase.id

                db_objective = await crud.objectivemetadata.create(
                    db=db,
                    objectivemetadata=schemas.ObjectiveMetadataCreate(
                        **objective_data
                    )
                )
                objectives_resume[objective_data["reference"]] = {
                    "id": db_objective.id,
                    "prerequisites": objective_data.get("prerequisites", [])
                }

                tasks_resume = {}
                task_data: dict
                for task_data in objective_data["tasks"]:
                    task_data["objectivemetadata_id"] = db_objective.id
                    sum = list(task_data["problemprofiles"]) + \
                        list(objective_data["problemprofiles"])
                    task_data["problemprofiles"] = list(set(sum))
                    db_task = await crud.taskmetadata.create(
                        db=db,
                        taskmetadata=schemas.TaskMetadataCreate(
                            **task_data
                        )
                    )
                    tasks_resume[task_data["reference"]] = {
                        "id": db_task.id,
                        "prerequisites": task_data.get("prerequisites", [])
                    }
                # prerequisites
                for key, task_resume in tasks_resume.items():
                    db_taskmetadata = await crud.taskmetadata.get(db=db, id=task_resume["id"])
                    prerequisite_reference: dict
                    for prerequisite_reference in task_resume["prerequisites"]:
                        if (ref := prerequisite_reference.get("item", None)):
                            db_prerequisite = await crud.taskmetadata.get(
                                db=db, id=tasks_resume[ref]["id"])
                            print(db_prerequisite, "is a prerequisite for", db_task)
                            await crud.taskmetadata.add_prerequisite(
                                db=db, taskmetadata=db_taskmetadata, prerequisite=db_prerequisite)
            for key, objective_resume in objectives_resume.items():
                db_objectivemetadata = await crud.objectivemetadata.get(
                    db=db, id=objective_resume["id"])
                prerequisite_reference: dict
                for prerequisite_reference in objective_resume["prerequisites"]:
                    if (ref := prerequisite_reference.get("item", None)):
                        db_prerequisite = await crud.objectivemetadata.get(
                            db=db, id=objectives_resume[ref]["id"])
                        print(db_prerequisite, "is a prerequisite for", db_objective)
                        await crud.objectivemetadata.add_prerequisite(
                            db=db, objectivemetadata=db_objectivemetadata, prerequisite=db_prerequisite)
        print(phases_resume)
        for key, phase_resume in phases_resume.items():
            db_phasemetadata = await crud.phasemetadata.get(db=db, id=phase_resume["id"])
            for prerequisite_reference in phase_resume["prerequisites"]:
                if (ref := prerequisite_reference.get("item", None)):
                    db_prerequisite = await crud.phasemetadata.get(
                        db=db, id=phases_resume[ref]["id"])
                    print(db_prerequisite, "is a prerequisite for", db_phasemetadata)
                    await crud.phasemetadata.add_prerequisite(
                        db=db, phasemetadata=db_phasemetadata, prerequisite=db_prerequisite)


async def init():
    db = SessionLocal()
    set_logging_disabled(True)

    try:

        # create problem profiles
        await create_problemprofiles(db)

        await create_coproductionschemas(db)

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
    
