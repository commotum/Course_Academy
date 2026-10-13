"""Parent actual maps, full scalar banks and every successive primitive stage."""
import sys,re,json,hashlib,importlib.util
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
def load(file,name):
 z=importlib.util.spec_from_file_location(name,file);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'spatial-jacobian-readback.py','spatial');x,y,z=p.x,p.y,p.z;u,v,w=p.u,p.v,p.w
n=dict(records=0,choices=0,source_prompts=0,source_values=0,source_solutions=0,source_refs=0,formal_inputs=0,jacobian_entries=0,cofactor_minors=0,cofactor_products=0,inverse_rows=0,density_rows=0,primitive_rows=0,endpoint_rows=0,individual_endpoint_components=0,complete_method_banks=0)
def group(text,pos):
 assert text[pos]=='{';start=pos+1;pos=start;depth=1
 while depth:depth+=(text[pos]=='{')-(text[pos]=='}');pos+=1
 return text[start:pos-1],pos
def prompt(text):
 blocks=p.displays(text)
 if blocks:change,integrand,region=[a.strip() for a in blocks]
 else:ins=re.findall(r'\$(.*?)\$',text,re.S);change,integrand,region=ins[0],ins[1],ins[3]
 change=change.replace(r'\quad','').replace(r'\,','');coords=[]
 for target,raw in zip(('u','v','w'),change.split(',')):
  a,b=raw.split('=',1);assert a.strip()==target;coords.append(p.scalar(b))
 integrand=re.sub(r'^\s*(?:\\iiint_R|\{∭\}_\{R\}|∭_\(R\))\s*','',integrand);integrand=re.sub(r'(?:\\,)?(?:\\mathrm\{d\}V|dV),?\s*$','',integrand);F=p.scalar(integrand)
 M=s.Matrix(coords).jacobian((x,y,z));D=s.factor(M.det());assert D!=0;sol=s.solve([a-b for a,b in zip(coords,(u,v,w))],(x,y,z),dict=True);assert len(sol)==1;inv=sol[0]
 region=region.split(':',1)[1].replace(r'\quad','').replace(r'\,','').strip().rstrip('.').rstrip('}').rstrip('\\');bounds=[]
 for var,raw in zip((u,v,w),region.split(',')):
  lo,e,hi=[p.scalar(v) for v in raw.split(r'\le')];e=s.simplify(e.subs(inv,simultaneous=True));factor=s.diff(e,var);assert factor.is_positive and p.same(e,factor*var);bounds.append((lo/factor,hi/factor))
 density=s.simplify(F.subs(inv,simultaneous=True)/s.Abs(D));bounds=tuple(bounds);value=integrate(density,bounds)
 return coords,F,M,D,inv,bounds,density,value
def integrate(fn,b):return s.simplify(s.integrate(fn,(w,*b[2]),(v,*b[1]),(u,*b[0])))
def full_integral(raw,bounds,number):
 pos=0
 for lo,hi in bounds[:number]:
  assert raw[pos:].startswith(r'\int_');pos+=5;l,pos=group(raw,pos);assert raw[pos]=='^';h,pos=group(raw,pos+1);assert p.same(p.scalar(l),lo) and p.same(p.scalar(h),hi)
 tail=raw[pos:];suffix=''.join(r'\,\mathrm{d}'+a for a in reversed(('u','v','w')[:number]))
 assert tail.endswith(suffix) if suffix else True
 tail=tail[:-len(suffix)] if suffix else tail
 return tail
def unwrap(raw):
 raw=raw.replace(r'\left','').replace(r'\right','').strip()
 if raw.startswith('('):
  depth=0
  for i,c in enumerate(raw):
   depth+=(c=='(')-(c==')')
   if depth==0:
    if i==len(raw)-1:return raw[1:-1]
    break
 return raw
def scalar_body(raw):return p.scalar(unwrap(raw))
def split_terms(raw):
 raw=raw.replace(r'\left','').replace(r'\right','').strip();depth=0;start=0;parts=[]
 for i,c in enumerate(raw):
  if c in '({[':depth+=1
  elif c in ')}]':depth-=1
  elif c in '+-' and depth==0 and i>start:parts.append(raw[start:i]);start=i
 parts.append(raw[start:]);return parts
