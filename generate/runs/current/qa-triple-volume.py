"""Root actual region/inverse/Jacobian, full volume banks and individual endpoints."""
import sys,re,json,hashlib,importlib.util
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
def load(file,name):
 z=importlib.util.spec_from_file_location(name,file);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'spatial-jacobian-readback.py','spatial');x,y,z=p.x,p.y,p.z;u,v,w=s.symbols('u v w',positive=True);UVW=(u,v,w)
def scalar(raw):return p.scalar(raw).xreplace({p.u:u,p.v:v,p.w:w})
same=p.same
n=dict(records=0,choices=0,source_prompts=0,source_values=0,source_solutions=0,source_refs=0,formal_inputs=0,jacobian_entries=0,cofactor_minors=0,cofactor_products=0,determinant_rows=0,inverse_map_inputs=0,density_rows=0,separated_factors=0,primitive_rows=0,individual_endpoint_components=0,complete_method_banks=0)
def matrix(raw):return s.Matrix([[scalar(z) for z in row.split('&')] for row in raw.split(r'\\')])
def region(text):
 chunks0=p.displays(text) or re.findall(r'\$(.*?)\$',text,re.S);block=next(z.strip() for z in chunks0 if r'\le' in z and ':' in z);inside=block.split(':',1)[1].strip().rstrip('.').removesuffix(r'\big\}').removesuffix('}').removesuffix(r'\}');inside=inside.replace(r'\,',' ').strip();chunks=re.split(r',\s*(?:\\quad\s*)?',inside);assert len(chunks)==3,(inside,chunks)
 coords=[];bounds=[]
 for raw in chunks:
  lo,e,hi=raw.split(r'\le');coords.append(scalar(e));bounds.append((scalar(lo),scalar(hi)))
 return tuple(coords),tuple(bounds)
def integral_total(fn,b):return s.simplify(s.integrate(fn,(w,*b[2]),(v,*b[1]),(u,*b[0])))
def topdiff(raw):
 raw=raw.replace(r'\left','').replace(r'\right','');assert raw.startswith('(') and raw.endswith(')');raw=raw[1:-1];depth=0
 for i,c in enumerate(raw):
  if c in '({[':depth+=1
  elif c in ')}]':depth-=1
  elif c=='-' and depth==0:return scalar(raw[:i]),scalar(raw[i+1:])
 raise AssertionError(raw)
