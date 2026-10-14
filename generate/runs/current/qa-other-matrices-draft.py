"""Root independently checks printed shapes, category partial order and subset banks."""
import hashlib,importlib.util,itertools,json,re,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186087698;D=R.parents[2]/f'generate/scratch/{K}-draft'
def mod(n,p):
 sp=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(sp);sys.modules[n]=m;sp.loader.exec_module(m);return m
G=mod('root_other_generator',D.with_suffix('.py'));P=mod('root_other_scalar',R/'ode-scalar-parser.py');F=mod('root_other_fidelity',R/'root-source-fidelity.py');originals,fidelity=F.check(G,K,D)
C=dict(records=0,matrices=0,cells=0,fields=0,values=0,predicate_choices=0,subset_pairs=0,solution_statements=0,conclusions=0,level_guards=0)
labels={'A row vector':'row','A column vector':'column','A column matrix':'column','A zero matrix':'zero','An identity matrix':'identity','A diagonal matrix':'diagonal','A square matrix':'square','Other':'other'}
def check(r,raw=False):
 q,m=r['question'],r['generation'];t=m['template'];objects=[]
 for name,body in re.findall(r'([A-Z])\s*=\s*\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',q[':question/problem'],re.S):
  a=s.Matrix([[P.scalar(x) for x in row.split('&')] for row in body.split(chr(92)*2)]);n,c=a.rows,a.cols;sq=n==c;di=sq and all(a[i,j]==0 for i in range(n) for j in range(c) if i!=j);identity=sq and a==s.eye(n);zero=all(v==0 for v in a);props={'row':n==1,'column':c==1,'square':sq,'diagonal':di,'identity':identity,'zero':zero,'other':n>1 and c>1 and not sq and not zero};objects.append((name,a,props));C['cells']+=n*c
 assert len(objects)==(1 if t=='classification' else 3);C['matrices']+=len(objects)
 fields=q[':question/answer-fields'];good=None
 if t=='classification':
  assert len(fields)==1;f=fields[0];values=[a[':answer/value'] for a in f[':answer-field/choices']];props=objects[0][2];assert len(values)==5 and len(set(values))==5
  true=[v for v in values if props[labels[v]]]
  true=[v for v in true if not (labels[v] in ('square','diagonal') and props['identity'] and 'An identity matrix' in values) and not (labels[v]=='square' and props['diagonal'] and 'A diagonal matrix' in values)]
  assert len(true)==1;good=true[0];C['predicate_choices']+=5
 elif t=='row_sets':
  assert len(fields)==1;f=fields[0];good={name for name,a,p in objects if p['row']};values=[set(re.findall(r'\$([A-Z])\$',a[':answer/value'])) for a in f[':answer-field/choices']];assert len(values)==5 and sum(v==good for v in values)==1
  for a,b in itertools.combinations(values,2):assert a!=b;C['subset_pairs']+=1
 else:assert len(fields)==3
 for f in fields:
  values=[a[':answer/value'] for a in f[':answer-field/choices']]
  if t in ('rows','columns'):
   assert set(values)=={'true','false'};obj=next(o for o in objects if o[0]==f[':answer-field/key']);good=str(obj[2]['row' if t=='rows' else 'column']).lower()
  else:assert len(set(values))==5
  if ':answer-field/correct' in f:
   actual=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert (set(re.findall(r'\$([A-Z])\$',actual)) if t=='row_sets' else actual)==good
  C['fields']+=1;C['values']+=len(values)
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution']
  if t=='classification':
   category=labels[good];assert category.replace('column','column').replace('row','row') in sol or category=='other' and 'no special name' in sol
   if category=='identity':assert 'diagonal entries are all ones' in sol and 'do not lie on the main diagonal are zeros' in sol
   elif category=='diagonal':assert 'diagonal entries are not all ones' in sol and 'do not lie on the main diagonal are zeros' in sol
   C['solution_statements']+=1
  else:
   kind='column' if t=='columns' else 'row';chunks=re.findall(r'^- (.*?)$',sol,re.M);assert len(chunks)==3;chosen=set()
   for text,(name,a,p) in zip(chunks,objects):
    assert text.startswith('$'+name+'$') and ('*not*' in text)==(not p[kind])
    if p[kind]:assert 'only one '+kind in text;chosen.add(name)
    elif p['column' if kind=='row' else 'row']:
     count=a.rows if kind=='row' else a.cols;assert f'${count}$' in text
    else:
     count=a.rows if kind=='row' else a.cols;assert f'${count}$' in text and 'more than $1$' in text
    C['solution_statements']+=1
   final=sol.split('Therefore,')[-1];assert set(re.findall(r'\$([A-Z])\$',final))==chosen and ('none' in final)==(not chosen);C['conclusions']+=1
 if not raw:
  level=q[':question/difficulty'].split('/')[-1];lo,hi={'easy':(1,6),'moderate':(7,8),'hard':(9,10)}[level];assert all(lo<=max(a.rows,a.cols)<=hi for name,a,p in objects)
  if level!='easy' and t!='classification':
   counts=[a.cols if t=='columns' else a.rows for name,a,p in objects];assert any(c!=1 for c in counts) and all(c==1 or lo<=c<=hi for c in counts)
  C['level_guards']+=1
 C['records']+=1
for r in json.loads((R/f'qa/{K}-sampled.json').read_text()):check(r)
for level in ('easy','moderate','hard'):
 for profile in G.DEFAULT_PROFILES:
  for seed in (36,78,113):check(G.generate(level,seed,profile=profile))
for c in json.loads((D/'source-cases.json').read_text()):check(G.generate(c.get('level','easy'),template=c['template'],parameters=c['parameters'],profile=c.get('bank_profile',c.get('profile'))),True)
result={'status':'passed','source':fidelity,'readback':C,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'database_writes':0};(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
