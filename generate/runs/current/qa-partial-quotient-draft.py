import sys
sys.dont_write_bytecode=True
import re,json,hashlib,copy,importlib.util
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186124643;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=load('parent_quotient_scalar',R/'partial-quotient-scalar.py');s=p.s;x,y,h=p.x,p.y,p.h
counts={'records':0,'choices':0,'solution_blocks':0,'source_banks':0,'source_values':0,'source_keys':0,'source_missing_keys':0,'source_solutions':0,'authored_hard_banks':0}
def balanced(text,start):
 opening=text[start];assert opening in '({'
 closing=')' if opening=='(' else '}';depth=1;i=start+1
 while depth:
  assert i<len(text)
  if text[i]==opening:depth+=1
  elif text[i]==closing:depth-=1
  i+=1
 return text[start+1:i-1],i
def math(text,F=None):
 text=text.strip().rstrip('.,').replace(r'\left','').replace(r'\right','').replace('⁡','')
 while (m:=re.search(r'\\sqrt\[3\]',text)):
  start=m.end();inside,end=balanced(text,start);text=text[:m.start()]+'(('+inside+')^{'+r'\frac{1}{3}'+'})'+text[end:]
 if F is not None:
  while (m:=re.search(r'(?<![A-Za-z])f\(',text)):
   inside,end=balanced(text,m.end()-1);parts=inside.split(',');assert len(parts)==2
   vals=[math(t) for t in parts];value=F.subs(dict(zip((x,y),vals)),simultaneous=True)
   text=text[:m.start()]+'('+s.latex(value,ln_notation=True)+')'+text[end:]
 if r'\sqrt[3]' in text:return math(text)
 return p.scalar(text)
def quotient(text,F=None):
 text=text.strip().rstrip('.,').replace(r'\left','').replace(r'\right','')
 text=text.replace('{lim}',r'\lim').replace('lim_(h → 0)',r'\lim_{h\to 0}')
 m=re.match(r'\\lim_\{h\s*\\to\s*0\}',text);assert m,('Missing h→0 limit',text)
 body=text[m.end():]
 if body.startswith('['):
  assert body.endswith(']');body='('+body[1:-1]+')'
 return math(body,F)
def same(a,b):
 d=s.expand(a-b)
 if d==0:return True
 return s.simplify(s.trigsimp(d))==0
def prose(text):return re.sub(r'\$\$.*?\$\$|(?<!\$)\$(?!\$).*?(?<!\$)\$(?!\$)','[MATH]',text,flags=re.S)
def prompt(q):
 islands=re.findall(r'(?<!\$)\$(?!\$)(.*?)\$',q[':question/problem'],re.S);assert len(islands)==2
 F=math(islands[0].split('=',1)[1]);ask=islands[1];m=re.search(r'(?:∂|\\partial)\s*([xy])',ask) or re.search(r'_\{?([xy])\}?',ask);assert m
 var=getattr(p,next(z for z in m.groups() if z));point=None
 if re.search(r'f_[xy]\(',ask):
  z,_=balanced(ask,ask.index('('));parts=z.split(',');assert len(parts)==2;point=dict(zip((x,y),map(math,parts)))
 return F,var,point

