"""Root actual substitutions, differential factorizations, source masks and banks."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
import sympy as s
from functools import lru_cache
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186184351;D=R.parents[2]/f'generate/scratch/{K}'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_complex_gen',D.with_suffix('.py'));P=load('root_complex_math',R/'elementary-integral-readback.py');x,u=P.x,P.u
N=dict(records=0,substitutions=0,differential_equalities=0,differential_relations=0,integral_sides=0,primitive_sides=0,formal_inputs=0,values=0,pairs=0,banks=0,negative_branches=0)
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']};fidelity=dict(prompts=0,solutions=0,banks=0,values=0,existing_keys=0,unrated=0)
@lru_cache(maxsize=30000)
def eq(a,b,U,var):
 d=s.expand(a-b)
 if d==0:return True
 E=[e for e in s.preorder_traversal(U)if e.func==s.exp or e.is_Pow and e.exp.has(var)and not e.base.has(var)]
 if E:
  rest=s.simplify(U-E[0])
  if not rest.has(var):
   positive=s.Symbol('root_positive_inner',positive=True);d=d.subs(E[0],positive-rest);d=s.powdenest(d,force=True)
  elif U.subs(var,0)==1:
   jet=d
   for _ in range(3):
    witness=s.simplify(jet.subs(var,0))
    if witness.is_zero is False:return False
    jet=P.derivative(jet,var)
 return s.simplify(d)==0
for case in json.load(open(D/'source-cases.json')):
 old=olds[case['source_id']];r=G.generate(case['level'],template=case['template'],profile=case['profile'],parameters=case['parameters']);q=r['question']
 assert q[':question/problem']==G.mf.normalize_prose(old[':question/problem']);fidelity['prompts']+=1
 for attr in (':question/difficulty',':question/worked-solution'):
  assert(attr in q)==(attr in old)
 if ':question/worked-solution'in old:assert q[':question/worked-solution']==G.mf.normalize_prose(old[':question/worked-solution']);fidelity['solutions']+=1
 else:fidelity['unrated']+=1
 for f,o in zip(q[':question/answer-fields'],old[':question/answer-fields']):
  assert sorted(a[':answer/value']for a in f[':answer-field/choices'])==sorted(G.mf.normalize_tex(a[':answer/value'])for a in o[':answer-field/choices']);assert f[':answer-field/key']==o[':answer-field/key'];assert(':answer-field/correct'in f)==(':answer-field/correct'in o)
  if ':answer-field/correct'in o:assert next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])==G.mf.normalize_tex(o[':answer-field/correct'][':answer/value']);fidelity['existing_keys']+=1
  fidelity['banks']+=1;fidelity['values']+=len(f[':answer-field/choices'])
def check(r):
 q,m=r['question'],r['generation'];F,var=P.prompt(q[':question/problem']);sol=q[':question/worked-solution'];defs=re.findall(r'\$u=([^$]+)\$',sol);assert defs;U=P.scalar(defs[0]);assert var in U.free_symbols
 for raw in defs:assert eq(P.scalar(raw),U,U,var);N['substitutions']+=1
 derivative=s.diff(U,var);block=next(b for b in re.findall(r'\$\$(.*?)\$\$',sol,re.S)if '⟹'in b);a,b=block.split('⟹');a=re.sub(r'\\(?:begin|end)\{aligned\}','',a).replace('&','').strip();parts=a.split('=');label=parts.pop(0).strip();assert re.fullmatch(r'\\frac\{\\text\{d\}u\}\{\\text\{d\}'+str(var)+r'\}',label),label
 for raw in parts:assert eq(P.scalar(raw),derivative,U,var);N['differential_equalities']+=1
 b=re.sub(r'\\(?:begin|end)\{aligned\}','',b).replace('&','').strip();dm=re.fullmatch(r'(.*?)'+P.DIFF+r'\s*=\s*(.*?)'+P.DIFF+r'\s*[.,]?',b,re.S);assert dm and dm[2]=='u'and dm[4]==str(var),b
 coeff=lambda raw:s.Integer(1)if not P.clean(raw).strip()else P.scalar(raw)
 assert eq(coeff(dm[1])*derivative,coeff(dm[3]),U,var);N['differential_relations']+=1
 for block in re.findall(r'\$\$(.*?)\$\$',sol,re.S):
  if r'\int'not in block:continue
  text=re.sub(r'\\(?:begin|end)\{aligned\}','',block).replace('&','')
  for row in text.split(r'\\'):
   for raw in row.split('='):
    if not raw.strip():continue
    value,inputs=P.side(raw,var,U);assert eq(value,F,U,var),('bad printed integral/primitive',m['template'],m['parameters'],raw,value,F);N['integral_sides'if inputs else'primitive_sides']+=1;N['formal_inputs']+=len(inputs)
 assert len(q[':question/answer-fields'])==1;f=q[':question/answer-fields'][0];assert f[':answer-field/type'].endswith('/radio')and len(f[':answer-field/choices'])==5
 values=[P.derivative(P.scalar(a[':answer/value']),var)for a in f[':answer-field/choices']];hits=[a[':answer/id']for a,v in zip(f[':answer-field/choices'],values)if eq(v,F,U,var)];assert hits==[f[':answer-field/correct'][1]],(m['template'],m['parameters'],hits)
 for i,v in enumerate(values):
  for w in values[:i]:assert not eq(v,w,U,var),('primitive-family collision',m['template'],m['parameters']);N['pairs']+=1
 if m['template']=='derivative_ratio'and U.subs(var,1)<0:
  canonical=next(v for a,v in zip(f[':answer-field/choices'],values)if a[':answer/id']==f[':answer-field/correct'][1]);assert s.simplify((canonical-F).subs(var,1))==0;N['negative_branches']+=1
 N['records']+=1;N['values']+=len(values);N['banks']+=1
if '--supplement-empirical' in sys.argv:
 prior=json.load(open(R/f'qa/{K}-root-readback.json'));assert prior['status']=='passed'and prior['script_sha256']==hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest();N.update(prior['readback'])
 seen={r['question'][':question/id']for r in json.load(open(D/'bounded-records.json'))}
 extras=[e['record']for e in json.load(open(D/'native-input.json'))if e['record']['question'][':question/id']not in seen]
 assert len(extras)==134
 for i,r in enumerate(extras):
  check(r)
  if i%30==0:print('Root empirical variants read',i,flush=True)
else:
 for name,sid in G.TEMPLATES.items():
  check(G.generate(G.DIFFICULTY[sid],template=name,parameters=G.ANCHORS[sid]));print('Root preflight passed',name,flush=True)
 for i,r in enumerate(json.load(open(D/'bounded-records.json'))):
  check(r)
  if i%100==0:print('Root complex records read',i,flush=True)
 for level in G.LEVELS:
  for seed in range(18):check(G.generate(level,seed))
result=dict(status='passed',source=fidelity,readback=N,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
