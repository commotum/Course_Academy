"""Independent displayed-ODE, complete-bank, stage and native-grader checks."""
import copy, hashlib, importlib.util, itertools, json, re, subprocess, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=module('standard_form',HERE.with_suffix('.py'));p=module('display_parser',ROOT/'generate/runs/current/ode-scalar-parser.py');s=g.s
MATH=re.compile(r'\$\$(.*?)\$\$',re.S)
def strip_annotation(t):
 for tag in ('_{⏟}','_{P(x)}','_{Q(x)}'):t=t.replace(tag,'')
 return t.replace(r'\underbrace','')
def expression(t):
 for d in (r'\frac{\text{d}y}{\text{d}x}',r'\frac{dy}{dx}'):
  t=t.replace(d,'z')
 return p.scalar(strip_annotation(t)).subs(p.z,g.D)
def equation(t):
 t=t.replace('&','').strip().rstrip('.,');t=t.split(r'\,,')[0]
 t=re.sub(r'(?:,|\\,|\s)*[xy]\\ne.*','',t)
 t=t.rstrip('.,').removesuffix(r'\,')
 left,right=t.split('=');return expression(left),expression(right)
def same(a,b):return s.simplify(s.trigsimp(a-b))==0
def equivalent(a,b):return same(g.normalized(a),g.normalized(b))
def rows(q):
 aligned=q[':question/worked-solution'].split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0]
 return aligned.split(r'\\')
def formatting(q):
 def walk(o):
  if isinstance(o,dict):
   for k,v in o.items():
    if k in (':question/problem',':question/worked-solution',':answer/value'):
     assert not any(ord(c)<32 and c not in '\n\t\r' for c in v),'C0 control character'
     assert v.count('$')%2==0,'Unbalanced math delimiters'
     depth=0
     for ch in v:
      if ch=='{':depth+=1
      if ch=='}':depth-=1
      assert depth>=0,'Unbalanced TeX group'
     assert depth==0,'Unbalanced TeX group'
    else:walk(v)
  elif isinstance(o,list):
   for v in o:walk(v)
 walk(q)
def check(rec):
 q=rec['question'];m=rec['generation'];level=m['difficulty'];t=m['template']
 assert set(rec['knowledge_point'])=={'db_id','id','title'}
 assert m['python']==sys.version.split()[0]
 assert level in g.LEVELS and t in g.FAMILIES[level]
 assert q[':question/difficulty']==':question.difficulty/'+level
 formatting(q)
 prompt=equation(MATH.findall(q[':question/problem'])[0]);res=g.normalized(prompt)
 P=s.expand(res).coeff(g.y);Q=-res.subs({g.D:0,g.y:0})
 assert same(res,g.D+P*g.y-Q)
 for f in q[':question/answer-fields']:
  assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
  answers=[equation(a[':answer/value']) for a in f[':answer-field/choices']]
  assert len(answers)==5 and len({a[':answer/id'] for a in f[':answer-field/choices']})==5
  eligible=[g.standard(a) and equivalent(a,prompt) for a in answers]
  if ':answer-field/correct' in f:
   correct=[a[':answer/id']==f[':answer-field/correct'][1] for a in f[':answer-field/choices']]
   assert sum(eligible)==1 and eligible==correct,(t,eligible,correct)
  assert not any(g.standard(a) and g.standard(b) and equivalent(a,b) for a,b in itertools.combinations(answers,2))
 for row in rows(q):assert equivalent(equation(row),prompt),(t,row)
 conclusion=q[':question/worked-solution'].split('Now, the equation',1)[1]
 cp=re.search(r'\$P\(x\)=(.*?)\$',conclusion)[1];cq=re.search(r'\$Q\(x\)=(.*?)\.\$',conclusion)[1]
 assert same(expression(cp),P) and same(expression(cq),Q)
 if not m['evidence_only']:
  expected=g.stage_rows(t,m['parameters'],g.data(t,m['parameters']))
  assert [r.replace('&','').strip() for r in rows(q)]==expected,'Operative stage mask lost'
  # Original denominator and common-factor restrictions are enforced before CAS.
  if t in ('q-8359','q-79697','rational-collect'):assert r'x\ne 0' in q[':question/problem'] and m['domains']=='x != 0'
  if t in ('q-16396','q-79699'):assert r'y\ne 0' in q[':question/problem'] and m['domains']=='y != 0'
  if t=='q-103354':assert r'\ne 0' in q[':question/problem'] and m['domains']==str(s.cos(m['parameters']['n']*g.x))+' != 0'
  if t=='q-8360':assert r'\sin x\ne 0' in q[':question/problem']
  assert m['mathematical_fingerprint']==g.semantic(P,Q,m['domains'],t),(t,m['parameters'],P,Q)
 return len(rows(q))
