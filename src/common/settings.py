from functools import cached_property
from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    model_version: str = "v0.0.0"
    random_state: int  = 42
    test_size: float   = 0.2
    data_dir: str      = "/data/mlops-hw05"

    @computed_field
    @cached_property
    def model_path(self) -> str:
        return f"{self.data_dir}/models/model_artifacts_{self.model_version}.pkl"

    # dataset_file: str  = "WineQT.csv"
    # params_file : str  = "params.yaml"
    # tracking_uri: str  = "http://localhost:5000"


settings = Settings()
