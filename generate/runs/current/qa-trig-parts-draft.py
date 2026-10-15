import sys
sys.dont_write_bytecode=True
import re,json,copy,hashlib,importlib.util
from pathlib import Path
from functools import lru_cache
import sympy as s
R=Path(__file__).resolve().parent;K=17592186064246;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 sp=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
E=load('root_trig_parts_elementary',R/'elementary-integral-readback.py');x=E.x
C=dict(records=0,definition_derivatives=0,ordered_parts_factors=0,concrete_integral_stages=0,primitive_stages=0,substitution_checks=0,whole_banks=0,source_values=0,source_fields=0,source_keys=0,source_prose_chains=0)
@lru_cache(maxsize=12000)
def equal(a,b):
 diff=s.expand(a-b)
 if diff==0:return True
 return s.trigsimp(diff,method='fu')==0 or s.simplify(diff.rewrite(s.sin))==0
@lru_cache(maxsize=12000)
def deriv(t,inner=None):return E.derivative(E.scalar(t),x,inner)
def blocks(t):return re.findall(r'\$\$(.*?)\$\$',t,re.S)
def chain(t):
 t=re.sub(r'\\(?:begin|end)\{(?:aligned|gathered)\}','',t).replace('&','');rr=[z.strip().rstrip('.')for z in t.split(chr(92)*2)];out=[]
 for z in rr:
  if out and out[-1].endswith('='):out[-1]+=z
  else:out.append(z)
 assert all('='in z for z in out);return out
def prose(t):return re.sub(r'\$\$.*?\$\$|\$(?!\$).*?\$','[MATH]',t,flags=re.S)
def definitions(sol):
 b=next(b for b in blocks(sol)if '⟹'in b);b=re.sub(r'\\(?:begin|end)\{aligned\}','',b);rr=b.split(chr(92)*2);assert len(rr)==2
 vals=[]
 for row in rr:
  halves=row.split('⟹');assert len(halves)==2
  vals.extend(E.scalar(z.split('=',1)[1].replace('&','').strip().rstrip('.'))for z in halves)
 return vals

def check(r,raw=False):
 q=r['question'];g=r['generation'];F,var,_=E.integrand(q[':question/problem']);assert var==x and F.free_symbols<={x};sol=q[':question/worked-solution'];u,du,vp,v=definitions(sol);assert equal(s.diff(u,x),du) and equal(s.diff(v,x),vp) and equal(u*vp,F);assert s.diff(u,x,2)==0 and du.is_Integer and 1<=du<=10;C['definition_derivatives']+=2
 inner=None
 hard=g['template']=='csc_log'
 if hard:
  um=re.search(r'\$u=(.*?),\$',sol);dm=re.search(r'\$\\text\{d\}u=(.*?)\\,?\s*\\text\{d\}x,\$',sol);assert um and dm,(um,dm);inner=E.scalar(um[1]);assert equal(s.diff(inner,x),E.scalar(dm[1]));assert inner.func==s.sin and s.diff(inner.args[0],x)==1;C['substitution_checks']+=1
 parts=next(b for b in blocks(sol)if r'\int u{v}^{′}'in b and r'\begin'in b);pc=chain(parts);assert len(pc)==(3 if hard else 2)
 formal=re.sub(r'\s|\\,','',pc[0]);assert formal==r'\intu{v}^{′}\text{d}x=uv-\intv{u}^{′}\text{d}x',formal
 lhs,rhs=pc[1].split('=',1);lf,lv,_=E.integrand(lhs);assert lv==x and equal(lf,F)
 before,after=rhs.split(r'-\int',1);pair=before.split(r'\cdot');assert len(pair)==2 and equal(E.scalar(pair[0]),u) and equal(E.scalar(pair[1]),v)
 residual,rv,m=E.integrand(r'\int'+after);ordered=m[1].replace(r'\,','').split(r'\cdot');assert len(ordered)==2 and equal(E.scalar(ordered[0]),v) and equal(E.scalar(ordered[1]),du) and rv==x;C['ordered_parts_factors']+=4
 for equation in pc[1:]:
  for text in equation.split('='):
   if text.strip():value,inputs=E.side(text,x,inner);assert equal(value,F),(text,value,F);C['concrete_integral_stages']+=1
 finalblock=blocks(sol)[-1];fc=chain(finalblock);expected_rows=4 if hard else 3 if g['template']in ('cos_frequency_expanded','cos_unit_expanded')else 2;assert len(fc)==expected_rows,(g['template'],fc)
 for equation in fc:
  for text in equation.split('='):
   if not text.strip():continue
   value,inputs=E.side(text,x,inner);assert equal(value,F),(text,value,F);C['concrete_integral_stages'if inputs else 'primitive_stages']+=1
 if hard:
  assert r'\frac{1}{u}'in fc[1] and r'\text{d}u'in fc[1] and ('|u|'in fc[2]) and 'sin'in fc[3]
 f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1 and f[':answer-field/key']=='selection' and f[':answer-field/type'].endswith('/radio');answers=f[':answer-field/choices'];assert len(answers)==5;values=[]
 for a in answers:
  assert re.search(r'\+\s*C\s*$',a[':answer/value']);values.append(deriv(a[':answer/value']))
 assert sum(equal(z,F)for z in values)==1
 assert equal(values[next(i for i,a in enumerate(answers)if a[':answer/id']==f[':answer-field/correct'][1])],F)
 assert all(not equal(a,b)for i,a in enumerate(values)for b in values[:i])
 if not g['evidence_only']:
  final=E.scalar(fc[-1].split('=',1)[1]);residual=final-u*v;expected=[final,u*v-residual,u*v,-u*v+residual,u*v+residual*u/du];wanted=[E.derivative(z,x)for z in expected];assert all(sum(equal(a,b)for b in wanted)==1 for a in values);C['whole_banks']+=1
  # Independently recover shift roles and arithmetic from printed definitions.
  a=du;b=s.expand(u).coeff(x,0);arg=vp.args[0] if vp.func in (s.sin,s.cos)else vp.base.args[0];k=s.diff(arg,x);h=s.expand(arg).coeff(x,0);level=q[':question/difficulty'].split('/')[-1];assert all(z.is_Integer for z in (a,b,k,h)) and abs(b)<=8 and abs(h)<=8 and 1<=k<=5
  if level=='easy':assert b==h==0
  elif level=='moderate':assert (b!=0) != (h!=0) and abs(a*b)<=64
  else:assert level=='hard' and b==0 and k==1 and hard
  for value in (a/k,a/k**2):assert abs(value.p)<=10 and value.q<=25
 C['records']+=1

