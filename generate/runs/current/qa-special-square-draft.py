"""Root independently parses rendered shapes/zero-one masks and cited witnesses."""
import hashlib,importlib.util,itertools,json,re,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186087697;D=R.parents[2]/f'generate/scratch/{K}-draft'
def mod(n,p):
 sp=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(sp);sys.modules[n]=m;sp.loader.exec_module(m);return m
G=mod('root_special_generator',D.with_suffix('.py'));F=mod('root_special_fidelity',R/'root-source-fidelity.py');originals,fidelity=F.check(G,K,D)
C=dict(records=0,actual_matrices=0,predicate_cells=0,fields=0,values=0,subset_pairs=0,witness_checks=0,classification_statements=0,identity_notices=0,conclusions=0,level_guards=0)
def check(r,raw=False):
 q,m=r['question'],r['generation'];kind='identity' if 'identity matrices?' in q[':question/problem'] else 'diagonal';objects=[]
 for l,body in re.findall(r'([A-Z])\s*=\s*\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',q[':question/problem'],re.S):
  body=re.sub(r'\\text\{[^}]*\}','',body);a=s.Matrix([[s.Rational(x.strip()) for x in row.split('&')] for row in body.split(chr(92)*2)]);sq=a.rows==a.cols;diag=sq and all(a[i,j]==0 for i in range(a.rows) for j in range(a.cols) if i!=j);identity=sq and a==s.eye(a.rows);objects.append((l,a,{'square':sq,'diagonal':diag,'identity':identity}));C['predicate_cells']+=a.rows*a.cols
 assert len(objects)==3;C['actual_matrices']+=3;chosen={l for l,a,p in objects if p[kind]};fields=q[':question/answer-fields']
 if fields[0][':answer-field/type'].endswith('checkbox'):
  assert len(fields)==3
  for f in fields:
   assert {a[':answer/value'] for a in f[':answer-field/choices']}=={'false','true'};truth='true' if f[':answer-field/key'] in chosen else 'false';assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==truth;C['fields']+=1;C['values']+=2
 else:
  assert len(fields)==1;f=fields[0];vals=[set(re.findall(r'\$([A-Z])\$',a[':answer/value'])) for a in f[':answer-field/choices']];assert len(vals)==5 and sum(v==chosen for v in vals)==1
  for a,b in itertools.combinations(vals,2):assert a!=b;C['subset_pairs']+=1
  if ':answer-field/correct' in f:assert [a[':answer/id'] for a,v in zip(f[':answer-field/choices'],vals) if v==chosen]==[f[':answer-field/correct'][1]]
  C['fields']+=1;C['values']+=5
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];chunks=re.split(r'(?m)^- ',sol)[1:];assert len(chunks)==3
  for part,(l,a,p) in zip(chunks,objects):
   assert part.startswith('$'+l+'$') and ('*not*' in part.split('\n')[0])==(not p[kind]);C['classification_statements']+=1
   if not p['square']:assert "it's not a square matrix" in part
   elif kind=='identity':
    if p['identity']:assert 'main diagonal are all ones' in part and 'rest of the entries are zeros' in part
    else:assert p['diagonal'] and 'diagonal entries are not all ones' in part
   else:
    assert 'same number of rows and columns' in part
    if p['diagonal']:
     assert 'do not lie on the main diagonal are zeros' in part
     assert ('not an identity matrix' in part)==(not p['identity'])
     assert ('diagonal entries are all ones' in part)==p['identity'];C['identity_notices']+=1
    else:
     witness=re.search(r'\$\{([a-z])\}_\{(\d)(\d)\}=(-?\d+)\\ne 0\$',part);assert witness and witness[1]==l.lower();i,j,v=map(int,witness.groups()[1:]);assert i!=j and a[i-1,j-1]==v and v!=0;C['witness_checks']+=1
  conclusion=sol.split('Therefore,')[-1];assert set(re.findall(r'\$([A-Z])\$',conclusion))==chosen and ('none' in conclusion)==(not chosen);C['conclusions']+=1
 if not raw:
  cells=sum(a.rows*a.cols for l,a,p in objects);level=q[':question/difficulty'].split('/')[-1];lo,hi={'easy':(3,36),'moderate':(37,45),'hard':(46,60)}[level];assert lo<=cells<=hi and all(1<=a.rows<=5 and 1<=a.cols<=5 for l,a,p in objects);C['level_guards']+=1
 C['records']+=1
for r in json.loads((R/f'qa/{K}-sampled.json').read_text()):check(r)
for level in ('easy','moderate','hard'):
 for template in G.TEMPLATES:
  for seed in (37,99):check(G.generate(level,seed,template=template))
for c in json.loads((D/'source-cases.json').read_text()):check(G.generate(c.get('level','easy'),template=c['template'],parameters=c['parameters'],profile=c['bank_profile']),True)
result={'status':'passed','source':fidelity,'readback':C,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'database_writes':0};(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
