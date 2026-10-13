"""Root reads actual function roles and compares complete universal relations."""
import importlib.util,json,re
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186064272;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_relationship_scalar',R/'ode-scalar-parser.py');g=module('root_relationship_generator',D.with_suffix('.py'));s=p.s
C=dict(instances=0,complete_equations=0,source_questions=0,source_values=0,source_banks=0,source_existing_refs=0,source_missing_refs=0,source_fieldless=0,source_exact_prompts=0,source_normalized_solutions=0,formal_direction_checks=0)
def roles(prompt):
 declarations=re.findall(r'^- \$([A-Za-z])\(([a-z])\)\$\s*-?\s*(.*)$',prompt,re.M);assert len(declarations) in (2,3),prompt
 T=declarations[0][1];assert all(z[1]==T for z in declarations);Q=declarations[0][0]
 if len(declarations)==2:
  R=declarations[1][0];desc=declarations[1][2];loss='decreasing' in desc;assert loss or 'increas' in desc
  return T,{Q:p.x,Q+"'":p.y,R:p.z,R+"'":p.t},-p.z if loss else p.z,'loss' if loss else 'growth'
 I,L=declarations[1][0],declarations[2][0];signed='signed contribution' in declarations[2][2]
 if signed:assert f'${L}({T})<0$' in prompt
 return T,{Q:p.x,Q+"'":p.y,I:p.u,L:p.v},p.u+p.v if signed else p.u-p.v,'signed' if signed else 'net'
def scalar(raw,T,bindings):
 raw=raw.replace('′',"'");raw=re.sub(r'\{([A-Za-z])\}',r'\1',raw);raw=re.sub(r'\^\{\s*\x27\s*\}',"'",raw)
 # Source r^2(t) means the squared supplied rate, not a derivative.
 for name,value in sorted(bindings.items(),key=lambda z:-len(z[0])):
  raw=re.sub(re.escape(name)+r'\('+T+r'\)',lambda m:'('+str(value)+')',raw)
  raw=re.sub(re.escape(name)+r'\^\{2\}\('+T+r'\)',lambda m:'('+str(value)+'^2)',raw)
 return p.scalar(raw)
def relation(raw,T,bindings):
 parts=raw.strip().rstrip('.,').split('=');assert len(parts)==2;return scalar(parts[0],T,bindings)-scalar(parts[1],T,bindings)
structures=set()
def check(r):
 q=r['question'];prompt=q[':question/problem'];T,bindings,want,kind=roles(prompt);structures.add(kind);f=q[':question/answer-fields'][0]
 residuals=[relation(z[':answer/value'],T,bindings) for z in f[':answer-field/choices']];assert len(residuals)==5
 good=[s.cancel(z.subs(p.y,want))==0 for z in residuals];assert sum(good)==1 and good[next(n for n,z in enumerate(f[':answer-field/choices']) if z[':answer/id']==f[':answer-field/correct'][1])]
 for n,a in enumerate(residuals):
  for b in residuals[:n]:assert s.cancel(a/b).free_symbols or s.cancel(a/b)==0
 worked=q[':question/worked-solution'];assert g.CLARIFIER in worked
 Q=next(name for name,z in bindings.items() if z==p.x)
 worked=worked.replace(r'\dfrac',r'\frac').replace(r'\textrm',r'\text')
 formal=re.findall(r'\\frac\{\\text\{d\}([A-Za-z])\(([a-z])\)\}\{\\text\{d\}([a-z])\}',worked);assert formal==[(Q,T,T)],(worked,formal)
 changes=re.findall(r'\\frac\{\\text\{Change in(?: |\xa0)\}([A-Za-z])\}\{\\text\{Change in(?: |\xa0)\}([a-z])\}',worked);assert changes==[(Q,T)]
 C['formal_direction_checks']+=2
 # Read every final relation actually printed in either inline or display math.
 found=[]
 for pair in re.findall(r'\$\$([\s\S]*?)\$\$|\$([^$]*)\$',worked):
  body=pair[0] or pair[1]
  if '=' not in body or r'\frac' in body:continue
  if re.search(r"\^\{′\}|'",body):found.append(relation(body,T,bindings))
 assert found and all(s.cancel(z.subs(p.y,want))==0 for z in found),(found,worked)
 if q[':question/difficulty'].endswith('/hard'):assert kind=='signed'
 C['instances']+=1;C['complete_equations']+=len(residuals)+len(found);return q
sources={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for c in json.loads((D/'source-cases.json').read_text()):
 old=sources[c['source_id']];q=check(g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']));assert q[':question/problem']==old[':question/problem'];C['source_exact_prompts']+=1
 if old.get(':question/worked-solution'):
  raw=old[':question/worked-solution']
  if c['source_id']=='q-112519':raw=raw.replace('inside the park $t$ minutes','inside the playground $t$ hours')
  if c['source_id']=='q-72105':raw=raw.replace('after $t$ hours','after $t$ minutes')
  assert q[':question/worked-solution']==raw+'\n\n'+g.CLARIFIER;C['source_normalized_solutions']+=1
 if not old.get(':question/answer-fields'):C['source_fieldless']+=1;C['source_missing_refs']+=1
 for of,nf in zip(old.get(':question/answer-fields',[]),q[':question/answer-fields']):
  assert sorted(z[':answer/value'] for z in of[':answer-field/choices'])==sorted(z[':answer/value'] for z in nf[':answer-field/choices']);C['source_values']+=len(of[':answer-field/choices']);C['source_banks']+=1
  if of.get(':answer-field/correct'):
   actual=next(z[':answer/value'] for z in nf[':answer-field/choices'] if z[':answer/id']==nf[':answer-field/correct'][1]);assert actual==of[':answer-field/correct'][':answer/value'];C['source_existing_refs']+=1
  else:C['source_missing_refs']+=1
 C['source_questions']+=1
for r in json.loads((D/'review.json').read_text()):check(r.get('record',r))
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
C['finite_universal_relationship_structures']=sorted(structures);C['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
