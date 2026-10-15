"""Independent rendered operands, keys, row stages, banks and native grading."""
import importlib.util,json,re,subprocess,hashlib
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('matrix_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def scan(text):
 """Read displayed matrices without relying on generator parameter metadata."""
 return [[row.split('&') for row in body.split('\\\\')] for body in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)]
def val(x):
 x=x.strip().replace(r'\cdot','*').replace('−','-')
 assert re.fullmatch(r'[\d +*()\-]+',x),x
 return int(s.sympify(x))
def check(r):
 q=r['question'];assert q[':question/difficulty']==':question.difficulty/easy'
 parsed=scan(q[':question/problem']);A=[[val(z) for z in row] for row in parsed[0]];v=[val(row[0]) for row in parsed[1]]
 assert len(A)==2 and all(len(row)==2 for row in A) and len(v)==2
 answer=[sum(x*y for x,y in zip(row,v)) for row in A]
 p=r['generation']['parameters'];g.guard(p)
 assert A==[[p['a'],p['b']],[p['c'],p['d']]] and v==[p['u'],p['v']]
 assert r['generation']['eligible_for_learning'] and r['knowledge_point']['db_id']==g.KP
 if r['generation']['template'].startswith('named'):
  names=re.search(r'Find \$([A-Z])([a-z])\$',q[':question/problem'])
  assert names and names[1]==p['matrix_name'] and names[2]==p['vector_name']
  assert '$'+p['matrix_name']+p['vector_name']+'=' in q[':question/worked-solution']
 fields=q[':question/answer-fields'];blank=r['generation']['template'].endswith('blank')
 assert len(fields)==(2 if blank else 1)
 for f in fields:
  answers={a[':answer/id']:a for a in f[':answer-field/choices']};correct=answers[f[':answer-field/correct'][1]][':answer/value']
  assert len(answers)==len(f[':answer-field/choices'])
  if blank:
   i=int(f[':answer-field/key'][-1])-1;assert val(correct)==answer[i]
   assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
  else:
   vectors=[tuple(val(row[0]) for row in scan(a[':answer/value'])[0]) for a in answers.values()]
   assert len(vectors)==len(set(vectors))==5
   assert tuple(val(row[0]) for row in scan(correct)[0])==tuple(answer)
   expected={z for _,z in g.bank(r['generation']['bank_profile'],p)};assert set(vectors)==expected
 solution=scan(q[':question/worked-solution']);assert len(solution)==(9 if r['generation']['template'].startswith('named') else 11)
 # Each row stage repeats the same operands, then shows its unevaluated dot sum,
 # then the accumulated result. Verify all rendered operations and output cells.
 assert solution[0]==parsed[0] and solution[1]==parsed[1] and solution[4]==parsed[0] and solution[5]==parsed[1]
 assert val(solution[2][0][0])==answer[0] and solution[2][1][0].strip()=='∗'
 assert val(solution[3][0][0])==answer[0] and solution[3][1][0].strip()=='∗'
 assert [val(row[0]) for row in solution[6]]==answer
 assert [val(row[0]) for row in solution[7]]==answer
 assert [val(row[0]) for row in solution[-1]]==answer
 if len(solution)==11:assert solution[8]==parsed[0] and solution[9]==parsed[1]
 # Inline conclusion repeats A,v before its final vector; named conclusion has one.
 return g.fingerprint(p)
def native(r,label=None):
 checks=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  if f[':answer-field/type'].endswith('/radio'):
   for a in f[':answer-field/choices']:checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'field-owned radio selection'})
  else:
   a=f[':answer-field/choices'][0][':answer/value'];n=int(a)
   for text,expected in [(a,'accepted'),(str(n*2)+'/2','accepted'),('('+a+')+0','accepted'),(str(n+1),'rejected')]:checks.append({'field_index':i,'submitted':text,'expected':expected,'purpose':'integer component equivalent and incorrect entry'})
 return {'label':label or r['question'][':question/id'],'record':r,'checks':checks}
