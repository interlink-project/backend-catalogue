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


def create_interlinker(metadata_path):
    ####################
    ## COMMON
    ####################
    str_metadata_path = str(metadata_path)
    with open(str_metadata_path) as json_file:
        data = json.load(json_file)

    # if already exists, stop iteration
    data["name_translations"] = data["name"]
    data["description_translations"] = data["description"]
    data["constraints_and_limitations_translations"] = data["constraints_and_limitations"]
    data["regulations_and_standards_translations"] = data["regulations_and_standards"]
    print(data["name_translations"])

    name = data["name"]["en"]
    slug = slugify(name)
    print(f"\n{bcolors.OKBLUE}Processing {bcolors.ENDC}{bcolors.BOLD}{name}{bcolors.ENDC}")

    if crud.interlinker.get_by_name(db=db, name=name):
        print(f"\t{bcolors.WARNING}Already in the database{bcolors.ENDC}")
        return

    parentparent = str(metadata_path.parents[0].parents[0])

    # parent folder where metadata.json is located
    folder = metadata_path.parents[0]

    # create directory in static for its files and clean if has contents
    str_static_path = f'/app/static/{slug}'
    static_path = Path(str_static_path)
    shutil.rmtree(static_path, ignore_errors=True)
    static_path.mkdir(parents=True, exist_ok=True)

    # get snapshots folder content and move them to static folder
    snapshots_folder = str(folder) + "/snapshots"
    static_snapshots_folder = f"{str_static_path}/snapshots"

    if os.path.isdir(snapshots_folder):
        snapshots = [
            f"/static/{slug}/snapshots/{file}" for file in os.listdir(snapshots_folder) if file.endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))]
        copy_tree(snapshots_folder, static_snapshots_folder)
        data["snapshots"] = snapshots

    ####################
    ## SOFTWARE
    ####################
    if "software" in parentparent:
        print("\tis software interlinker")
        # set nature
        data["nature"] = "softwareinterlinker"

        # get logotype and move it to static folder
        file_path = path_leaf(data["logotype"])
        filename, file_extension = os.path.splitext(file_path)
        origin = str(folder) + "/" + file_path
        destination = f"{str_static_path}/logotype{file_extension}"
        move_file(origin, destination)
        data["logotype"] = f"/static/{slug}/logotype{file_extension}"

        # create interlinker
        crud.interlinker.create(
            db=db,
            interlinker=schemas.SoftwareInterlinkerCreate(**data),
        )
        print(f"\t{bcolors.OKGREEN}Created successfully!{bcolors.ENDC}")

    ####################
    ## KNOWLEDGE
    ####################
    if "knowledge" in parentparent:
        error = False
        # set nature
        data["nature"] = "knowledgeinterlinker"

        # get instructions file contents if IS FILE PATH
        if not "http" in data["instructions"]:
            filename = path_leaf(data["instructions"])
            with open(str(folder) + "/" + filename, 'r') as f:
                data["instructions"] = f.read()

        # create knowledge interlinker
        knowledgeinterlinker = crud.interlinker.create(
                db=db,
                interlinker=schemas.KnowledgeInterlinkerCreate(**data),
            )

        # loop over representations and create them
        for representation in data["representations"]:
            # get file contents in file and send to the software interlinker

            service = representation["softwareinterlinker"]
            softwareinterlinker = crud.interlinker.get_softwareinterlinker_by_path(
                db=db, path=service)
            if not softwareinterlinker:
                print(f"\t{bcolors.FAIL}there is no {service} softwareinterlinker")
                return
            
            try:
                print(f"\tis {service} supported knowledge interlinker")

                filename = path_leaf(representation["file"])
                short_filename, file_extension = os.path.splitext(filename)
                
                if "json" in file_extension:
                    with open(str(folder) + "/" + filename, 'r') as f:
                        response = requests.post(
                            f"http://{service}/assets", data=f.read()).json()
                else:
                    files_data = {'file': (name + file_extension, open(str(folder) + "/" + filename, "rb").read())}
                    response = requests.post(
                        f"http://{service}/assets", files=files_data).json()

                print(f"ANSWER FOR {service}")
                print(response)
                representation["knowledgeinterlinker_id"] = knowledgeinterlinker.id
                representation["softwareinterlinker_id"] = softwareinterlinker.id
                representation["genesis_asset_id"] = response["id"] if "id" in response else response["_id"]
                print(f"\t{bcolors.HEADER}Representation with {service} created successfully!{bcolors.ENDC}")
                crud.representation.create(
                    db=db,
                    representation=schemas.RepresentationCreate(**representation)
                )
            except Exception as e:
                error = True
                print(f"\t{bcolors.FAIL}{str(e)}{bcolors.ENDC}")

            if error:
                crud.interlinker.remove(db=db, id=knowledgeinterlinker.id)
            else:
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
                problem["name_translations"] =  problem["name"]
                problem["description_translations"] =  problem["description"]
                problem["functionality_translations"] =  problem["functionality"]
                crud.problemprofile.create(
                    db=db,
                    problemprofile=schemas.ProblemProfileCreate(**problem)
                )
                print(f"\t{bcolors.OKGREEN}Problem profile {id} successfully!{bcolors.ENDC}")

    # create software interlinkers first
    for metadata_path in Path("/app/interlinkers-data/interlinkers").glob("software/**/metadata.json"):
        create_interlinker(metadata_path)

    # then knowledge interlinkers
    for metadata_path in Path("/app/interlinkers-data/interlinkers").glob("knowledge/**/metadata.json"):
        create_interlinker(metadata_path)

    
    db.close()
    logger.info("Initial data created")