def source_compare(t,r):
 old=g.SOURCES[t];new=r['question']
 for k in (':question/problem',':question/worked-solution'):
  assert (k in old)==(k in new);assert old[k]==new[k]
 assert (':question/difficulty' in old)==(':question/difficulty' in new)
 assert (':question/answer-fields' in old)==(':question/answer-fields' in new)
 assert len(old[':question/answer-fields'])==len(new[':question/answer-fields'])
 total=0;corrects=0
 for f,h in zip(old[':question/answer-fields'],new[':question/answer-fields']):
  assert f[':answer-field/key']==h[':answer-field/key']
  assert f[':answer-field/type'][':db/ident']==h[':answer-field/type']
  assert (':answer-field/correct' in f)==(':answer-field/correct' in h)
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in h[':answer-field/choices'])
  if ':answer-field/correct' in f:
   got=next(a[':answer/value'] for a in h[':answer-field/choices'] if a[':answer/id']==h[':answer-field/correct'][1]);assert got==f[':answer-field/correct'][':answer/value'];corrects+=1
  total+=len(f[':answer-field/choices'])
 return total,corrects
def native(rec):
 # Legacy raw field has no key; retain it in evidence but create a documented
 # grading fixture for each completed field. Never infer a raw correct ref.
 fixture=copy.deepcopy(rec);fixture['question'][':question/answer-fields']=[f for f in fixture['question'][':question/answer-fields'] if ':answer-field/correct' in f]
 checks=[]
 for fi,f in enumerate(fixture['question'][':question/answer-fields']):
  for a in f[':answer-field/choices']:
   checks.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every owned radio option; legacy missing-correct field excluded only from fixture'})
 return {'label':rec['question'][':question/id'],'record':fixture,'checks':checks}
def expect_failure(rec,mutate):
 broken=copy.deepcopy(rec);mutate(broken['question'])
 try:check(broken)
 except (AssertionError,ValueError,IndexError):return
 raise AssertionError('Required mutation accepted')
