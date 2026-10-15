"""Independent rendered mathematics and real learner-grader validation."""
import copy, hashlib, importlib.util, json, re, subprocess
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('matrix3_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(path,x):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(x,indent=2,default=str)+'\n')
def scan(text):
 return [[row.split('&') for row in body.split('\\\\')] for body in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)]
def clean(text):
 return text.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace(r'\,','').replace(r'\cdot','*').replace('−','-').strip()
def val(text):
 text=clean(text);assert re.fullmatch(r'[\d +*()\-\s]+',text),repr(text)
 return int(s.sympify(text))
def normalize(q):
 out={k:copy.deepcopy(q[k]) for k in (':question/id',':question/problem',':question/worked-solution') if k in q}
 if ':question/id' in out:out[':question/id']=str(out[':question/id'])
 if ':question/difficulty'in q:out[':question/difficulty']=str(q[':question/difficulty'][':db/ident'])
 out[':question/answer-fields']=[]
 for f in q.get(':question/answer-fields',[]):
  z={':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']]}
  if ':answer-field/correct' in f:z[':answer-field/correct']=[':answer/id',str(f[':answer-field/correct'][':answer/id'])]
  out[':question/answer-fields'].append(z)
 return out

def check(r,check_bank=True):
 q=r['question'];assert q[':question/difficulty']==':question.difficulty/moderate'
 m=scan(q[':question/problem']);A=[[val(z) for z in row] for row in m[0]];v=[val(row[0]) for row in m[1]]
 assert len(m)==2 and len(A)==len(v)==3 and all(len(row)==3 for row in A)
 answer=[sum(a*b for a,b in zip(row,v)) for row in A]
 p=r['generation']['parameters'];g.guard(p)
 assert A==p['A'] and v==p['v'] and r['knowledge_point']['db_id']==g.KP
 template=r['generation']['template'];blank=template.endswith('blank')
 if template.startswith('named'):
  names=re.search(r'Find \$([A-Z])([a-z])\$',q[':question/problem']);assert names and (names[1],names[2])==(p['matrix_name'],p['vector_name'])
  assert r'\begin{aligned}'+names[1]+names[2]+' & =' in q[':question/worked-solution']
 fields=q[':question/answer-fields'];assert len(fields)==(3 if blank else 1)
 assert {f[':answer-field/key'] for f in fields}==({'field-1','field-2','field-3'} if blank else {'selection'})
 for f in fields:
  answers={a[':answer/id']:a for a in f[':answer-field/choices']};assert len(answers)==len(f[':answer-field/choices'])
  correct=answers[f[':answer-field/correct'][1]][':answer/value']
  if blank:
   i=int(f[':answer-field/key'][-1])-1;assert val(correct)==answer[i] and len(answers)==1
   assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
  else:
   assert f[':answer-field/type']==':answer-field.type/radio'
   values=[tuple(val(row[0]) for row in scan(g.normalize_tex(a[':answer/value']))[0]) for a in answers.values()]
   assert len(values)==len(set(values))==5
   assert tuple(val(row[0]) for row in scan(g.normalize_tex(correct))[0])==tuple(answer)
   if check_bank:assert set(values)=={v for _,v in g.bank(r['generation']['bank_profile'],p)}
 solution=scan(q[':question/worked-solution']);assert len(solution)==5
 assert [[val(z) for z in row] for row in solution[0]]==A
 assert [val(row[0]) for row in solution[1]]==v
 for i,row in enumerate(solution[2]):
  text=clean(''.join(row))
  factors=re.findall(r'(\(-?\d+\)|-?\d+)\s*\*\s*(\(-?\d+\)|-?\d+)',text)
  assert [(val(a),val(b)) for a,b in factors]==list(zip(A[i],v))
  assert val(text)==answer[i]
 for stage in solution[3:]:
  assert len(stage)==3 and [val(''.join(row)) for row in stage]==answer
 return g.fingerprint(p)
def native(r,label=None):
 checks=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  if f[':answer-field/type'].endswith('/radio'):
   for a in f[':answer-field/choices']:checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'field-owned radio answer'})
  else:
   a=f[':answer-field/choices'][0][':answer/value'];n=int(a)
   for text,expected in [(a,'accepted'),(str(2*n)+'/2','accepted'),('('+a+')+0','accepted'),(str(n+1),'rejected')]:checks.append({'field_index':i,'submitted':text,'expected':expected,'purpose':'exact, equivalent, and incorrect integer entry'})
 return {'label':label or r['question'][':question/id'],'record':r,'checks':checks}
def source_record(q):
 mid=q[':question/math-academy-id']
 return {'knowledge_point':{'db_id':g.KP,'title':g.TITLE},'question':normalize(q),'generation':{'template':g.template_of(mid),'bank_profile':mid,'parameters':g.parameters(q),'eligible_for_learning':True}}
