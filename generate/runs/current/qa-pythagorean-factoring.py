"""Root independent full trig-polynomial banks and ordered solution readback."""
import importlib.util,json,re,sys,hashlib,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;D=R.parents[2]/'generate/scratch/17592186059641'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'pythagorean-readback.py','p');g=load(D.with_suffix('.py'),'g')
n=dict(records=0,choices=0,whole_banks=0,printed_equalities=0,known_raw_errors=0,source_prompts=0,source_solutions=0,source_values=0,source_designations=0)
def scalar(t):return p.scalar(t.strip().rstrip('.,').replace(r'\alpha','t'))
def chain(text,truth,raw_error=False):
 text=text.replace(r'\begin{aligned}','').replace(r'\end{aligned}','');last=None
 for row in text.split(r'\\'):
  parts=row.replace('&','').strip().split('=')
  for part in parts:
   if not part.strip():continue
   v=scalar(part)
   if last is not None:
    if raw_error and not p.equal(v,last):n['known_raw_errors']+=1
    else:assert p.equal(v,last),(row,v,last);n['printed_equalities']+=1
   last=v
  assert p.equal(last,truth) or raw_error,(row,last,truth)
def check(r):
 q=r['question'];m=r['generation'];assert m['eligible_for_learning']==(not m['evidence_only']);prompt=q[':question/problem'];expr=re.search(r'\$(.*?)\$',prompt,re.S)[1].rstrip('.');truth=scalar(expr)
 f=q[':question/answer-fields'][0];values=[scalar(a[':answer/value']) for a in f[':answer-field/choices']];assert all(not p.equal(a,b) for i,a in enumerate(values) for b in values[:i]);matches=[i for i,v in enumerate(values) if p.equal(v,truth)];assert len(matches)==1
 if ':answer-field/correct' in f:assert f[':answer-field/choices'][matches[0]][':answer/id']==f[':answer-field/correct'][1]
 if m.get('profile')=='authored_operations':
  z=m['parameters'];F=z['a']*p.S**z['p']*p.C**z['q'];level=q[':question/difficulty'].split('/')[-1]
  if level=='easy':expected=[F,2*F,-F,F*(p.S**2+p.C**2-1),F*(p.S**2-p.C**2)]
  elif level=='hard':
   G=z['b']*p.C**z['n'];expected=[F+G,F-G,-F+G,F*(p.S**2-p.C**2)+G,F+G*(p.S**2-p.C**2)]
  else:
   u,v=(z['q'],z['p']) if z['family']!='same' else (z['p'],z['q']);T=z['b']*p.S**u*p.C**v
   expected=[F+T,F-T,-F+T,F*(p.S**2-p.C**2)+T,2*F+T] if z['family']=='opposite' else [F+T,F-T,-F-T,F*(p.S**2-p.C**2)+T,F+2*T] if z['family']=='same' else [z['a'],2*z['a'],-z['a'],0,F-T]
  if f[':answer-field/type'].endswith('blank'):expected=expected[:1]
  assert len(values)==len(expected) and all(sum(p.equal(v,e) for v in values)==1 for e in expected),'Complete operation bank differs'
 n['choices']+=len(values);n['whole_banks']+=1
 sol=q.get(':question/worked-solution');sid=m.get('source_ids',[''])[0]
 if sol:
  blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks)==3;assert 'factor' in sol and 'conclude that' in sol
  for j,b in enumerate(blocks):
   if m['evidence_only'] and sid=='q-65229' and j==1:
    assert '{cos}^{2})' in b;n['known_raw_errors']+=1;continue
   chain(b,truth,m['evidence_only'] and sid=='q-119362' and j==1)
  for inline in re.findall(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',re.sub(r'\$\$.*?\$\$','',sol,flags=re.S),re.S):
   if '=' in inline:
    a,b=inline.split('=');assert p.equal(scalar(a),scalar(b));n['printed_equalities']+=1
  if m.get('template') in ('authored_easy','authored_moderate','authored_hard') or m.get('bank_profile')=='authored':
   assert r'\cdot 1' in sol
 n['records']+=1
if __name__=='__main__':
 old={q[':question/math-academy-id']:q for q in json.load(open(D/'source.json'))['record'][':knowledge-point/questions']}
 assert json.load(open(D/'source.json'))==json.load(open(R/'sources/17592186059641.json'))
 for c in json.load(open(D/'source-cases.json')):
  r=g.generate(c['level'],template=c['template'],profile=c['bank_profile'],parameters=c['parameters']);o=old[c['source_id']];q=r['question'];check(r)
  for k in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (k in q)==(k in o)
   if k in o:assert q[k]==(o[k][':db/ident'] if k.endswith('difficulty') else o[k])
  n['source_prompts']+=1;n['source_solutions']+=int(':question/worked-solution' in o)
  of=o[':question/answer-fields'][0];gf=q[':question/answer-fields'][0];assert sorted(a[':answer/value'] for a in of[':answer-field/choices'])==sorted(a[':answer/value'] for a in gf[':answer-field/choices']);n['source_values']+=5
  assert (':answer-field/correct' in of)==(':answer-field/correct' in gf)
  if ':answer-field/correct' in of:
   ov=next(a[':answer/value'] for a in of[':answer-field/choices'] if a[':answer/id']==of[':answer-field/correct'][':answer/id']);gv=next(a[':answer/value'] for a in gf[':answer-field/choices'] if a[':answer/id']==gf[':answer-field/correct'][1]);assert ov==gv;n['source_designations']+=1
  for swap in (False,True):check(g.generate(c['level'],template=c['template'],profile='repaired:'+c['source_id'],parameters={'angle':r'\alpha','swap':swap}))
 for level in ('easy','moderate','hard'):
  for seed in range(35):
   r=g.generate(level,seed=14000+seed);check(r);z=g.generate(level,seed=15000+seed,parameters=r['generation']['parameters']);assert r['question'][':question/id']==z['question'][':question/id'];check(g.generate(level,seed=14000+seed,parameters=r['generation']['parameters'],field_type='blank'))
 for r in json.load(open(D/'review.json')):check(r.get('record',r))
 for file,digest in json.load(open(D/'hashes.json')).items():assert hashlib.sha256((R.parents[2]/file).read_bytes()).hexdigest()==digest
 (R/'qa/17592186059641-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
