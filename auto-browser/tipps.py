from pathlib import Path
from typing import List

import yaml
from pydantic import BaseModel


class Begegnungen(BaseModel):
    heim_mannschaft: str
    gast_mannschaft: str
    heim_tore: int
    gast_tore: int

class Spiele(BaseModel):
    spieltag: int
    begegnungen: List[Begegnungen]

class Saison(BaseModel):
    jahr: str
    spiele: List[Spiele]

class Tipps(BaseModel):
    saison: Saison

def load_tipp() -> Tipps:
    script_path = Path(__file__).resolve()
    project_root = script_path.parent.parent
    tipps_path = project_root / 'tipps.yaml'

    with open(tipps_path, 'r') as f:
        data = yaml.safe_load(f)
    return Tipps(**data)
