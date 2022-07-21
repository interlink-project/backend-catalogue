import importlib
import json
from pathlib import Path
import sys
from colors import bcolors

# boolean to know if an exception have occurred somewhere
general_error = False

ids = []
# search for schemas
for schema_path in Path("./interlinkers").glob("**/schema.py"):
    schema_error = False
    str_path = str(schema_path)
    pat = str(schema_path.parents[0]).replace("/", ".")
    print(f"{pat}.{schema_path.stem}")
    # schema.py imported dynamically
    Schema = importlib.import_module(
        f"{pat}.{schema_path.stem}"
    ).Schema
    parent_path = schema_path.parents[0]

    print(
        f"\n{bcolors.HEADER}{bcolors.BOLD}Checking {schema_path}{bcolors.ENDC}"
    )
    # searches for metadata inside the parent directory where schema is located
    for metadata_path in Path(str(parent_path)).glob("**/metadata.json"):
        str_path = str(metadata_path)
        with open(str_path) as json_file:
            print(f"{bcolors.OKBLUE}## PROCESSING {bcolors.ENDC}{str_path}{bcolors.OKBLUE}")
            # loads data from metadata.json and validates it
            data = json.load(json_file)
            id = data["id"]
            if id in ids:
                print(f"{bcolors.FAIL}ERROR DETECTED: id {id} already present")
                raise Exception(f"id {id} already present")
            ids.append(id)
            try:
                Schema(**data)
            except Exception as e:
                # if not valid, raises exception, which is captured to continue the execution of the loop
                general_error = True
                schema_error = True
                print(f"{bcolors.FAIL}ERROR DETECTED:")
                print(str(e) + bcolors.ENDC)

        # Show warning if there is not snapshots directory where the metadata.json is located
        if not Path(str(metadata_path.parents[0]) + "/snapshots").is_dir():
            print(
                f"{bcolors.WARNING} ## WARNING Snapshots directory not present{bcolors.ENDC}"
            )
    
    # convert pydantic schema to jsonschema that non-technical users can use to validate data easily
    with open(f"{schema_path.parents[0]}/schema.json", "w") as f:
        json.dump(Schema.schema(), f, indent=4)

    # If this iteration has not thrown any exception, show "all checks passed" 
    schema_error or print(
        f"\n{bcolors.OKGREEN}All checks passed for {schema_path}!{bcolors.ENDC}"
    )


# Validate coproduction tree
from schemas.schemas import Phase, CoproductionSchema
import os

# convert pydantic schema to jsonschema that non-technical users can use to validate data easily
with open(f"schemas/metadata_schema.json", "w") as f:
    json.dump(CoproductionSchema.schema(), f, indent=4)

with open(f"schemas/phase_schema.json", "w") as f:
    json.dump(Phase.schema(), f, indent=4)

print(
        f"\n{bcolors.HEADER}{bcolors.BOLD}Checking coproduction tree{bcolors.ENDC}"
    )

for schema_metadata_path in Path("./schemas").glob("**/metadata.json"):
    with open(str(schema_metadata_path)) as json_file:
        print(f"{bcolors.OKBLUE}## PROCESSING {bcolors.ENDC}{schema_metadata_path}")
        parent = str(schema_metadata_path.parents[0])
        phases = os.listdir(parent + "/phases")
        CoproductionSchema(**json.load(json_file))
        for phase in phases:
            print(f"\t{bcolors.OKCYAN}## PROCESSING {bcolors.ENDC}{phase}")
            with open(parent + "/phases/" + phase) as phase_metadata:
                Phase(**json.load(phase_metadata))
        print(
            f"\n{bcolors.OKGREEN}Phase {schema_metadata_path} valid!{bcolors.ENDC}"
        )
# if an exception has been thrown along the execution of the script, exit with error code
if general_error:
    sys.exit(1)
sys.exit(0)