if __name__=='__main__':
 G=load('root_trig_parts_generator',D.with_suffix('.py'));src=json.loads((R/'refresh-2026-10-14/sources'/f'{K}.json').read_text());assert src==json.loads((D/'source.json').read_text());originals={q[':question/math-academy-id']:q for q in src['record'][':knowledge-point/questions']}
 for c in json.loads((D/'source-cases.json').read_text()):
  level=originals[c['source_id']][':question/difficulty'][':db/ident'].split('/')[-1];r=G.generate(level,template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);q=r['question'];o=originals[c['source_id']];check(r)
  assert equal(E.integrand(q[':question/problem'])[0],E.integrand(o[':question/problem'])[0]) and prose(q[':question/problem'])==prose(o[':question/problem']);assert prose(q[':question/worked-solution'])==prose(o[':question/worked-solution']);C['source_prose_chains']+=1
  # Read every original operative stage too, without relying on generator recipes.
  original=copy.deepcopy(r);original['question']=copy.deepcopy(o);original['question'][':question/answer-fields']=copy.deepcopy(q[':question/answer-fields']);check(original,True)
  of=o[':question/answer-fields'][0];nf=q[':question/answer-fields'][0];remaining=[deriv(z[':answer/value'])for z in nf[':answer-field/choices']]
  for z in of[':answer-field/choices']:
   wanted=deriv(z[':answer/value']);matches=[i for i,vv in enumerate(remaining)if equal(vv,wanted)];assert len(matches)==1;remaining.pop(matches[0]);C['source_values']+=1
  assert not remaining;C['source_fields']+=1
  correct=next(z[':answer/value']for z in nf[':answer-field/choices']if z[':answer/id']==nf[':answer-field/correct'][1]);assert equal(deriv(correct),deriv(of[':answer-field/correct'][':answer/value']));C['source_keys']+=1
 samples=json.loads((R/'qa'/f'{K}-sampled.json').read_text())
 for r in samples:check(r)
 for name,data in G.TEMPLATES.items():
  for seed in (903,1206):check(G.generate(data[0],seed=seed,template=name))
 probe=copy.deepcopy(samples[0]);text=probe['question'][':question/worked-solution'];bad=text.replace(r'\cdot', '+',1);assert text!=bad;probe['question'][':question/worked-solution']=bad;saved=copy.deepcopy(C)
 try:check(probe)
 except (AssertionError,ValueError):pass
 else:raise AssertionError('Wrong concrete by-parts operation survived unchanged key')
 C=saved;C.update(status='passed',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),unchanged_key_wrong_parts_operation_rejected=True,database_writes=0);(R/'qa'/f'{K}-root-readback.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
