"""Root independent affine-equation classification, reduction and whole subset banks."""
import sys,json,re,hashlib,importlib.util,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186204089;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_ns_gen',D.with_suffix('.py'));P=load('root_ns_math',R/'ode-scalar-parser.py');x=P.x
N=dict(records=0,equations=0,reduction_rows=0,classification_claims=0,banks=0,values=0,checkbox_keys=0,radio_keys=0,radio_targets={},controlled_targets=0)
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']};fidelity=dict(prompts=0,solutions=0,fields=0,values=0,refs=0,unrated=0)
for tid,old in olds.items():
 assert G.replay_source(tid)==old;fidelity['prompts']+=1;fidelity['solutions']+=(':question/worked-solution' in old);fidelity['unrated']+=(':question/difficulty' not in old)
 for f in old[':question/answer-fields']:fidelity['fields']+=1;fidelity['values']+=len(f[':answer-field/choices']);fidelity['refs']+=(':answer-field/correct' in f)
def scalar(raw,variable):
 text=raw.strip().rstrip('.').replace('&','').replace(' ','');assert not re.search(r'[^0-9xuyzwv+*/(){}\\a-z\-]',text)
 # Source fields contain only affine integer math and scalar rational solutions.
 text=text.replace(variable,'x');value=P.scalar(text);assert value.free_symbols<={x} and s.Poly(value,x).degree()<=1;return value
def equation(raw,variable):
 parts=raw.replace('&','').strip().rstrip('.').split('=');assert len(parts)==2;return tuple(scalar(z,variable) for z in parts)
def eq(a,b):return s.expand(a-b)==0
def subset(text):
 z={0 if v=='I' else 1 if v=='II' else 2 for v in re.findall(r'\bIII\b|\bII\b|\bI\b',text)};assert z and re.sub(r'\bIII\b|\bII\b|\bI\b|only|and|[,\s]','',text)=='';return z
def check(r):
 q,m=r['question'],r['generation'];prompt=q[':question/problem'];raw=re.findall(r'\$([^$]*=[^$]*)\$',prompt);assert len(raw)==3;labels=re.findall(r'(?:^|\n)(?:- \*\*)?(III|II|I)\.',prompt);assert labels==['I','II','III'];variable=re.search(r'[xuyzwv]',raw[0])[0];pairs=[equation(z,variable) for z in raw]
 states=[];solutions=[]
 for lhs,rhs in pairs:
  delta=s.expand(lhs-rhs);coef=delta.coeff(x);constant=delta.subs(x,0);state='U' if coef!=0 else 'I' if constant==0 else 'N';states.append(state);solutions.append(-constant/coef if coef!=0 else None);N['equations']+=1
 assert variable==m['parameters']['variable'];none={i for i,z in enumerate(states) if z=='N'};assert none
 field=q[':question/answer-fields'][0];radio=field[':answer-field/type'].endswith('/radio');sol=q[':question/worked-solution']
 if m['template']=='summary-spaced':
  reduction=sol.split('respectively to ',1)[1].split('. Only',1)[0];items=reduction.replace('$','').replace(', and ', ', ').split(', ');assert len(items)==3
  for i,z in enumerate(items):
   if states[i]=='I':assert z=='an identity'
   else:
    lhs,rhs=equation(z,variable)
    if states[i]=='N':assert lhs==pairs[i][0].subs(x,0) and rhs==pairs[i][1].subs(x,0)
    else:assert lhs==x and eq(rhs,solutions[i])
   N['reduction_rows']+=1
  assert sol.endswith('Only the '+('first','second','third')[next(iter(none))]+' has no solutions.')
 else:
  blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(blocks)==3
  for i,block in enumerate(blocks):
   lhs,rhs=pairs[i];a,b,c,d=lhs.coeff(x),lhs.subs(x,0),rhs.coeff(x),rhs.subs(x,0)
   wanted=[(lhs,rhs)]
   if a==c:wanted.extend([(lhs-a*x,rhs-a*x),(b,d)])
   else:
    wanted.append((lhs-c*x-b,rhs-c*x-b))
    if a-c!=1:wanted.append(((a-c)*x,d-b))
    wanted.append((x,solutions[i]))
   actual=[equation(row,variable) for row in block.split(r'\\')];assert len(actual)==len(wanted) and all(eq(z,w) for pair,target in zip(actual,wanted) for z,w in zip(pair,target));N['reduction_rows']+=len(actual)
  footer=re.search(r'Therefore, the correct answer is "(.*?)\."$',sol);assert footer and subset(footer[1])==none
  claims=re.findall(r'Therefore, the equation \$([^$]*=[^$]*)\$ (has no solutions|has the unique solution \$([^$]*)\$)',sol);wanted=[i for i,z in enumerate(states) if z!='I'];assert len(claims)==len(wanted)
  for claim,i in zip(claims,wanted):
   assert all(eq(z,w) for z,w in zip(equation(claim[0],variable),pairs[i]))
   if states[i]=='N':assert claim[1]=='has no solutions'
   else:
    lhs,rhs=equation(claim[2],variable);assert lhs==x and eq(rhs,solutions[i])
   N['classification_claims']+=1
 if radio:
  assert len(q[':question/answer-fields'])==1;choices=field[':answer-field/choices'];sets=[subset(z[':answer/value']) for z in choices];assert len(sets)==5 and len({tuple(sorted(z)) for z in sets})==5
  assert sum(z==none for z in sets)==1 and next(z for z,a in zip(sets,choices) if a[':answer/id']==field[':answer-field/correct'][1])==none
  order=m['parameters']['label_permutation'];assert sorted(order)==[0,1,2] and states==[('N','U','I')[i] for i in order]
  source_sets=({0},{0,2},{0,1},{0,1,2},{1,2});expected=[{new for new,old in enumerate(order) if old in oldset} for oldset in source_sets];assert sets==expected
  key=''.join('I'*(i+1) for i in sorted(none));N['radio_targets'][key]=N['radio_targets'].get(key,0)+1;N['radio_keys']+=1;N['values']+=5;N['banks']+=1
 else:
  assert 'Select all that apply.' in prompt and [f[':answer-field/key'] for f in q[':question/answer-fields']]==['I','II','III']
  for i,f in enumerate(q[':question/answer-fields']):
   assert f[':answer-field/type'].endswith('/checkbox');choices=f[':answer-field/choices'];assert [z[':answer/value'] for z in choices]==['false','true'];correct=next(z[':answer/value'] for z in choices if z[':answer/id']==f[':answer-field/correct'][1]);assert correct==('true' if i in none else 'false');N['checkbox_keys']+=1;N['values']+=2;N['banks']+=1
 N['records']+=1
for r in json.load(open(R/f'qa/{K}-sampled.json')):check(r)
for level in G.SUPPORTED_LEVELS:
 for template in G.TEMPLATES:
  for p in G.CATALOG[level][template]:check(G.generate(level,template=template,parameters=p))
for case in G.SOURCE_CASES:check(G.generate('easy',template=case['template'],parameters=case['parameters'],profile=case['bank_profile']))
for r in json.load(open(D/'target-change-review.json')):
 # Review may include provenance alongside each generated record.
 check(r.get('record',r));N['controlled_targets']+=1
result=dict(status='passed',source=fidelity,readback=N,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
