"""Freeze the full topic audit's source links without changing source captures."""
import hashlib
import json
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
questions = json.loads((HERE / 'questions.json').read_text())
newer = json.loads((HERE / 'newer-source-records.json').read_text())
occurrences = json.loads((HERE / 'source-occurrences.json').read_text())
all_occurrences = json.loads((ROOT / 'reference/edb-math/imports/math-academy/newer-captures/source-occurrences.json').read_text())['records']
original_path = Path('/home/jake/Developer/MA/DATA/Lessons/865/Source/865.html')
original = BeautifulSoup(original_path.read_text(), 'html.parser')
extra_directories = [ROOT / 'reference/mathacademy/capture/linear' / name
                     for name in ['14290754', '14289418', '14274580', '14322646']]
directories = {Path(r['source_directory']) for r in newer}
directories.update(ROOT / r['source_file'] for r in [])
directories.update((ROOT / r['source_file']).parent for r in occurrences)
directories.update(Path(r['source_directory']) for r in all_occurrences
                   if r.get('topic_id') == 865)
directories.update(extra_directories)
directories = sorted(directories)

def descriptor(path, html, role):
    return {'path': str(path), 'role': role, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'html': html}

manifest = []
for question in questions:
    mid = question[':question/math-academy-id']
    number = mid.split('-')[-1]
    row = {'entity': question[':db/id'], 'mid': mid, 'prompt_sources': [], 'solution_sources': []}
    if mid.startswith('q-'):
        node = original.select_one('#question-' + number)
        if node:
            row['prompt_sources'].append(descriptor(original_path, str(node), 'original lesson snapshot'))
    for directory in directories:
        prompt_paths = [directory / (mid + '-before.json')]
        solution_paths = [directory / ('history-' + mid + '.json')]
        if mid.startswith('e-'):
            prompt_paths = [directory / ('example-' + number + '.json')]
            solution_paths = prompt_paths
        observations = directory / 'observations'
        if observations.exists():
            prompt_paths += list(observations.glob('history-' + mid + '-*.json'))
            solution_paths += list(observations.glob('history-solution-' + mid + '-*.json'))
        for role, paths in [('prompt_sources', prompt_paths), ('solution_sources', solution_paths)]:
            for path in paths:
                if not path.is_file():
                    continue
                capture = json.loads(path.read_text())
                html = capture.get('html', '')
                if html:
                    row[role].append(descriptor(path, html, 'saved original DOM'))
    # Original lesson SVGs contain the complete canonical examples, including
    # their source TeX. Keep them as a second independent source for examples.
    if mid.startswith('e-'):
        step_ids = {'e-5427': '19996', 'e-5428': '19997', 'e-5429': '19998', 'e-5430': '19999'}
        node = original.select_one('#step-' + step_ids[mid])
        if node:
            row['prompt_sources'].append(descriptor(original_path, str(node), 'original lesson snapshot'))
            row['solution_sources'].append(descriptor(original_path, str(node), 'original lesson snapshot'))
    manifest.append(row)

(HERE / 'source-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
compact = [{k: ([{a: b for a, b in s.items() if a != 'html'} for s in v]
                    if isinstance(v, list) else v) for k, v in row.items()} for row in manifest]
(HERE / 'source-links.json').write_text(json.dumps(compact, indent=2) + '\n')
missing = [r['mid'] for r in manifest if not r['prompt_sources']]
print(json.dumps({'questions': len(manifest), 'with_original_prompt': len(manifest)-len(missing),
                  'missing_original_prompt': missing,
                  'with_original_solution_capture': sum(bool(r['solution_sources']) for r in manifest)}, indent=2))
