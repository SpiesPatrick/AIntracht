from pathlib import Path

import yaml
from pydantic import BaseModel


class User(BaseModel):
    name: str
    e_mail: str
    password: str

class Kicktipp(BaseModel):
    group_name: str
    saison_id: str

class Config(BaseModel):
    user: User
    kicktipp: Kicktipp

def load_config() -> Config:
    script_path = Path(__file__).resolve()
    project_root = script_path.parent.parent
    config_path = project_root / "config.yaml"

    with open(config_path, "r") as f:
        data = yaml.safe_load(f)
    return Config(**data)