def check(rec):
 q=rec['question'];meta=rec['generation'];name=meta['template'];coords,bounds=region(q[':question/problem']);sol=q[':question/worked-solution'];blocks=[z.strip() for z in p.displays(sol)]
 inverseblock=next(z for z in blocks if 'T(u,v,w)=' in z);tail=inverseblock.split('=',1)[1].rstrip('.').removeprefix(r'\left(').removesuffix(r'\right)');inverse=tuple(scalar(z) for z in tail.split(','));assert len(inverse)==3
 for f,target in zip(coords,UVW):assert same(f.subs(dict(zip((x,y,z),inverse)),simultaneous=True),target);n['inverse_map_inputs']+=1
 M=s.Matrix(coords).jacobian((x,y,z));D=s.factor(M.det());Du=s.simplify(D.subs(dict(zip((x,y,z),inverse)),simultaneous=True));inverseJ=s.simplify(s.Matrix(inverse).jacobian(UVW).det());J=s.simplify(s.Abs(inverseJ));V=integral_total(J,bounds);assert V.is_positive
 jac=next(b for b in blocks if r'\begin{vmatrix}' in b and r'\partial(u,v,w)' in b);mats=re.findall(r'\\begin\{vmatrix\}(.*?)\\end\{vmatrix\}',jac,re.S);assert len(mats)==5
 labels=re.findall(r'\\frac\{\\partial ([uvw])\}\{\\partial ([xyz])\}',mats[0]);assert labels==[(a,b) for a in 'uvw' for b in 'xyz'];n['formal_inputs']+=9
 assert matrix(mats[1])==M;n['jacobian_entries']+=9
 for i,raw in enumerate(mats[2:]):assert matrix(raw)==M.minor_submatrix(0,i);n['cofactor_minors']+=1
 rows=jac.split(r' \\  & =');assert len(rows) in (4,5);expansion=rows[2]
 flat=re.sub(r'\\begin\{vmatrix\}.*?\\end\{vmatrix\}','MINOR',expansion,flags=re.S)
 factors=re.findall(r'\\left\((.*?)\\right\)\(-1\)\^\{1\+([123])\}',flat);assert len(factors)==3
 for i,(raw,power) in enumerate(factors):assert int(power)==i+1 and same(scalar(raw),M[0,i]);n['cofactor_products']+=1
 assert same(scalar(rows[3].removesuffix(r'\end{aligned}')),D);n['determinant_rows']+=1
 if len(rows)==5:assert same(scalar(rows[4].removesuffix(r'\end{aligned}')),Du);n['determinant_rows']+=1
 jb=next(b for b in blocks if r'\right)^{-1}=' in b);assert same(scalar(jb.split('=')[-1]),inverseJ)
 cv=next(b for b in blocks if b.startswith('u='));assert all(same(scalar(raw.split('=',1)[1]),f) for raw,f in zip(cv.rstrip('.').split(r',\quad '),coords))
 domain=next(b for b in blocks if b.startswith(r'\Delta='));part=domain.split(':',1)[1].split(r'\big\}')[0]
 for var,raw,(lo,hi) in zip(('u','v','w'),part.split(r',\quad '),bounds):
  a,b,c=raw.split(r'\le ');assert b==var and same(scalar(a),lo) and same(scalar(c),hi)
 rows=blocks[-1].removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(r' \\ ');assert len(rows)==7;rhs=[r.split(' & =',1)[1] for r in rows]
 assert same(scalar(rhs[0].split('|')[1]),inverseJ)
 pat=r'\\int_\{(.*?)\}\^\{(.*?)\}';actualbounds=[(scalar(a),scalar(b)) for a,b in re.findall(pat,rhs[1])];assert tuple(actualbounds)==bounds;actualdensity=scalar(re.sub(pat,'',rhs[1]).split(r'\,\mathrm{d}')[0]);assert same(actualdensity,J);n['density_rows']+=2
 separated=rhs[2].split(r'\cdot ');constant=scalar(separated[0]);fs=[]
 for raw,var,(lo,hi) in zip(separated[1:],UVW,bounds):
  lims=re.findall(pat,raw);assert len(lims)==1 and same(scalar(lims[0][0]),lo) and same(scalar(lims[0][1]),hi);fn=scalar(re.sub(pat,'',raw).split(r'\,\mathrm{d}')[0]);fs.append(fn);n['separated_factors']+=1
 assert same(constant*s.prod(fs),J)
 primparts=rhs[3].split(r'\cdot ');assert same(scalar(primparts[0]),constant);prim=[]
 for raw,var,fn,(lo,hi) in zip(primparts[1:],UVW,fs,bounds):
  m=re.fullmatch(r'\[(.*?)\]_\{(.*?)\}\^\{(.*?)\}',raw);assert m and same(scalar(m[2]),lo) and same(scalar(m[3]),hi);P=scalar(m[1]);assert same(s.diff(P,var),fn);prim.append(P);n['primitive_rows']+=1
 for index in (4,5):
  parts=rhs[index].split(r'\cdot ');assert len(parts)==4 and same(scalar(parts[0]),constant)
  for raw,var,P,(lo,hi) in zip(parts[1:],UVW,prim,bounds):a,b=topdiff(raw);assert same(a,P.subs(var,hi)) and same(b,P.subs(var,lo));n['individual_endpoint_components']+=2
  assert same(scalar(rhs[index]),V)
 assert same(scalar(rhs[6]),V)
 field=q[':question/answer-fields'][0];vs=[scalar(a[':answer/value']) for a in field[':answer-field/choices']];assert len(vs)==5 and all(a.is_positive for a in vs) and all(not same(a,b) for i,a in enumerate(vs) for b in vs[:i]);du,dv,dw=[hi-lo for lo,hi in bounds];B=du*dv*dw
 if name=='affine':wrong=[B,B/J,V/du,V/dv]
 elif name in ('linear_yz','shear','linear_xz'):wrong=[V/du,V/dv,V/dw,V*bounds[0][1]/du]
 elif name=='log':b=s.simplify(1/(J*u));wrong=[B,b*dv*dw*(bounds[0][1]**2-bounds[0][0]**2)/2,V/dv,dv*dw*s.log(bounds[0][1])/b]
 elif name=='sqrt':wrong=[B,V/2,du*dv*(bounds[2][1]**3-bounds[2][0]**3)/3,du*dv*bounds[2][1]**2]
 elif name=='reciprocal':wrong=[B,du*dv*(bounds[2][1]**3-bounds[2][0]**3)/3,du*dv/bounds[2][1],du*dv*(1/bounds[2][0]**2-1/bounds[2][1]**2)]
 else:assert name=='cube';lin=s.Abs(M[:2,:2].det());wrong=[B,3*V,lin*V,V/du]
 assert all(sum(same(a,b) for b in [V]+wrong)==1 for a in vs);selected=next(a for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1]);assert same(scalar(selected[':answer/value']),V)
 n['complete_method_banks']+=1;n['records']+=1;n['choices']+=5
if __name__=='__main__':
 kp=17592186198399;D=R.parents[2]/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'generator');src=json.load(open(D/'source.json'));assert src==json.load(open(R/'sources'/f'{kp}.json'));old={str(q[':db/id']):q for q in src['record'][':knowledge-point/questions']}
 for c in json.load(open(D/'source-cases.json')):
  rec=g.generate(c['level'],template=c['template'],profile=c['bank_profile'],parameters=c['parameters']);q=rec['question'];o=old[str(c['source_id'])]
  coords,bounds=region(q[':question/problem']);solutions=s.solve([a-b for a,b in zip(coords,UVW)],(x,y,z),dict=True);assert len(solutions)==1
  inv=solutions[0];J=s.simplify(s.Abs(s.Matrix([inv[a] for a in (x,y,z)]).jacobian(UVW).det()));value=integral_total(J,bounds)
  for key in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (key in q)==(key in o)
   if key in o:assert q[key]==(o[key][':db/ident'] if key.endswith('difficulty') else o[key])
  assert len(q[':question/answer-fields'])==len(o[':question/answer-fields'])
  for f,of in zip(q[':question/answer-fields'],o[':question/answer-fields']):
   assert sorted(re.sub(r'\s+','',a[':answer/value']) for a in f[':answer-field/choices'])==sorted(re.sub(r'\s+','',a[':answer/value']) for a in of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
   if ':answer-field/correct' in of:
    actual=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert actual==of[':answer-field/correct'][':answer/value'] and same(scalar(actual),value);n['source_refs']+=1
   n['source_values']+=5
  n['source_prompts']+=1;n['source_solutions']+=int(':question/worked-solution' in o)
 for item in json.load(open(D/'review.json')):
  rec=item.get('record',item)
  if rec['generation']['eligible_for_learning']:check(rec)
 for level,fs in g.FAMILIES.items():
  for family in fs:
   for seed in range(4):check(g.generate(level,seed=72000+seed,template=family))
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
