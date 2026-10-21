"""Replay captured legacy generated inventory without database access."""
import importlib.util,json
from pathlib import Path
import audit as a
W=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('legacy',W/'checks/legacy_generator.py');legacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(legacy)
inventory=json.loads((a.JOB/'source/inventory.json').read_text());source=json.loads((a.JOB/'source/source.json').read_text())
originals={q[':question/id'] for q in source['material']['kp'][':knowledge-point/questions']}
records=[];affected=[]
for q in inventory['questions']:
 if q[':question/id'] in originals:continue
 level=q[':question/difficulty'][':db/ident'].split('/')[-1]
 rhs=a.parse(q[':question/problem'].split('=')[1].split('$')[0].rstrip('., '));num,den=a.s.fraction(rhs)
 p={'a':int(num.expand().coeff(a.x,2)),'b':int(num.subs(a.x,0))}
 if level=='hard':p['d']=int(den.subs(a.y,0))
 r=legacy.generate(level,seed=0,parameters=p)
 for k in (':question/id',':question/problem',':question/worked-solution'):assert r['question'][k]==q[k]
 sf=q[':question/answer-fields'][0]
 assert sorted(z[':answer/value'] for z in a.field(r)[':answer-field/choices'])==sorted(z[':answer/value'] for z in sf[':answer-field/choices'])
 assert a.answer_id(a.field(r))==sf[':answer-field/correct'][':answer/id']
 assert a.shortcut(r)==[a.answer_id(a.field(r))]
 records.append(r)
 affected.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'finding':'6343bb7c5cb9de00ecc6: R, -R, 2R bank uniquely exposes the correct equation.','reproduction':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python checks/inventory.py; legacy.generate('+repr(level)+', seed=0, parameters='+repr(p)+')','evidence_path':'../workspace/evidence/generated-records.json'})
for name,obj in [('generated-records.json',records),('affected-inventory.json',{'affected_questions':affected}),('inventory-results.json',{'basis':inventory['basis'],'captured_questions':len(inventory['questions']),'source_excluded':len(originals),'generated_tested':len(records),'affected':len(affected),'replay':'Legacy implementation snapshot reproduces stored IDs, prompts, solutions, full banks and key. Stored capture omits generation metadata; retained replay metadata names its parameters and seed.','scope':'All captured non-source questions tested; no database modifications. evidence_path is relative to the supplied author-1 evidence_root, referring into this workspace as required by workspace-only writes.'})]:
 (W/'evidence'/name).write_text(json.dumps(obj,indent=2)+'\n')
print(json.dumps({'captured':len(inventory['questions']),'originals_excluded':len(originals),'legacy_generated_replayed_and_affected':len(affected)}))
