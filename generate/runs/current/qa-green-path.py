"""Root source-field replay and actual general-path Green/polar stages/banks."""
import json,re,hashlib,sys,importlib.util
from pathlib import Path
import sympy as s
import mpmath as mp
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186175987;D=ROOT/f'generate/scratch/{K}'
def load(path,name):
 q=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(q);sys.modules[name]=m;q.loader.exec_module(m);return m
c=load(R/'qa-green-circular.py','root_path_circular');base=c.base;v=load(R/'polar-evaluation-readback.py','root_path_values');p=c.p;x,y,r,theta=c.x,c.y,c.r,c.theta;math,eq=c.scalar,c.equal
GEOMETRY={'constant':(2,-s.pi/2,s.pi/2),'cubic_y':(1,s.pi,3*s.pi/2),'linear_pair':(8,-s.pi,s.pi/2),'factored':(3,s.pi/2,3*s.pi/2),'linear_y':(1,s.pi,2*s.pi),'radial_square':(3,0,s.pi),'mixed_cancel':(5,0,s.pi/2),'constant_mixed':(4,3*s.pi/2,2*s.pi),'affine_y':(6,s.pi/2,2*s.pi),'square_difference':(1,-s.pi/2,s.pi)}
C={k:0 for k in ('records','cross_partials','curl_stages','polar_stages','full_integral_stages','choice_integrals','whole_banks','full_value_pairs','blank_fragments','geometry','normal_no_indentation')}
def unwrap(raw):
 raw=raw.strip().rstrip(' .?');m=re.fullmatch(r'(-?\d+)\\left\((.*)\\right\)',raw,re.S)
 if m:
  a,b=unwrap(m[2]);return s.Integer(m[1])*a,b
 return s.Integer(1),raw.rstrip('.,?')
def field(q):
 text=q[':question/problem'];vec=re.search(r'F\(x,y\)=⟨(.*?)⟩',text,re.S)
 if vec:return tuple(math(z) for z in vec[1].replace(r'\,','').split(','))
 body=next(b for b in p.blocks(text) if ('∮' in b or r'\oint_C' in b));a,body=unwrap(body);body=re.sub(r'^(?:\{∮\}_\{C\}|\\oint_C)','',body);P,Q=body.split(r'\,dx+',1);Q=Q.split(chr(92)+',dy',1)[0];return a*math(P),a*math(Q)
def region(q,family):
 path=Path(re.findall(r'!\[\]\(([^)]+)\)',q[':question/problem'])[0]);assert path.exists();side=path.with_suffix('.json')
 if side.exists():
  z=json.loads(side.read_text());assert z['orientation']=='counterclockwise';assert hashlib.sha256(path.read_bytes()).hexdigest()==z['sha256'];rad=s.Integer(z['radius']);a,b=[s.sympify(w) for w in z['theta']]
 else:
  rad,a,b=GEOMETRY[family]
 return s.sympify(rad),s.sympify(a),s.sympify(b)
def full(raw):
 a,body=unwrap(raw);body=body.replace(r'{\int }',r'\int').replace(r'\,','')
 bounds,fn=v.p.integral(body);aa,bb,low,high=bounds;assert eq(low,0)
 return a*fn,aa,bb,high,None

def num(fn,a,b,rad):
 mp.mp.dps=35;f=s.lambdify((r,theta),fn,'mpmath');aa,bb,rr=[mp.mpf(str(s.N(z,35))) for z in (a,b,rad)]
 return mp.quad(lambda tt:mp.quad(lambda rho:f(rho,tt),[0,rr/2,rr]),[aa,(aa+bb)/2,bb])
