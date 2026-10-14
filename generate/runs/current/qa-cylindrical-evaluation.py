"""Root actual cylindrical calculus, full banks and individual primitive endpoints."""
import json,re,sys,hashlib,importlib.util
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186129278;D=ROOT/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);sys.modules[name]=m;z.loader.exec_module(m);return m
b=load(R/'qa-cylindrical-setup.py','cylinder_eval_parent');p=b.p;x,y,z,r,theta=b.x,b.y,b.z,b.r,b.theta;math,eq=b.math,b.eq

def raw(g):
 old={q[':db/id']:q for q in json.loads((R/f'sources/{K}.json').read_text())['record'][':knowledge-point/questions']};C=dict(prompts=0,solutions=0,fields=0,values=0,keys=0,missing_keys=0,missing_ratings=0)
 for case in json.loads((D/'source-cases.json').read_text()):
  o=old[case['source_id']];q=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])['question']
  for k in (':question/problem',':question/worked-solution',':question/answer-fields',':question/difficulty'):assert (k in o)==(k in q)
  assert q[':question/problem']==o[':question/problem'];C['prompts']+=1
  if ':question/worked-solution' in o:assert q[':question/worked-solution']==o[':question/worked-solution'];C['solutions']+=1
  if ':question/difficulty' not in o:C['missing_ratings']+=1
  for f,f0 in zip(q[':question/answer-fields'],o[':question/answer-fields']):
   assert f[':answer-field/type']==f0[':answer-field/type'][':db/ident'] and f[':answer-field/key']==f0[':answer-field/key'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in f0[':answer-field/choices']);C['fields']+=1;C['values']+=len(f0[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in f0)
   if ':answer-field/correct' in f0:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==f0[':answer-field/correct'][':answer/value'];C['keys']+=1
   else:C['missing_keys']+=1
 return C

def integrals(raw):
 raw=raw.strip().rstrip('.,');vals=[];cursor=0
 while raw[cursor:].startswith(r'\int'):
  cursor+=4;assert raw[cursor]=='_';lo,cursor=p.group(raw,cursor+1);assert raw[cursor]=='^';hi,cursor=p.group(raw,cursor+1);vals.append((math(lo),math(hi)))
 return vals,re.sub(r'\\,d(?:z|r|\\theta)','',raw[cursor:])
def bracket(raw):
 start=raw.index('[');end=raw.rindex(']');factor=math(raw[:start]) if start else s.Integer(1);primitive=math(raw[start+1:end]);tail=raw[end+1:];assert tail.startswith('_{');lo,i=p.group(tail,1);assert tail[i]=='^';hi,i=p.group(tail,i+1);lv,lo=lo.split('=',1);hv,hi=hi.split('=',1);assert lv==hv;var={r'\theta':theta,'r':r,'z':z}[lv];return factor,primitive,var,math(lo),math(hi)
def operands(raw):
 out=[];i=0
 while i<len(raw):
  if raw[i] in '+-':i+=1
  assert raw[i]=='(',raw;i+=1;start=i;depth=1
  while depth:depth+=(raw[i]=='(')-(raw[i]==')');i+=1
  out.append(math(raw[start:i-1]))
 return out
C={k:0 for k in ('records','actual_integrands','actual_heights','converted_heights','pointwise_substitutions','integral_stages','primitive_derivatives','radial_endpoint_components','angular_endpoint_components','complete_choices','whole_banks','geometry','source_factorization_checks')}
def check(rec):
 q=rec['question'];text=q[':question/problem'];wanted,F,n=b.read(q)
 if r'x\ge 0' in text and r'y\ge 0' in text:wanted=(s.Integer(0),s.pi/2,*wanted[2:])
 a,d,lo,rad,low,high,fn=wanted;C['actual_integrands']+=1;C['actual_heights']+=2;zp=s.integrate(fn,z);ze=s.expand(zp.subs(z,high)-zp.subs(z,low));rp=s.integrate(ze,r);rr=s.expand(rp.subs(r,rad)-rp.subs(r,0));value=s.simplify(s.integrate(rr,(theta,a,d)));sol=q[':question/worked-solution'];fam=rec['generation']['template']
 for raw0,expected in zip(re.findall(r'bounded (?:below|above) by \$z=(.*?)\$',sol),(low,high)):
  l,h=raw0.rstrip('.,').split('=',1);assert eq(math(l).subs({x:r*s.cos(theta),y:r*s.sin(theta)},simultaneous=True),math(h)) and eq(math(h),expected);C['converted_heights']+=1
 path=Path(re.search(r'!\[\]\((.*?)\)',sol)[1]);side=json.loads(path.with_suffix('.json').read_text());assert side['n']==n and eq(s.sympify(side['a']),a) and eq(s.sympify(side['d']),d) and side['sha256']==hashlib.sha256(path.read_bytes()).hexdigest();C['geometry']+=1
 chain=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)[1];rows=chain.split(chr(92)*2);last_prim={};last_factor={};rad_index=None;theta_index=None
 for idx,row in enumerate(rows):
  lhs,body=row.replace('&','').split('=',1);body=body.strip().rstrip('.,')
  if body.startswith(r'\iiint_\Delta'):
   body=body[len(r'\iiint_\Delta'):].split(r'\,dz',1)[0];assert eq(math(body),fn);C['pointwise_substitutions']+=1;continue
  bounds,expr=integrals(body);num=len(bounds);expected_bounds=((a,d),(0,rad),(low,high))[:num];assert all(eq(u,w) for pair,required in zip(bounds,expected_bounds) for u,w in zip(pair,required))
  if '[' in expr:
   factor,primitive,var,l,h=bracket(expr);assert eq(s.diff(factor*primitive,var),fn if var==z else ze if var==r else rr);assert eq(l,low if var==z else 0 if var==r else a) and eq(h,high if var==z else rad if var==r else d);C['primitive_derivatives']+=1;last_prim[var]=factor*primitive;last_factor[var]=factor
   if var==r:rad_index=idx
   if var==theta:theta_index=idx
  else:
   actual=math(expr);expected=fn if num==3 else ze if num==2 else rr if num==1 else value;assert eq(actual,expected),(fam,expr,actual,expected)
   if rad_index is not None and idx in (rad_index+1,rad_index+2):
    terms=last_prim[r].as_ordered_terms() if last_prim[r].is_Add else [last_prim[r]];observed=operands(expr);required=[term.subs(r,v) for term in terms for v in (rad,0)];assert len(observed)==len(required) and all(eq(u,v) for u,v in zip(observed,required));C['radial_endpoint_components']+=len(observed)
   if theta_index is not None and idx==theta_index+1 and fam!='half_linear':
    terms=last_prim[theta].as_ordered_terms() if last_prim[theta].is_Add else [last_prim[theta]];observed=operands(expr);required=[term.subs(theta,v) for term in terms for v in (d,a)];assert len(observed)==len(required) and all(eq(u,v) for u,v in zip(observed,required));C['angular_endpoint_components']+=len(observed)
   if theta_index is not None and fam=='half_linear' and idx==theta_index+2:
    terms=s.expand(last_prim[theta]).as_ordered_terms();observed=operands(expr);required=[term.subs(theta,v) for term in terms for v in (d,a)];assert len(observed)==len(required) and all(eq(u,v) for u,v in zip(observed,required));C['angular_endpoint_components']+=len(observed)
  if bounds:C['integral_stages']+=1
 if fam=='half_linear':
  assert r'(\cos(\theta)-\sin(\theta))' in chain or r'(\cos\theta-\sin\theta)' in chain;assert last_factor[theta]!=1;C['source_factorization_checks']+=1
 wrong_extra=s.integrate(s.integrate(ze*r**(2 if fam=='reciprocal' else 1),(r,0,rad)),(theta,a,d));half=s.integrate(s.integrate(ze,(r,0,rad/2)),(theta,a,d));double=s.integrate(rr,(theta,a,a+2*(d-a)))
 wrong=s.integrate(rr,(theta,0,s.pi)) if fam=='half_linear' else s.integrate(s.integrate(s.expand_trig(ze).subs(s.cos(theta)**2,s.Integer(1)),(r,0,rad)),(theta,a,d)) if fam=='reciprocal' else s.integrate(rr,(theta,a,(a+d)/2))
 # Reciprocal source error replaces cos(2theta) by1; do not use cos² alone.
 if fam=='reciprocal':wrong=s.integrate(s.integrate(ze.subs(s.cos(2*theta),1),(r,0,rad)),(theta,a,d))
 bank=[value,wrong_extra,half,wrong,double];f=q[':question/answer-fields'][0];vs=[math(z[':answer/value']) for z in f[':answer-field/choices']];assert len(vs)==5 and all(sum(eq(u,v) for v in vs)==1 for u in bank);assert next(z[':answer/id'] for z,v in zip(f[':answer-field/choices'],vs) if eq(v,value))==f[':answer-field/correct'][1];C['complete_choices']+=5;C['whole_banks']+=1;C['records']+=1
if __name__=='__main__':
 g=load(D.with_suffix('.py'),'root_cylinder_eval_gen');source=raw(g);records=json.loads((R/f'qa/{K}-sampled.json').read_text())
 for fam,(lev,sid,params) in g.SPECS.items():
  if fam!='cross_z':records.append(g.generate(lev,template=fam,seed=571))
 for rec in records:check(rec)
 out=dict(status='passed',source=source,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
