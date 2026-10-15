"""Root third/fourth derivative readback of printed givens, targets and stages."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186059679;D=R.parents[2]/f'generate/scratch/{K}'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_higher_gen',D.with_suffix('.py'));P=load('root_higher_math',R/'higher-derivative-readback.py');x=P.x
N=dict(records=0,equalities=0,operands=0,targets=0,values=0,pairs=0,banks=0,blanks=0)
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']};fidelity=dict(raw=0,served=0,values=0,solutions=0,existing_designations=0,authored_missing_bank=0)
def presentation(t):return re.sub(r'(?<![A-Za-z\\])(sin|cos|ln)(?=x)',lambda m:'\\'+m[1]+' ',t.replace('⁡',''))
for case in json.load(open(D/'source-cases.json')):
 sid=case['source_id'];old=olds[sid];assert G.generate(case['difficulty'],profile='raw-evidence',parameters={'source_id':sid})['question']==old;fidelity['raw']+=1
 r=G.generate(case['difficulty'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);q=r['question'];expected_prompt=presentation(old[':question/problem']);assert q[':question/problem']==expected_prompt or sid=='q-28551' and q[':question/problem'].startswith(expected_prompt)
 if ':question/worked-solution'in old:
  expected=presentation(old[':question/worked-solution']);expected=expected.replace('h(x)','y')if sid=='q-28551'else expected;assert q[':question/worked-solution']==expected;fidelity['solutions']+=1
 for f,o in zip(q[':question/answer-fields'],old.get(':question/answer-fields',[])):
  positive=r['generation']['domain']=='x>0';ov=[P.scalar(presentation(a[':answer/value'].replace('\\\\','\\')),positive)for a in o[':answer-field/choices']];nv=[P.scalar(a[':answer/value'],positive)for a in f[':answer-field/choices']];assert len(ov)==len(nv)and all(sum(P.eq(v,w,positive)for w in nv)==1 for v in ov)
  if ':answer-field/correct'in o:
   correct=P.scalar(presentation(o[':answer-field/correct'][':answer/value'].replace('\\\\','\\')),positive);assert P.eq(correct,next(v for a,v in zip(f[':answer-field/choices'],nv)if a[':answer/id']==f[':answer-field/correct'][1]),positive);fidelity['existing_designations']+=1
  fidelity['values']+=len(ov)
 fidelity['served']+=1;fidelity['authored_missing_bank']+=not bool(old.get(':question/answer-fields'))
def check(r):
 q,m=r['question'],r['generation'];positive=m['domain']=='x>0';name,base,fun=P.givens(q[':question/problem'],positive);assert base==0;order=3 if q[':question/difficulty']!=':question.difficulty/hard' else 4;assert m['order']==order
 prompt=P.clean(q[':question/problem']);target=re.search(r"([fgh])('+)\(x\)",prompt)or re.search(r'@D(\d+)(y)@',prompt);assert target
 if target[1].isdigit():assert int(target[1])==order and target[2]==name
 else:assert target[1]==name and len(target[2])==order
 assert not re.search(r'(?<![A-Za-z\\])(sin|cos|ln)(?=x)',q[':question/problem']+q[':question/worked-solution']),('noncanonical math operator',m['template'])
 blocks=re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S);actual_orders=[]
 for block in blocks:
  first=block.replace(r'\begin{aligned}','').split('=',1)[0].replace('&','').strip();bn,bo=P.name_order(first);assert bn==name;actual_orders.append(bo)
  for key,count in P.stage(block,fun,name,0,bo,positive=positive).items():N[key]+=count
 assert actual_orders==list(range(1,order+1))or actual_orders==list(range(order+1)),actual_orders
 assert len(q[':question/answer-fields'])==1;f=q[':question/answer-fields'][0];values=[P.scalar(a[':answer/value'],positive)for a in f[':answer-field/choices']];answer=s.diff(fun,x,order);hits=[a[':answer/id']for a,v in zip(f[':answer-field/choices'],values)if P.eq(v,answer,positive)];assert hits==[f[':answer-field/correct'][1]],(m['template'],answer,values)
 for i,v in enumerate(values):
  for w in values[:i]:assert not P.eq(v,w,positive);N['pairs']+=1
 N['records']+=1;N['values']+=len(values);N['banks']+=1;N['blanks']+=f[':answer-field/type'].endswith('/blank')
records=json.load(open(D/'bounded-records.json'))
for i,old in enumerate(records):
 m=old['generation'];level=old['question'][':question/difficulty'].split('/')[-1];r=G.generate(level,m['seed'],template=m['template'],parameters=m['parameters'],profile=m['profile']);check(r)
 if i%250==0:print('Root actual current records read',i,flush=True)
for level in ('easy','moderate','hard'):
 for seed in range(18):check(G.generate(level,seed))
result=dict(status='passed',source=fidelity,readback=N,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
