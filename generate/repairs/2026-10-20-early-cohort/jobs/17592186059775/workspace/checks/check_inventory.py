"""Read-only reproduction of stored legacy generated questions and their weaknesses."""
import sys
sys.dont_write_bytecode=True
import importlib.util
import json
import re
from pathlib import Path
W=Path(__file__).resolve().parents[1];sys.path.insert(0,str(W))
JOB=Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186059775')
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
v=load('readback',W/'17592186059775/validate.py');old=load('legacy',W/'evidence/legacy/17592186059775.py')
inventory=json.loads((JOB/'source/inventory.json').read_text())
archived=json.loads((W/'17592186059775/reference/replenishment/basis-2480/generated.json').read_text())
records=[];affected=[];observations=[];latest_cue=[]
for stored in inventory['questions']:
 if ':question/math-academy-id' in stored:
  # Original captures remain original; never fabricate generation metadata.
  observations.append({'question_id':stored[':question/id'],'source_id':stored[':question/math-academy-id'],'tested_as_generated':False})
  continue
 matches=[r for r in archived if r['question'][':question/id']==stored[':question/id']]
 assert len(matches)==1,'Stored generated record has no archived metadata'
 saved=matches[0];meta=saved['generation'];sid,k=meta['parameters']
 r=old.generate(stored[':question/difficulty'][':db/ident'].split('/')[-1],meta['seed'],sid,meta['parameters'])
 assert r==saved,'Exact legacy reproducibility failed'
 q=r['question'];assert q[':question/id']==stored[':question/id']
 for name in (':question/problem',':question/worked-solution'):assert q[name]==stored[name]
 f=q[':question/answer-fields'][0];sf=stored[':question/answer-fields'][0]
 assert f[':answer-field/id']==sf[':answer-field/id']
 # The stored migration promoted inline matrix text to display math; reproduce
 # that wrapper change explicitly, retaining answer IDs and generation metadata.
 for a in f[':answer-field/choices']:
  b=next(b for b in sf[':answer-field/choices'] if b[':answer/id']==a[':answer/id'])
  assert v.object_value(a[':answer/value'])==v.object_value(b[':answer/value'])
  value=re.sub(r'^\$(M.*?),\$\n',lambda m:'$$\n'+m[1]+',\n$$\n',a[':answer/value'],flags=re.S)
  assert value==b[':answer/value'], 'Unexpected stored normalization difference'
  a[':answer/value']=value
 assert f[':answer-field/correct'][1]==sf[':answer-field/correct'][':answer/id']
 bank=f[':answer-field/choices'];idx=next(i for i,a in enumerate(bank) if a[':answer/id']==f[':answer-field/correct'][1])
 if 'and then solve' in q[':question/problem']:
  consistent=[i for i,a in enumerate(bank) if (lambda m:m[:,:2]*v.sp.Matrix(v.pair(a[':answer/value']))==m[:,2])(v.printed_matrices(a[':answer/value'])[0])]
  assert consistent==[idx]
  finding='Only keyed matrix/solution pair is internally consistent; supplied augmented matrix can be ignored.'
 else:
  ranks=[]
  for p in old.domain(sid):
   rr=old.generate(old.level(sid),meta['seed'],sid,p);ff=rr['question'][':question/answer-fields'][0]
   chosen=next(a for a in ff[':answer-field/choices'] if a[':answer/id']==ff[':answer-field/correct'][1])
   ys=sorted(v.printed_matrices(a[':answer/value'])[0][1,2] for a in ff[':answer-field/choices'])
   ranks.append(ys.index(v.printed_matrices(chosen[':answer/value'])[0][1,2]))
  assert set(ranks)=={2}
  finding='Key is always the median second-row constant in this recognizable source profile, at every supported RHS scale.'
 records.append(r)
 ordered=sorted(bank,key=lambda a:v.printed_matrices(a[':answer/value'])[0][1,2])
 pivot=v.printed_matrices(q[':question/problem'])[0][0,0]
 guessed=ordered[3 if pivot==1 else 0]
 latest_cue.append({'question_id':q[':question/id'],'parameters':meta['parameters'],
                    'pivot_rank_strategy_hit':guessed[':answer/id']==f[':answer-field/correct'][1]})
 affected.append({'question_id':stored[':question/id'],'entity_id':stored[':db/id'],'finding':finding,'reproduction':f'python checks/check_inventory.py # legacy.generate({old.level(sid)!r}, {meta["seed"]}, {sid!r}, {meta["parameters"]!r})','evidence_path':'../workspace/evidence/inventory-generated-records.json'})
(W/'evidence/inventory-generated-records.json').write_text(json.dumps(records,indent=2)+'\n')
report={'affected_questions':affected,'inventory_basis':inventory['basis'],'generated_records_tested':len(records),'original_source_records':observations,'latest_batch_finding':{'id':'9e827407d5429a1f8827','stored_generated_records':latest_cue,'hits':sum(x['pivot_rank_strategy_hit'] for x in latest_cue),'tested':len(latest_cue),'scope':'Exact pivot/rank cue tested on every stored generated record. The five-item q-73439 scaled-role batch is not stored here; older demonstrated shortcuts remain affected below. Source captures were inspected as sources, not fabricated as generated records.'},'scope':'All three stored generated instances reproduced with exact archived generation metadata; source captures kept separate, not marked generated. CLI failure is a package defect and has no stored-record manifestation.'}
(W/'affected-inventory.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'generated_tested':len(records),'demonstrated_affected':len(affected),'original_sources_separate':len(observations)}))
