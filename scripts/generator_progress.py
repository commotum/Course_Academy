"""Durable no-progress fingerprints for generator repair jobs."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def material_identity(pipeline):
    """Count runtime changes, not fresh agent reports or growing history files."""
    try:
        candidate = pipeline.candidate_hash()
    except (KeyError, OSError, TypeError, ValueError):
        # An incomplete authoring attempt may not have a valid manifest yet.
        # Restrict fallback evidence to authored source/configuration files.
        workspace = pipeline.directory / 'workspace'
        candidate = _digest({str(path.relative_to(workspace)): hashlib.sha256(path.read_bytes()).hexdigest()
                             for path in sorted(workspace.rglob('*'))
                             if path.is_file() and not path.is_symlink()
                             and path.suffix in {'.py', '.json', '.toml', '.yaml', '.yml'}
                             and not any(part.startswith('.') or part == '__pycache__' for part in path.relative_to(workspace).parts)})
    return {'candidate': candidate, 'source': pipeline.state.get('source_hash'),
            'engine': pipeline.engine_identity()}


def failure_signature(reason, material):
    """Normalize per-attempt directories so the same failure stays identical."""
    def normalize(value):
        if isinstance(value, str):
            return re.sub(r'\b(author|runtime|outputs|review)-\d+\b', r'\1-ATTEMPT', value)
        if isinstance(value, list):
            return [normalize(item) for item in value]
        if isinstance(value, dict):
            return {key: normalize(item) for key, item in value.items()
                    if key not in {'timestamp', 'created', 'updated', 'attempt'}}
        return value
    return _digest({'failure': normalize(reason), 'material': material})