def main():
 replay=[];cases=[];profiles={};slots={};reviews=[]
 for mid,q in g.SOURCES.items():
  p=g.parameters(q);t=g.template_of(mid);entries=g.bank(mid,p);rows=[]
  for f in q[':question/answer-fields']:
   values=[tuple(val(row[0]) for row in scan(g.normalize_tex(a[':answer/value']))[0]) if entries else (val(a[':answer/value']),) for a in f[':answer-field/choices']]
   expected=[z for _,z in entries] if entries else [(g.dot(p)[int(f[':answer-field/key'][-1])-1],)]
   assert sorted(values)==sorted(expected),(mid,values,expected)
   correct=f.get(':answer-field/correct');key_checked=False
   if correct:
    cv=tuple(val(row[0]) for row in scan(g.normalize_tex(correct[':answer/value']))[0]) if entries else (val(correct[':answer/value']),)
    assert cv==(g.dot(p) if entries else expected[0]);key_checked=True
   rows.append({'field':f[':answer-field/key'],'matched':len(values),'total':len(values),'missing':[],'extra':[],'correct_designation_verified':key_checked,'choice_mapping':[{'answer_id':a[':answer/id'],'value':values[i],'recipe':next((recipe for recipe,z in entries if z==values[i]),'exact-component')} for i,a in enumerate(f[':answer-field/choices'])]})
  replay.append({'source':mid,'template':t,'profile':mid,'fields':rows,'generalized_sampling_supported':mid not in g.EXCLUDED,'exclusion':g.EXCLUDED.get(mid),'replay_method':'formula' if mid not in g.EXCLUDED else 'exact observed values, original parameters only; does not establish generalized fidelity'})
  if ':question/difficulty'in q:
   r=source_record(q);check(r,False);cases.append(native(r,'existing-'+mid))
  if mid not in g.EXCLUDED:
   r=g.generate('moderate',7,t,p,mid);check(r);cases.append(native(r,'source-replay-'+mid))
   reviews.append({'source':mid,'source_problem':q[':question/problem'],'source_solution':q[':question/worked-solution'],'replayed':r,'variants':[]})
 for t,ps in g.ELIGIBLE.items():
  for profile in ps:
   for seed in range(150):
    r=g.generate('moderate',seed,t,profile=profile);check(r);assert r==g.generate('moderate',seed,t,profile=profile)
    p=r['generation']['parameters'];profiles[profile]=profiles.get(profile,0)+1
    for row in range(3):
     for col in range(3):slots.setdefault('A_'+str(row)+str(col),set()).add(p['A'][row][col])
     slots.setdefault('v_'+str(row),set()).add(p['v'][row])
    for k in ('matrix_name','vector_name'):slots.setdefault(k,set()).add(p[k])
    if seed<3:
     cases.append(native(r,profile+'-'+str(seed)))
     next(z for z in reviews if z['source']==profile)['variants'].append(r)
 # Boundary cases and a changed-name case with mathematical operands held fixed.
 for profile in [p for ps in g.ELIGIBLE.values() for p in ps]:
  for n in (-8,8):
   p={'A':[[n,0,1],[1,n,0],[0,1,n]],'v':[0,1,2],'matrix_name':'Z','vector_name':'n'}
   try:r=g.generate('moderate',19,g.template_of(profile),p,profile)
   except ValueError:continue # Complete-bank collisions are required rejections.
   check(r);cases.append(native(r,'boundary-'+profile+'-'+str(n)))
 p=g.parameters(g.SOURCES['q-318606']);a=g.generate('moderate',0,'named-blank',p,'q-318606');b=g.generate('moderate',0,'named-blank',{**p,'matrix_name':'Z','vector_name':'n'},'q-318606');check(a);check(b)
 assert g.fingerprint(p)==g.fingerprint(b['generation']['parameters'])
 bad=copy.deepcopy(b);bad['question'][':question/worked-solution']=a['question'][':question/worked-solution']
 try:check(bad)
 except AssertionError:pass
 else:raise AssertionError('Stale name survived validation')
 bad=copy.deepcopy(b);bad['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='987654'
 try:check(bad)
 except AssertionError:pass
 else:raise AssertionError('Wrong key survived validation')
 for level in ('easy','hard'):
  try:g.generate(level)
  except ValueError:pass
  else:raise AssertionError('Unsupported level accepted')
 assert all(values==set(range(-8,9)) for name,values in slots.items() if name.startswith(('A_','v_')))
 save(HERE/'source-bank-replay.json',replay);save(HERE/'slot-coverage.json',{'profiles':profiles,'slots':{k:sorted(v) for k,v in slots.items()},'name_change_preserves_operands':True,'stale_name_and_key_rejected':True,'target_role':'all three ordered output coordinates; no selected-cell slot','full_signed_integer_domain_covered_per_slot':True})
 save(HERE/'review.json',reviews);save(HERE/'native-input.json',cases)
 subprocess.run([str(HERE.parents[2]/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
 matched=sum(f['matched'] for r in replay for f in r['fields'])
 save(HERE/'validation.json',{'passed':True,'sampled_instances':sum(profiles.values()),'all_source_values_accounted_for':matched,'supported_source_profiles':list(profiles),'excluded_sampling_profiles':g.EXCLUDED,'fidelity':{'supported_profiles':'complete banks, values, correct designations, prompt structure, field keys, ordered solution stages preserved','unsupported_profiles':'exact observed-bank replay only; no claim of generalized recipes','layout_difference':'decorative aligned spacing simplified; signed products and all three instructional stages retained'},'correctness':'independent rendered matrix operands, every expanded factor, every intermediate sum, all correct keys','grading':'actual course_academy_engine::learning::grade_field, source and generated radio choices; blank equivalents and wrong entries','deterministic_replay':True,'supported_levels':['moderate'],'unsupported_levels':['easy','hard']})
 print('Validated',sum(profiles.values()),'instances;',matched,'source values accounted for')
if __name__=='__main__':main()
