from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


class AppConfig(BaseModel):
    project_root: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[2])
    raw_dir: Path = Field(default_factory=lambda: Path("data/raw"))
    processed_dir: Path = Field(default_factory=lambda: Path("data/processed"))
    artifacts_dir: Path = Field(default_factory=lambda: Path("artifacts"))
    spacy_model: str = "en_core_web_sm"

    def ensure_directories(self) -> None:
        for path in (self.raw_dir, self.processed_dir, self.artifacts_dir):
            path.mkdir(parents=True, exist_ok=True)


DEFAULT_CONFIG = AppConfig()

