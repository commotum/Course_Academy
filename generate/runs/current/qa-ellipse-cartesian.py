"""Root reads displayed parametrization, all solution equalities and full curves."""
import sys,re,json,hashlib,importlib.util
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
def load(file,name):
 z=importlib.util.spec_from_file_location(name,file);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','scalar');x,y,I=p.x,p.y,p.i
n=dict(records=0,choices=0,solution_equalities=0,formal_axes=0,squared_axes=0,identity_stages=0,full_equation_banks=0,source_prompts=0,source_values=0,source_solutions=0,source_refs=0)
def scalar(raw):return p.scalar(raw.replace(r'\theta','i').replace('θ','i').replace('⁡',''))
def same(a,b):return s.simplify(s.trigsimp(a-b))==0
def equivalent(a,b):
 pa=s.Poly(s.expand(a),x,y);pb=s.Poly(s.expand(b),x,y);return same(pa.monic().as_expr(),pb.monic().as_expr())
def resid(v):
 parts=v.split('=');assert len(parts)<=2;return scalar(parts[0])-(scalar(parts[1]) if len(parts)==2 else 1)
def check(rec):
 rec=rec.get('record',rec);q=rec['question'];g=rec['generation'];prompt=q[':question/problem'];blocks=re.findall(r'\$\$(.*?)\$\$',prompt,re.S);assert len(blocks)==1
 # Formal equations read from actual prompt, treating the known raw t/theta
 # mismatch separately; t is mapped solely for checking the preserved evidence.
 block=blocks[0].replace(r'\,',r'\quad');pieces=block.split(r'\quad');pieces=[z.strip(' ,\n') for z in pieces];assert len(pieces)==3
 xy=[]
 for piece,var in zip(pieces[:2],(x,y)):
  lhs,rhs=piece.split('=');left,right=scalar(lhs),scalar(rhs.replace('⁡t',r'\theta'));result=s.solve(left-right,var);assert len(result)==1;xy.append(result[0]);n['formal_axes']+=1
 Xf,Yf=xy;h=Xf.subs(I,s.pi/2);k=Yf.subs(I,0);a=Xf.subs(I,0)-h;b=Yf.subs(I,s.pi/2)-k;assert a>0 and b>0 and same(Xf,a*s.cos(I)+h) and same(Yf,b*s.sin(I)+k)
 assert re.fullmatch(r'0\\leq?\s*(?:\\theta|θ)\s*<2\\pi\.?',pieces[2].replace(' ',''))
 if '\\theta' in prompt and '⁡t' in prompt:assert g['evidence_only'] and not g['eligible_for_learning']
 expected=(x-h)**2/a**2+(y-k)**2/b**2-1;sol=q[':question/worked-solution'];solblocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(solblocks)==4
 for i,block in enumerate(solblocks):
  text=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','');rows=text.split(r'\\');rowexpr=[]
  for row in rows:
   terms=[scalar(t.replace('&','').strip()) for t in row.split('=')];assert len(terms)>=2
   for lhs,rhs in zip(terms,terms[1:]):assert same((lhs-rhs).subs({x:Xf,y:Yf}),0),(g['template'],row,lhs,rhs);n['solution_equalities']+=1
   rowexpr.append(terms)
  if i<2:
   assert len(rowexpr)>=2;coordinate=x if i==0 else y;target=s.cos(I) if i==0 else s.sin(I)
   assert any(same(row[-1],target) for row in rowexpr) and sum(same(row[-1],target**2) for row in rowexpr)>=1;n['squared_axes']+=1
   if g['template']!='easy_supplied_isolation':assert rowexpr[0][0]==coordinate
  else:
   assert equivalent(rowexpr[0][0]-1,expected);assert rowexpr[0][-1]==1;n['identity_stages']+=1
 f=q[':question/answer-fields'][0];vs=[resid(a[':answer/value']) for a in f[':answer-field/choices']];assert all(not equivalent(v,w) for i,v in enumerate(vs) for w in vs[:i]);assert sum(equivalent(v,expected) for v in vs)==1
 assert equivalent(vs[next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])],expected)
 if f[':answer-field/type'].endswith('/blank'):assert '='+str(1) in prompt or '=1' in prompt.replace(' ','');assert '{{'+f[':answer-field/key']+'}}' in prompt;assert all('=' not in a[':answer/value'] for a in f[':answer-field/choices'])
 if g['eligible_for_learning']:
  level=q[':question/difficulty'].split('/')[-1]
  if level=='easy':assert h==k==0 and 2<=a<=12 and 2<=b<=12 and a.is_Integer and b.is_Integer and r'\frac{x}' in prompt and r'\frac{y}' in prompt
  elif level=='moderate':assert h==k==0 and g['template'] in [z for z in ORIGINAL_LEVELS if ORIGINAL_LEVELS[z]=='moderate']
  else:assert level=='hard' and h!=0 and k!=0 and abs(h)<=12 and abs(k)<=12 and h.is_Integer and k.is_Integer
  if g['authored_bank'] or g['authored']:
   wanted=[expected,(x+h)**2/a**2+(y+k)**2/b**2-1,(x-h)**2/a+(y-k)**2/b-1,(x-h)**2/b**2+(y-k)**2/a**2-1,(x-h)**2/a**2-(y-k)**2/b**2-1] if h or k else [expected,x**2/b**2+y**2/a**2-1,x**2/a+y**2/b-1,x**2/a**2-y**2/b**2-1,x**2/a**2+y**2/b-1]
   assert all(sum(equivalent(v,e) for v in vs)==1 for e in wanted);n['full_equation_banks']+=1
 n['records']+=1;n['choices']+=len(vs)
if __name__=='__main__':
 kp=17592186152188;D=R.parents[2]/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'generator');src=json.load(open(D/'source.json'));assert src==json.load(open(R/'sources'/f'{kp}.json'));old={q[':question/math-academy-id']:q for q in src['record'][':knowledge-point/questions']};ORIGINAL_LEVELS={k:q[':question/difficulty'][':db/ident'].split('/')[-1] for k,q in old.items()}
 for c in json.load(open(D/'source-cases.json')):
  rec=g.generate(c['difficulty'],template=c['template'],profile=c['bank_profile'],parameters=c['parameters']);check(rec);q=rec['question'];o=old[c['source_id']]
  for key in (':question/problem',':question/worked-solution'):assert q[key]==o[key]
  f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert f[':answer-field/type']==of[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value']
  n['source_prompts']+=1;n['source_values']+=len(f[':answer-field/choices']);n['source_solutions']+=1;n['source_refs']+=1
 for rec in json.load(open(D/'review.json'))+json.load(open(R/'qa'/f'{kp}-sampled.json')):check(rec)
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
