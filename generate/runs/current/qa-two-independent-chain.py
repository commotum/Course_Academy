"""Root actual-prompt and held-coordinate checks for the two-path chain rule."""
import importlib.util,json,re,hashlib
from pathlib import Path
import sympy as s
from sympy.simplify.fu import fu
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186166749
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);g=importlib.util.module_from_spec(z);z.loader.exec_module(g);return g
p=load(R/'ode-scalar-parser.py','tworootparser');u,v=s.symbols('u v',real=True);p.locals_.update(u=u,v=v)
def scalar(z):
 z=z.replace(r'\,','').strip().rstrip('.,').replace(r'\left','').replace(r'\right','')
 z=re.sub(r'(\\operatorname\{(?:sin|cos|tan|cot|csc|sec)\}⁡?)(\d+)\(([^()]*)\)',lambda m:m[1]+'('+m[2]+'('+m[3]+'))',z)
 bits=re.split(r'(\\[A-Za-z]+|arccos|arcsin|arctan|sqrt|cos|sin|tan|cot|csc|sec|ln|log|exp|text|mathrm)',z)
 for j in range(0,len(bits),2):bits[j]=bits[j].replace('s','u').replace('t','v')
 return p.scalar(''.join(bits))
def same(a,b):
 d=s.cancel(s.expand(a-b))
 d=d.xreplace({f:f.func(s.expand(f.args[0])) for f in d.atoms(s.sin,s.cos,s.tan,s.cot,s.csc,s.sec)})
 d=fu(d)
 if d==0:return True
 for U,V in ((1,2),(2,3),(3,1)):
  e=d.subs({u:U,v:V})
  if e.is_finite is True and e.is_real is True and e.is_zero is False:return False
 return s.simplify(s.trigsimp(d))==0

def task(q):
 prompt=q[':question/problem'];mf=re.search(r'\$f\(x,y\)=(.*?)\$',prompt);mx=re.search(r'where \$x=(.*?)\$',prompt);my=re.search(r'and \$y=(.*?)\$',prompt);variable=re.findall(r'\\frac\{∂f\}\{∂([st])\}',prompt);assert mf and mx and my and len(variable)==1,prompt
 F=scalar(mf[1]);X=scalar(mx[1]);Y=scalar(my[1]);var=variable[0];a=u if var=='s' else v;other=v if a==u else u;assert F.free_symbols<={p.x,p.y} and X.free_symbols<={u,v} and Y.free_symbols<={u,v}
 partials=[s.diff(F,z) for z in (p.x,p.y)];components=[z.subs({p.x:X,p.y:Y},simultaneous=True) for z in partials];maps=[s.diff(z,a) for z in (X,Y)];answer=s.diff(F.subs({p.x:X,p.y:Y},simultaneous=True),a);assert same(answer,sum(z*w for z,w in zip(components,maps)))
 return F,X,Y,var,a,other,partials,components,maps,answer

def stages(q,n):
 F,X,Y,var,a,other,partials,components,maps,answer=task(q);FX=r'\frac{∂f}{∂x}';FY=r'\frac{∂f}{∂y}';D=r'\frac{∂f}{∂'+var+'}';XD=r'\frac{∂x}{∂'+var+'}';YD=r'\frac{∂y}{∂'+var+'}';rule=FX+r'\cdot '+XD+'+'+FY+r'\cdot '+YD
 blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',q[':question/worked-solution'],re.S);assert len(blocks)==5;assert blocks[0].strip()==D+'='+rule
 for bi,block in enumerate(blocks[1:],1):
  values={FX:partials[0] if bi==1 else components[0],FY:partials[1] if bi==1 else components[1],XD:maps[0],YD:maps[1],D:answer};current=None
  for row in block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\'):
   for piece in re.split(r',\\,',row):
    parts=[z.strip().rstrip('.,') for z in piece.replace('&','').split('=')]
    if parts[0]:current=parts[0]
    assert current in values,(bi,current,piece)
    for expr in parts[1:]:
     for tag,value in values.items():expr=expr.replace(tag,'('+s.latex(value,ln_notation=True)+')')
     actual=scalar(expr);assert same(actual,values[current]),(bi,piece,actual,values[current]);n[{1:'formal_partial_stages',2:'substitution_stages',3:'held_coordinate_stages',4:'product_reduction_stages'}[bi]]+=1
 return task(q)

