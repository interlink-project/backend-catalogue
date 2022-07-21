from pydantic import BaseModel, validator
import json
from colors import bcolors


class ProblemProfile(BaseModel):
    id: str
    name_translations: dict
    description_translations: dict
    functionality_translations: dict


problemprofiles_ids = []
with open("./problemprofiles/problemprofiles.json") as json_file:
    for i in json.load(json_file):
        ProblemProfile(**i)
        problemprofiles_ids.append(i["id"])

class WithProblemProfiles(BaseModel):
    problemprofiles: list

    @validator('problemprofiles')
    def problemprofiles_valid(cls, v, values, **kwargs):
        if len(v) == 0:
            print(
                f"{bcolors.WARNING} ## WARNING Problem profiles empty {values}{bcolors.ENDC}"
            ) 
        for id in v:
            if id not in problemprofiles_ids:
                raise ValueError(f'Invalid problem profile id {id}')
        return v