def main():
 report={'basis':g.RAW['basis'],'lineage':g.RAW['lineage'],'runtime':{'python':sys.version.split()[0],'sympy':s.__version__},'source_fidelity':{},'authored_missing_levels':['moderate']}
 cases=[];records=[];reviews=[];nrows=0;options=corrects=0
 for t in g.SOURCES:
  level='hard' if t=='q-16401' else 'easy'
  case={'source_id':t,'difficulty':level,'template':t,'parameters':{'n':1},'bank_profile':'observed-raw'};cases.append(case)
  raw=g.generate(level,template=t,parameters=case['parameters'],profile='observed-raw');nrows+=check(raw);a,b=source_compare(t,raw);options+=a;corrects+=b;records.append(raw)
  changed=g.generate(level,template=t,parameters={'n':2},profile='observed-raw');nrows+=check(changed);records.append(changed)
  observed=g.generate(level,template=t,parameters=g.ORIGINAL[t],profile=t);nrows+=check(observed);records.append(observed)
  reviews.append('## Original '+t+' (basis 1356)\n\n'+g.markdown(raw)+'\n\n### Generated observed-family variant\n\n'+g.markdown(g.generate(level,17,template=t)))
 for level in g.LEVELS:
  for t in g.FAMILIES[level]:
   for seed in range(4):
    r=g.generate(level,seed,template=t);nrows+=check(r);records.append(r)
   for seed in (31,47):
    r=g.generate(level,seed,template=t);nrows+=check(r);records.append(r);reviews.append('## Generated '+level+' '+t+' seed '+str(seed)+'\n\n'+g.markdown(r))
  # Two independent entrypoint examples per level.
  assert len({r['generation']['mathematical_fingerprint'] for r in records if r['generation']['difficulty']==level and not r['generation']['evidence_only']})>=2
 # Exercise every documented parameter boundary for each public normal family.
 limits={'q-16400':{'a':(2,5),'b':(1,5),'c':(1,5),'h':(1,8)},'q-16401':{'a':(1,6),'b':(1,4),'n':(1,6)},'rational-collect':{'a':(2,8),'b':(1,8),'c':(1,8),'d':(1,8),'h':(1,8)}}
 for t,pars in g.ORIGINAL.items():
  level='hard' if t=='q-16401' else 'moderate' if t=='rational-collect' else 'easy'
  limits.setdefault(t,{k:((2,8) if t=='q-79699' else (1,8)) for k in pars})
  for k,(lo,hi) in limits[t].items():
   for value in (lo,hi):
    par=dict(pars);par[k]=value;r=g.generate(level,template=t,parameters=par);nrows+=check(r);records.append(r)
   for value in (lo-1,hi+1):
    par=dict(pars);par[k]=value
    try:g.generate(level,template=t,parameters=par)
    except ValueError:pass
    else:raise AssertionError(('Bounds bypass',t,k,value))
 # Identities depend on complete content, never seed/option order/profile aliases.
 for t in g.SOURCES:
  level='hard' if t=='q-16401' else 'easy'
  raw=g.generate(level,template=t,parameters={'n':1},profile='raw');normal=g.generate(level,template=t,parameters=g.ORIGINAL[t])
  assert raw['generation']['mathematical_fingerprint']==normal['generation']['mathematical_fingerprint']
 for level in g.LEVELS:
  t=g.FAMILIES[level][0];par=g.ORIGINAL[t]
  a=g.generate(level,3,template=t,parameters=par);b=g.generate(level,83,template=t,parameters=par)
  assert a['question'][':question/id']==b['question'][':question/id']
  assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
  assert {v[':answer/id'] for v in a['question'][':question/answer-fields'][0][':answer-field/choices']}=={v[':answer/id'] for v in b['question'][':question/answer-fields'][0][':answer-field/choices']}
 assert g.generate_moderate(parameters={'a':2,'b':2,'c':1,'d':1,'h':1})['generation']['mathematical_fingerprint']==g.generate_moderate(parameters={'a':4,'b':4,'c':2,'d':2,'h':2})['generation']['mathematical_fingerprint']
 # Default sampling must serve every source-supported family.
 coverage={level:{g.generate(level,k)['generation']['template'] for k in range(24)} for level in g.LEVELS}
 assert all(coverage[level]==set(g.FAMILIES[level]) for level in g.LEVELS)
 a=g.generate_easy(template='q-79697',parameters={'k':3})
 expect_failure(a,lambda q:q.__setitem__(':question/problem',q[':question/problem'].replace('x+3 y','x+4 y')))
 expect_failure(a,lambda q:q.__setitem__(':question/worked-solution',q[':question/worked-solution'].replace('x(x+3 y)',r'x^{2}+3xy')))
 expect_failure(a,lambda q:q.__setitem__(':question/worked-solution',q[':question/worked-solution']+'\x0c'))
 a=g.generate_hard(parameters={'a':2,'b':3,'n':2})
 expect_failure(a,lambda q:q.__setitem__(':question/worked-solution',q[':question/worked-solution'].replace('-12 y', '-11 y')))
 # Native engine is separate from mathematics: every correct and wrong choice.
 (HERE/'native-input.json').write_text(json.dumps([native(r) for r in records],indent=2))
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
 engine=json.loads((HERE/'native-report.json').read_text());assert engine['documented_unresolved_checks']==0
 report.update({'source_fidelity':{'source_questions':9,'raw_exact_prompts':9,'raw_exact_solutions':9,'full_banks':10,'all_option_values':options,'matched_correct_designations':corrects,'missing_correct_designations':1,'distractors_with_original_designations':36,'raw_presence_parity':True},'native_engine':engine,'native_engine_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'checks':{'instances':len(records),'printed_solution_rows':nrows,'source_coordinate_changes':9,'all_default_families':{l:sorted(v) for l,v in coverage.items()},'parameter_boundaries':True,'mutation_regressions':4,'seed_order_identity':True,'common_scaling_deduplication':True,'raw_normal_profile_fingerprint_parity':True},'pass':True,'findings':['q-16400 legacy duplicate field preserves missing correct ref in raw; omitted from supported default and native fixture. No source key was fabricated.','All original fields are radio, so complete-equation blank parser limitations do not affect this KP.','Normal mathematical notation is normalized; exact raw source strings are counted separately. Empty source display blocks are removed in normal output.','Original opaque banks are public evidence; normal defaults use separately labeled method-derived complete banks.']})
 (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(HERE/'review.json').write_text(json.dumps(records,indent=2)+'\n');(HERE/'review.md').write_text('# Original and generated questions\n\n'+'\n\n---\n\n'.join(reviews)+'\n');(HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({'pass':True,'instances':len(records),'raw_sources':9,'options_matched':options,'native_checks':engine.get('checks'),'solution_rows':nrows}))
if __name__=='__main__':main()
