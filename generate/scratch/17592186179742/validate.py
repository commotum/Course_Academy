"""Independent curve/field/statement checks and actual application grading."""
import copy,hashlib,importlib.util,itertools,json,re,subprocess,sys
from pathlib import Path
import sympy as s
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('work_sign_generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def engine_item(r,label=None):
 checks=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  for a in f[':answer-field/choices']:checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete field-owned bank'})
 return {'label':label or r['question'][':question/id'],'record':r,'checks':checks}
def native(records,p):
 p.mkdir(parents=True,exist_ok=True);save(p/'input.json',[engine_item(r) for r in records]);subprocess.run([str(D/'reference/native/check-engine'),str(p/'input.json'),str(p/'report.json')],check=True,timeout=55)
def independent(level,p):
 # Derive force directions from printed-geometry axes; do not use g.math_data.
 t=s.symbols('u',real=True);a,b=p['a'],p['b'];ang=s.pi*(p['start']+p['direction']*t)/2;r=s.Matrix([a*s.cos(ang),b*s.sin(ang)]);v=r.diff(t)
 fx,fy=(p['force_sign']*-a*a*r[1],p['force_sign']*b*b*r[0]) if level=='easy' else (p['force_sign']*b*b*r[0],p['force_sign']*a*a*r[1])
 dot=s.trigsimp(fx*v[0]+fy*v[1]);sign=p['direction']*p['force_sign'] if level=='easy' else 0
 if level=='moderate':assert dot==0
 else:
  assert s.trigsimp(fx*v[1]-fy*v[0])==0
  # Strict positivity on every point follows from a,b>0 and sin²+cos²=1.
  expected=p['force_sign']*p['direction']*s.pi*a*b*(a*a*s.sin(ang)**2+b*b*s.cos(ang)**2)/2
  assert s.trigsimp(dot-expected)==0
 return sign

def check_record(r):
 q=r['question'];m=r['generation'];assert r['knowledge_point']['db_id']==g.KP[':db/id'];assert not m['evidence_only'] and m['eligible_for_learning']
 level=q[':question/difficulty'].split('/')[-1];p=m['parameters'];g.guard(level,p);sign=independent(level,p);assert sign==m['sign']
 assert m['mathematical_fingerprint']==g.fingerprint(level,p)
 statements=re.findall(r'\$\{\\int \}_\{(-?C)\}F\\cdot \\text\{d\}r([<>=])0\$',q[':question/problem']);assert len(statements)==3
 values=[{'<':(-sign if path=='-C' else sign)<0,'>':(-sign if path=='-C' else sign)>0,'=':sign==0}[op] for path,op in statements]
 for i,f in enumerate(q[':question/answer-fields']):
  vals=[a[':answer/value'] for a in f[':answer-field/choices']];assert len(vals)==len(set(vals));correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
  if f[':answer-field/type'].endswith('/checkbox'):assert sorted(vals)==['false','true'] and correct==str(values[i]).lower()
  else:assert sorted(vals)==sorted(['I only','II only','III only','I and III only','II and III only']) and correct==g.subset(values)
 solution=q[':question/worked-solution'];assert 'Statement I is '+str(values[0]).lower() in solution and 'statement II is '+str(values[1]).lower() in solution and 'Statement III is '+str(values[2]).lower() in solution
 assert 'correct answer is "'+g.subset(values)+'."' in solution
 expected={1:'>0',-1:'<0',0:'=0'};assert r'${\int }_{C}F\cdot \text{d}r'+expected[sign] in solution;assert r'${\int }_{-C}F\cdot \text{d}r'+expected[-sign] in solution
 for key in (':question/problem',':question/worked-solution'):
  for ref in re.findall(r'!\[.*?\]\((.*?)\)',q[key]):assert (ROOT/ref).is_file() if not ref.startswith('images/') else (Path('/media/jake/SSD/EDB/math')/ref).is_file()
 return True

def main():
 records=[];source_report=[];options=0;distractors=0
 for mid in g.SOURCES:
  r=g.replay(mid);q=g.SOURCES[mid];assert r['question']==g.normalize(q);family,sign,profile=g.SOURCE_CASES[mid];truth=g.truth(sign,profile)
  for i,f in enumerate(q[':question/answer-fields']):
   bank=[a[':answer/value'] for a in f[':answer-field/choices']];expected=str(truth[i]).lower() if f[':answer-field/type'][':db/ident'].endswith('/checkbox') else g.subset(truth)
   assert f[':answer-field/correct'][':answer/value']==expected;options+=len(bank);distractors+=len(bank)-1
  records.append(r);source_report.append({'source':mid,'family':family,'profile':profile,'sign':sign,'complete_bank_match':True,'exact_prompt_and_solution':True})
 # Exhaust every bounded geometry slot; no rendering needed for symbolic checks.
 domain={};coverage={};full=0
 for level in g.LEVELS:
  fps=set();seen={k:set() for k in ('a','b','start','sweep','direction','force_sign')}
  for ab,start,sweep,direction,force in itertools.product(((1,1),(2,1),(1,2),(3,2),(2,3)),range(4),(2,3) if level=='easy' else (1,2),(-1,1),(-1,1)):
   p=dict(a=ab[0],b=ab[1],start=start,sweep=sweep,direction=direction,force_sign=force);assert independent(level,p)==g.math_data(level,p)['sign'];fps.add(g.fingerprint(level,p));full+=1
   for k,v in p.items():seen[k].add(v)
  domain[level]=len(fps);coverage[level]={k:sorted(v) for k,v in seen.items()}
 profiles={'easy':['positive-negative-reverse-positive'],'moderate':['positive-zero-reverse-zero','negative-zero-reverse-negative','negative-zero-reverse-positive','positive-zero-reverse-negative']}
 for level in g.LEVELS:
  for i,profile in enumerate(profiles[level]):
   for direction,force in itertools.product((-1,1),(-1,1)):
    p=dict(a=2,b=1,start=i,sweep=2,direction=direction,force_sign=force)
    r=g.generate(level,17,p,profile);check_record(r);records.append(r)
   if profile in ('positive-negative-reverse-positive','positive-zero-reverse-zero'):
    r=g.generate(level,1,p,profile,'radio');check_record(r);records.append(r)
 # Changed geometry with all other slots fixed: check keys, solution, plot bytes,
 # endpoints; seed cannot alter identities for the same mathematical parameters.
 a=dict(a=2,b=1,start=0,sweep=2,direction=1,force_sign=1);b={**a,'sweep':3}
 r=g.generate('easy',1,a);z=g.generate('easy',1,b);check_record(r);check_record(z);assert r['question'][':question/id']!=z['question'][':question/id'];assert Path(r['generation']['assets']['prompt']).read_bytes()!=Path(z['generation']['assets']['prompt']).read_bytes();assert g.fingerprint('easy',a)!=g.fingerprint('easy',b)
 assert g.generate('easy',1,a)['question']==g.generate('easy',999,a)['question']
 # Deliberately stale answer and solution must fail validation.
 mutations=0
 for key in ('answer','solution'):
  bad=copy.deepcopy(r)
  if key=='answer':
   f=bad['question'][':question/answer-fields'][0];f[':answer-field/correct'][1]=next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])
  else:bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('Statement I is true','Statement I is false')
  try:check_record(bad)
  except AssertionError:mutations+=1
  else:raise AssertionError('Stale rendered content accepted')
 try:g.generate('hard',0)
 except ValueError:pass
 else:raise AssertionError('Hard accepted')
 native(records,D/'reference/validation-grading');save(D/'reference/review.json',records)
 (D/'reference/review.md').write_text('\n\n'.join('## '+r['generation'].get('source_id',r['question'][':question/id'])+'\n\n'+r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in records))
 report={'passed':True,'source_basis':g.RAW['basis'],'source_complete_banks_matched':len(source_report),'source_complete_banks_total':len(g.SOURCES),'source_options_matched':options,'source_distractors_matched':distractors,'source_replay':source_report,'exhaustive_geometry_cases':full,'finite_domain':domain,'slot_coverage':coverage,'native_grading':json.loads((D/'reference/validation-grading/report.json').read_text()),'mutation_rejections':mutations,'hard_rejected':True,'fidelity':'All observed instances replay verbatim, including complete field-owned banks; new ellipse diagrams are analytic same-method realizations, not recovered source formulas. Segment and general-curve sources replay only.','mathematical_scope':'Tangent ellipses (easy), normal ellipses (moderate); exact dot-product sign proved for complete bounded domain.','script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()};save(D/'validation.json',report);print(json.dumps({k:v for k,v in report.items() if k not in ('native_grading','source_replay','slot_coverage')}))
if __name__=='__main__':main()
