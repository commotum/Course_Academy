"""Parent independent triple-setup regions, all Jacobian entries and whole banks."""
import sys,re,json,hashlib,importlib.util
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
def load(file,name):
 z=importlib.util.spec_from_file_location(name,file);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'spatial-jacobian-readback.py','spatial');X,Y,Z=p.x,p.y,p.z;U,V,W=p.u,p.v,p.w
n=dict(records=0,choices=0,jacobian_entries=0,formal_inputs=0,cofactor_minors=0,cofactor_products=0,determinant_rows=0,inverse_rows=0,transformed_density_rows=0,region_bounds=0,source_prompts=0,source_values=0,source_solutions=0,source_refs=0)
def group(text,pos):
 assert text[pos]=='{';start=pos+1;pos=start;depth=1
 while depth:depth+=(text[pos]=='{')-(text[pos]=='}');pos+=1
 return text[start:pos-1],pos
def integral(text):
 bounds=[];pos=0;text=text.strip().rstrip('.,')
 for _ in range(3):
  assert text[pos:].startswith(r'\int_');pos+=5;lo,pos=group(text,pos);assert text[pos]=='^';hi,pos=group(text,pos+1);bounds.append((p.scalar(lo),p.scalar(hi)))
 tail=text[pos:];assert tail.startswith(r'\left(') and tail.endswith(r'\right)\,dw\,dv\,du'),text
 return p.scalar(tail[len(r'\left('):-len(r'\right)\,dw\,dv\,du')]),tuple(bounds)
