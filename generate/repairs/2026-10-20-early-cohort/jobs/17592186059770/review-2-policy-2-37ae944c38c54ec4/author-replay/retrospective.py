#!/usr/bin/env python3
"""Reproduce archived generated instances and demonstrate the old bank-only cue."""
import json,shutil,subprocess,os
from pathlib import Path
import validate as v
legacy=v.E/'legacy';legacy.mkdir(exist_ok=True)
shutil.copy2(v.REPO/'generate/scratch/17592186059770.py',legacy/'17592186059770.py')
(legacy/'17592186059770').mkdir(exist_ok=True)
shutil.copy2(v.W/'17592186059770/source.json',legacy/'17592186059770/source.json')
archived=json.loads((v.W/'17592186059770/reference/replenishment/basis-2349/generated.json').read_text())
inventory=json.loads((v.W/'../source/inventory.json').read_text());byid={q[':question/id']:q for q in inventory['questions']}
reproduced=[];affected=[];commands=[]
for old in archived:
 meta=old['generation'];cmd=[v.PY,str(legacy/'17592186059770.py'),'--difficulty','moderate','--count','1','--seed',str(meta['seed']),'--format','json','--template',meta['template'],'--profile',meta['bank_profile']]
 run=subprocess.run(cmd,capture_output=True,text=True);assert run.returncode==0,run.stderr
 r=json.loads(run.stdout)[0];assert r==old,'Exact archived record / generation metadata mismatch'
 q=r['question'];stored=byid[q[':question/id']]
 assert q[':question/problem']==stored[':question/problem'] and q[':question/worked-solution']==stored[':question/worked-solution']
 f=q[':question/answer-fields'][0];sf=stored[':question/answer-fields'][0]
 assert {a[':answer/id']:a[':answer/value'] for a in f[':answer-field/choices']}=={a[':answer/id']:a[':answer/value'] for a in sf[':answer-field/choices']}
 if meta['template']=='coefficient':
  picks=[a for a in f[':answer-field/choices'] if len(v.matrix(a[':answer/value'])[0])==3 and v.matrix(a[':answer/value'])[0][2]<0]
  finding='Legacy q-1070 bank identifies the correct 2x3 candidate by its negative top-right entry without reading the system.'
 else:
  picks=[a for a in f[':answer-field/choices'] if len(v.matrix(a[':answer/value'])[0])==4 and v.matrix(a[':answer/value'])[0][3]==0 and v.matrix(a[':answer/value'])[0][1]<-1 and v.matrix(a[':answer/value'])[1][3]<0]
  finding='Legacy q-1073 bank identifies the correct 2x4 candidate by zero top RHS, top-middle entry below -1 and negative bottom RHS without reading the system.'
 assert len(picks)==1 and picks[0][':answer/id']==f[':answer-field/correct'][1]
 assert v.matrix(picks[0][':answer/value'])==v.witness(r)
 commands.append(cmd);reproduced.append(r)
 index=len(reproduced)-1
 affected.append({'question_id':q[':question/id'],'entity_id':stored[':db/id'],'finding':finding,'reproduction':f"{v.PY} checks/retrospective.py (record index {index}; exact CLI command in evidence/retrospective-commands.json)",'evidence_path':'generated-records.json'})
v.save('generated-records.json',reproduced);v.save('retrospective-commands.json',commands)
(v.E/'affected-inventory.json').write_text(json.dumps({'affected_questions':affected},indent=2)+'\n')
v.save('inventory-audit.json',{'captured_basis':inventory['basis'],'inventory_questions':len(byid),'archived_generated_records_reproduced':len(reproduced),'affected_generated_questions':len(affected),'source_questions_marked_generated':0,'limits':'Five archived generated records exactly replayed and matched to inventory IDs, prompts, solutions and owned choices. Other source questions inspected for source analysis, not certified free of every possible shortcut. CLI band mismatch is a package failure, not a stored content defect. No database access.'})
print('Retrospective:',len(reproduced),'complete generated records exactly reproduced;',len(affected),'stored questions affected by demonstrated bank-only cues')