def check(rec):
 q=rec['question'];meta=rec['generation'];coords,F,M,D,inv,bounds,density,answer=prompt(q[':question/problem']);f=q[':question/answer-fields'][0];vs=[p.scalar(a[':answer/value']) for a in f[':answer-field/choices']];assert len(vs)==5 and all(not p.same(a,b) for i,a in enumerate(vs) for b in vs[:i]);hits=[i for i,a in enumerate(vs) if p.same(a,answer)];assert len(hits)==1
 if ':answer-field/correct' in f:assert f[':answer-field/choices'][hits[0]][':answer/id']==f[':answer-field/correct'][1]
 else:assert meta['evidence_only'] and not meta['eligible_for_learning']
 if not meta['eligible_for_learning']:n['raw_math_records']=n.get('raw_math_records',0)+1;return
 name=meta['template'];J=1/s.Abs(D);c=M[2,2];wrong=[integrate(density/J,bounds),integrate(density/J*s.Abs(D),bounds)]
 if name=='power':degree=s.degree(density,u);wrong+= [(degree+1)*answer,answer/c if degree==1 else 2*answer]
 elif name=='vcosu':wrong+=[integrate(-J*v*s.sin(u),bounds),2*answer]
 elif name=='ucosv':wrong+=[2*answer,integrate(-J*u*s.sin(v),bounds)]
 elif name=='sum':wrong+=[integrate(J*w,bounds),integrate(J*u,bounds)]
 elif name=='exp':wrong+=[J*s.exp(bounds[0][1])*(bounds[1][1]**2-bounds[1][0]**2)/2*(bounds[2][1]-bounds[2][0]),2*answer]
 elif name=='zcosu':wrong+=[integrate(J*w*w*s.cos(u),bounds),3*answer]
 elif name=='sinsin':wrong+=[answer/c,-answer]
 else:raise AssertionError(name)
 assert all(sum(p.same(a,b) for b in [answer]+wrong)==1 for a in vs);n['complete_method_banks']+=1
 sol=q[':question/worked-solution'];sec=sol.split('**Step 2**:')[1].split('**Step 3**:')[0];mats=re.findall(r'\\begin\{vmatrix\}(.*?)\\end\{vmatrix\}',sec,re.S);assert len(mats)==3
 formal=re.findall(r'\\frac\{\\partial ([uvw])\}\{\\partial ([xyz])\}',mats[0]);assert formal==[(a,b) for a in 'uvw' for b in 'xyz'];n['formal_inputs']+=9
 matrix=lambda a:s.Matrix([[p.scalar(z) for z in row.split('&')] for row in a.split(r'\\')]);assert matrix(mats[1])==M and matrix(mats[2])==M[:2,:2];n['jacobian_entries']+=9;n['cofactor_minors']+=1
 factor=sec.split(r'\begin{vmatrix}',2)[1] # Full first-row matrix prefix is not a factor.
 expansion=sec.split(r' \\  & =')[2];prefix=expansion.split(r'\begin{vmatrix}',1)[0];assert p.same(p.scalar(prefix),M[2,2]);n['cofactor_products']+=1
 tail=sec.rsplit(r'\end{vmatrix}',1)[1].split(r' \\  & =');assert p.same(p.scalar(tail[1]),D) and p.same(p.scalar(tail[2].split(r'\end{aligned}')[0]),D)
 sec3=sol.split('**Step 3**:')[1].split('**Step 4**:')[0];shown=sec3.split(r'\right)^{-1}=',1)[1].split('.',1)[0];assert p.same(p.scalar(shown),1/D);n['inverse_rows']+=1
 sec4=sol.split('**Step 4**:')[1];arith=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sec4,re.S)[0];rows=arith.split(r' \\ ');assert len(rows)==15
 first=rows[0].split(' & =',1)[1].split(r'\iiint_\Delta ',1)[1];fshown,jshown=first.split(r'\cdot \left|',1);js=p.scalar(jshown.split(r'\right|',1)[0]);assert p.same(js,1/D) and p.same(p.scalar(fshown)*s.Abs(js),density)
 second=rows[1].split(r'\iiint_\Delta ',1)[1].split(r'\,\mathrm{d}',1)[0];assert p.same(p.scalar(second),density);n['density_rows']+=2
 full=rows[2].split(' & =',1)[1];assert p.same(scalar_body(full_integral(full,bounds,3)),density)
 current=density
 for pos,var,offset in ((2,w,3),(1,v,7),(0,u,11)):
  body=full_integral(rows[offset].split(' & =',1)[1],bounds,pos)
  if body.startswith(r'\left(') and body.endswith(r'\right)'):body=body[len(r'\left('):-len(r'\right)')]
  prim=body.split(r'\left[',1)[1].split(r'\right]',1)[0];primitive=p.scalar(prim);assert p.same(s.diff(primitive,var),current)
  suffix=body.split(r'\right]',1)[1];assert suffix.startswith('_');lo,end=group(suffix,1);assert suffix[end]=='^';hi,end=group(suffix,end+1)
  for value in (lo,hi):assert value.startswith(('u','v','w')[pos]+'=')
  lo=lo.split('=',1)[1];hi=hi.split('=',1)[1];assert end==len(suffix) and p.same(p.scalar(lo),bounds[pos][0]) and p.same(p.scalar(hi),bounds[pos][1]),(body,suffix,end,bounds,pos);n['primitive_rows']+=1
  expected=s.simplify(primitive.subs(var,bounds[pos][1])-primitive.subs(var,bounds[pos][0]));terms=s.Add.make_args(s.expand(primitive))
  for rowidx in (offset+1,offset+2,offset+3):
   raw=full_integral(rows[rowidx].split(' & =',1)[1],bounds,pos);assert p.same(scalar_body(raw),expected);n['endpoint_rows']+=1
   raw=unwrap(raw)
   if rowidx in (offset+1,offset+2):
    parts=split_terms(raw);assert len(parts)==2*len(terms),(raw,parts,terms)
    wanted=[value for term in terms for value in (term.subs(var,bounds[pos][1]),-term.subs(var,bounds[pos][0]))]
    for rawpart in parts:
     value=p.scalar(rawpart);indices=[i for i,z in enumerate(wanted) if p.same(value,z)];assert indices,(rawpart,value,wanted);wanted.pop(indices[0]);n['individual_endpoint_components']+=1
    assert not wanted
  if q[':question/difficulty'].endswith('hard'):assert all(s.simplify(term.subs(var,bounds[pos][0]))!=0 for term in terms)
  current=expected
 assert p.same(current,answer);n['records']+=1;n['choices']+=5
if __name__=='__main__':
 kp=17592186198398;D=R.parents[2]/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'generator');src=json.load(open(D/'source.json'));assert src==json.load(open(R/'sources'/f'{kp}.json'));old={str(q[':db/id']):q for q in src['record'][':knowledge-point/questions']} | {q[':question/math-academy-id']:q for q in src['record'][':knowledge-point/questions']}
 for c in json.load(open(D/'source-cases.json')):
  rec=g.generate(c['level'],template=c['template'],profile=c['bank_profile'],parameters=c['parameters']);check(rec);q=rec['question'];o=old[c['source_id']]
  for key in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (key in q)==(key in o)
   if key in o:assert q[key]==(o[key][':db/ident'] if key.endswith('difficulty') else o[key])
  f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
  if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];n['source_refs']+=1
  n['source_prompts']+=1;n['source_values']+=5;n['source_solutions']+=int(':question/worked-solution' in o)
 for item in json.load(open(D/'review.json'))['generated_variants']:check(item.get('record',item))
 for level in g.LEVELS:
  for family in (('power',) if level=='easy' else g.FAMILIES):
   for seed in range(3):check(g.generate(level,seed=44000+seed,template=family))
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
