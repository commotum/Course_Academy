"""Parent independently reads ambient selection, complete equations and shared stages."""
import importlib.util,json,re,hashlib
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=17592186078583;D=P.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('root_cooling_scalar',P/'ode-scalar-parser.py');g=module('root_cooling_model',D.with_suffix('.py'));T,k=p.x,p.k
TEMP=re.compile(r'\{?(\d+)\}?\^\{(?:∘|\\circ)\}(?:\\text\{([CF])\}|([CF]))')
C=dict(instances=0,choices=0,formal_newton_stages=0,substituted_stages=0,ambient_prose=0,source_banks=0,source_values=0,source_prompts=0,source_keys=0,source_missing_keys=0,source_full_solutions=0,raw_duplicate_wrong_pairs=0)
def rhs(raw,ambient=None):
 raw=raw.split('=',1)[-1].strip().rstrip('.,').replace('T(t)','T')
 if ambient is not None:raw=raw.replace(r'{T}_{S}',str(ambient))
 raw=re.sub(r'\\[A-Za-z]+|T',lambda m:'x' if m[0]=='T' else m[0],raw)
 return s.expand(p.scalar(raw))
def check(r):
 q=r['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];level=q[':question/difficulty'].split('/')[-1]
 temperatures=[(int(m[1]),m[2] or m[3],m.start()) for m in TEMP.finditer(prompt)];assert len(temperatures)=={'easy':1,'moderate':2,'hard':3}[level],prompt
 # Read the surrounding/room/kitchen role explicitly from actual prose.
 role=re.search(r'(?:temperature of the surroundings is|(?:room|kitchen) temperature is|room at)\s*\$',prompt);assert role,prompt
 m=TEMP.search(prompt,role.end());assert m and m.start()-role.end()<5;ambient=int(m[1]);unit=m[2] or m[3];assert len({u for v,u,pos in temperatures})==1
 assert ambient==min(v for v,u,pos in temperatures)
 if level!='easy':
  I=temperatures[0][0];assert I>=ambient+10
  if 'thermometer' in prompt:assert 90<=I<=110 and unit=='F'
  if 'turkey' in prompt:assert 120<=I<=180 and unit=='F'
  if 'pot of soup' in prompt:assert 140<=I<=212 and unit=='F'
  if 'straightener' in prompt:assert 200<=I<=450 and unit=='F'
  if 'water' in prompt and unit=='C':assert 40<=I<=99
 if level=='hard':
  I,S,M=[v for v,u,pos in temperatures];assert S==ambient and S+5<=M<=I-5
  time=int(re.search(r'After \$(\d+)\$ minutes?',prompt)[1]);assert 1<=time<=20
 target=s.expand(-k*(T-ambient));f=q[':question/answer-fields'][0];vs=[rhs(z[':answer/value']) for z in f[':answer-field/choices']];assert len(vs)==5
 assert [z[':answer/id'] for z,v in zip(f[':answer-field/choices'],vs) if s.expand(v-target)==0]==[f[':answer-field/correct'][1]]
 pairs=sum(s.expand(v-w)==0 for i,v in enumerate(vs) for w in vs[:i]);raw=r['generation']['bank_profile']=='q-106936';assert pairs==int(raw);C['raw_duplicate_wrong_pairs']+=pairs
 blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);assert len(blocks)==2
 assert r'{T}_{S}' in blocks[0] and rhs(blocks[0],ambient)==target;assert rhs(blocks[1])==target;C['formal_newton_stages']+=1;C['substituted_stages']+=1
 given=re.search(r'\$\{T\}_\{S\}=(.*?)\$',sol)[1];m=TEMP.search(given);assert m and int(m[1])==ambient and (m[2] or m[3])==unit;C['ambient_prose']+=1
 if not r['generation']['bank_profile'] in g.TEMPLATES:
  assert 'in terms of the given constant $k$' in prompt
  expected={target,k*(T-ambient),-k*(T+ambient),-k*T*(T-ambient),-k*T} if level=='easy' else {target,-k*(T-I),-I*k*(T-ambient),-k*(T-I-ambient),k*(T-ambient)} if level=='moderate' else {target,-k*(T-I),-k*(T-M),-k*(T-I+ambient),k*(T-ambient)}
  if r['generation']['bank_profile']=='oil_repaired':expected={target,k*(T-ambient),-k*T*(T-ambient),-k*T,-k*(T+ambient)}
  assert set(vs)==set(map(s.expand,expected))
 C['choices']+=5;C['instances']+=1;return q
sources={q[':question/math-academy-id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 q=check(g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']));old=sources[case['source_id']];assert q[':question/problem']==old[':question/problem'];C['source_prompts']+=1
 f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0];unused=list(range(5));vs=[rhs(z[':answer/value']) for z in f[':answer-field/choices']]
 for choice in of[':answer-field/choices']:
  matches=[i for i in unused if s.expand(vs[i]-rhs(choice[':answer/value']))==0];assert matches;unused.remove(matches[0]);C['source_values']+=1
 assert not unused;C['source_banks']+=1
 if of.get(':answer-field/correct'):assert rhs(of[':answer-field/correct'][':answer/value'])==next(v for z,v in zip(f[':answer-field/choices'],vs) if z[':answer/id']==f[':answer-field/correct'][1]);C['source_keys']+=1
 else:C['source_missing_keys']+=1
 if old.get(':question/worked-solution'):assert q[':question/worked-solution']==old[':question/worked-solution'];C['source_full_solutions']+=1
 for seed in range(24):check(g.generate(case['level'],seed+64,template=case['template'],profile=case['bank_profile']))
for r in json.loads((P/'qa'/f'{K}-sampled.json').read_text()):check(r)
for level in ('easy','moderate','hard'):
 for seed in range(60):check(g.generate(level,seed))
C['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
