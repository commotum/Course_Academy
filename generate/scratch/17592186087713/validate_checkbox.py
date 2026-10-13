"""Validate the current checkbox generator and exact scoped current source replay."""
import copy, hashlib, importlib.util, json, pathlib, subprocess, uuid
HERE=pathlib.Path(__file__).resolve().parent; ROOT=HERE.parents[2]
def module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
g=module('current_matrix_generator',HERE.with_suffix('.py'));v=module('legacy_validator',HERE/'validate.py')
def save(name,x): (HERE/'reference'/name).write_text(json.dumps(x,indent=2,default=str)+'\n')
def validate(rec):
 q=rec['question'];meta=rec['generation'];p=meta['parameters']
 radio=g.generate_radio(meta['level'],seed=meta['seed'],template=meta['template'],parameters=p,profile=meta['legacy_radio_profile']);v.validate_record(radio)
 target,arrays=v.parse_prompt(q[':question/problem']);assert len(q[':question/answer-fields'])==3
 assert q[':question/worked-solution']==radio['question'][':question/worked-solution']
 assert q[':question/problem']==radio['question'][':question/problem'].replace('\n\n','\n\nSelect all that apply.\n\n',1)
 assert meta['mathematical_task_fingerprint']==radio['generation']['mathematical_task_fingerprint']
 identity=g.digest({'version':g.CHECKBOX_VERSION,'prompt':q[':question/problem'],'solution':q[':question/worked-solution'],'type':'checkbox','keys':p['labels']})
 assert q[':question/id']==g.uid(identity) and meta['content_hash']==identity
 bykey={f[':answer-field/key']:f for f in q[':question/answer-fields']};assert set(bykey)=={a[0] for a in arrays}
 checks=[]
 for i,(label,d,_) in enumerate(arrays):
  f=bykey[label];assert f[':answer-field/type']==':answer-field.type/checkbox';assert f[':answer-field/id']==g.uid(identity+':'+label)
  choices=f[':answer-field/choices'];assert len(choices)==2 and {a[':answer/value'] for a in choices}=={'false','true'}
  correct=str(d==target).lower()
  for a in choices:
   assert a[':answer/type']==':answer.type/text';assert a[':answer/id']==g.uid(f[':answer-field/id']+':'+a[':answer/value'])
   assert (f[':answer-field/correct'][1]==a[':answer/id'])==(a[':answer/value']==correct)
   checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==correct else 'rejected'})
 return checks

def main():
 cases=json.loads((HERE/'source-cases.json').read_text());current=json.loads((HERE/'reference/current-kp.json').read_text())[0][0]
 source={q[':question/math-academy-id']:q for q in current[':knowledge-point/questions']}
 items=[];fidelity=[]
 for case in cases:
  rec=g.generate(case['level'],parameters=case['parameters'],template=case['template'],profile=case['bank_profile']);checks=validate(rec);old=source[case['source_id']];q=rec['question']
  expected_prompt=q[':question/problem'].replace('\\cdot','\\times') if case['source_id'] in ('q-69514','q-69515') else q[':question/problem']
  assert expected_prompt==old[':question/problem'],case['source_id']+' prompt'
  if case['source_id'] not in ('q-69514','q-69515'): assert q[':question/worked-solution']==old[':question/worked-solution'],case['source_id']+' solution'
  else:
   target,arrays=v.parse_prompt(old[':question/problem']);assert old[':question/worked-solution'].endswith('Only '+next(a[0] for a in arrays if a[1]==target)+' has the requested dimensions.')
  for f in q[':question/answer-fields']:
   of=next(fld for fld in old[':question/answer-fields'] if fld[':answer-field/key']==f[':answer-field/key'])
   assert {a[':answer/value'] for a in of[':answer-field/choices']}=={'false','true'}
   cv=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
   assert cv==of[':answer-field/correct'][':answer/value']
  fidelity.append(case['source_id']);items.append({'label':case['source_id']+' current checkbox replay','record':rec,'checks':checks})
 for level in ('easy','moderate','hard'):
  for seed in range(120):
   rec=g.generate(level,seed);checks=validate(rec)
   again=g.generate(level,seed+900,parameters=rec['generation']['parameters'],template=rec['generation']['template'],profile=rec['generation']['legacy_radio_profile']);assert again['question']==rec['question']
   items.append({'label':level+' checkbox '+str(seed),'record':rec,'checks':checks})
 save('checkbox-native-input.json',items)
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'reference/checkbox-native-input.json'),str(HERE/'reference/checkbox-native-report.json')],check=True)
 nr=json.loads((HERE/'reference/checkbox-native-report.json').read_text());assert nr['accepted_checks']==3*len(items) and nr['rejected_checks']==3*len(items) and nr['documented_unresolved_checks']==0
 report={'passed':True,'current_source_prompts_and_complete_banks_matched':fidelity,'records':len(items),'native_accepted':nr['accepted_checks'],'native_rejected':nr['rejected_checks'],'generator_id':g.GENERATOR_ID,'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'finite_catalog':{'easy':12,'moderate':1920,'hard':25},'difficulty_origins':{'easy':'authored','moderate':'observed and authored peers','hard':'authored close-count comparison'},'plots':'none','current_source_corrections':'Two formerly unrated records now use times notation and independently authored short solutions; all eight displayed arrays and full Boolean banks replay exactly. Six observed full solutions remain exact. Historical radio fidelity is retained separately.'}
 save('checkbox-validation.json',report);print(json.dumps(report))
if __name__=='__main__':main()
