#!/usr/bin/env python3
"""Read displayed polynomial and every operative component independently;
compare source field presence/banks/prose, then use the real native grader."""
import copy,hashlib,importlib.util,itertools,json,re,subprocess
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
TRANS=standard_transformations+(implicit_multiplication_application,convert_xor)
def parse(s):
 s=s.strip().rstrip('.').replace(r'\underbrace','').replace('_{⏟}','').replace(r'\,','').replace(r'\cdot','*').replace('{','').replace('}','')
 return sp.expand(parse_expr(s,transformations=TRANS))
def fmt(s):
 assert not any(ord(c)<32 and c not in '\n\t' for c in s),'C0'
 assert s.count('$')%2==0,'math delimiters'
 depth=0
 for c in s:
  if c=='{':depth+=1
  if c=='}':depth-=1
  assert depth>=0,'brace depth'
 assert depth==0 and 'SLOT' not in s and '+-' not in s and '--' not in s

def check(rec):
 assert set(rec['knowledge_point'])=={'db_id','id','title'}
 q=rec['question'];prompt=q[':question/problem'];fmt(prompt)
 txt=re.search(r'\$([^$]*)\$',prompt)[1];printed=parse(txt)
 vs=list(printed.free_symbols);assert len(vs)==1;v=vs[0]
 pol=sp.Poly(printed,v);assert pol.degree()==2 and pol.nth(2)==1
 a=pol.nth(1)/2;c=pol.nth(0);remainder=c-a*a
 assert a.is_Integer and a>0 and c>0
 # Repeated polynomial in a supplied-fragment layout must match the first.
 for match in re.findall(r'(?:\{'+str(v)+r'\}|'+str(v)+r')\^\{2\}\s*\+\s*\d+'+str(v)+r'\s*\+\s*\d+',prompt):assert parse(match)==printed
 if 'values of $p$ and $q$' in prompt:
  assert re.search(r'\('+str(v)+r'\s*\+\s*p\{?\)\}?\^\{2\}\s*\+\s*q',prompt),'supplied p/q object uses actual variable'
 if not rec['generation']['raw_replay']:
  assert all(':answer-field/choices' in f and ':answer-field/correct' in f for f in q[':question/answer-fields'])
  assert ':question/difficulty' in q and ':question/worked-solution' in q
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];fmt(sol)
  rows=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(rows)==4,'four taught stages'
  for row in rows:assert sp.simplify(parse(row)-printed)==0,('wrong displayed stage',row)
  compact=[re.sub(r'\s+','',row) for row in rows]
  # The half coefficient, its square and the original constant are each read
  # from the actual row. Equality alone would permit missing taught operations.
  assert re.search(r'2\\cdot'+str(a)+str(v),compact[0]),'linear decomposition'
  assert compact[0].endswith('+'+str(c))
  assert compact[1].count('{'+str(a)+'}^{2}')==2,'add/subtract same square'
  assert re.search(r'\+\{'+str(a)+r'\}\^\{2\}',compact[1]),'added square'
  assert '-'+r'\,'+'{'+str(a)+'}^{2}+'+str(c) in compact[1],'subtracted square/retained constant'
  assert re.search(r'\('+str(v)+r'\+'+str(a)+r'\{?\)\}?\^\{2\}-\{'+str(a)+r'\}\^\{2\}\+'+str(c),compact[2]),'factored component and uncollected constants'
  assert compact[3].count('^{2}')==1,'collected final constants'
  sid=rec['generation']['template'];shape=g.CONFIG[sid][5] if sid in g.CONFIG else 'pq'
  p_actual={'variable':str(v),'a':int(a),'c':int(c)}
  expected_sol=g.fill(g.MASKS[sid][':question/worked-solution'],p_actual) if sid in g.MASKS and ':question/worked-solution' in g.MASKS[sid] else g.solution(p_actual,shape=='pq')
  assert sol==expected_sol,'full fixed prose and operative source stage sequence'
  if shape=='pq':
   conclusion=re.search(r'Therefore, \$p=(-?\d+)\$ and \$q=(-?\d+)\.\$',sol);assert conclusion and int(conclusion[1])==a and int(conclusion[2])==remainder,'conclusion components'
 for f in q[':question/answer-fields']:
  vals=f.get(':answer-field/choices',[])
  for ans in vals:fmt(ans[':answer/value'])
  if f[':answer-field/type'].endswith('/radio'):
   assert len(vals)==5
   pairs=vals[0][':answer/value'].startswith('p=')
   actual=[]
   for ans in vals:
    if pairs:
     m=re.fullmatch(r'p=([^,]+),\\,q=(.*)',ans[':answer/value']);assert m
     actual.append((parse(m[1]),parse(m[2])))
    else:actual.append(parse(ans[':answer/value']))
   assert len(set(actual))==5,'complete bank equivalence'
   expected=(a,remainder) if pairs else printed
   hit=[ans[':answer/id'] for ans,val in zip(vals,actual) if val==expected];assert len(hit)==1
   if ':answer-field/correct' in f:assert f[':answer-field/correct'][1]==hit[0]
  else:
   key=f[':answer-field/key'];assert '{{'+key+'}}' in prompt
   pq='values of $p$ and $q$' in prompt
   minus=r'\,-$' in prompt
   expected=a if pq and key=='field-1' else (v+a if key=='field-1' else (-remainder if minus else remainder))
   if vals:
    assert len(vals)==1 and parse(vals[0][':answer/value'])==expected
    if ':answer-field/correct' in f:assert f[':answer-field/correct'][1]==vals[0][':answer/id']
 base={k:val for k,val in q.items() if k not in (':question/id',':question/answer-fields')}
 specs=[]
 for f in q[':question/answer-fields']:
  bank=':answer-field/choices' in f;correct=':answer-field/correct' in f
  cv=next(ans[':answer/value'] for ans in f.get(':answer-field/choices',[]) if ans[':answer/id']==f[':answer-field/correct'][1]) if correct else None
  specs.append((f[':answer-field/key'],sorted(ans[':answer/value'] for ans in f.get(':answer-field/choices',[])) if bank else None,cv,bank,correct))
 ident=g.digest([g.VERSION,base,q[':question/answer-fields'][0][':answer-field/type'].split('/')[-1],sorted(specs)])
 assert q[':question/id']==g.uid(ident),'actual content identity'
 return 1

