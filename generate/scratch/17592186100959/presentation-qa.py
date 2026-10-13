#!/usr/bin/env python3
"""Presentation-only review rebuild and unchanged-record/fidelity regression.
Existing symbolic and native reports remain valid: no mathematical records change.
"""
from pathlib import Path
import hashlib,importlib.util,json,subprocess
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
review_bytes=(HERE/'review.json').read_bytes();review=json.loads(review_bytes)
source_matches=0;levels=set()
for row in review:
    r=row['record'];meta=r['generation'];level=r['question'][':question/difficulty'].rsplit('/',1)[1]
    regenerated=g.generate(level,seed=meta['seed'],template=meta['template'],parameters=meta['parameters'] if meta['evidence_only'] else None,profile=meta['bank_profile'])
    assert regenerated==r,'Presentation revision altered a mathematical record'
    rendered=g.markdown(r)
    assert g.preview_label(r) in rendered
    assert rendered.count('**(correct)**')==1 and rendered.count('**Correct answer:**')==1
    correct_id=r['question'][':question/answer-fields'][0][':answer-field/correct'][1]
    correct=next(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'] if a[':answer/id']==correct_id)
    assert '**Correct answer:** '+correct in rendered
    if meta['evidence_only']:
        assert level=='moderate' and 'Observed' in rendered and 'evidence only' in rendered
    else:
        assert 'Authored' in rendered;levels.add(level)
    if row['label'].startswith('original '):
        q=g.SOURCES[meta['source_id']]
        assert r['question'][':question/problem']==q[':question/problem']
        assert r['question'][':question/worked-solution']==q[':question/worked-solution']
        source_matches+=1
assert source_matches==11 and levels=={'easy','moderate','hard'}
md=['## '+row['label']+' | '+g.preview_label(row['record'])+'\n\n'+g.markdown(row['record']) for row in review]
(HERE/'review.md').write_text('# Originals and labeled generated variants\n\n'+'\n\n'.join(md)+'\n')
assert (HERE/'review.json').read_bytes()==review_bytes
ROOT=HERE.parents[2]
base=[str(ROOT/'.venv/bin/python'),str(HERE.with_suffix('.py')),'--difficulty','all','--count','2','--seed','19']
js=subprocess.check_output(base+['--format','json']);expected=json.loads((HERE/'boundary-validation.json').read_text())['cli_sha256'];assert hashlib.sha256(js).hexdigest()==expected
markdown=subprocess.check_output(base+['--format','markdown']);assert markdown==subprocess.check_output(base+['--format','markdown'])
text=markdown.decode();assert text.count('**(correct)**')==6 and text.count('**Correct answer:**')==6
for label in ['Easy (E)','Moderate (M)','Hard (H)']:assert text.count(label)==2
raw=subprocess.check_output([str(ROOT/'.venv/bin/python'),str(HERE.with_suffix('.py')),'--difficulty','moderate','--profile','q-141096','--format','markdown']).decode();assert 'Moderate (M)' in raw and 'Observed original; evidence only' in raw and '**Correct answer:** I only' in raw
report={'pass':True,'review_records_unchanged':len(review),'raw_source_prompt_solution_pairs_exact':source_matches,'all_review_difficulty_origin_correct_labels_checked':len(review),'authored_levels':sorted(levels),'cli_json_sha256_unchanged':expected,'cli_markdown_records_checked':6,'cli_markdown_sha256':hashlib.sha256(markdown).hexdigest(),'raw_source_cli_checked':True,'math_stage_bank_grading_changes':0}
(HERE/'presentation-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
