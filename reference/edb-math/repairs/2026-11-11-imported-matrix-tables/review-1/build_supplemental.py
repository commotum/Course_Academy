#!/usr/bin/env python3
"""Repair the complete excluded Newton iterate cohort; never write EDB."""
import collections
import gzip
import html
import json
import re
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
ROOT=next(p for p in HERE.parents if (p/'scripts/question_capture/math_format.py').exists())
sys.path.insert(0,str(ROOT))
from scripts.question_capture.math_format import matrix_equation,validate_prose,MATH
from scripts.audit_imported_matrix_tables import table_blocks
AUDIT=ROOT/'reference/edb-math/audits/2026-11-11-imported-matrix-tables'
ledger=[json.loads(l) for l in (AUDIT/'all-imported-tables.jsonl').open()]
existing={(p['entity'],p['attribute']):p for p in json.loads((BASE/'proposals.json').read_text())}
blocks=[c for c in ledger if any('Newton' in t for t in c['titles']) and c['priority']!='canonical'
        and c['table'] in existing.get((c['entity'],c['attribute']),{'after':c['table']})['after']]
assert len(blocks)==34
ids={c['entity'] for c in blocks}
original={}
with gzip.open(AUDIT/'snapshot.jsonl.gz','rt') as stream:
    for line in stream:
        row=json.loads(line)
        if row['e'] in ids and row['a'] in ['question/problem','question/worked-solution'] and row.get('raw_string') is not None:
            original[(row['e'],row['a'])]=row['raw_string']
questions={q[':db/id']:q for q in json.loads((BASE/'capture/questions.json').read_text())}
for capture_path in [BASE/'supplemental-capture/questions.json',BASE/'newton-capture/questions.json',BASE/'supplemental-newton/questions.json']:
    if capture_path.exists():questions.update({q[':db/id']:q for q in json.loads(capture_path.read_text())})
markers=re.compile(r'\{\{[^{}]+\}\}')
proposals=[];reviews=[];missing=[]
for c in blocks:
    entity=c['entity'];attr=c['attribute'];before=original[(entity,attr)];start,end=c['span']
    assert before[start:end]==c['table']
    if entity in questions:
        assert questions[entity][':'+attr]==before,(entity,'fresh capture differs')
    rows=[[html.unescape(v[1:-1]) if v.startswith('$') and v.endswith('$') else v for v in row if v] for row in c['rows']]
    assert len(rows)==2 and len(rows[0])==3 and len(rows[1])==1
    label,first,right=rows[0];second=rows[1][0]
    assert label.endswith('[') and right==']'
    assert '=' in label or '≈' in label
    cells=[[first],[second]]
    after_table=matrix_equation([label[:-1],cells])
    after=before[:start]+after_table+before[end:]
    validate_prose(after)
    assert collections.Counter(markers.findall(before))==collections.Counter(markers.findall(after))
    assert not any(markers.search(m[0]) for m in MATH.finditer(after_table))
    combined=existing.get((entity,attr),{'after':before})['after'].replace(c['table'],after_table)
    assert not [b for b in table_blocks(combined) if not b['canonical']],entity
    reason='Additional layout missed by census exclusions: the Newton iterate label contains = or ≈ followed by [, and ] spans both rows; the first component is in the middle first-row cell and the second component is the sole nonempty lower-row cell. These are a 2×1 iterate vector, not table headings. Preserve supplied values and field identities.'
    evidence={'source_census_classification':c['priority'],'source_rows':c['rows'],'source_titles':c['titles'],
              'source_imported_ids':c['imported_ids'],'source_topic_ids':c['topics'],
              'matrix_rows':cells,'equation_label':label[:-1],
              'source_family_html':'/home/jake/Developer/MA/DATA/Lessons/'+('5377' if c['topics']==[17592186048637] else '5379')+'/Source/'+('5377' if c['topics']==[17592186048637] else '5379')+'.html',
              'fresh_capture_compared':entity in questions,'original_basis':14355}
    patch={'start':start,'end':end,'before':c['table'],'after':after_table,'candidate_indices':[],
           'additional_layout':True,'reason':reason,'evidence':evidence}
    proposals.append({'entity':entity,'attribute':attr,'before':before,'after':after,'candidate_indices':[],
                      'additional_layout':True,'rationale':reason,'evidence':evidence,'replacements':[patch]})
    reviews.append({'entity':entity,'attribute':attr,'status':'confirmed','reasoning':reason,'evidence':evidence})
    if entity in questions:
        q=questions[entity];fieldkeys={f[':answer-field/key']:f for f in q.get(':question/answer-fields',[])}
        placeholderkeys={s[2:-2] for s in markers.findall(after)}
        orphans=sorted(placeholderkeys-set(fieldkeys))
        incomplete=[{'entity':f[':db/id'],'key':k,'type':f.get(':answer-field/type'),
                     'choices':f.get(':answer-field/choices',[]),'correct':f.get(':answer-field/correct')}
                    for k,f in fieldkeys.items() if not f.get(':answer-field/correct')]
        if orphans or incomplete or not q.get(':question/worked-solution'):
            missing.append({'entity':entity,'orphan_placeholder_keys':orphans,'incomplete_fields':incomplete,
                            'worked_solution_missing':not bool(q.get(':question/worked-solution'))})
    else:missing.append({'entity':entity,'fresh_capture_missing':True})

# Record explicit same-family exclusions separately for root assignment.
owned=json.loads((HERE/'assigned.json').read_text());owned_topics={t for c in owned for t in c['topics']}
other=[c for c in ledger if set(c['topics'])&owned_topics and c['priority']=='other_math_layout'
       and not any('Newton' in t for t in c['titles'])]
(HERE/'additional-source-family-question-ids.json').write_text(json.dumps(sorted({c['entity'] for c in other}),indent=2)+'\n')
(HERE/'additional-source-family-blocks.json').write_text(json.dumps(other,ensure_ascii=False,indent=2)+'\n')
for name,value in [('supplemental-proposals.json',proposals),('supplemental-reviews.json',reviews),('supplemental-missing-state.json',missing)]:
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'newton_supplemental_fields':len(proposals),'fresh_capture_compared':sum(p['evidence']['fresh_capture_compared'] for p in proposals),
                  'source_family_exclusions_other_than_newton':len(other),'missing_state_count':len(missing)},indent=2))