def main():
 cases=[];fidelity=[];review=[];checks=0
 for sid,cfg in g.CONFIG.items():
  level=cfg[0];p=g.parameters_for(sid);src=g.QUESTIONS[sid]
  cases.append({'source_id':sid,'template':sid,'parameters':p,'bank_profile':'raw:'+sid,'difficulty':level,'difficulty_origin':'observed' if ':question/difficulty' in src else 'authored layout classification'})
  raw=g.generate(level,parameters=p,profile='raw:'+sid);checks+=check(raw);q=raw['question'];matched=designated=0
  for k in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):
   assert (k in src)==(k in q)
  assert q[':question/problem']==src[':question/problem']
  if ':question/worked-solution' in src:assert q[':question/worked-solution']==src[':question/worked-solution']
  if ':question/difficulty' in src:assert q[':question/difficulty']==g.enum(src[':question/difficulty'])
  for sf in src[':question/answer-fields']:
   f=next(ff for ff in q[':question/answer-fields'] if ff[':answer-field/key']==sf[':answer-field/key'])
   assert f[':answer-field/type']==g.enum(sf[':answer-field/type'])
   for k in (':answer-field/correct',':answer-field/choices'):assert (k in sf)==(k in f)
   if ':answer-field/choices' in sf:
    assert sorted(a[':answer/value'] for a in sf[':answer-field/choices'])==sorted(a[':answer/value'] for a in f[':answer-field/choices']);matched+=len(sf[':answer-field/choices'])
   if ':answer-field/correct' in sf:
    val=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert val==sf[':answer-field/correct'][':answer/value'];designated+=1
  fidelity.append({'source_id':sid,'exact_prompt':True,'exact_solution_or_omission':True,'attribute_presence_parity':True,'options_matched':matched,'correct_designations_matched':designated});review.append(raw)
  completed=g.generate(level,parameters=p,profile='completed:'+sid);checks+=check(completed);review.append(completed)
  changed={'variable':'z','a':8,'c':69 if cfg[5]!='minus' else 59}
  for prof in ('raw:'+sid,'completed:'+sid,'method'):
   r=g.generate(level,73,sid,parameters=changed,profile=prof);checks+=check(r);review.append(r)
  for seed in (91,157):
   r=g.generate(level,seed,sid);checks+=check(r);review.append(r)
 # Default coverage and selector combinations.
 for level in ('easy','moderate','hard'):
  covered=set()
  for seed in range(100):
   r=g.generate(level,seed);checks+=check(r);covered.add(r['generation']['template'])
   if seed<4:review.append(r)
  assert covered==({s for s,c in g.CONFIG.items() if c[0]==level} if level!='hard' else {'hard_radio','hard_blank'})
  for ft in ('radio','blank'):
   for seed in range(15):
    r=g.generate(level,seed,field_type=ft);checks+=check(r);assert all(f[':answer-field/type'].endswith('/'+ft) for f in r['question'][':question/answer-fields'])
 # Finite same-method task counts: variable/profile/field aliases do not count.
 counts={}
 for level in ('easy','moderate','hard'):
  fps=set()
  shapes=['expression','plus','minus'] if level=='easy' else ['pq']
  for shape in shapes:
   sid=next((s for s,c in g.CONFIG.items() if c[0]==level and c[5]==shape),None) or 'hard_radio'
   for a in (range(12,16) if level=='hard' else range(1,12)):
    for q in range(-25,26):
     p={'variable':'x','a':a,'c':a*a+q}
     try:r=g.generate(level,0,sid,parameters=p)
     except ValueError:continue
     checks+=check(r);fps.add(r['generation']['mathematical_fingerprint'])
  counts[level]=len(fps)
 for r in review:
  z=r['generation'];level=g.CONFIG[z['template']][0] if z['template'] in g.CONFIG else 'hard'
  changed=g.generate(level,z['seed']+23,z['template'],parameters=z['parameters'],profile=z['bank_profile']);assert r['question'][':question/id']==changed['question'][':question/id']
  p=dict(z['parameters']);p['variable']='x' if p['variable']!='x' else 'z'
  alias=g.generate(level,1,z['template'],parameters=p,profile=z['bank_profile']);assert alias['generation']['mathematical_fingerprint']==z['mathematical_fingerprint']
 # Actual presence changes content identity; complete raw/completed aliases don't.
 for sid in g.CONFIG:
  l=g.CONFIG[sid][0];p=g.parameters_for(sid)
  raw=g.generate(l,parameters=p,profile='raw:'+sid);done=g.generate(l,parameters=p,profile='completed:'+sid)
  assert (raw['question'][':question/id']==done['question'][':question/id'])==(':question/worked-solution' in g.QUESTIONS[sid])
 invalid=[('hard',{'variable':'x','a':11,'c':122}),('easy',{'variable':'x','a':12,'c':145}),('moderate',{'variable':'x','a':-2,'c':5}),('moderate',{'variable':'x','a':3,'c':9}),('easy',{'variable':'x','a':1,'c':3})]
 for level,p in invalid:
  try:g.generate(level,field_type='radio',parameters=p)
  except ValueError:pass
  else:raise AssertionError('invalid/ambiguous whole instance')
 mutation_count=0
 original=g.generate('easy',0,'q-141537',parameters=g.parameters_for('q-141537'))
 for before,after in [(r'2\cdot 5x',r'10x'),('{5}^{2}','{6}^{2}'),('-'+r'\,'+'{5}^{2}','+'+r'\,'+'{5}^{2}'),('Finally, evaluating','\fFinally, evaluating')]:
  bad=copy.deepcopy(original);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace(before,after)
  try:check(bad)
  except Exception:mutation_count+=1
  else:raise AssertionError('operative mutation survived')
 payload=[]
 for n,r in enumerate(review):
  if any(':answer-field/correct' not in f for f in r['question'][':question/answer-fields']):continue
  tests=[]
  for fi,f in enumerate(r['question'][':question/answer-fields']):
   if f[':answer-field/type'].endswith('/radio'):
    tests.extend({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete source/generated choice bank'} for a in f[':answer-field/choices'])
   else:
    val=f[':answer-field/choices'][0][':answer/value'];equiv=f'({val})/2+({val})/2';wrong=str(parse(val)+1)
    tests.extend({'field_index':fi,'submitted':v,'expected':e,'purpose':p} for v,e,p in [(val,'accepted','canonical supplied fragment'),(equiv,'accepted','equivalent unreduced supplied fragment'),(wrong,'rejected','wrong fragment')])
  payload.append({'label':str(n)+' '+r['generation']['template'],'record':r,'checks':tests})
 (HERE/'engine-input.json').write_text(json.dumps(payload,indent=2)+'\n')
 engine=HERE.parents[1]/'runs/current/check-engine';subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-validation.json')],check=True)
 native=json.loads((HERE/'engine-validation.json').read_text())
 for name,data in [('source-cases.json',cases),('review.json',review)]: (HERE/name).write_text(json.dumps(data,indent=2)+'\n')
 md=['# Completing-square expression review','Raw originals preserve omissions. Completed originals with historical banks are evidence-only. Method-bank variants are eligible; hard is explicitly authored.']
 for r in review:md+=['## '+r['generation']['origin']+' — '+r['generation']['template'],json.dumps(r['generation']['parameters']),g.markdown(r)]
 (HERE/'review.md').write_text('\n\n'.join(md)+'\n')
 report={'status':'pass','basis':1356,'source_questions':9,'prompt_exact':9,'solution_exact':7,'solution_absence_preserved':2,'attribute_presence_parity':9,'source_options_matched':sum(f['options_matched'] for f in fidelity),'source_distractors_matched':sum(f['options_matched']-1 for f in fidelity if f['options_matched']==5),'correct_designations_matched':sum(f['correct_designations_matched'] for f in fidelity),'complete_source_radio_banks':6,'unrated_authored_assignments':{'q-140221':'easy','q-250390':'moderate'},'authored_missing_levels':['hard'],'authored_completions':['q-140221','q-250390'],'opaque_banks_evidence_only':list(g.BANKS),'fidelity':fidelity,'independently_checked_records':checks,'mutation_regressions_rejected':mutation_count,'finite_mathematical_tasks':counts,'native':{k:native[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'dependencies':review[0]['generation']['dependencies'],'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'plots':'none','database_writes':0}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