def save(path,x):path.write_text(json.dumps(x,indent=2,default=str)+'\n')
def main():
 replay=[];cases=[];coverage={};slots={k:set() for k in ('a','b','c','d','u','v','matrix_name','vector_name')}
 for mid,q in g.SOURCES.items():
  p=g.parameters(q);t=g.template_of(mid);bank=g.bank(mid,p);rows=[]
  for f in q[':question/answer-fields']:
   values=[]
   for a in f[':answer-field/choices']:
    raw=a[':answer/value'];normalized=raw.replace('\\\\begin','\\begin').replace('\\\\end','\\end')
    value=tuple(val(row[0]) for row in scan(normalized)[0]) if '/radio' in f[':answer-field/type'][':db/ident'] else (val(raw),)
    values.append(value)
   expected=[v for _,v in bank] if bank else [(g.dot(p)[int(f[':answer-field/key'][-1])-1],)]
   assert sorted(values)==sorted(expected),(mid,values,expected)
   corr=f.get(':answer-field/correct');correct=None
   if corr:
    raw=corr[':answer/value'].replace('\\\\begin','\\begin').replace('\\\\end','\\end');correct=tuple(val(row[0]) for row in scan(raw)[0]) if bank else (val(raw),)
    assert correct==(g.dot(p) if bank else expected[0])
   rows.append({'field_id':f[':db/id'],'matched':len(values),'total':len(values),'missing':[],'extra':[],'correct_present':bool(corr),'correct_verified':bool(corr)})
  replay.append({'source':mid,'template':t,'profile':mid,'fields':rows,'learning_sampling_supported':mid not in ('q-126512','q-13566'),'notation_correction':'double-escaped begin/end normalized for generated radio values' if bank else None})
  if mid not in ('q-126512','q-13566'):
   r=g.generate('easy',7,t,p,mid);check(r);cases.append(native(r,'source-'+mid))
 for t,profiles in g.ELIGIBLE.items():
  for profile in profiles:
   for seed in range(120):
    r=g.generate('easy',seed,t,profile=profile);check(r)
    assert r==g.generate('easy',seed,t,profile=profile)
    for k,z in r['generation']['parameters'].items():slots[k].add(z)
    coverage[profile]=coverage.get(profile,0)+1
    if seed<3:cases.append(native(r,profile+'-'+str(seed)))
 # Hold mathematical data fixed while varying both rendered names.
 p=g.parameters(g.SOURCES['q-275589']);original=g.generate('easy',0,'named-blank',p,'q-275589')
 changed=g.generate('easy',0,'named-blank',{**p,'matrix_name':'Z','vector_name':'n'},'q-275589');check(original);check(changed)
 assert g.fingerprint(p)==g.fingerprint(changed['generation']['parameters'])
 assert original['question'][':question/problem']!=changed['question'][':question/problem']
 import copy
 stale=copy.deepcopy(changed);stale['question'][':question/worked-solution']=original['question'][':question/worked-solution']
 try:check(stale)
 except AssertionError:pass
 else:raise AssertionError('Stale label reference accepted')
 for level in ('moderate','hard'):
  try:g.generate(level)
  except ValueError:pass
  else:raise AssertionError('Unsupported level accepted')
 save(HERE/'source-bank-replay.json',replay)
 save(HERE/'slot-coverage.json',{'profiles':coverage,'slots':{k:sorted(v) for k,v in slots.items()},'target_roles':'entire product and both rows remain fixed; no selected-cell slot','signed_and_zero_matrix_entries':True,'nonzero_signed_vector_entries':True})
 save(HERE/'native-input.json',cases)
 subprocess.run([str(HERE.parents[2]/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
 save(HERE/'validation.json',{'passed':True,'sampled_instances':sum(coverage.values()),'source_banks':len(replay),'source_fields':sum(len(z['fields']) for z in replay),'matched_source_choices':sum(f['matched'] for z in replay for f in z['fields']),'all_source_choices_replayed':True,'supported_profiles':list(coverage),'excluded_profiles':['q-126512','q-13566'],'grader':'course_academy_engine::learning::grade_field','supported_levels':['easy'],'unsupported_levels':['moderate','hard'],'deterministic_replay':True,'independently_checked_rendered_dot_products':True})
 print('Validated',sum(coverage.values()),'instances')
if __name__=='__main__':main()