def check():
 g=load(ROOT/f'generate/scratch/{K}.py','g749');originals=json.loads((R/f'sources/{K}.json').read_text())['record'][':knowledge-point/questions'];cases=json.loads((ROOT/f'generate/scratch/{K}/source-cases.json').read_text());src=dict(prompts=0,solutions=0,fields=0,values=0,keys=0)
 for c in cases:
  original=next(q for q in originals if c['source_id'] in (q[':db/id'],q[':question/id'],q[':question/math-academy-id']));lv=original[':question/difficulty'][':db/ident'].split('/')[-1];q=g.generate(lv,template=c['template'],parameters=c['parameters'],profile=c['bank_profile'])['question']
  for key in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (key in q)==(key in original);assert q[key]==(original[key].get(':db/ident') if isinstance(original[key],dict) else original[key]),(c,key)
  src['prompts']+=1;src['solutions']+=1;F,X,Y,var,a,other,P,C,M,answer=task(original)
  for f,f0 in zip(q[':question/answer-fields'],original[':question/answer-fields']):
   assert f[':answer-field/key']==f0[':answer-field/key'] and f[':answer-field/type']==f0[':answer-field/type'][':db/ident'];assert sorted(z[':answer/value'] for z in f[':answer-field/choices'])==sorted(z[':answer/value'] for z in f0[':answer-field/choices']);src['fields']+=1;src['values']+=len(f[':answer-field/choices']);selected=next(z for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);assert selected[':answer/value']==f0[':answer-field/correct'][':answer/value'];assert same(scalar(selected[':answer/value']),answer);src['keys']+=1
 records=json.loads((R/f'qa/{K}-sampled.json').read_text());n=dict(records=0,formal_partial_stages=0,substitution_stages=0,held_coordinate_stages=0,product_reduction_stages=0,choices=0,complete_method_banks=0,normal_anchor_cases=0)
 for c in cases:
  records.append(g.generate(g.TEMPLATES[c['template']],template=c['template'],parameters=c['parameters']));n['normal_anchor_cases']+=1
 for r in records:
  q=r['question'];F,X,Y,var,a,other,P,C,M,answer=stages(q,n);f=q[':question/answer-fields'][0];vals=[]
  for option in f[':answer-field/choices']:
   got=scalar(option[':answer/value']);assert same(got,answer)==(option[':answer/id']==f[':answer-field/correct'][1]);assert not any(same(got,z) for z in vals);vals.append(got);n['choices']+=1
  U,V=C[0]*M[0],C[1]*M[1];kind=r['generation']['template']
  if kind=='zero_exponential':expected=[answer,s.diff(F.subs({p.x:X,p.y:Y},simultaneous=True),other),C[1],C[1]*s.diff(Y,other),Y*M[1]]
  elif kind=='affine_two_maps':expected=[answer,s.diff(F.subs({p.x:X,p.y:Y},simultaneous=True),other),U-V,U,V]
  else:expected=[answer,U,V,U-V,sum(C)]
  assert all(any(same(got,w) for w in expected) for got in vals);n['complete_method_banks']+=1;n['records']+=1
  if kind in g.FAMILIES:
   source=g.SOURCES[g.FAMILIES[kind]];assert re.split(r'\$\$.*?\$\$',q[':question/worked-solution'],flags=re.S)==re.split(r'\$\$.*?\$\$',source[':question/worked-solution'],flags=re.S)
 out=dict(status='passed',kp_id=K,source=src,readback=n,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{K}.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':check()
