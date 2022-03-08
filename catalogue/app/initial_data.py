import json
import logging
import ntpath
import os
import shutil
from distutils.dir_util import copy_tree
from pathlib import Path

import requests
from slugify import slugify

from app import crud, schemas
from app.general.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# in start-dev.sh and start-prod.sh it is made a git clone of https://github.com/interlink-project/interlinkers-data/

db = SessionLocal()


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


def create_softwareinterlinker(metadata_path):
    ####################
    # COMMON
    ####################
    str_metadata_path = str(metadata_path)
    with open(str_metadata_path) as json_file:
        data = json.load(json_file)

    name = data["name_translations"]["en"]
    print(f"\n{bcolors.OKBLUE}Processing {bcolors.ENDC}{bcolors.BOLD}{name}{bcolors.ENDC}")

    if crud.interlinker.get_by_name(db=db, name=name):
        print(f"\t{bcolors.WARNING}Already in the database{bcolors.ENDC}")
        return

    # parent folder where metadata.json is located
    folder = metadata_path.parents[0]
    slug = slugify(name)
    str_static_path = f'/app/static/{slug}'
    data["snapshots"] = get_snapshots(folder, str_static_path)
    data["logotype"] = get_logotype(data["logotype"], folder, str_static_path) if "logotype" in data else None

    # set nature
    data["nature"] = "softwareinterlinker"

    print(data)
    # create interlinker
    interlinker = crud.interlinker.create(
        db=db,
        interlinker=schemas.SoftwareInterlinkerCreate(**data),
    )

    if "integration" in data:
        integrationData = data["integration"]
        integrationData["softwareinterlinker_id"] = interlinker.id

        # capabilities to root
        integrationData = {**integrationData, **data["integration"]["capabilities"]}
        integrationData = {**integrationData, **data["integration"]["capabilities_translations"]}
        
        crud.integration.create(
            db=db,
            obj_in=schemas.IntegrationCreate(**integrationData)
        )

    print(f"\t{bcolors.OKGREEN}Created successfully!{bcolors.ENDC}")


def create_knowledgeinterlinker(metadata_path):
    str_metadata_path = str(metadata_path)
    with open(str_metadata_path) as json_file:
        knowledgeinterlinker = json.load(json_file)

    name = knowledgeinterlinker["name_translations"]["en"]
    print(f"\n{bcolors.OKBLUE}Processing {bcolors.ENDC}{bcolors.BOLD}{name}{bcolors.ENDC}")

    if crud.interlinker.get_by_name(db=db, name=name):
        print(f"\t{bcolors.WARNING}Already in the database{bcolors.ENDC}")
        return

    error = False
    # loop over representations and create them
    
    knowledgeinterlinker["nature"] = "knowledgeinterlinker"

    folder = metadata_path.parents[0]
    slug = slugify(name)

    # get instructions file contents if IS FILE PATH
    for key, value in knowledgeinterlinker["instructions_translations"].items():
        if not "http" in value:
            filename = path_leaf(value)
            with open(str(folder) + "/" + filename, 'r') as f:
                knowledgeinterlinker["instructions_translations"][key] = f.read()

    # get file contents in file and send to the software interlinker
    service = knowledgeinterlinker["softwareinterlinker"]
    softwareinterlinker = crud.interlinker.get_softwareinterlinker_by_service_name(
        db=db, service_name=service)
    if not softwareinterlinker:
        print(f"\t{bcolors.FAIL}there is no {service} softwareinterlinker")
        return

    try:
        print(f"\tis {service} supported knowledge interlinker")

        for key, value in knowledgeinterlinker["file_translations"].items():
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
            knowledgeinterlinker["softwareinterlinker_id"] = softwareinterlinker.id
            if not "genesis_asset_id_translations" in knowledgeinterlinker:
                knowledgeinterlinker["genesis_asset_id_translations"] = {}
            knowledgeinterlinker["genesis_asset_id_translations"][key] = response["id"] if "id" in response else response["_id"]

        # parent folder where metadata.json is located
        str_static_path = f'/app/static/{slug}'
        knowledgeinterlinker["snapshots"] = get_snapshots(folder, str_static_path)
            
        crud.interlinker.create(
            db=db,
            interlinker=schemas.KnowledgeInterlinkerCreate(
                **knowledgeinterlinker)
        )
        print(
            f"\t{bcolors.HEADER}Knowledge interlinker with {service} created successfully!{bcolors.ENDC}")
        
    except Exception as e:
        error = True
        print(f"\t{bcolors.FAIL}{str(e)}{bcolors.ENDC}")

    if not error:
        print(f"\t{bcolors.OKGREEN}Created successfully!{bcolors.ENDC}")


if __name__ == "__main__":
    logger.info("Creating initial data")

    # create problem profiles
    with open("/app/interlinkers-data/problem_profiles.json") as json_file:
        for problem in json.load(json_file):
            id = problem["id"]
            if not crud.problemprofile.get(
                db=db,
                id=id
            ):
                crud.problemprofile.create(
                    db=db,
                    problemprofile=schemas.ProblemProfileCreate(**problem)
                )
                print(f"\t{bcolors.OKGREEN}Problem profile {id} successfully!{bcolors.ENDC}")

    # create software interlinkers first
    for metadata_path in Path("/app/interlinkers-data/interlinkers").glob("software/**/metadata.json"):
        create_softwareinterlinker(metadata_path)

    # then knowledge interlinkers
    for metadata_path in Path("/app/interlinkers-data/interlinkers").glob("knowledge/**/metadata.json"):
        create_knowledgeinterlinker(metadata_path)

    db.close()
    logger.info("Initial data created")
