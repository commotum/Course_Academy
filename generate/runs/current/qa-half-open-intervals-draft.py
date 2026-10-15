"""Root independently checks endpoint set semantics and each explanatory role."""
import sys,json,re,hashlib,importlib.util,copy
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186059827;D=R.parents[2]/f'generate/scratch/{K}-draft';SCRIPT_SHA=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('root_half_interval_parser',R/'interval-readback.py');g=module('root_half_interval_gen',D.with_suffix('.py'));C=dict(records=0,choices=0,solution_sets=0,endpoint_statements=0,source_banks=0,source_values=0,source_keys=0,source_solutions=0,MA_originals=0,nonMA_inventory=0,raw_missing_fields=0);tasks={l:set()for l in g.LEVELS};roles=set()
def check(r):
 q=r.get('record',r)['question'];prompt=q[':question/problem'];target=p.task(prompt);assert target.left_open!=target.right_open;f=q[':question/answer-fields'][0];values=[p.meaning(a[':answer/value']) for a in f[':answer-field/choices']];assert len(set(values))==len(values)==5;correct=[a[':answer/id']for a,v in zip(f[':answer-field/choices'],values)if v==target];assert len(correct)==1
 if ':answer-field/correct'not in f:assert ':question/worked-solution'not in q and ':question/difficulty'not in q;C['raw_missing_fields']+=1
 else:
  assert f[':answer-field/correct']==[':answer/id',correct[0]];sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);assert len(blocks)==2
  variable=re.search(r'\b([xyut])\b',re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',prompt,re.S)[0])[1]
  for block in blocks:
   assert p.meaning(block)==target,(block,target);found=re.findall(r'(?<![A-Za-z])([xyut])(?![A-Za-z])',block)
   assert all(v==variable for v in found);C['solution_sets']+=1
  direction='interval_to_inequality'if'corresponds to the inequality'in prompt else'inequality_to_interval'
  statements=re.findall(r'- The (left|right) endpoint \$(.*?)\$ (.*?) included in the interval\. Therefore, we use \$(.*?)\$',sol);assert len(statements)==2
  for side,ep,words,symbol in statements:
   left=side=='left';expected=target.start if left else target.end;opened=target.left_open if left else target.right_open;assert p.endpoint(ep)==expected
   assert ('not' in words)==bool(opened)
   symbol=p.clean(symbol).replace(' ','').rstrip('.')
   expected_symbol=('('if opened else'[')if left else(')'if opened else']')
   if direction=='interval_to_inequality':expected_symbol='<'if opened else r'\le'
   assert symbol==expected_symbol,(side,symbol,expected_symbol);C['endpoint_statements']+=1
  level=q[':question/difficulty'].split('/')[-1];tasks[level].add((target.start,target.end,bool(target.left_open),direction));roles.add((level,direction,bool(target.left_open),variable))
 C['records']+=1;C['choices']+=5;return q
src=json.loads((D/'source.json').read_text())['record'][':knowledge-point/questions'];sources={q.get(':question/math-academy-id')or str(q[':db/id']):q for q in src}
for spec in json.loads((D/'component-map.json').read_text()):
 old=sources[spec['source_id']];difficulty=spec['difficulty'];level=difficulty[':db/ident'].split('/')[-1]if difficulty else'hard'if spec['source_id']=='q-25754'else'easy';r=g.generate(level,template=spec['template'],parameters=spec['original_parameters'],profile=spec['profile']);q=check(r);f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
 assert g.fmt.normalize_prose(old[':question/problem'])==q[':question/problem'];assert {p.meaning(a[':answer/value'])for a in of[':answer-field/choices']}=={p.meaning(a[':answer/value'])for a in f[':answer-field/choices']};C['source_banks']+=1;C['source_values']+=len(f[':answer-field/choices']);C['MA_originals'if spec['source_id'].startswith('q-')else'nonMA_inventory']+=1
 if of.get(':answer-field/correct'):
  cv=p.meaning(of[':answer-field/correct'][':answer/value']);assert cv==p.task(q[':question/problem']);C['source_keys']+=1
 if old.get(':question/worked-solution'):assert g.fmt.normalize_prose(old[':question/worked-solution'])==q[':question/worked-solution'];C['source_solutions']+=1
for items in json.loads((D/'variants.json').read_text()).values():
 for r in items:check(r)
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
assert len(roles)==3*2*2*4,(len(roles),roles)
base=g.generate('easy',template='inequality_to_interval',parameters={'a':'-7','b':'4','variable':'x','left_closed':True})
for old,new in [(r'-7 \le x < 4',r'-6 \le x < 4'),('endpoint $-7$ *is*','endpoint $-7$ *is not*'),('we use $[$','we use $($')]:
 bad=copy.deepcopy(base);before=bad['question'][':question/worked-solution'];assert old in before;bad['question'][':question/worked-solution']=before.replace(old,new,1)
 try:check(bad)
 except AssertionError:pass
 else:raise AssertionError('corrupted intermediate passed')
assert hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()==SCRIPT_SHA
proof={'status':'passed','script_sha256':SCRIPT_SHA,'source_and_readback':C,'sampled_actual_tasks':{l:len(v)for l,v in tasks.items()},'direction_closure_variable_roles':len(roles),'negative_controls':3,'scope':'Same finite interval/compound-inequality two endpoint decisions. Integer/rational/surd forms are reading, not solving; no graphs/unions/unbounded tasks. Observed unbounded wrong choice retained only in its full source profile.','database_writes':0};(R/'qa'/f'{K}-root-readback.json').write_text(json.dumps(proof,indent=2)+'\n');print(proof)
