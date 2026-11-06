"""Bind active agent results to supplied inputs, separately from their outputs."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
from pathlib import Path
import time


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()


def policy_identity(root, role):
    root = Path(root)
    if not (root / 'generate/pipeline').is_dir():
        root = Path(__file__).resolve().parents[1]
    name = {'investigate': 'investigator', 'author': 'author', 'review': 'reviewer'}[role]
    paths = [root / f'generate/pipeline/{name}.md', root / f'generate/pipeline/{role}.schema.json',
             root / 'generate/pipeline/source-account.md', root / 'generate/pipeline/source-account.schema.json',
             root / 'generate/pipeline/exemplar-review.md',
             root / 'generate/principles.md', root / 'generate/pipeline/validation-tools.md',
             *sorted((root / 'generate/docs').rglob('*.md'))]
    # Follow required local Markdown references outside the guide directory too.
    seen = set()
    while paths:
        path = paths.pop().resolve()
        if path in seen or not path.is_file() or not path.is_relative_to(root.resolve()):
            continue
        seen.add(path)
        if path.suffix == '.md':
            for reference in re.findall(r'(?:\]\(|`)([^\s`\)]+\.md)(?:\)|`)', path.read_text()):
                for candidate in (path.parent / reference, root / reference):
                    if candidate.is_file():
                        paths.append(candidate)
                        break
    return {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(seen)}


def input_binding(role, context, root):
    # Pipeline callers freeze the supplied account/example inputs once per
    # session. A verifier's own edits are outputs, checked by final-binding,
    # and must not invalidate that same verifier's persistent session.
    inputs = context.get('session_inputs')
    if inputs is None:
        inputs = {key: value for key, value in context.items() if key != 'resume_session_id'}
    root = Path(root)
    if not (root / 'generate/pipeline').is_dir():
        root = Path(__file__).resolve().parents[1]
    return {'format': 1, 'role': role, 'inputs': inputs, 'policy_root': str(root), 'policy': policy_identity(root, role)}


def bind_session(directory, binding):
    """Archive stale results without replenishing durable execution budgets."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    for name, identity in binding.get('policy', {}).items():
        source = Path(binding['policy_root']) / name
        target = directory / 'instruction-inputs' / identity / name
        if not target.exists():
            if hashlib.sha256(source.read_bytes()).hexdigest() != identity:
                raise ValueError('Instruction changed while binding session inputs')
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    path = directory / 'input-binding.json'
    previous = json.loads(path.read_text()) if path.exists() else None
    if previous != binding and any((directory / name).exists() for name in ('result.json', 'prompt.txt')):
        archive = directory / 'input-revisions' / (str(time.time_ns()) + '-' + digest(previous)[:12])
        archive.mkdir(parents=True)
        for name in ('input-binding.json', 'result.json', 'prompt.txt', 'supplied-inputs.json', 'session-outputs.json'):
            item = directory / name
            if item.is_file():
                item.replace(archive / name)
    path.write_text(json.dumps(binding, indent=2, ensure_ascii=False) + '\n')

