"""Consolidate reviewed source-backed math-only repairs and renderer inputs."""
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def entities(value):
    if isinstance(value, dict):
        if ':db/id' in value:
            yield value
        for child in value.values():
            yield from entities(child)
    elif isinstance(value, list):
        for child in value:
            yield from entities(child)


def update(value, proposals):
    for entity in entities(value):
        for proposal in proposals:
            if entity[':db/id'] == proposal['entity'] and proposal['attribute'] in entity:
                assert entity[proposal['attribute']] == proposal['before']
                entity[proposal['attribute']] = proposal['after']


if __name__ == '__main__':
    snapshot = json.loads((HERE / 'snapshot.json').read_text())
    proposals = sum((json.loads((HERE / (name + '-proposals.json')).read_text())
                     for name in ['lines2d', 'lines3d', 'planes']), [])
    keys = [(p['entity'], p['attribute']) for p in proposals]
    assert len(keys) == len(set(keys))
    allowed = {':question/problem', ':question/worked-solution', ':answer-field/key', ':answer/value'}
    for proposal in proposals:
        assert proposal['attribute'] in allowed and proposal['before'] != proposal['after']
        matches = [e for e in entities(snapshot) if e[':db/id'] == proposal['entity'] and proposal['attribute'] in e]
        assert matches and all(e[proposal['attribute']] == proposal['before'] for e in matches)
    source_paths = sorted({s.split('#')[0] for p in proposals for s in p['source']})
    hashes = {s: hashlib.sha256((ROOT / s).read_bytes()).hexdigest() for s in source_paths}
    manifest = {'basis_reviewed': snapshot['basis'], 'proposals': proposals, 'source_sha256': hashes,
                'changed_attributes': len(proposals),
                'changed_questions': len({p['entity'] for p in proposals if p['attribute'].startswith(':question/')})}
    (HERE / 'proposal.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    proposed = copy.deepcopy(snapshot)
    update(proposed, proposals)
    fields = {}
    for entity in entities(proposed):
        for attr in (*sorted(allowed), ':tutorial/content'):
            value = entity.get(attr)
            if isinstance(value, str) and value:
                fields[entity[':db/id'], attr] = {'entity': entity[':db/id'], 'attribute': attr, 'value': value}
    (HERE / 'render-input.json').write_text(json.dumps(list(fields.values()), indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'changed_attributes': len(proposals), 'changed_questions': manifest['changed_questions'],
                      'source_files': len(hashes), 'render_fields': len(fields)}))
