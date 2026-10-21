#!/usr/bin/env python3
"""Audit publication filtering against saved inventory without a database connection."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from scripts.generator_publish import ImageLibrary, enum, localize_record, prepare_records


class AuditImages(ImageLibrary):
    """Read canonical images in place; store all localized bytes under evidence."""
    def __init__(self, output_root, asset_root, canonical_root):
        super().__init__(output_root, asset_root)
        self.canonical_root = Path(canonical_root).resolve()

    def resolve(self, source):
        reference = source.strip().strip('<>')
        mapped = self.mapping.get(reference, reference)
        parsed = urlsplit(mapped)
        relative = Path(unquote(parsed.path))
        if not parsed.scheme and relative.parts[:1] == ('images',):
            candidate = (self.canonical_root / relative).resolve()
            if candidate.is_relative_to(self.canonical_root) and candidate.is_file():
                data = candidate.read_bytes()
                expected = self.expected_hashes.get(mapped)
                if expected and hashlib.sha256(data).hexdigest() != expected:
                    raise ValueError('Captured image differs from its source manifest: ' + source)
                return self.store(data, source)
        return super().resolve(source)


def audit(records, inventory, source, difficulty, output, asset_root, math_root):
    output, math_root = Path(output).resolve(), Path(math_root).resolve()
    if output.is_relative_to(math_root):
        raise ValueError('Audit output must be outside the published math root')
    if not isinstance(records, list):
        raise ValueError('Input must be a JSON array of generated records')
    for key in ('database', 'lineage', 'kp_id'):
        if inventory.get(key) != source[key]:
            raise ValueError('Inventory/source mismatch: ' + key)
    if any(enum(r['question'].get(':question/difficulty')) != ':question.difficulty/' + difficulty for r in records):
        raise ValueError('Input contains a record outside the requested difficulty; the runner rejects this batch')
    kp_uuid = source['material']['kp'][':knowledge-point/id']
    staged = output / 'assets'

    def localize(record, _math_root, _asset_root):
        return localize_record(record, staged, asset_root,
                               library=AuditImages(staged, asset_root, math_root))

    accepted, duplicates = prepare_records(records, source['kp_id'], kp_uuid,
        inventory['fingerprints'], staged, asset_root, localizer=localize)
    output.mkdir(parents=True, exist_ok=True)
    (output / 'accepted.json').write_text(json.dumps(accepted, indent=2, ensure_ascii=False) + '\n')
    report = {
        'database_writes': 0, 'inventory_basis': inventory['basis'],
        'kp_id': source['kp_id'], 'difficulty': difficulty,
        'input_count': len(records), 'duplicate_count': duplicates, 'accepted_count': len(accepted),
        'accepted_file': 'accepted.json', 'asset_root': 'assets',
        'stages_examined': ['requested difficulty', 'knowledge-point identity', 'image localization',
                            'question validation', 'stable identities', 'inventory and batch deduplication'],
        'limits': ['Uses captured inventory; concurrent publication may change duplicates.',
                   'Does not examine generator rejection/resampling or certify mathematical or pedagogical correctness.',
                   'Does not simulate learner history, weighted selection, database identity collisions, or publication.'],
    }
    (output / 'delivery.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('input', 'inventory', 'source', 'output'):
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--difficulty', choices=('easy', 'moderate', 'hard'), required=True)
    parser.add_argument('--asset-root', type=Path, help='Generated asset directory; defaults to input parent')
    parser.add_argument('--math-root', type=Path, default=Path('/media/jake/SSD/EDB/math'))
    args = parser.parse_args()
    paths = {'input': args.input, 'inventory': args.inventory, 'source': args.source}
    data = {name: json.loads(path.read_text()) for name, path in paths.items()}
    report = audit(data['input'], data['inventory'], data['source'], args.difficulty,
                   args.output, args.asset_root or args.input.resolve().parent, args.math_root)
    report['input_sha256'] = {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in paths.items()}
    report['implementation_sha256'] = {str(path.relative_to(REPO)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in (Path(__file__), REPO / 'scripts/generator_publish.py', REPO / 'capture/scripts/database/images.py')}
    (args.output / 'delivery.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in ('input_count', 'duplicate_count', 'accepted_count', 'inventory_basis')}
                     | {'report': str(args.output / 'delivery.json')}))


if __name__ == '__main__':
    main()
