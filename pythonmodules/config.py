from pathlib import Path

import yaml
from pydantic import BaseModel


class Gemini(BaseModel):
    api_key: str
    bot_model: str
class Config(BaseModel):
    gemini: Gemini

def load_config() -> Config:
    script_path = Path(__file__).resolve()
    project_root = script_path.parent.parent
    config_path = project_root / "config.yaml"

    with open(config_path, "r") as f:
        data = yaml.safe_load(f)
    return Config(**data)