def check(rec):
 q=rec['question'];fam=rec['generation']['template'];rad,a,b=region(q,fam);sol=q[':question/worked-solution'];C['geometry']+=1
 if fam=='polar_blanks':
  assert all(not re.match(r' {4}',line) for line in q[':question/problem'].splitlines() if line.strip());C['normal_no_indentation']+=1
  body=re.search(r'\$\{∬\}_\{D\}(.*?)\\,\\text\{d\}A',q[':question/problem'])[1];curl=math(body);fields={f[':answer-field/key']:f for f in q[':question/answer-fields']};actual={key:math(f[':answer-field/choices'][0][':answer/value']) for key,f in fields.items()};assert eq(actual['field-1'],curl.subs({x:r*s.cos(theta),y:r*s.sin(theta)},simultaneous=True)*r) and eq(actual['field-2'],b) and eq(actual['field-3'],rad);C['blank_fragments']+=3;py=qx=None
 else:
  P,Q=field(q);py,qx=s.diff(P,y),s.diff(Q,x);curl=s.expand(qx-py)
  # Verify every actual inline definition and cross partial from its complete input.
  for fn,expr in re.findall(r'\$([PQ])\(x,y\)=(.*?)\$',sol):assert eq(math(expr.rstrip(',')),P if fn=='P' else Q)
  partials=re.findall(r'\\frac\{(?:∂|\\partial )([PQ])\}\{(?:∂|\\partial )([xy])\}=(.*?)(?=,\\,|,\\qquad|\.\\end|\.)',sol)
  assert len(partials)==2,(fam,partials)
  for fn,axis,expr in partials:assert (fn,axis) in (('P','y'),('Q','x')) and eq(math(expr),py if fn=='P' else qx);C['cross_partials']+=1
 pol=s.trigsimp(curl.subs({x:r*s.cos(theta),y:r*s.sin(theta)},simultaneous=True)*r)
 roles=[]
 for group in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S):
  for row in group.split(chr(92)*2):
   if '=' not in row:continue
   body=row.split('=',1)[1].replace('&','').strip();factor,body=unwrap(body)
   if body.startswith((r'{∬}_{D}',r'\iint_D')):
    expr=re.sub(r'^(?:\{∬\}_\{D\}|\\iint_D)','',body);expr=re.split(r'\\(?:text|mathrm)\{d\}A|dA',expr)[0].rstrip().removesuffix(r'\,')
    if '∂' in expr or r'\partial' in expr:
     if fam=='polar_blanks':raise AssertionError('Blank acquired a new Green derivation')
     expr=expr.replace(r'\frac{∂Q}{∂x}','('+s.latex(qx)+')').replace(r'\frac{∂P}{∂y}','('+s.latex(py)+')').replace(r'\frac{\partial Q}{\partial x}','('+s.latex(qx)+')').replace(r'\frac{\partial P}{\partial y}','('+s.latex(py)+')')
    assert eq(factor*math(expr),curl),(fam,expr,curl);C['curl_stages']+=1;roles.append('curl')
   elif body.startswith((r'{∬}_{Δ}',r'\iint_\Delta')):
    expr=re.sub(r'^(?:\{∬\}_\{Δ\}|\\iint_\\Delta)','',body);expr=re.split(r'\\(?:text|mathrm)\{d\}r|dr',expr)[0].rstrip().removesuffix(r'\,');assert eq(factor*math(expr),pol),(fam,expr,pol);C['polar_stages']+=1;roles.append('polar')
   elif r'\int' in body:
    fn,aa,bb,ro,val=full(row.split('=',1)[1].replace('&',''));assert eq(fn,pol) and eq(aa,a) and eq(bb,b) and eq(ro,rad);C['full_integral_stages']+=1;roles.append('integral')
 assert roles and roles[-1]=='integral'
 if fam!='polar_blanks':
  f=q[':question/answer-fields'][0];integrals=[full(z[':answer/value']) for z in f[':answer-field/choices']];correct=[z for z,a0 in zip(f[':answer-field/choices'],integrals) if eq(a0[0],pol) and eq(a0[1],a) and eq(a0[2],b) and eq(a0[3],rad)];assert len(correct)==1 and correct[0][':answer/id']==f[':answer-field/correct'][1]
  actual=[num(*t0[:4]) for t0 in integrals];assert all(abs(z-w)>mp.mpf('1e-20') for i,z in enumerate(actual) for w in actual[:i]);C['choice_integrals']+=5;C['full_value_pairs']+=10;C['whole_banks']+=1
 C['records']+=1;return roles
if __name__=='__main__':
 g=load(D.with_suffix('.py'),'green_path_gen');source=base.raw(g,K,D);records=json.loads((R/f'qa/{K}-sampled.json').read_text());families={}
 for fam in list(g.SPECS)+['easy_constant','hard_polynomial']:records.append(g.generate('easy' if fam=='easy_constant' else 'hard' if fam=='hard_polynomial' else 'moderate',template=fam,seed=617))
 for z in records:
  seq=check(z);fam=z['generation']['template'];assert fam not in families or families[fam]==seq;families[fam]=seq
 out=dict(status='passed',source=source,readback=C,operative_sequences=families,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
