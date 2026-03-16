from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class CheckpointState:
    completed_keys: set[str] = field(default_factory=set)
    metadata: dict[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {
            "completed_keys": sorted(self.completed_keys),
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, object] | None) -> "CheckpointState":
        if not payload:
            return cls()
        completed_keys = payload.get("completed_keys", [])
        metadata = payload.get("metadata", {})
        if not isinstance(completed_keys, list):
            completed_keys = []
        if not isinstance(metadata, dict):
            metadata = {}
        return cls(completed_keys=set(str(key) for key in completed_keys), metadata=dict(metadata))


class CheckpointStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> CheckpointState:
        if not self.path.exists():
            return CheckpointState()
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        return CheckpointState.from_dict(payload)

    def save(self, state: CheckpointState) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(state.to_dict(), indent=2, sort_keys=True),
            encoding="utf-8",
        )

    def mark_completed(self, key: str) -> CheckpointState:
        state = self.load()
        state.completed_keys.add(key)
        self.save(state)
        return state
