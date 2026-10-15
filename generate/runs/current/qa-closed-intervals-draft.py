"""Parent independently reads complete closed-interval banks and actual teaching sets."""
import sys,json,re,hashlib,copy,importlib.util
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186059829;D=R.parents[2]/f'generate/scratch/{K}-draft';SCRIPT_SHA=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()
def module(name,path):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=module('root_closed_sets',R/'interval-readback.py');g=module('root_closed_generator',D.with_suffix('.py'));C=dict(records=0,choices=0,solution_sets=0,source_banks=0,source_values=0,source_keys=0,source_missing_assessments=0,source_prose=0,captured_inventory=0);tasks={l:set()for l in('easy','moderate','hard')};roles=set()
def check(r):
 q=r['question'];prompt=q[':question/problem'].replace(']?$',' ]$?');target=p.task(prompt);assert not target.left_open and not target.right_open
 f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];values=[p.meaning(a[':answer/value'])for a in choices];assert len(values)==len(set(values))==5;assert len([v for v in values if v==target])==1
 if f.get(':answer-field/correct'):assert next(v for a,v in zip(choices,values)if a[':answer/id']==f[':answer-field/correct'][1])==target
 else:assert ':question/difficulty'not in q and ':question/worked-solution'not in q;C['source_missing_assessments']+=1
 if q.get(':question/worked-solution'):
  sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);assert len(blocks)in(2,3);pv=set(re.findall(r'(?<![A-Za-z])([xyt])(?![A-Za-z])',re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',prompt,re.S)[0]));assert len(pv)==1;variable=next(iter(pv))
  for block in blocks:assert p.meaning(block)==target,(block,target);assert set(re.findall(r'(?<![A-Za-z])([xyt])(?![A-Za-z])',block))<=pv;C['solution_sets']+=1
  assert 'endpoints' in sol and ('*are* included'in sol or 'are *included*'in sol)
  for left,right in re.findall(r'endpoints \$(.*?)\$ and \$(.*?)\$',sol):assert {p.endpoint(left),p.endpoint(right)}=={target.start,target.end}
  level=q[':question/difficulty'].split('/')[-1];direction='inequality_to_interval'if'The inequality'in prompt else'interval_to_inequality';orientation='descending'if re.search(r'\\ge|>',re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',prompt,re.S)[0])else'ascending';roles.add((level,direction,variable,orientation));tasks[level].add((target,direction))
 C['records']+=1;C['choices']+=5;return q
sources=json.loads((D/'source.json').read_text())['record'][':knowledge-point/questions'];ma=[q for q in sources if ':question/math-academy-id'in q]
for old in ma:
 r=g.replay_source(old[':question/math-academy-id']);q=check(r);assert q[':question/problem']==old[':question/problem'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0];assert {p.meaning(a[':answer/value'])for a in of[':answer-field/choices']}=={p.meaning(a[':answer/value'])for a in f[':answer-field/choices']};C['source_banks']+=1;C['source_values']+=5
 if of.get(':answer-field/correct'):assert p.meaning(of[':answer-field/correct'][':answer/value'])==p.task(q[':question/problem'].replace(']?$',' ]$?'));C['source_keys']+=1
 if old.get(':question/worked-solution'):assert old[':question/worked-solution']==q[':question/worked-solution'];C['source_prose']+=1
for old in sources:
 if ':question/math-academy-id'in old:continue
 q=copy.deepcopy(old);q[':question/difficulty']=q[':question/difficulty'][':db/ident']
 for f in q[':question/answer-fields']:f[':answer-field/type']=f[':answer-field/type'][':db/ident'];f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
 check({'question':q});C['captured_inventory']+=1
for r in json.loads((D/'samples.json').read_text())+json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
for level,params in [('easy',{'a':'-3','b':'5'}),('moderate',{'a':'-3/2','b':'5/3'}),('hard',{'a':'-sqrt(2)','b':'sqrt(3)'})]:
 for template in g.TEMPLATES:
  for variable in g.VARIABLES:
   for orientation in g.ORIENTATIONS:check(g.generate(level,parameters=params,template=template,profile='observed_interval'if template=='inequality_to_interval'else'observed_inequality',variable=variable,orientation=orientation))
# Interval prompts have no displayed chain orientation; verify their corresponding
# solution/choices nevertheless reverse and retain the same set via actual reader.
for level in tasks:
 assert {role[2]for role in roles if role[0]==level}==set(g.VARIABLES)
base=g.generate('easy',parameters={'a':'-3','b':'5'},template='inequality_to_interval',profile='observed_interval',variable='x',orientation='ascending')
bad=copy.deepcopy(base);text=bad['question'][':question/worked-solution'];bad['question'][':question/worked-solution']=text.replace('-3', '-2',1)
try:check(bad)
except AssertionError:pass
else:raise AssertionError('Stale intermediate endpoint passed')
assert hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()==SCRIPT_SHA
proof={'status':'passed','script_sha256':SCRIPT_SHA,'source_and_readback':C,'sampled_actual_tasks':{l:len(v)for l,v in tasks.items()},'scope':'Finite closed-interval/inequality translation, both directions, three variable aliases, ascending/descending relations. Authored rational/surd endpoint reading, no solving or open/unbounded assessed targets; outside rays remain whole-source distractors.','database_writes':0};(R/'qa'/f'{K}-root-readback.json').write_text(json.dumps(proof,indent=2)+'\n');print(proof)
