import copy,importlib.util,json,re,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(H/'generator'));from generator import SPECS,generate,replay_source,mul
from product_highlights import product_solution
sys.path.insert(0,str(R))
from scripts.generator_packages import build_manifest,manifest_digest
# Original raw replays retain the exact old evidence API values.
oldpath=Path('/media/jake/SSD/EDB/math/generators/c6/c62b54d8ef950438382d6e06550ade42523c5f1bc54c398a1b10b760c2b35b64/generator.py')
records=[];checks=[]
for sid,spec in SPECS.items():
 for seed in range(12):records.append(generate('easy',9047000+seed,template=sid))
 # Keep evidence-only observed banks out of the serving sample grading claim.
 raw=replay_source(sid);assert raw['generation']['evidence_only'] and not raw['generation']['eligible_for_learning']
 old=subprocess.run([sys.executable,'-c',"import json,sys;sys.path.insert(0,sys.argv[1]);import generator;print(json.dumps(generator.replay_source(sys.argv[2])))",str(oldpath.parent),sid],capture_output=True,text=True,check=True)
 oldq=json.loads(old.stdout)['question'];rawq=raw['question'];assert oldq[':question/problem']==rawq[':question/problem'] and oldq.get(':question/worked-solution')==rawq.get(':question/worked-solution')
for r in records:
 q=r['question'];a,b,t=[r['generation']['parameters'][key]for key in ['A','B','targets']];product=mul(a,b);sol=q[':question/worked-solution'];assert sol.count('For entry $c_')==len(t)
 assert sol.count('color{#4169E1}')>=len(t) and sol.count('color{red}')>=len(t)
 bank={v[':answer/id']:v for f in q[':question/answer-fields']for v in f[':answer-field/choices']};tests=[]
 for i,f in enumerate(q[':question/answer-fields']):
  correct=bank[f[':answer-field/correct'][1]]
  if f[':answer-field/type']==':answer-field.type/blank':
   pos=t[int(f[':answer-field/key'].split('-')[-1])-1];assert int(correct[':answer/value'])==product[pos[0]][pos[1]]
   tests.extend([{'field_index':i,'submitted':correct[':answer/value'],'expected':'accepted'},{'field_index':i,'submitted':'987654321','expected':'rejected'}])
  else:
   from product_highlights import matrix
   assert correct[':answer/value']==matrix(product)
   tests.extend({'field_index':i,'submitted_answer_id':v[':answer/id'],'expected':'accepted'if v==correct else'rejected'}for v in f[':answer-field/choices'])
  tests=[{**test,'purpose':'Presentation-only replacement retains independently calculated product grading'}for test in tests]
 checks.append({'label':q[':question/id'],'record':r,'checks':tests})
(H/'generator-samples.json').write_text(json.dumps(records,indent=2)+'\n');(H/'generator-grading-input.json').write_text(json.dumps(checks,indent=2)+'\n');subprocess.run([str(R/'.local/edb/html-table-repair/check-engine'),str(H/'generator-grading-input.json'),str(H/'generator-grading.json')],check=True)
candidates=json.loads((H/'generator-candidates.json').read_text())
for c in candidates:c['approved_digest']=manifest_digest(build_manifest(Path(c['directory']),c['entrypoint'],c['files'],dependencies=c['dependencies']))
(H/'generator-candidates.json').write_text(json.dumps(candidates,indent=2)+'\n');(H/'generator-validation.json').write_text(json.dumps({'passed':True,'samples':len(records),'templates':len(SPECS),'raw_replays_preserved':len(SPECS)},indent=2)+'\n');print('Checked',len(records),'fresh records across',len(SPECS),'families; raw replay content preserved.')
