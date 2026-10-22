"""Retained findings 2197e08f74d72428c019 and c9f6edae44c110e17773.
Read displayed vectors/choices, solve independently, and test whole families.
Only evidence files are written; runtime package files are never modified.
"""
import importlib.util,json,re,sys
from pathlib import Path
from collections import Counter
sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent/'author-check-current'; E.mkdir(exist_ok=True); W=Path(__file__).resolve().parent.parent/'workspace'
sys.path.insert(0,str(W))
import sympy as sp
spec=importlib.util.spec_from_file_location('generator',W/'17592186119854.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
source=json.loads((W.parent/'source/source.json').read_text())['material']['kp']
records=[];rows=[];coverage={};replays=[]
def save(name,data): (E/name).write_text(json.dumps(data,indent=2,default=str)+'\n')
def vectors(q):
 blocks=re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',q[':question/problem'],re.S)
 vs=[sp.Matrix([sp.Rational(v.strip()) for v in block.split(r'\\')]) for block in blocks]
 assert len(vs)==4 and all(v.shape==(3,1) for v in vs)
 return sp.Matrix.hstack(*vs[:3]),vs[3]
def answer(q):
 f=q[':question/answer-fields'][0];key=f[':answer-field/correct'];aid=key[1] if isinstance(key,list) else key[':answer/id']
 return next(a for a in f[':answer-field/choices'] if a[':answer/id']==aid)
def weights(q):
 target=q[':question/problem'].split('then what is')[1].replace('{','').replace('}','')
 # Read the visible target, rather than relying on the profile metadata.
 terms=re.findall(r'([+-]?)\s*x_\{?([123])\}?',target)
 assert len(terms)==3, target
 return sp.Matrix([-1 if sign=='-' else 1 for sign,_ in terms])
def expected(q):
 A,b=vectors(q)
 return 'No solution' if A.rank()<A.row_join(b).rank() else str((A.inv()*b).dot(weights(q)))
def numeric_rank(q):
 a=answer(q);ns=sorted(sp.Rational(x[':answer/value']) for x in q[':question/answer-fields'][0][':answer-field/choices'] if x[':answer/type']==':answer.type/math')
 return ns.index(sp.Rational(a[':answer/value']))+1

def rational(v):
 v=re.sub(r'\\(?:d?frac)\{([^{}]+)\}\{([^{}]+)\}',r'(\1)/(\2)',v.strip())
 return sp.Rational(sp.sympify(v))
def check(r,label):
 q=r['question'];A,b=vectors(q);want=expected(q);s=q[':question/worked-solution']
 if q[':question/answer-fields']:
  f=q[':question/answer-fields'][0];assert len(f[':answer-field/choices'])==5
  assert answer(q)[':answer/value']==want,(label,want,answer(q))
  assert len({(a[':answer/type'],a[':answer/value']) for a in f[':answer-field/choices']})==5
 if want!='No solution':
  x=A.inv()*b
  for i,v in enumerate(x):assert f'$x_{i+1}={sp.latex(v)}$' in s,(label,x)
  assert '='+want+'.' in s.split('Consequently,')[-1],(label,want)
 else:assert 'system has no solution' in s
 mats=re.findall(r'\\begin\{array\}\{ccc\|c\}(.*?)\\end\{array\}',s,re.S)
 assert len(mats)>=3
 for block in mats:
  m=sp.Matrix([[rational(v) for v in row.split('&')] for row in block.split(r'\\')]);assert m.rref()[0]==A.row_join(b).rref()[0],(label,m)
 records.append(r);rows.append({'label':label,'template':r['generation']['template'],'expected':want,'augmented_matrices':len(mats),'passed':True})

# Exact retained counterexample; neither record may conceal an incorrect key.
pair=[g.generate('moderate',613,template='q-73992',parameters={'b':b}) for b in [[5,15,4],[7,20,5]]]
for i,r in enumerate(pair):check(r,f'latest-pair-{i}')
assert [expected(r['question']) for r in pair]==['6','7']
assert len({numeric_rank(r['question']) for r in pair})==2,'Retained smallest-number bypass survives'
save('counterexample-records.json',pair)

# Every complete current source bank, including formerly missing families.
for q in source[':knowledge-point/questions']:
 sid=q[':question/math-academy-id'];lev=q[':question/difficulty'][':db/ident'].split('/')[-1];A,b=vectors(q)
 r=g.generate(lev,901,template=sid,parameters={'b':list(map(int,b))});check(r,'source-'+sid)
 sf=q[':question/answer-fields'][0];rf=r['question'][':question/answer-fields'][0]
 source_bank=sorted((a[':answer/type'][':db/ident'],a[':answer/value']) for a in sf[':answer-field/choices'])
 generated_bank=sorted((a[':answer/type'],a[':answer/value']) for a in rf[':answer-field/choices'])
 assert source_bank==generated_bank,(sid,source_bank,generated_bank)
 assert sf[':answer-field/correct'][':answer/value']==answer(r['question'])[':answer/value']==expected(q)
 replays.append({'template':sid,'source_id':q[':question/id'],'choices_matched':5,'bank_match':True,'answer':expected(q)})
# Canonical is a worked-example replay only, with no invented answer bank.
q=source[':knowledge-point/canonical-example'];A,b=vectors(q)
r=g.generate('moderate',901,template='e-6191',parameters={'b':list(map(int,b))});check(r,'canonical')
assert r['question'][':question/answer-fields']==[] and expected(r['question'])=='-2'
save('canonical-replay.json',r)
save('source-replay.json',{'complete_banks':len(replays),'matched_choices':sum(x['choices_matched'] for x in replays),'cases':replays,'canonical_answer':'-2','canonical_answer_bank':'absent, preserved'})

# Every eligible anchor with fixed mathematics, then fresh sampling per matrix.
fresh=[];controlled=[]
for q in source[':knowledge-point/questions']:
 sid=q[':question/math-academy-id'];lev=q[':question/difficulty'][':db/ident'].split('/')[-1]
 if lev!='moderate':continue
 A,_=vectors(q);b=list(map(int,A*sp.Matrix([1,2,3])))
 n=sum(a[':answer/type'][':db/ident']==':answer.type/math' for a in q[':question/answer-fields'][0][':answer-field/choices'])
 cr=[]
 for rank in range(1,n+1):
  r=g.generate('moderate',612,template=sid,parameters={'b':b,'numeric_rank':rank});check(r,f'anchor-{sid}-{rank}');cr.append(r);controlled.append(r)
 assert {numeric_rank(r['question']) for r in cr}==set(range(1,n+1))
 assert len({expected(r['question']) for r in cr})==1
 assert len({r['question'][':question/problem'] for r in cr})==1
 assert len({r['question'][':question/worked-solution'] for r in cr})==1
 assert len({r['question'][':question/id'] for r in cr})==n
 rs=[g.generate('moderate',seed,template=sid) for seed in range(260,268)]
 for i,r in enumerate(rs):check(r,f'fresh-{sid}-{i}')
 fresh.extend(rs);ranks=Counter(numeric_rank(r['question']) for r in rs);positions=Counter(next(i for i,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/id']==answer(r['question'])[':answer/id'])+1 for r in rs)
 assert len(ranks)>1,(sid,'fixed rank',ranks)
 assert len(positions)>1,(sid,'fixed position',positions)
 coverage[sid]={'fresh':len(rs),'semantic_instances':len({r['question'][':question/problem'] for r in rs}),'ranks':dict(ranks),'positions':dict(positions),'controlled_ranks':list(range(1,n+1)),'best_fixed_rank_success':max(ranks.values()),'best_fixed_position_success':max(positions.values()),'numeric_rank_baseline':1/n,'position_baseline':.2}

# Signed/zero boundaries in restored families and the retained subtraction case.
for sid in ['q-34243','q-74043','q-74028']:
 A,_=vectors(next(q for q in source[':knowledge-point/questions'] if q[':question/math-academy-id']==sid))
 for x in [[-7,7,-7],[0,0,0],[7,-7,7]]:
  check(g.generate('moderate',49,template=sid,parameters={'b':list(map(int,A*sp.Matrix(x)))}),f'boundary-{sid}-{x}')
# Relevant and target-preserving counterfactuals from independent witness triples.
sid='q-73992';A,_=vectors(next(q for q in source[':knowledge-point/questions'] if q[':question/math-academy-id']==sid))
pairs=[g.generate('moderate',613,template=sid,parameters={'b':list(map(int,A*sp.Matrix(x)))}) for x in [[1,2,3],[1,2,4],[2,1,3]]]
for i,r in enumerate(pairs):check(r,f'counterfactual-{i}')
assert [expected(r['question']) for r in pairs]==['6','7','6']
assert len({r['question'][':question/problem'] for r in pairs})==3
assert len({r['question'][':question/worked-solution'] for r in pairs})==3
save('counterfactual-records.json',pairs)
save('fresh-moderate.json',fresh);save('controlled-bank-records.json',controlled)
save('math-results.json',{'checks':len(rows),'failures':[],'cases':rows})
save('coverage-before.json',coverage)
cases=[]
for i,r in enumerate(records):
 if not r['question'][':question/answer-fields']:continue
 q=r['question'];want=expected(q)
 cases.append({'label':str(i)+'-'+r['generation']['template'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==want else 'rejected','purpose':'Independent exact solver reads displayed vectors and target; test every selectable choice.'} for a in q[':question/answer-fields'][0][':answer-field/choices']]})
save('grader-input.json',cases)
batch_profiles={r['generation']['template'] for seed in range(5) for r in g.batch('moderate',5,seed)}
assert len(batch_profiles)==8,'Normal five-record CLI batches omit supported matrix profiles'
save('regression-results.json',{'status':'passed','finding_ids':['2197e08f74d72428c019','c9f6edae44c110e17773'],'latest_pair_ranks':[numeric_rank(r['question']) for r in pair],'source_banks':len(replays),'matched_choices':5*len(replays),'fresh_moderate':len(fresh),'controlled_bank_cases':len(controlled),'math_checks':len(rows),'native_grader_cases_prepared':len(cases)})
print(json.dumps(json.loads((E/'regression-results.json').read_text())))
