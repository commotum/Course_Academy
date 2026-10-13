"""Root actual vector/linear equation readback and complete method banks."""
import sys,re,json,hashlib,importlib.util
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
def load(file,name):
 z=importlib.util.spec_from_file_location(name,file);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'vector-math-parser.py','vector');X=p.x
n=dict(records=0,choices=0,formal_inputs=0,dot_rows=0,linear_equations=0,whole_method_banks=0,easy=0,raw_alias_errors=0,source_prompts=0,source_values=0,source_solutions=0,source_refs=0)
def check(rec):
 q=rec['question'];meta=rec['generation'];level=q[':question/difficulty'].split('/')[-1];f=q[':question/answer-fields'][0];vs=[p.scalar(a[':answer/value']) for a in f[':answer-field/choices']];assert len(vs)==(1 if f[':answer-field/type'].endswith('/blank') else 5);assert all(not s.simplify(a-b)==0 for i,a in enumerate(vs) for b in vs[:i]);correct=next(p.scalar(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);text=q[':question/problem'];sol=q[':question/worked-solution']
 if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in text
 if level=='easy':
  assert correct==0 and ('perpendicular' in text or r'90^\circ' in text) and ('perpendicular' in sol or r'\cos(90^\circ)' in sol);assert len(vs)==1
  if r'90^\circ' in text:
   block=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)[0];rows=block.split(r'\\');assert len(rows)==4
   rhs=[raw.split('=',1)[1].strip().rstrip('.') for raw in rows];assert rhs==[r'|a|\cos\theta',r'|a|\cos(90^\circ)',r'|a|\cdot 0','0'];assert s.cos(s.pi/2)==0
  assert meta['mathematical_fingerprint'] if 'mathematical_fingerprint' in meta else True
  n['easy']+=1
 else:
  m=re.match(r'Let \$([a-z])=(.*?)\$ and \$([a-z])=(.*?)\.\$',text);assert m;A,araw,B,braw=m.groups();a,b=p.vector(araw),p.vector(braw);assert len(a)==len(b)==3;products=[s.expand(x*y) for x,y in zip(a,b)];dot=s.expand(sum(products));assert s.degree(dot,X)==1;coef=dot.coeff(X);const=dot.subs(X,0);expected=-const/coef;assert coef!=0 and s.simplify(correct-expected)==0 and all(sum(z.subs(X,expected)**2 for z in vec)!=0 for vec in (a,b))
  blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(blocks)==2;rows=blocks[0].split(r' \\  & =');assert len(rows)==3
  allowed_error=meta['evidence_only'] and meta.get('profile')=='observed:q-275256'
  aa,bb=('p','q') if allowed_error else (A,B);lhs,rhs=rows[0].split(' & =');assert lhs==aa+r'\cdot '+bb,(lhs,aa,bb,meta.get('source_id'),meta['evidence_only'])
  labels=re.findall(r'\{([a-z])\}_\{([xyz])\}',rhs);assert labels==[(name,coord) for coord in 'xyz' for name in (aa,bb)];n['formal_inputs']+=6
  if allowed_error:n['raw_alias_errors']+=1
  for raw in rows[1:]:assert s.simplify(p.scalar(raw)-dot)==0;n['dot_rows']+=1
  for row in blocks[1].split(r'\\'):
   lhs,rhs=row.strip().split(' & =')
   if r'\cdot' in lhs:assert lhs==aa+r'\cdot '+bb and p.scalar(rhs)==0;residual=dot
   else:residual=p.scalar(lhs)-p.scalar(rhs)
   ratio=s.simplify(residual/dot);assert ratio!=0 and not ratio.has(X) and s.simplify(residual.subs(X,expected))==0,(row,residual,dot);n['linear_equations']+=1
  assert blocks[1].split(r'\\')[-1].strip().startswith('x & =')
  if level=='hard':assert sum(z.has(X) for z in products)==2 and all(z!=0 for z in products) and abs(coef)>=2
  else:assert sum(z.has(X) for z in products)==1
  if meta['eligible_for_learning'] and len(vs)==5:
   known=[(x,y) for x,y in zip(a,b) if not (x*y).has(X) and x*y!=0];profile=meta['profile']
   if profile=='method:hard':cs=[z.coeff(X) for z in products if z.has(X)];want=[expected,-expected,-const/cs[0],-const/cs[1],-const]
   elif profile=='method:two-products':k=[x*y for x,y in known];want=[expected,-expected,-k[0]/coef,-k[1]/coef,-const]
   elif profile=='method:two-products-unit':k=[x*y for x,y in known];want=[expected,-expected,-k[0]/coef,-k[1]/coef,(k[0]-k[1])/coef]
   elif profile=='method:one-product':x,y=known[0];want=[expected,-expected,-const,x,y]
   else:assert profile=='method:one-product-unit';x,y=known[0];want=[expected,-expected,x,y,-(x+y)/coef]
   assert all(sum(s.simplify(a-b)==0 for b in want)==1 for a in vs);n['whole_method_banks']+=1
 n['records']+=1;n['choices']+=len(vs)
if __name__=='__main__':
 kp=17592186105918;D=R.parents[2]/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'generator');src=json.load(open(D/'source.json'));assert src==json.load(open(R/'sources'/f'{kp}.json'));old={str(q[':db/id']):q for q in src['record'][':knowledge-point/questions']}
 for c in json.load(open(D/'source-cases.json')):
  rec=g.generate(c['level'],template=c['template'],profile=c['profile'],parameters=c['parameters']);check(rec);q=rec['question'];o=old[str(c['source_id'])]
  for key in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (key in q)==(key in o)
   if key in o:assert q[key]==(o[key][':db/ident'] if key.endswith('difficulty') else o[key])
  f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident'];want=[p.scalar(a[':answer/value']) for a in of[':answer-field/choices']];vals=[p.scalar(a[':answer/value']) for a in f[':answer-field/choices']];assert len(want)==len(vals) and all(sum(s.simplify(a-b)==0 for b in vals)==1 for a in want)
  selected=next(p.scalar(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert s.simplify(selected-p.scalar(of[':answer-field/correct'][':answer/value']))==0;n['source_refs']+=1;n['source_prompts']+=1;n['source_values']+=len(vals);n['source_solutions']+=1
 for item in json.load(open(D/'review.json')):check(item.get('record',item))
 for level in ('easy','moderate','hard'):
  for seed in range(18):check(g.generate(level,seed=110000+seed))
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
