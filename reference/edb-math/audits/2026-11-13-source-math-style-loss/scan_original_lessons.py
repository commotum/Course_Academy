"""Read original lesson HTML; adjacent normalized JSON supplies identities only."""
import collections
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'scripts'))
from audit_capture_math_styles_sources import extract_html, digest, dump, STYLE

base = Path('/home/jake/Developer/MA/DATA/Lessons')
paths = [p for p in subprocess.check_output(['rg', '--files', '--no-ignore', str(base), '-g', '*.html'], text=True).splitlines() if Path(p).parent.name == 'Source']
cache, records, counts = {}, {}, collections.Counter()
start = time.time()
with (HERE / 'external-source-inventory.jsonl').open('w') as inventory, (HERE / 'external-source-unknowns.jsonl').open('w') as unknowns, (HERE / 'external-source-formulas.jsonl').open('w') as output:
    for rawpath in sorted(paths):
        path = Path(rawpath)
        meta_path = path.with_suffix('.json')
        row = {'path': rawpath}
        counts['files_enumerated'] += 1
        try:
            if not meta_path.exists():
                row['status'] = 'missing_identity_sidecar'
            else:
                metadata = json.loads(meta_path.read_text())
                mapping = {}
                for item in metadata.get('lesson', {}).get('items', []):
                    dom = item.get('dom_id')
                    if not dom:
                        continue
                    if item.get('item_type') == 'question' and item.get('question_id'):
                        mapping[dom] = 'q-' + str(item['question_id'])
                    elif item.get('step_type') in ('example', 'tutorial') and item.get('content_id'):
                        prefix = 'e-' if item['step_type'] == 'example' else 'tutorial-'
                        mapping[dom] = prefix + str(item['content_id'])
                content = path.read_text()
                counts['bytes_examined'] += path.stat().st_size
                row['sha256'] = hashlib.sha256(content.encode()).hexdigest()
                row['identity_mappings'] = len(mapping)
                if not STYLE.search(content):
                    row['status'] = 'no_style_signature'
                else:
                    found = extract_html(content, {}, mapping, cache)
                    row['formulas'] = len(found)
                    for formula in found:
                        identity = formula['math_academy_id']
                        evidence = {'path': rawpath, 'locator': formula['locator'], 'role': formula['role']}
                        if not identity:
                            counts['unknown_identity_formulas'] += 1
                            unknowns.write(dump({'source_path': rawpath, **formula}) + '\n')
                            continue
                        key = digest(dump([identity, formula['role'], formula['source_tex'], formula['errors']]))
                        if key not in records:
                            record = {**formula, 'formula_hash': key, 'source_path': rawpath,
                                      'evidence': [evidence], 'evidence_count': 1,
                                      'coverage': 'Original lesson HTML; normalized sidecar used only for DOM-to-MA identity mapping'}
                            records[key] = record
                            output.write(dump(record) + '\n')
                        counts['identified_formula_occurrences'] += 1
                    row['status'] = 'processed_original_html'
        except Exception as error:
            row.update(status='error', error=repr(error))
        counts[row['status']] += 1
        inventory.write(dump(row) + '\n')
        if counts['files_enumerated'] % 100 == 0:
            output.flush()
            print(dump({'files': counts['files_enumerated'], 'unique_formulas': len(records), 'seconds': round(time.time() - start)}), flush=True)
summary = {'complete': True, 'root': str(base), 'counts': dict(counts),
           'unique_formulas': len(records), 'identities': len({r['math_academy_id'] for r in records.values()}),
           'formula_errors': sum(bool(r['errors']) for r in records.values()),
           'elapsed_seconds': round(time.time() - start, 2),
           'normalized_json_used_for_math_evidence': False}
(HERE / 'external-source-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary, indent=2))
