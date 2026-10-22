"""Replay source banks and identify stored originals with demonstrated answer-length cues."""
import copy
import importlib.util
import json
from pathlib import Path
import re
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location('current_generator',ROOT/'17592186087886.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def size(value):return len(re.sub(r'\\(?:left|right|operatorname)|[{}\s]|\u2061','',value))
def main():
    inv=json.loads((ROOT.parent/'source/inventory.json').read_text());affected=[];records=[];tested=[]
    for q in inv['questions']:
        t=q.get(':question/math-academy-id');assert t in g.ORIGINAL
        r=g.generate('easy',0,t,{'k':g.ORIGINAL[t]});f=q[':question/answer-fields'][0];choices=f[':answer-field/choices']
        assert sorted(a[':answer/value'] for a in choices)==sorted(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])
        assert q[':question/problem']==r['question'][':question/problem'] and q[':question/worked-solution']==r['question'][':question/worked-solution']
        j=next(i for i,a in enumerate(choices) if a[':answer/id']==f[':answer-field/correct'][':answer/id']);sizes=[size(a[':answer/value']) for a in choices]
        witness='longest' if t in ('q-14314','q-14316','q-14323') and sizes[j]==max(sizes) and sizes.count(max(sizes))==1 else 'shortest' if t=='q-90600' and sizes[j]==min(sizes) and sizes.count(min(sizes))==1 else None
        tested.append({'question_id':q[':question/id'],'source_id':t,'applicable_family_cue':witness})
        if witness:
            record={'question':copy.deepcopy(q),'knowledge_point':copy.deepcopy(r['knowledge_point']),'generation':{'audit_kind':'original-source-replay','newly_generated':False,'source_question_id':q[':question/id'],'source_db_id':q[':db/id'],'template':t,'parameters':{'k':g.ORIGINAL[t]},'replay_seed':0,'parameter_fingerprint':r['generation']['parameter_fingerprint']}}
            records.append(record)
            affected.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'finding':f'{t}: unique {witness} answer selects the key without using the prompt, agreeing with the demonstrated family-level cue. This is an original source record, not a generated question.', 'reproduction':f'/home/jake/Developer/Course_Academy/.venv/bin/python checks/check_inventory_shortcuts.py (template={t}, k={g.ORIGINAL[t]}, replay_seed=0)', 'evidence_path':'../workspace/evidence/affected-inventory-records.json'})
    (ROOT/'affected-inventory.json').write_text(json.dumps({'affected_questions':affected},indent=2)+'\n')
    (ROOT/'evidence/affected-inventory-records.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
    (ROOT/'evidence/inventory-shortcut-audit.json').write_text(json.dumps({'basis':inv['basis'],'tested_count':len(tested),'affected_count':len(affected),'tested':tested,'note':'All eight captured inventory questions are original source items. None was reclassified as generated. Complete audit replay records retain stored question/field/answer identities and use explicit original-source-replay metadata. No historical generated records are present in this captured inventory. evidence_path values are relative to the supplied evidence_root (author-2).'},indent=2)+'\n')
    print(json.dumps({'tested':len(tested),'affected_original_source_records':len(affected)}))
if __name__=='__main__':main()
