from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Iterator, TypeVar

from pydantic import BaseModel, ValidationError


ModelT = TypeVar("ModelT", bound=BaseModel)


def stream_jsonl(
    path: str | Path,
    model: type[ModelT] | None = None,
    errors_path: str | Path | None = None,
) -> Iterator[dict[str, Any] | ModelT]:
    source_path = Path(path)
    error_target = Path(errors_path) if errors_path else None

    with source_path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue

            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                log_invalid_row(
                    error_target,
                    source=source_path,
                    line_number=line_number,
                    raw_line=line,
                    error_type="malformed_json",
                    message=str(exc),
                )
                continue

            if model is None:
                yield payload
                continue

            try:
                yield model.model_validate(payload)
            except ValidationError as exc:
                log_invalid_row(
                    error_target,
                    source=source_path,
                    line_number=line_number,
                    raw_line=line,
                    error_type="validation_error",
                    message=exc.json(),
                )


def load_jsonl(
    path: str | Path,
    model: type[ModelT] | None = None,
    errors_path: str | Path | None = None,
) -> list[dict[str, Any] | ModelT]:
    return list(stream_jsonl(path, model=model, errors_path=errors_path))


def log_invalid_row(
    errors_path: Path | None,
    *,
    source: Path,
    line_number: int,
    raw_line: str,
    error_type: str,
    message: str,
) -> None:
    if errors_path is None:
        return

    record = {
        "source": str(source),
        "line_number": line_number,
        "error_type": error_type,
        "message": message,
        "raw_line": raw_line,
    }
    errors_path.parent.mkdir(parents=True, exist_ok=True)
    with errors_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=True) + "\n")


def write_jsonl(path: str | Path, records: Iterable[dict[str, Any]]) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=True) + "\n")
