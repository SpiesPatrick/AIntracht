from pathlib import Path

import yaml
from pydantic import BaseModel


class Begegnungen(BaseModel):
    heim_mannschaft: str
    gast_mannschaft: str
    heim_tore: int
    gast_tore: int

class Spiele(BaseModel):
    spieltag: int
    begegnungen: Begegnungen

class Saison(BaseModel):
    jahr: str
    spiele: Spiele


class Config(BaseModel):
    saison: Saison
    saison: Saison
