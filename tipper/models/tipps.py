from pathlib import Path
from typing import List, Optional

import yaml
from pydantic import BaseModel


class Begegnungen(BaseModel):
    heim_mannschaft: str
    gast_mannschaft: str
    heim_tore: int
    gast_tore: int

class Spiele(BaseModel):
    saison: int
    spieltag: int
    getippt: Optional[bool] = None
    begegnungen: List[Begegnungen]

class Tipps(BaseModel):
    spiele: Spiele

def load_tipp() -> Tipps:
    script_path = Path(__file__).resolve()
    project_root = script_path.parent.parent
    tipps_path = project_root / 'tipps.yaml'

    with open(tipps_path, 'r') as f:
        data = yaml.safe_load(f)
    return Tipps(**data)

def convert_yaml(obj) -> Tipps:
    data = yaml.dump(data=obj)
    return Tipps(**data)
