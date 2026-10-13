"""Root independently parses two-path, one-independent-variable chain rule."""
import importlib.util,json,re,hashlib
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186166747
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);g=importlib.util.module_from_spec(z);z.loader.exec_module(g);return g
p=load(R/'ode-scalar-parser.py','generalrootparser');u=s.Symbol('u',positive=True);p.locals_['u']=u
FX=r'\frac{∂f}{∂x}';FY=r'\frac{∂f}{∂y}'
def scalar(z,var):
 z=re.sub(r'(?<![A-Za-z\\])'+var+r'(?![A-Za-z])','u',z.replace(r'\,','').strip().rstrip('.,'));return p.scalar(z)
def same(a,b):
 d=s.cancel(s.expand(a-b))
 if d==0:return True
 # Exact, finite witnesses are used only to establish nonidentity.
 for at in (s.Rational(1,7),s.Rational(1,3),2,5):
  value=d.subs(u,at)
  if value.is_real is True and value.is_finite is True and value.is_zero is False:return False
 return s.simplify(s.trigsimp(d))==0

def task(q):
 text=q[':question/problem'];var='s' if r'{\text{d}s}' in text or '{ds}' in text else 't'
 f=re.search(r'f\(x,\s*y\)\s*=\s*(.*?)(?:,\s*(?:\\,)?\s*x\s*=|\$)',text);mx=re.search(r'(?:\$|,)\s*x\s*=\s*(.*?)(?:\$|,)',text);my=re.search(r'(?:\$|,)\s*y\s*=\s*(.*?)\$',text);assert f and mx and my,text
 F=scalar(f[1],var);X=scalar(mx[1],var);Y=scalar(my[1],var);assert F.free_symbols<={p.x,p.y} and X.free_symbols<={u} and Y.free_symbols<={u}
 A=s.diff(F,p.x);B=s.diff(F,p.y);aa=A.subs({p.x:X,p.y:Y},simultaneous=True);bb=B.subs({p.x:X,p.y:Y},simultaneous=True);dx=s.diff(X,u);dy=s.diff(Y,u);answer=s.diff(F.subs({p.x:X,p.y:Y},simultaneous=True),u);assert same(answer,aa*dx+bb*dy)
 return var,F,X,Y,A,B,aa,bb,dx,dy,answer

def stages(q,stats):
 var,F,X,Y,A,B,aa,bb,dx,dy,answer=task(q);D=r'\frac{\text{d}f}{\text{d}'+var+'}';DX=r'\frac{\text{d}x}{\text{d}'+var+'}';DY=r'\frac{\text{d}y}{\text{d}'+var+'}';expected_rule=FX+r'\cdot '+DX+'+'+FY+r'\cdot '+DY
 blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',q[':question/worked-solution'],re.S);assert len(blocks)==5;assert blocks[0].strip()==D+'='+expected_rule
 for bi,block in enumerate(blocks[1:],1):
  current=None
  for row in block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\'):
   for piece in re.split(r',\\,',row):
    bits=[a.strip().rstrip('.,') for a in piece.replace('&','').split('=')]
    if bits[0]:current=bits[0]
    assert current in (FX,FY,DX,DY,D),current
    values={FX:A if bi==1 else aa,FY:B if bi==1 else bb,DX:dx,DY:dy,D:answer}
    for z in bits[1:]:
     for tag,value in values.items():z=z.replace(tag,'('+s.latex(value,ln_notation=True)+')')
     actual=scalar(z,var);assert same(actual,values[current]),(bi,piece,actual,values[current]);stats[{1:'partial_stages',2:'substitution_stages',3:'coordinate_derivative_stages',4:'product_reduction_stages'}[bi]]+=1
 return task(q)

def check():
 g=load(ROOT/f'generate/scratch/{K}.py','generalgen');originals=json.loads((R/f'sources/{K}.json').read_text())['record'][':knowledge-point/questions'];cases=json.loads((ROOT/f'generate/scratch/{K}/source-cases.json').read_text());src=dict(prompts=0,solutions=0,fields=0,values=0,keys=0,missing_designations=0)
 for c in cases:
  original=next(q for q in originals if c['source_id'] in (q[':db/id'],q[':question/id'],q[':question/math-academy-id']));q=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile'])['question']
  for key in (':question/problem',':question/difficulty',':question/worked-solution'):
   assert (key in q)==(key in original)
   if key in q:assert q[key]==(original[key].get(':db/ident') if isinstance(original[key],dict) else original[key]),(c,key)
  src['prompts']+=1;src['solutions']+=(':question/worked-solution' in original);var,F,X,Y,A,B,aa,bb,dx,dy,answer=task(original)
  for f,f0 in zip(q[':question/answer-fields'],original[':question/answer-fields']):
   assert f[':answer-field/key']==f0[':answer-field/key'] and f[':answer-field/type']==f0[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in f0[':answer-field/choices']);src['fields']+=1;src['values']+=len(f[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in f0)
   if ':answer-field/correct' in f:
    selected=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert selected[':answer/value']==f0[':answer-field/correct'][':answer/value'];assert same(scalar(selected[':answer/value'],var),answer);src['keys']+=1
   else:src['missing_designations']+=1
 records=json.loads((R/f'qa/{K}-sampled.json').read_text());stats=dict(records=0,partial_stages=0,substitution_stages=0,coordinate_derivative_stages=0,product_reduction_stages=0,choices=0,complete_method_banks=0,normal_original_parameter_cases=0)
 # Verify all original normal family masks, including those absent from samples.
 for name in g.NAMES:
  records.append(g.generate_easy(template=name,parameters=g.ORIGINAL[name]));stats['normal_original_parameter_cases']+=1
 for r in records:
  q=r['question'];var,F,X,Y,A,B,aa,bb,dx,dy,answer=stages(q,stats);field=q[':question/answer-fields'][0];vals=[]
  for a in field[':answer-field/choices']:
   value=scalar(a[':answer/value'],var);assert same(value,answer)==(a[':answer/id']==field[':answer-field/correct'][1]);assert not any(same(value,w) for w in vals);vals.append(value);stats['choices']+=1
  expected=[aa*dx+bb*dy,aa*dx,bb*dy,aa*dx-bb*dy,-aa*dx-bb*dy];assert all(any(same(value,w) for w in expected) for value in vals);stats['complete_method_banks']+=1;stats['records']+=1
  if r['generation']['template'] in g.NAMES:
   source=g.QMAP[r['generation']['template']]
   if ':question/worked-solution' in source:
    assert re.split(r'\$\$.*?\$\$',q[':question/worked-solution'],flags=re.S)==re.split(r'\$\$.*?\$\$',source[':question/worked-solution'],flags=re.S)
 out=dict(status='passed',kp_id=K,source=src,readback=stats,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{K}.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':check()
