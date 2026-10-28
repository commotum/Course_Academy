import collections,json,re,sys
from pathlib import Path
import sympy as sp
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from vector_engine import *
D=json.loads((H/'snapshot.json').read_text());topic=next(t['entity']for t in D['topics']if t['ma_id']==2746);ids={q for t,k,q in D['links']if t==topic};completion={r['field']:r['answer']for r in json.loads((H/'missing-key-completions.json').read_text())};checks=[];unresolved=[];T=SYMS['T'];S=sp.Symbol('phase',real=True)
def param(value):
 value=normalize_source_tex(value).replace(r'\,',' ').strip();parts=[]
 for var in ['x','y']:
  m=re.search(r'(?<![A-Za-z])'+var+r'\s*=\s*([\s\S]+?)(?=,\s*[xy]\s*=|$)',value)
  if not m:raise Unsupported('coordinate pair unavailable')
  parts.append(scalar(m[1]))
 return sp.Matrix(parts)
def model(P):
 atoms=[a for e in P for a in e.atoms(sp.sin,sp.cos)];freqs={abs(sp.diff(a.args[0],T))for a in atoms}
 if len(freqs)!=1:raise Unsupported('different or missing harmonic frequencies')
 freq=next(iter(freqs))
 if freq==0 or freq.free_symbols:raise Unsupported('nonconstant frequency')
 R=P.subs(T,S/freq);R=R.applyfunc(sp.expand_trig);co=[];center=[]
 for e in R:
  e=sp.expand(e);a=e.coeff(sp.cos(S));b=e.coeff(sp.sin(S));c=sp.simplify(e-a*sp.cos(S)-b*sp.sin(S))
  if any(v.has(S)for v in[a,b,c]):raise Unsupported('not an affine harmonic ellipse')
  co.append([a,b]);center.append(c)
 M=sp.Matrix(co);Q=sp.simplify(M*M.T)
 return {'center':sp.Matrix(center),'M':M,'Q':Q,'frequency':freq,'nondegenerate':M.det()!=0,'orientation':sp.sign(M.det()),'start':P.subs(T,0)}
for q in D['questions']:
 if q[':db/id']not in ids:continue
 try:
  fs=q.get(':question/answer-fields',[])
  if not fs:raise Unsupported('canonical worked example withoutbank; geometry/derivationreviewseparate')
  f=max(fs,key=lambda f:bool(f.get(':answer-field/correct'))*10**16+f[':db/id']);cid=completion.get(f[':db/id'],f.get(':answer-field/correct',{}).get(':db/id'));right=next(a for a in f[':answer-field/choices']if a[':db/id']==cid);P=param(right[':answer/value']);target=model(P);prompt=q[':question/problem'];low=prompt.lower();start=None
  if'starting'in low:
   pts=tuples(prompt[low.index('starting'):])
   if not pts:raise Unsupported('startingpointrequiresimage-onlyA inspection')
   start=sp.Matrix(pts[0])
  direction=1 if re.search(r'counter[- ]?clockwise',low)else -1 if'clockwise'in low else None;once='once'in low;statedcenter=None;statedradii=None
  if re.search(r'centered at (?:the )?origin',low):statedcenter=sp.Matrix([0,0])
  elif'centered at'in low:
   pts=tuples(prompt[low.index('centered at'):]);statedcenter=sp.Matrix(pts[0])if pts else None
  hr=re.search(r'horizontal radius\s*\$([^$]+)\$',prompt);vr=re.search(r'vertical radius\s*\$([^$]+)\$',prompt)
  if hr and vr:statedradii=(scalar(hr[1]),scalar(vr[1]))
  targetok=target['nondegenerate']and(statedcenter is None or equal(target['center'],statedcenter))and(statedradii is None or equal(target['Q'],sp.diag(*(r*r for r in statedradii))));rows=[]
  for a in f[':answer-field/choices']:
   try:
    p=param(a[':answer/value']);m=model(p);locus=m['nondegenerate']and equal(m['center'],target['center'])and equal(m['Q'],target['Q']);interval=True # All scoped source/fresh prompts specify theta in [0,2pi), checked in full prompt below.
    if not re.search(r'0\s*,\s*2(?:π|\\pi)',prompt):raise Unsupported('nonstandardparameterintervalrequiresdedicatedreview')
    interval=(m['frequency']==1)if once else(m['frequency']>=1);startok=start is None or equal(m['start'],start);orient=direction is None or m['orientation']==direction;passes=bool(locus and interval and startok and orient);rows.append({'answer':a[':db/id'],'value':a[':answer/value'],'locus_matches':bool(locus),'start_matches':bool(startok),'orientation_matches':bool(orient),'interval_traversal_matches':bool(interval),'passes':passes,'orientation':str(m['orientation']),'start':str(m['start'])})
   except Exception as ex:rows.append({'answer':a[':db/id'],'value':a[':answer/value'],'passes':False,'interpretation':str(ex)})
  valid=[r['answer']for r in rows if r['passes']];checks.append({'entity':q[':db/id'],'source':q.get(':question/math-academy-id'),'field':f[':db/id'],'canonical':cid,'full_prompt':prompt,'stated_center':str(statedcenter),'stated_radii':str(statedradii),'start_constraint':str(start),'orientation_constraint':direction,'once_constraint':once,'target_geometry_valid':bool(targetok),'matching_answers':valid,'canonical_valid':bool(targetok and cid in valid),'unique':valid==[cid],'choices':rows,'geometry_evidence_limit':'Ifcenter/radiinotstated, locusreferenceiscurrentcanonicalandrequiresseparateimagegeometryreview.'})
 except Exception as ex:unresolved.append({'entity':q[':db/id'],'source':q.get(':question/math-academy-id'),'reason':str(ex)})
(H/'ellipse-param-math-validation.json').write_text(json.dumps({'checks':checks,'failures':[r for r in checks if not r['canonical_valid']or not r['unique']],'unresolved':unresolved,'resolved_false_positive_regressions':[r for r in checks if r['entity']in[17592186152432,17592186152796]]},indent=2));print('ellipsefullconstraints',len(checks),'failures',sum(not r['canonical_valid']or not r['unique']for r in checks),'unresolved',len(unresolved))