def total(e,b):return s.simplify(s.integrate(e,(W,*b[2]),(V,*b[1]),(U,*b[0])))
def pairs_same(a,b):return all(p.same(x,y) for p0,p1 in zip(a,b) for x,y in zip(p0,p1))
def check(rec):
 q=rec['question'];meta=rec['generation'];name=meta['template'];level=q[':question/difficulty'].split('/')[-1];text=q[':question/problem'];sol=q[':question/worked-solution'];bs=p.displays(text)
 change=bs[1].strip().rstrip(',');coords=[]
 for target,z in zip(('u','v','w'),change.split(',\\quad ')):
  lhs,rhs=z.split('=',1);assert lhs==target;coords.append(p.scalar(rhs))
 inverse=s.solve([f-v for f,v in zip(coords,(U,V,W))],(X,Y,Z),dict=True);assert len(inverse)==1;inv=inverse[0];J=s.Matrix(coords).jacobian((X,Y,Z));det=s.factor(J.det());dnew=s.simplify(det.subs(inv));jd=s.simplify(1/dnew)
 if name=='sqrt':assert '$w>0$' in sol;dnew=dnew.xreplace({s.Abs(W):W});jd=jd.xreplace({s.Abs(W):W})
 region=bs[0].strip().split(': ',1)[1].split(r'\}',1)[0];constraints=[]
 for z in region.split(',\\quad '):
  lo,e,hi=z.split(r'\le ');constraints.append(tuple(p.scalar(v) for v in (lo,e,hi)))
 bounds=[]
 for i,(lo,e,hi) in enumerate(constraints):
  expr=s.simplify(e.subs(inv,simultaneous=True));lo=s.simplify(lo.subs(inv,simultaneous=True));hi=s.simplify(hi.subs(inv,simultaneous=True));var=(U,V,W)[i]
  if name=='sqrt' and i==2:
   assert expr==W**2 and lo==1 and p.same(hi,U*V);bounds.append((1,s.sqrt(U*V)))
  else:
   k=s.diff(expr,var);assert k.is_positive and p.same(expr,k*var);bounds.append((lo/k,hi/k))
 bounds=tuple(bounds)
 displayed=re.search(r'Δ=\\\{\(u,v,w\): (.*?)\\\}',sol)[1]
 shown=[]
 for target,z in zip(('u','v','w'),displayed.split(',\\quad ')):
  lo,var,hi=z.split(r'\le ');assert var==target;shown.append((p.scalar(lo),p.scalar(hi)))
 assert pairs_same(bounds,shown);n['region_bounds']+=6
 if name=='product':assert bounds[1][0]*bounds[1][1]>0;ab=jd if bounds[1][0]>0 else -jd
 elif name=='sqrt':ab=-jd
 else:ab=s.Abs(jd)
 density=p.scalar(re.search(r'\\iiint_R (.*?)\\,dV',text,re.S)[1]);ft=s.simplify(density.subs(inv,simultaneous=True))
 if name=='sqrt':ft=ft.xreplace({s.Abs(W):W})
 correct=s.simplify(ft*ab)
 sec=sol.split('**Step 2**')[1].split('**Step 3**')[0];mats=re.findall(r'\\begin\{vmatrix\}(.*?)\\end\{vmatrix\}',sec,re.S);assert len(mats)==5
 labels=re.findall(r'\\frac\{\\partial ([uvw])\}\{\\partial ([xyz])\}',mats[0]);assert labels==[(a,b) for a in 'uvw' for b in 'xyz'];n['formal_inputs']+=9
 matrix=lambda text:s.Matrix([[p.scalar(z) for z in row.split('&')] for row in text.split(r'\\')])
 assert matrix(mats[1])==J;n['jacobian_entries']+=9
 for j,raw in enumerate(mats[2:]):assert matrix(raw)==J.minor_submatrix(0,j);n['cofactor_minors']+=1
 expansion=sec.split(r'\\ &=')[2];factors=re.findall(r'\((.*?)\)\\begin\{vmatrix\}',expansion);assert len(factors)==3
 assert re.findall(r'\\end\{vmatrix\}([+-])',expansion)==['-','+']
 for j,z in enumerate(factors):assert p.same(p.scalar(z),J[0,j]);n['cofactor_products']+=1
 last=sec.split(r'\\ &=')[-2:];assert p.same(p.scalar(last[0]),det) and p.same(p.scalar(last[1].split(r'.\end{aligned}')[0]),dnew);n['determinant_rows']+=2
 sec3=sol.split('**Step 3**')[1].split('**Step 4**')[0];assert p.same(p.scalar(re.search(r'\)\^\{-1\}=(.*?)\.\s*\$\$',sec3,re.S)[1]),jd);n['inverse_rows']+=1
 initial=re.search(r'&=\\iiint_Δ \\left\((.*?)\\right\)\\left\|\\frac',sol,re.S)[1];assert p.same(p.scalar(initial),ft)
 middle=re.search(r'\\\\ &=\\iiint_Δ \\left\((.*?)\\right\)\\left\|(.*?)\\right\|',sol,re.S);assert p.same(p.scalar(middle[1]),ft) and p.same(p.scalar(middle[2]),jd);n['transformed_density_rows']+=2
 final=re.search(r'\\\\ &=((?:\\int_).*?)\.\\end\{aligned\}',sol,re.S)[1];fn,b=integral(final);assert p.same(fn,correct) and pairs_same(b,bounds)
 f=q[':question/answer-fields'][0];forms=[(p.scalar(a[':answer/value']),bounds) if level=='easy' else integral(a[':answer/value']) for a in f[':answer-field/choices']];assert len(forms)==5
 # Entire independently derived banks, not just four arbitrary incorrect scalars.
 if name=='exp':c=s.simplify(ft/(U*s.exp(V)));a=s.Abs(det)-1;expected=[(correct,bounds),(ft,bounds),(correct.subs({U:V,V:U},simultaneous=True),bounds),(c*s.exp(V)/(a+1),bounds),(c*s.exp(U)/(a+1),bounds)]
 elif name=='sin':a=J[0,0];c=s.simplify(ft/(s.sin(U)*s.cos(V)));expected=[(e,bounds) for e in (correct,ft,ft*a,c*s.sin(V)*s.cos(U)/a,c*s.sin(U)*s.sin(V)/a)]
 elif name=='log':a=J[1,0];c=s.simplify(ft/(V*s.log(U)));expected=[(e,bounds) for e in (correct,ft,ft*a,c*U*s.log(U)/a,-correct)]
 elif name=='cos2':a=J[0,1];c=s.trigsimp(ft/(s.cos(U+V)**2*s.cos(V)));expected=[(e,bounds) for e in (correct,ft,ft*a,c*s.cos(U-V)**2*s.cos(V)/a,c*s.cos(U)**2*s.cos(V)/a)]
 elif name=='product':
  a=J[2,2];sgn=1 if bounds[1][0]>0 else -1;c=s.expand(ft).coeff(U*V);d=a*s.expand(ft).coeff(V*W);expected=[(e,bounds) for e in (correct,ft,ft*sgn*a*V,(c*U+d*V*W/a)*ab,(c*U*V+d*V*W)*ab)]
 else:
  a=J[0,1];c=s.simplify(ft/W);expected=[(correct,bounds),(ft,bounds),(correct,(bounds[0],bounds[1],(1,U*V))),(correct,(bounds[0],bounds[1],(1,s.sqrt(U+V)))),(c*W/(2*a),bounds)]
 for e,b in forms:assert sum(p.same(e,z) and pairs_same(b,b0) for z,b0 in expected)==1,(name,e,b,expected)
 if level!='easy':
  values=[total(e,b) for e,b in forms];assert all(not p.same(z,w) for i,z in enumerate(values) for w in values[:i])
 else:assert all(not p.same(z,w) for i,(z,b) in enumerate(forms) for w,b0 in forms[:i])
 selected=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]);assert p.same(forms[selected][0],correct) and pairs_same(forms[selected][1],bounds)
 n['records']+=1;n['choices']+=5
if __name__=='__main__':
 kp=17592186198397;D=R.parents[2]/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'generator');src=json.load(open(D/'source.json'));assert src==json.load(open(R/'sources'/f'{kp}.json'));old={q[':question/math-academy-id']:q for q in src['record'][':knowledge-point/questions']}
 for c in json.load(open(D/'source-cases.json')):
  rec=g.generate(c['level'],template=c['template'],profile=c['bank_profile'],parameters=c['parameters']);q=rec['question'];o=old[c['source_id']]
  for key in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (key in q)==(key in o)
   if key in o:assert q[key]==(o[key][':db/ident'] if key.endswith('difficulty') else o[key])
  f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
  if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];n['source_refs']+=1
  n['source_prompts']+=1;n['source_values']+=5;n['source_solutions']+=int(':question/worked-solution' in o)
 for item in json.load(open(D/'review.json')):
  rec=item.get('record',item)
  if rec['generation']['eligible_for_learning']:check(rec)
 for level,fs in g.FAMILIES.items():
  for family in fs:
   for seed in range(5):check(g.generate(level,seed=7300+seed,template=family))
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
