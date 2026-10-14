"""Root full equation/order/bank/prose/feedback and permutation-alias readback."""
import hashlib,importlib.util,itertools,json,re,sys
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186166813;D=R.parents[2]/f'generate/scratch/{K}-draft'
def mod(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);sys.modules[n]=m;z.loader.exec_module(m);return m
G=mod('root_order_generator',D.with_suffix('.py'));P=mod('root_order_jets',R/'ode-jet-order-readback.py');F=mod('root_order_fidelity',R/'root-source-fidelity.py');originals,fidelity=F.check(G,K,D)
words=['first','second','third','fourth','fifth','sixth','seventh','eighth'];ordinal={w:n for n,w in enumerate(words,1)}
ALLOW_PENDING='--pending' in sys.argv
C=dict(records=0,full_equations=0,derivative_occurrences=0,fields=0,values=0,operative_highest_references=0,verdicts=0,conclusions=0,whole_banks=0,feedback_references=0,permutation_aliases=0,pending_grammar=0,pending_permutations=0)
def highest(t):return max(n for a,b,n in P.tokens(t))
def check(r,raw=False):
 q,m=r['question'],r['generation'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];fields=q[':question/answer-fields'];selected=[]
 if len(fields)==3:
  target=ordinal[re.search(r'are (\w+)-order',prompt)[1]];equations=dict(re.findall(r'- \*\*(I|II|III)\.\*\* \$(.*?)\$',prompt));assert set(equations)=={'I','II','III'}
  for f in fields:
   key=f[':answer-field/key'];res,n,ds,masked=P.equation(equations[key]);values=f[':answer-field/choices'];assert sorted(a[':answer/value'] for a in values)==['false','true'] and f[':answer-field/type']==':answer-field.type/checkbox';expected='true' if n==target else 'false';actual=next(a[':answer/value'] for a in values if a[':answer/id']==f[':answer-field/correct'][1]);assert actual==expected
   if n==target:selected.append(key)
   sentence=re.search(r'- Equation '+key+r' (.*?)(?=\n\n|$)',sol,re.S)[1];shown=re.search(r'highest derivative in this equation is \$(.*?)\$',sentence)[1];assert highest(shown)==n
   assert bool(re.search(r'is not an? ',sentence))==(n!=target)
   if n!=target:assert re.search(r'this is an? (\w+)-order',sentence)[1]==words[n-1]
   if not raw:
    if 'a eighth' in sentence:assert ALLOW_PENDING;C['pending_grammar']+=1
    if q[':question/difficulty'].endswith('/moderate'):assert n<=3 and target<=3 and len(ds) in (1,2)
    else:
     assert 4<=n<=8 and 4<=target<=8 and len(ds)==4 and len(set(z for a,b,z in ds))>=3 and r'\frac' in equations[key]
   for a in values:
    if ':answer/feedback' in a:
     fb=a[':answer/feedback'];refs=P.tokens(fb) if r'\frac' in fb else [(0,0,sum({'′':1,'″':2,'‴':3,"'":1}[c] for c in z)) for z in re.findall(r"y([′″‴']+)",fb)];assert refs and max(v[2] for v in refs)==n
     assert f'Equation {key}' in fb
     if key=='I':assert words[n-1]+' order' in fb
     if key=='II':assert 'factor y^5 does not change' in fb and '{y}^{5}' in equations[key]
     if key=='III':assert 'square root does not change' in fb and r'\sqrt' in equations[key]
     C['feedback_references']+=1
   C['full_equations']+=1;C['derivative_occurrences']+=len(ds);C['operative_highest_references']+=1;C['verdicts']+=1;C['fields']+=1;C['values']+=2
  first=re.search(r'largest derivative term in the equation is \$(.*?)\$',sol);assert first and highest(first[1])==target
  ending=re.search(r'correct answer is "(.*?)\."',sol)[1];expected='none' if not selected else 'all three' if len(selected)==3 else ' and '.join(selected)+' only';assert ending==expected;C['conclusions']+=1;C['whole_banks']+=1
 else:
  equation=prompt.split('$$')[1] if '$$' in prompt else re.findall(r'\$(.*?)\$',prompt)[0];res,n,ds,masked=P.equation(equation);f=fields[0];vals=[int(a[':answer/value']) for a in f[':answer-field/choices']];actual=int(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]));assert actual==n and len(vals)==len(set(vals))
  shown=re.search(r'highest derivative in the given ODE is \$(.*?)\$',sol);assert shown and highest(shown[1])==n
  assert int(re.search(r'which has order \$(\d+)\.',sol)[1])==int(re.search(r'order of the ODE is \$(\d+)\.',sol)[1])==n
  if not raw:
   ordinary=list(map(int,re.findall(r'\{x\}\^\{(\d+)\}',masked)));assert len(ordinary)==1;low=min(v[2] for v in ds);assert len(ds)==2 and 3<=n<=7 and 1<=low<=n-2 and n+2<=ordinary[0]<=9
   assert set(vals)=={n,low,ordinary[0],n-1,n+1};C['whole_banks']+=1
  C['full_equations']+=1;C['derivative_occurrences']+=len(ds);C['operative_highest_references']+=1;C['fields']+=1;C['values']+=len(vals);C['conclusions']+=1
 C['records']+=1
for r in json.loads((R/f'qa/{K}-sampled.json').read_text()):check(r)
for c in json.loads((D/'source-cases.json').read_text()):check(G.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']),True)
for l in ('moderate','hard'):
 for seed in (43,107):
  r=G.generate(l,seed);p=r['generation']['parameters'];check(r)
  for perm in itertools.permutations(range(3)):
   pp={k:[v[i] for i in perm] if isinstance(v,list) else v for k,v in p.items()};z=G.generate(l,seed+5,parameters=pp);check(z)
   same=z['question'][':question/id']==r['question'][':question/id'] and z['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
   if not same:assert ALLOW_PENDING;C['pending_permutations']+=1
   else:C['permutation_aliases']+=1
for pp in ({'orders':{'1':2,'2':5}},{'orders':{'1':4,'2':8}}):check(G.generate('moderate',template='q-96676',parameters=pp,profile='observed'),True)
pending=C['pending_grammar'] or C['pending_permutations'];result=dict(status='pending_corrections' if pending else 'passed',source=fidelity,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f"qa/{K}-root-readback{'-pending' if pending else ''}.json").write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
