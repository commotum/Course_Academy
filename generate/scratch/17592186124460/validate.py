#!/usr/bin/env python3
"""Read displayed math independently, all source fields, identities and native grading."""
import copy, hashlib, importlib.util, json, re, subprocess, sys, uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('g',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,i,j=sp.symbols('x y i j',real=True)
TRANS=standard_transformations+(implicit_multiplication_application,)
LOCAL=dict(x=x,y=y,i=i,j=j,pi=sp.pi,e=sp.E,sin=sp.sin,cos=sp.cos,tan=sp.tan,sec=sp.sec,ln=sp.log,sqrt=sp.sqrt)

def eq(a,b):assert sp.simplify(a-b)==0,(a,b)
def group(s,start):
 assert s[start]=='{',s[start:];depth=1;k=start+1
 while depth:
  assert k<len(s),s
  if s[k]=='{':depth+=1
  elif s[k]=='}':depth-=1
  k+=1
 return s[start+1:k-1],k

def math(s):
 s=s.strip().rstrip('.').replace('⁡','').replace('π',r'\pi').replace('−','-').replace(r'\,','').replace(r'\!','')
 s=s.replace(r'\left','').replace(r'\right','')
 s=re.sub(r'\\operatorname\{(sin|cos|tan|ln)\}',r'\\\1',s)
 s=s.replace('{sec}',r'\sec');s=re.sub(r'\\text\{[^}]*\}','',s)
 # TeX sec^2 x must become (sec(x))^2; parse separately before normal commands.
 s=re.sub(r'\\sec\^\{2\}\(([^()]+)\)',r'(sec(\1))^2',s)
 s=re.sub(r'\\sec\^\{2\}([xy])',r'(sec(\1))^2',s)
 out='';k=0
 while k<len(s):
  if s.startswith(r'\frac',k):
   a,n=group(s,k+5);b,n=group(s,n);out+='(('+convert(a)+')/('+convert(b)+'))';k=n
  elif s.startswith(r'\sqrt',k):a,n=group(s,k+5);out+='sqrt('+convert(a)+')';k=n
  elif s[k]=='{':a,n=group(s,k);out+='('+convert(a)+')';k=n
  else:out+=s[k];k+=1
 out=out.replace(r'\cdot','*').replace('^','**')
 for cmd in ('sin','cos','tan','sec','ln'):out=out.replace('\\'+cmd,' '+cmd+' ')
 out=out.replace(r'\pi',' pi ')
 out=re.sub(r'(?<=\d)(?=[ij])','*',out)
 assert '\\' not in out and not re.search(r'[∂∇⟨⟩‖]',out),out
 return sp.simplify(parse_expr(out,local_dict=LOCAL,transformations=TRANS))
def convert(s):
 # Recursive math conversion can print expressions, retaining free symbols.
 return str(math(s))

def split_top(s,separator=','):
 s=s.replace(r'\,','')
 depth=0;ans=[];start=0
 for k,c in enumerate(s):
  if c in '({':depth+=1
  elif c in ')}':depth-=1
  elif c==separator and depth==0:ans.append(s[start:k]);start=k+1
 ans.append(s[start:]);return ans

def vector(s):
 s=s.strip();m=re.search('⟨(.*?)⟩',s)
 if m:
  parts=split_top(m[1]);assert len(parts)==2,s
  scale=s[:m.start()].strip();assert not s[m.end():].strip(),s
  if scale.endswith(r'\cdot'):scale=scale[:-5]
  c=math(scale) if scale else sp.Integer(1)
  return tuple(c*math(z) for z in parts)
 e=sp.expand(math(s));assert e.subs({i:0,j:0})==0 and sp.Poly(e,i,j).total_degree()<=1,s
 return tuple(e.coeff(z) for z in (i,j))

def formatting(s):
 assert not any(ord(c)<32 and c not in '\n\t' for c in s),'C0 character'
 assert s.count('$')%2==0
 depth=0
 for c in s:
  if c=='{':depth+=1
  elif c=='}':depth-=1
  assert depth>=0,s
 assert depth==0,s
 assert '--' not in s and '+-' not in s,s
 assert not re.search(r'\\\\[A-Za-z]',s),s

def printed(rec):
 q=rec['question'];p=q[':question/problem']
 first=re.search(r'\$([fg])\(x, ?y\)\s*=\s*(.*?)\$',p);assert first,p
 F=math(first[2]);point=re.search(r'at the point \$\((.*?)\)\$',p);h,k=map(math,split_top(point[1]));grad=tuple(sp.diff(F,z) for z in (x,y));E=tuple(sp.simplify(z.subs({x:h,y:k})) for z in grad)
 V=re.search(r'v\s*=\s*⟨([^⟩]+)⟩',p)
 if V:
  v=tuple(map(math,split_top(V[1])));N=sp.sqrt(sum(z*z for z in v));u=tuple(z/N for z in v);ans=sp.simplify(sum(a*b for a,b in zip(E,u)));mode='vector'
 else:v=None;N=None;u=None;mode='increase' if 'increases' in p else 'decrease';ans=sp.sqrt(sum(z*z for z in E))*(1 if mode=='increase' else -1)
 return F,(h,k),grad,E,v,N,u,sp.simplify(ans),mode

def signed_terms(s):
 s=s.replace(r'\,','');depth=0;ans=[];start=0
 for n,c in enumerate(s):
  if c in '({':depth+=1
  elif c in ')}':depth-=1
  elif c in '+-' and depth==0 and n>start:
   ans.append(s[start:n]);start=n
 ans.append(s[start:]);return ans

def operations_from_prompt(F,P,E,v,N,ans,t):
 h,k=P;A,B=E
 dot=lambda a,b:sp.simplify((a*v[0]+b*v[1])/N)
 if t=='quotient':
  c=sp.cancel(F*y/x**2);assert c.is_Integer and 1<=c<=4
  return [ans,dot(-A,B),dot(A,-B),A*v[0]+B*v[1],dot(A,-c*h/k**2)]
 if t=='ratio_sum':
  eq(F,x/y+y/x)
  return [ans,dot(1/k+k/h**2,B),dot(A,1/h+h/k**2),dot(1/k+k/h**2,1/h+h/k**2),N]
 if t=='sine_quotient':
  a=sp.simplify(F.coeff(sp.sin(sp.pi*x))*y);b=sp.simplify((F-a*sp.sin(sp.pi*x)/y)/(sp.pi*x*y));assert a.is_Integer and b.is_Integer and 1<=a<=4 and 1<=b<=4
  return [ans,A*v[0]+B*v[1],-ans,dot(b*sp.pi*k,B),(A*v[0]+B*v[1])/N**2]
 if t=='tangent':
  a=sp.simplify(F.coeff(sp.tan(y))/x);eq(F,a*x*sp.tan(y)-a*y*sp.tan(x));assert a.is_Integer and 1<=a<=6
  return [ans,A*v[0]+B*v[1],-ans,dot(a*sp.tan(k),-a*sp.tan(h)),dot(-2*a*k,2*a*h)]
 if t=='exp_bilinear':
  atoms=list(F.atoms(sp.exp));assert len(atoms)==1;ex=atoms[0];b=sp.diff(ex.args[0],x);eq(ex.args[0],b*x-y);a=sp.simplify((F-ex)/(x*y));assert 2<=a<=6 and 2<=b<=5 and A<=30 and B<=12;eq(k,b*h)
  return [ans,-ans,-sp.sqrt((a*k+1)**2+(a*h-1)**2),-sp.sqrt(b*b+1),-abs(A)]
 if t=='sumlog':
  logs=list(F.atoms(sp.log));assert len(logs)==1;arg=logs[0].args[0];a,b=sp.diff(arg,x),sp.diff(arg,y);eq(arg,a*x+b*y);eq(F,arg*sp.log(arg));eq(a*h+b*k,1);assert a.is_Integer and b.is_Integer and 1<=a<=8 and 1<=b<=8
  return [ans,-ans,0,-abs(A),-(A+B)]
 c=sp.simplify(F/sp.sin(y*sp.log(x)));n=sp.log(h);assert c.is_Integer and 1<=c<=4 and n.is_Integer and 1<=n<=4
 return [ans,c*sp.sqrt(k*k+n*n),c*sp.sqrt((k/h)**2+h*h),abs(A)+abs(B),abs(A)]

def inspect(rec,raw=False):
 assert set(rec['knowledge_point'])=={'db_id','id','title'};assert rec['knowledge_point']['db_id']==g.KP_ID
 q=rec['question'];F,P,grad,E,v,N,u,ans,mode=printed(rec)
 formatting(q[':question/problem']);uuid.UUID(q[':question/id']);f=q[':question/answer-fields'][0];uuid.UUID(f[':answer-field/id']);assert f[':answer-field/type']==':answer-field.type/radio'
 values=[math(a[':answer/value']) for a in f[':answer-field/choices']];assert len(values)==5
 for n,a in enumerate(values):
  assert not a.has(sp.zoo,sp.oo,sp.nan) and a.is_real
  for b in values[:n]:assert sp.simplify(a-b)!=0
 if not rec['generation']['evidence_only']:
  wanted=operations_from_prompt(F,P,E,v,N,ans,rec['generation']['template'])
  for value in values:assert sum(sp.simplify(value-sp.sympify(w))==0 for w in wanted)==1,(value,wanted)
 expected=-ans if raw and mode=='decrease' else ans
 match=[a[':answer/id'] for a,z in zip(f[':answer-field/choices'],values) if sp.simplify(z-expected)==0];assert len(match)==1,(mode,ans,values)
 if ':answer-field/correct' in f:assert f[':answer-field/correct']==[':answer/id',match[0]]
 else:assert raw
 for a in f[':answer-field/choices']:
  formatting(a[':answer/value']);assert '$' not in a[':answer/value'];uuid.UUID(a[':answer/id']);assert a[':answer/type']==':answer.type/math'
 if ':question/worked-solution' not in q:assert raw;return ans
 sol=q[':question/worked-solution'];formatting(sol)
 for coord in re.findall(r'[fg]\(([^()]*)\)',sol):
  if coord.replace(' ','')=='x,y':continue
  if ',' in coord:
   got=tuple(map(math,split_top(coord)))
   for a,b in zip(got,P):eq(a,b);blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(blocks)==(3 if v else 2)
 # Every introductory/concluding coordinate is independently read from prose.
 for p in re.findall(r'(?:point \$|[fg]\()\((.*?)\)\$',sol):
  if ',' in p:
   try:point=tuple(map(math,split_top(p)));assert point==P,(point,P)
   except (SyntaxError,ValueError):raise AssertionError(('prose coordinates',p))
 if v:
  rows=blocks[0].split(chr(92)*2);assert len(rows)==2
  rhs=rows[0].split('& =')[1];a,b=rhs.split('=');eq(math(a),N);eq(math(b),N)
  for aa,bb in zip(vector(rows[1].split('& =')[1]),u):eq(aa,bb)
 b=blocks[1] if v else blocks[0];rows=b.split(chr(92)*2)
 wantcount={'quotient':4,'ratio_sum':4,'sine_quotient':5,'tangent':5,'sinlog':4,'exp_bilinear':4,'sumlog':4}[rec['generation']['template']];assert len(rows)==wantcount
 sign=-1 if mode=='decrease' else 1
 formal=rows[0].split('& =')[1]
 # Extract full operands from each formal partial, not just a final gradient.
 for z in ('x','y'):
  op=r'\frac{∂}{∂'+z+'}';assert op in formal,formal
  assert ('-'+op in formal)==(mode=='decrease'),formal
  segment=formal.split(op,1)[1];assert segment.startswith('(');dep=1;k=1
  while dep:
   if segment[k]=='(':dep+=1
   if segment[k]==')':dep-=1
   k+=1
  eq(math(segment[1:k-1]),F)
 general=vector(rows[1].split('& =')[1])
 for a,b in zip(general,grad):
  # Raw q37083 deliberately retains source's missing signs; this exception has
  # its own failure finding, never applies to normal output.
  eq(a,b if raw and rec['generation']['template']=='sumlog' else sign*b)
 sub=vector(rows[2].split('& =')[1]);final=vector(rows[-1].split('& =')[1])
 for a,b in zip(sub,E):eq(a,sign*b)
 for a,b in zip(final,E):eq(a,sign*b)
 # Independently check each individually evaluated trig component, before sums.
 if len(rows)==5:
  mid=rows[3].split('& =')[1];vv=vector(mid)
  for a,b in zip(vv,E):eq(a,b)
  pieces=split_top(re.search('⟨(.*?)⟩',mid)[1]);subparts=split_top(re.search('⟨(.*?)⟩',rows[2].split('& =')[1])[1])
  # derivative substitution operations must survive: tangent tan/sec product,
  # sine quotient cos/pi + second polynomial term; equality alone insufficient.
  if rec['generation']['template']=='tangent':assert r'\operatorname{tan}' in rows[2] and '{sec}^{2}' in rows[2] and r'\cdot' in rows[3]
  else:assert r'\operatorname{cos}' in rows[2] and r'\operatorname{sin}' in rows[2] and ',' in mid
  for a,b in zip(pieces,subparts):
   eq(math(a),math(b));ma=signed_terms(a);sb=signed_terms(b);assert len(ma)==len(sb)==2,(ma,sb)
   for term,source_term in zip(ma,sb):eq(math(term),math(source_term))
 # Read evaluation coordinate labels as actual math, independently from metadata.
 lhs=rows[2].split('&')[0];m=re.search(r'[fg]\((.*?)\)',lhs);assert m,lhs
 for a,b in zip(map(math,split_top(m[1])),P):eq(a,b)
 calc=blocks[-1].split(chr(92)*2)
 if v:
  assert len(calc)==(5 if rec['generation']['template']=='tangent' else 4)
  dot=calc[1].split('& =')[1];left,right=dot.split(r'\cdot',1)
  for a,b in zip(vector(left),E):eq(a,b)
  for a,b in zip(vector(right),u):eq(a,b)
  # Every numeric dot-product factor must equal the printed gradient/direction
  # factors, not only their final sum. Split source numerator at top-level plus.
  arithmetic=calc[2].split('& =')[1];eq(math(arithmetic),ans)
  assert r'\frac{' in arithmetic and (r'\cdot' in arithmetic or rec['generation']['template']=='ratio_sum')
  # Numerator terms are the two independently computed coordinate products.
  m=arithmetic.index('{');num,_=group(arithmetic,m);den_start=group(arithmetic,m)[1];den,_=group(arithmetic,den_start)
  terms=split_top(num,'+');assert len(terms)==2,(num,terms)
  coeff=math(den);actual_products=[math(z) for z in terms];desired=[sp.simplify(E[n]*u[n]*coeff) for n in (0,1)]
  for a,b in zip(actual_products,desired):eq(a,b)
  for row in calc[3:]:eq(math(row.split('& =')[1]),ans)
 else:
  assert len(calc)==3
  rhs=calc[0].split('& =')[1].strip();assert rhs.startswith('‖') and rhs.endswith('‖')
  for a,b in zip(vector(rhs[1:-1]),E):eq(a,sign*b)
  squ=calc[1].split('& =')[1];m=squ.index('{');body,_=group(squ,m);components=split_top(body,'+');assert len(components)==2
  for a,b in zip(components,E):eq(math(a),b*b)
  eq(math(squ),sp.sqrt(sum(z*z for z in E)));eq(math(calc[2].split('& =')[1]),sp.sqrt(sum(z*z for z in E)))
  if mode=='decrease' and not raw:
   final=re.search(r'Therefore, the signed rate .*? is \$(.*?)\.\$',sol);assert final,sol;eq(math(final[1]),ans)
 # End-to-end record identity derives from actual displayed content. Shuffle/seed
 # tests below ensure rendering order is excluded from content identity.
 assert rec['generation']['eligible_for_learning']==(not rec['generation']['evidence_only'])
 return ans

def identity(rec):
 q=rec['question'];f=q[':question/answer-fields'][0];selected=f.get(':answer-field/correct');correct=next((a[':answer/value'] for a in f[':answer-field/choices'] if selected and a[':answer/id']==selected[1]),None)
 payload=dict(version=g.VERSION,level=q.get(':question/difficulty'),problem=q[':question/problem'],solution=q.get(':question/worked-solution'),bank=sorted(a[':answer/value'] for a in f[':answer-field/choices']),field_type='radio',correct_present=selected is not None,correct_value=correct)
 h=g.digest(payload);assert h==rec['generation']['content_identity'];assert q[':question/id']==g.uid(h);assert f[':answer-field/id']==g.uid(h+'/selection')
 for a in f[':answer-field/choices']:assert a[':answer/id']==g.uid(h+'/selection/'+a[':answer/value'])

def radio_checks(rec):
 f=rec['question'][':question/answer-fields'][0]
 return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'native radio ID against independently verified complete displayed bank'} for a in f[':answer-field/choices']]

