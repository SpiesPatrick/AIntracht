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

def load_tipp_from_yamlfile() -> Tipps:
    script_path = Path(__file__).resolve()
    project_root = script_path.parent.parent
    tipps_path = project_root / 'tipps.yaml'

    with open(tipps_path, 'r') as f:
        data = yaml.safe_load(f)
    return Tipps(**data)

# convert db to yaml
def form_yaml(tipps, saison, match_day) -> Tipps:
    begegnungen = [Begegnungen(
        heim_mannschaft=r[0],
        gast_mannschaft=r[1],
        heim_tore=r[2],
        gast_tore=r[3]

    ) for r in tipps]

    spiele = Spiele(
        begegnungen=begegnungen,
        saison=saison,
        spieltag=match_day,
    )

    return Tipps(spiele=spiele)

def convert_yaml(obj) -> Tipps:
    data = yaml.safe_load(obj)
    return Tipps(**data)
    # Old way as Backup
    # yaml_string = yaml.dump(data=obj)
    # return Tipps(**obj)
    # return Tipps(**obj)