def check(record):
 q=record['question'];F,var,pt=prompt(q);held=y if var==x else x;shifted=F.subs(var,var+h);expected=(shifted-F)/h
 if pt:expected=expected.subs(pt,simultaneous=True)
 f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1 and f[':answer-field/type']==':answer-field.type/radio';values=[quotient(z[':answer/value']) for z in f[':answer-field/choices']];assert len(values)==5
 for i,a in enumerate(values):assert all(not same(a,b) for b in values[:i])
 good=[same(z,expected) for z in values];assert sum(good)==1,(q[':question/problem'],values,expected)
 if ':answer-field/correct' in f:assert good[next(i for i,z in enumerate(f[':answer-field/choices']) if z[':answer/id']==f[':answer-field/correct'][1])]
 if ':question/worked-solution' in q:
  solution=q[':question/worked-solution'];blocks=re.findall(r'\$\$(.*?)\$\$',solution,re.S);assert len(blocks)==3
  first=blocks[0].split('=',1)[1].strip();final=blocks[2].split('=',1)[1].strip();assert same(quotient(first,F),expected) and same(quotient(final),expected)
  # Actual shifted function equation, plus original-point equation for authored hard.
  equations=blocks[1].split(r'\qquad');assert len(equations)==(2 if pt else 1)
  for equation in equations:
   lhs,rhs=equation.strip().rstrip('.,').split('=',1);assert same(math(lhs,F),math(rhs))
  assert '$'+str(var)+'$' in solution.split('given by the limit')[0]
  if not record['generation'].get('evidence_only'):assert r'h\ne 0' in solution and '$'+str(held) in solution
  counts['solution_blocks']+=3
 if pt:
  origin=F.subs(pt,simultaneous=True);left=F.subs(var,var+h).subs(pt,simultaneous=True);other=F.subs(held,held+h).subs(pt,simultaneous=True);both=F.subs({var:var+h,held:held+h},simultaneous=True).subs(pt,simultaneous=True)
  bank=[(left-origin)/h,(other-origin)/h,(both-origin)/h,(left+origin)/h,(origin-left)/h]
  assert all(sum(same(a,b) for b in bank)==1 for a in values);counts['authored_hard_banks']+=1
 counts['records']+=1;counts['choices']+=5

if __name__=='__main__':
 g=load('parent_quotient_generation',D.with_suffix('.py'));source=json.loads((R/'refresh-2026-10-14/sources'/f'{K}.json').read_text());assert json.loads((D/'source.json').read_text())==source;originals={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
 for case in json.loads((D/'source-cases.json').read_text()):
  r=g.generate(case.get('difficulty',case.get('level')),template=case['template'],parameters=case['parameters'],profile='observed');q=r['question'];old=originals[case['source_id']];check(r)
  a,av,ap=prompt(q);b,bv,bp=prompt(old);assert same(a,b) and av==bv and ap==bp and prose(q[':question/problem'])==prose(old[':question/problem'])
  of,nf=old[':question/answer-fields'][0],q[':question/answer-fields'][0];remaining=[quotient(z[':answer/value']) for z in nf[':answer-field/choices']]
  for z in of[':answer-field/choices']:
   found=[i for i,a in enumerate(remaining) if same(a,quotient(z[':answer/value']))];assert len(found)==1;remaining.pop(found[0]);counts['source_values']+=1
  assert not remaining;counts['source_banks']+=1
  if ':answer-field/correct' in of:
   value=next(z[':answer/value'] for z in nf[':answer-field/choices'] if z[':answer/id']==nf[':answer-field/correct'][1]);assert same(quotient(value),quotient(of[':answer-field/correct'][':answer/value']));counts['source_keys']+=1
  else:assert ':answer-field/correct' not in nf;counts['source_missing_keys']+=1
  for key in (':question/worked-solution',':question/difficulty'):assert (key in old)==(key in q)
  if ':question/worked-solution' in old:assert prose(old[':question/worked-solution'])==prose(q[':question/worked-solution']);counts['source_solutions']+=1
 samples=json.loads((R/'qa'/f'{K}-sampled.json').read_text())
 for record in samples:check(record)
 for name,sp in g.TEMPLATES.items():
  for swap in (False,True):
   pars=dict(sp['anchor'],swap=swap);check(g.generate(sp['level'],template=name,parameters=pars))
 mutant=copy.deepcopy(samples[0]);f=mutant['question'][':question/answer-fields'][0];a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);old=a[':answer/value'];a[':answer/value']=old.replace('h','x');saved=copy.deepcopy(counts)
 try:check(mutant)
 except (AssertionError,ValueError):pass
 else:raise AssertionError('Wrong limit variable survived unchanged designation')
 counts=saved;counts.update(status='passed',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),unchanged_key_wrong_limit_variable_rejected=True,database_writes=0)
 (R/'qa'/f'{K}-root-readback.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