def save(name,obj):(D/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def main():
 review=[];cases=[];source_fidelity=[];native=[];count=0;fps={l:set() for l in ('easy','moderate','hard')};records=[]
 for sid,(t,p) in g.ANCHORS.items():
  l=g.TEMPLATES[t];old=g.SOURCES[sid];rec=g.generate(l,template=t,parameters=p,profile='raw-'+sid);q=rec['question'];inspect(rec,True);identity(rec)
  for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in old),(sid,key)
  assert q[':question/problem']==old[':question/problem'];assert q.get(':question/worked-solution')==old.get(':question/worked-solution')
  of=old[':question/answer-fields'][0];f=q[':question/answer-fields'][0];assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
  assert f[':answer-field/key']==of[':answer-field/key'];assert f[':answer-field/type']==of[':answer-field/type'][':db/ident']
  if ':answer-field/correct' in of:
   actual=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert actual==of[':answer-field/correct'][':answer/value']
  if ':question/difficulty' in old:assert q[':question/difficulty']==old[':question/difficulty'][':db/ident']
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices'])
  cases.append({'source_id':sid,'source_db_id':old[':db/id'],'source_question_uuid':old[':question/id'],'template':t,'parameters':p,'bank_profile':'raw-'+sid,'level':l,'level_origin':'observed' if ':question/difficulty' in old else 'authored replay routing; raw difficulty absent'})
  source_fidelity.append({'source_id':sid,'exact_prompt':True,'complete_bank_exact':True,'displayed_values_matched':5,'available_solution_exact':':question/worked-solution' in old,'attribute_presence_parity':True,'correct_designation_matched':':answer-field/correct' in of,'mathematically_correct_source':t not in ('exp_bilinear','sumlog')})
  review.append({'label':'Original '+sid+'; raw public replay; ineligible evidence','record':rec,'raw_capture':old})
  if ':answer-field/correct' in f:native.append({'label':'Raw source '+sid+' (documented teaching errors retained)','record':rec,'checks':radio_checks(rec)})
  # Raw recipes have changed-parameter witnesses, same public interface.
  changed=dict(p)
  if t in ('quotient','sinlog'):changed['c']=1 if t=='sinlog' else 2;changed['j']=2 if t=='sinlog' else None;changed.pop('j',None) if t=='quotient' else None
  elif t=='ratio_sum':changed['h']='1'
  elif t=='sine_quotient':changed['b']=2
  elif t=='tangent':changed['a']=3
  else:changed['a']=3
  vr=g.generate(l,template=t,parameters=changed,profile='raw-'+sid);inspect(vr,True);assert vr['question'][':question/problem']!=q[':question/problem'];review.append({'label':'Changed parameter raw-profile evidence '+sid,'record':vr})
  completed=g.generate(l,template=t,parameters=p,profile='completed-'+sid);inspect(completed);identity(completed);native.append({'label':'Inferred historical-key completion '+sid,'record':completed,'checks':radio_checks(completed)})
  normal=g.generate(l,seed=61,template=t,parameters=p);inspect(normal);identity(normal);review.append({'label':'Authored/mathematically repaired source-shaped anchor '+sid,'record':normal});native.append({'label':'Eligible normal anchor '+sid,'record':normal,'checks':radio_checks(normal)});count+=1
 for t,l in g.TEMPLATES.items():
  print('Checking',t,flush=True)
  for seed in range(60):
   rec=g.generate(l,seed=seed+700,template=t);inspect(rec);identity(rec);records.append(rec);fps[l].add(rec['generation']['mathematical_fingerprint']);count+=1
   if seed<2:review.append({'label':'Generated '+l+' / '+t+' / '+str(seed),'record':rec});native.append({'label':'Generated '+t+' '+str(seed),'record':rec,'checks':radio_checks(rec)})
   p=rec['generation']['parameters'];again=g.generate(l,seed=seed+9000,template=t,parameters=p);assert again['question'][':question/id']==rec['question'][':question/id'];assert again['generation']['mathematical_fingerprint']==rec['generation']['mathematical_fingerprint']
 # Default family coverage, scalar positive common direction scale invariance.
 coverage={l:set() for l in fps}
 for l in coverage:
  for seed in range(50):coverage[l].add(g.generate(l,seed=seed)['generation']['template'])
  assert coverage[l]=={t for t,a in g.TEMPLATES.items() if a==l}
 for t in ('quotient','ratio_sum','sine_quotient','tangent'):
  r=next(r for r in records if r['generation']['template']==t);p=dict(r['generation']['parameters']);p['v1']=str(2*g.expr(p['v1']));p['v2']=str(2*g.expr(p['v2']));r2=g.generate(g.TEMPLATES[t],template=t,parameters=p)
  assert r['generation']['mathematical_fingerprint']==r2['generation']['mathematical_fingerprint'];assert r['question'][':question/id']!=r2['question'][':question/id']
 r=g.generate('hard',template='sumlog',parameters=dict(a=3,b=2,h=1));r2=g.generate('hard',template='sumlog',parameters=dict(a=3,b=2,h=3));assert r['generation']['mathematical_fingerprint']==r2['generation']['mathematical_fingerprint'];assert r['question'][':question/id']!=r2['question'][':question/id']
 positions={l:set() for l in fps}
 for r in records:
  f=r['question'][':question/answer-fields'][0];positions[g.TEMPLATES[r['generation']['template']]].add(next(n for n,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
 assert all(p==set(range(5)) for p in positions.values())
 # Negative controls remove a real operation, alter component signs/factors and
 # final prose while preserving row count; validation must reject each mutation.
 mutations=[]
 for t,field,old,new in [('sumlog',':question/worked-solution',' & =-',' & ='),('exp_bilinear',':question/worked-solution','Therefore, the signed rate','Therefore, the unsigned rate'),('sine_quotient',':question/worked-solution',r'\operatorname{cos}',r'\operatorname{sin}'),('tangent',':question/worked-solution','{sec}^{2}','{sec}^{3}'),('quotient',':question/worked-solution',r'\frac{∂}{∂x}',r'\frac{∂}{∂y}'),('ratio_sum',':question/worked-solution',r'\cdot u',r'\cdot u\x0c')]:
  r=copy.deepcopy(next(r for r in records if r['generation']['template']==t));assert old in r['question'][field];r['question'][field]=r['question'][field].replace(old,new,1)
  if t=='ratio_sum':r['question'][field]+='\x0c'
  try:inspect(r)
  except Exception:mutations.append(t)
  else:raise AssertionError(('negative control survived',t))
 # All rendered constants/bank coefficients actual runtime is exact SymPy math;
 # deliberately reject silent coercion, unsupported difficulty and explicit bounds.
 rejected=0
 for l,t,p in [('easy','quotient',dict(c=0,h=2,k=1,v1=-1,v2=3)),('moderate','sine_quotient',dict(a=0,b=1,h=1,k=1,v1=-1,v2=1)),('hard','sumlog',dict(a=9,b=1,h=2)),('hard','exp_bilinear',dict(a=6,b=5,h=4)),('easy','quotient',dict(c=1,h=2,k=1,v1='e',v2=1)),('moderate','tangent',dict(a=2,h=0,k=0,v1=-1,v2=1))]:
  try:g.generate(l,template=t,parameters=p)
  except (ValueError,AssertionError):rejected+=1
  else:raise AssertionError('invalid explicit workload allowed')
 missing_native=[]
 for sid in ('q-36297','q-37074'):
  t,p=g.ANCHORS[sid];r=g.generate(g.TEMPLATES[t],template=t,parameters=p,profile='raw-'+sid);save('missing-key-'+sid+'-input.json',[{'label':sid,'record':r,'checks':[]}]);run_missing=subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(D/('missing-key-'+sid+'-input.json')),str(D/('missing-key-'+sid+'-output.json'))],text=True,capture_output=True);assert run_missing.returncode!=0 and 'correct lookup ref required' in run_missing.stderr;missing_native.append({'source_id':sid,'exit_code':run_missing.returncode,'reason':run_missing.stderr.strip(),'interpretation':'native fixture cannot instantiate absent correct lookup; no actual grade_field result exists for raw source'})
 save('missing-native-keys.json',missing_native)
 save('source-cases.json',cases);save('source-fidelity.json',source_fidelity);save('review.json',review);save('engine-input.json',native)
 run=subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(D/'engine-input.json'),str(D/'engine-report.json')],text=True,capture_output=True);(D/'engine.log').write_text(run.stdout+run.stderr);assert run.returncode==0,run.stderr
 engine=json.loads((D/'engine-report.json').read_text())
 text=['# Directional-rate generator review\n\nRaw originals are ineligible evidence. Changed raw witnesses prove recipe replay; normal anchors and variants use authored complete operation banks. Hard normal solutions retain the source norm chain and conclude with the negative signed rate.\n']
 for row in review:text+=['\n## '+row['label']+'\n\n',g.markdown(row['record'])+'\n']
 (D/'review.md').write_text(''.join(text))
 save('validation.json',{'passed':True,'basis':1356,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'source_coverage':{'practice_sources':7,'exact_prompts':7,'complete_banks_exact':7,'displayed_values_matched':35,'displayed_values_total':35,'captured_distractors_matched':20,'captured_distractors_total':20,'inferred_unrated_distractors_matched':8,'inferred_unrated_distractors_total':8,'available_solutions_exact':5,'available_solutions_total':5,'attribute_presence_parity':7,'available_correct_designations_matched':5,'available_correct_designations_total':5,'independently_inferred_missing_keys':2,'authored_missing_solutions':2,'correct_signed_source_questions':5,'signed_rate_source_errors':2,'formal_partial_sign_source_errors':1},'normal_math_records_checked':count,'all_five_radio_positions_reached_per_level':True,'sampled_distinct_tasks_lower_bound':{l:len(a) for l,a in fps.items()},'default_family_coverage':{l:sorted(v) for l,v in coverage.items()},'positive_direction_scaling_deduplicated':True,'log_product_level_line_displacement_deduplicated':True,'exponential_finite_task_domain':39,'log_product_finite_meaningful_coefficient_domain':64,'negative_controls_detected':mutations,'explicit_invalid_inputs_rejected':rejected,'native_grading':{k:engine[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},'raw_native_skipped_missing_key_count':2,'raw_native_false_key_math_count':2,'plots':'none','limitations':['Two fastest-decrease sources report positive norms; retained as evidence only, normal signed rates repaired.','q37083 formal partial reduction drops both minus signs; raw retained, normal repaired.','Two unrated source solutions and correct refs absent; authored completion uses independent mathematics, original widgets supply no additional keys/solutions.','Historical scalar banks have unresolved wrong-operation intentions; public evidence profiles only.','Native radio selection establishes engine contract but does not assess displayed math; independent displayed-formula checks do.'],'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (D.with_suffix('.py'),Path(__file__),D/'source.json',ROOT/'generate/runs/current/check-engine',ROOT/'generate/runs/current/check-engine.rs')}})
 print('Validated',count,'normal instances;',len(review),'review records;',run.stdout.strip())
if __name__=='__main__':main()
