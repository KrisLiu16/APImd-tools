"""Utilities to load documents from YAML or JSON files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Union

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    yaml = None

from .document import Document


def load_document(source: Union[str, Path]) -> Document:
    """Load a :class:`Document` from a YAML or JSON file."""

    path = Path(source)
    if not path.exists():
        raise FileNotFoundError(path)

    content = path.read_text(encoding="utf-8")
    if not content.strip():
        raise ValueError("Document definition is empty")

    if path.suffix.lower() in {".yaml", ".yml"}:
        if yaml is None:
            raise RuntimeError(
                "PyYAML is required to read YAML files. Install the optional dependency with"
                " `pip install apimd-tools[dev]` or `pip install PyYAML`."
            )
        data = yaml.safe_load(content)
    elif path.suffix.lower() == ".json":
        data = json.loads(content)
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")

    if not isinstance(data, dict):
        raise ValueError("Document definition must be a mapping")

    return Document.from_dict(data)
