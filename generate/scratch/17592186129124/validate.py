"""Independent printed-math, fidelity, scope, identity and native grading checks."""
import importlib.util,json,re,sys,hashlib,subprocess,itertools
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X,Z=sp.symbols('x z',real=True)

def parse(s):
 s=s.replace('\u2061','').replace('π','pi').replace('∘','circ')
 s=re.sub(r'\\operatorname\{(sin|cos)\}',r'\1',s)
 s=s.replace(r'\sin','sin').replace(r'\cos','cos').replace(r'\pi','pi').replace(r'\infty','oo')
 s=s.replace(r'^{\circ}','').replace('^{circ}','')
 while '\\frac' in s:
  new=re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',r'((\1)/(\2))',s)
  assert new!=s,s
  s=new
 s=s.replace('{','(').replace('}',')').replace('^','**').strip().rstrip('.?')
 return parse_expr(s,local_dict={'x':X,'z':Z,'sin':lambda v:sp.sin(v,evaluate=False),'cos':lambda v:sp.cos(v,evaluate=False),'pi':sp.pi,'oo':sp.oo},transformations=standard_transformations+(implicit_multiplication_application,))

def prompt_math(q):
 part=re.search(r'\$(.*?)\$',q[':question/problem'],re.S).group(1)
 rhs=part.split('=',1)[1]
 m=re.search(r'\\(?:sin|cos|operatorname\{(?:sin|cos)\})',rhs)
 prefix=rhs[:m.start()].strip();a=parse('-1' if prefix=='-' else prefix or '1')
 end=rhs.rfind(')');d=parse(rhs[end+1:]);trig=parse(rhs[m.start():end+1])
 b=sp.diff(trig.args[0],X)
 assert b!=0 and b.is_real and not b.has(X)
 return a,d,trig

def interval(s):
 content=s.split('∈',1)[-1] if '∈' in s else s.split(r'\in ',1)[-1]
 content=content.strip();br=content[0]+content[-1];ends=content[1:-1].split(',');assert len(ends)==2
 return parse(ends[0]),parse(ends[1]),br

def formatting(text):
 assert text.count('$')%2==0
 depth=0
 for i,c in enumerate(text):
  if c in '{}':
   depth+=1 if c=='{' else -1;assert depth>=0,(text,i)
 assert depth==0,text
 assert not re.search(r'(?<!\\)[+-]{2}',text)

def check_record(r,raw=False):
 q=r['question'];a,d,t=prompt_math(q);lo,hi=d-abs(a),d+abs(a)
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 for s in [q[':question/problem'],q.get(':question/worked-solution','')]:formatting(s)
 if not raw:
  p={k:sp.sympify(v) for k,v in r['generation']['parameters'].items()};g.guard(q[':question/difficulty'].split('/')[-1],g.TEMPLATES[r['generation']['template']],p)
  assert (a,d)==(p['A'],p['D'])
  # Parse actual four printed rows and verify all three numeric endpoints and
  # complete middle expressions; no metadata-derived row equality shortcuts.
  sol=q[':question/worked-solution'];block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S).group(1)
  rows=block.split(' \\\\  & ');assert len(rows)==4
  for i,row in enumerate(rows):
   row=row.replace('& ','').strip().rstrip('.')
   parts=re.split(r'\\le|\\ge',row);assert len(parts)==3,row
   left,right=parse(parts[0]),parse(parts[2]);mid=parts[1]
   expected=[(-1,1),(-a,a),(d-a,d+a),(lo,hi)][i];assert (left,right)==expected,row
   op='\\ge' if a<0 and i in (1,2) else '\\le';assert row.count(op)==2,row
   if i<3:
    midexpr=parse(mid);zexpr=midexpr.xreplace({t:Z})
    assert sp.simplify(zexpr-[Z,a*Z,a*Z+d][i])==0,row
    for val in (-1,0,1):
     center=zexpr.subs(Z,val);assert left>=center>=right if op=='\\ge' else left<=center<=right
   else:assert mid.strip() in ('y','f(x)')
  ending=sol.split('Therefore,')[-1]
  if r['generation']['mathematical_task']['response']=='minimum':assert parse(re.search(r'\$(.*?)\$',ending).group(1))==lo
  else:assert interval(re.search(r'\$(.*?)\$',ending).group(1).rstrip('.'))==(lo,hi,'[]')
  # Horizontal input must be the actual prompt argument in every trig stage.
  for segment in re.findall(r'\$\$.*?\$\$',sol,re.S)[1:]:
   if 'aligned' not in segment: assert t in parse(segment.strip('$\n').split('\\le')[1]).atoms(sp.sin,sp.cos)
 for f in q.get(':question/answer-fields',[]):
  options=f[':answer-field/choices'];assert len(options)==5
  for option in options:formatting(option[':answer/value'])
  values=[interval(x[':answer/value']) if '\\in ' in x[':answer/value'] or '∈' in x[':answer/value'] else parse(x[':answer/value']) for x in options]
  assert len(set(map(str,values)))==5
  if not raw or ':answer-field/correct' in f:
   correct=f[':answer-field/correct'][1];assert sum(x[':answer/id']==correct for x in options)==1
   actual=values[next(i for i,x in enumerate(options) if x[':answer/id']==correct)]
   response=r['generation']['mathematical_task']['response'];assert actual==(lo,hi,'[]') if response=='range' else actual==lo
 return True

def main():
 cases=[];raw_records=[];bank_count=choice_count=designation_count=solution_count=0
 for sid,src in g.ORIGINALS.items():
  params=g.source_parameters(sid);case=dict(source_id=sid,template='source_'+sid,level=g.RAW[sid]['level'],parameters=params,bank_profile='raw_'+sid);cases.append(case)
  r=g.generate(case['level'],template=case['template'],parameters=params,profile=case['bank_profile']);q=r['question'];raw_records.append(r)
  assert q[':question/problem']==src[':question/problem']
  for k in (':question/difficulty',':question/answer-fields',':question/worked-solution'):assert (k in q)==(k in src),(sid,k)
  assert q.get(':question/worked-solution')==src.get(':question/worked-solution');solution_count+=int(':question/worked-solution' in src)
  if ':question/answer-fields' in src:
   f,sf=q[':question/answer-fields'][0],src[':question/answer-fields'][0]
   assert f[':answer-field/type']==sf[':answer-field/type'][':db/ident'];assert f[':answer-field/key']==sf[':answer-field/key']
   assert (':answer-field/correct' in f)==(':answer-field/correct' in sf)
   assert sorted(x[':answer/value'] for x in f[':answer-field/choices'])==sorted(x[':answer/value'] for x in sf[':answer-field/choices'])
   bank_count+=1;choice_count+=len(f[':answer-field/choices']);designation_count+=int(':answer-field/correct' in sf)
  assert r['generation']['evidence_only'] and not r['generation']['eligible_for_learning']
  check_record(r,raw=True)
  # Different original integer A,D replay through normal masks (not literals).
  changed={**params,'D':str(int(params['D'])+ (1 if int(params['D'])>0 else -1))}
  rr=g.generate(case['level'],parameters=changed,profile=case['bank_profile']);assert rr['question'][':question/problem']!=q[':question/problem']
 (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
 records=[];coverage=set();task_counts={};rng_counts={}
 for level in g.LEVELS:
  levelrecords=[]
  for seed in range(160):
   r=g.generate(level,seed);check_record(r);levelrecords.append(r);coverage.add((level,r['generation']['template'],r['generation']['bank_profile']))
  for template,s in g.TEMPLATES.items():
   profiles=(['endpoints'] if s['unit']=='degree' else ['endpoints','outer_transform']) if s['response']=='range' else ['extrema']
   for profile in profiles:
    for seed in (13,71):
     r=g.generate(level,seed,template,profile=profile);check_record(r);records.append(r)
     p=r['generation']['parameters'];rr=g.generate(level,seed+1000,template,parameters=p,profile=profile)
     assert rr['question'][':question/id']==r['question'][':question/id']
     # Explicit spelling equivalence does not change content/task identity.
     ps={**p,'A':str(2*sp.Rational(p['A']))+'/2'}
     rrr=g.generate(level,1,template,parameters=ps,profile=profile);assert rrr['question'][':question/id']==r['question'][':question/id']
  rng_counts[level]=len({r['generation']['parameter_fingerprint'] for r in levelrecords})
  # Enumerate true tasks ignoring horizontal factors, phases, functions/banks.
  aa=list(range(1,7)) if level=='easy' else list(range(-6,0)) if level=='moderate' else sorted({sp.Rational(-n,m) for n in range(1,13) for m in (2,3,4) if n%m and sp.Rational(n,m)<=6})
  dd=[d for d in range(-8,9) if d] if level!='hard' else sorted({sp.Rational(n,m) for n in range(-16,17) for m in (2,3,4) if n and n%m and abs(sp.Rational(n,m))<=8})
  count={'range':len(aa)*len(dd),'minimum':0}
  for a,d in itertools.product(aa,dd):
   try:g.bank(g.TEMPLATES['minimum_cos_linear'],dict(A=sp.Rational(a),B=sp.Integer(2),C=sp.Integer(0),D=sp.Rational(d)),'extrema');count['minimum']+=1
   except g.SampleRejected:pass
  task_counts[level]=count
 # Strict explicit-input rejection and bank collision guards.
 rejects=0
 for level,p in [('easy',dict(A=-2,B=2,C=0,D=3)),('moderate',dict(A=2,B=2,C=0,D=3)),('hard',dict(A=-2,B=2,C=0,D='1/2')),('hard',dict(A='-1/5',B=2,C=0,D='1/2')),('hard',dict(A='-13/2',B=2,C=0,D='1/2')),('easy',dict(A=2,B=0,C=0,D=3)),('moderate',dict(A=-2,B=2,C=0,D=0))]:
  try:g.generate(level,parameters=p,template='range_cos_linear');raise AssertionError('invalid explicit input accepted')
  except ValueError:rejects+=1
 for profile,p in [('outer_transform',dict(A=2,B=1,C=0,D=3)),('extrema',dict(A=2,B=2,C=0,D=4))]:
  try:g.generate('easy',parameters=p,template='range_cos_linear' if profile=='outer_transform' else 'minimum_cos_linear',profile=profile);raise AssertionError('collision accepted')
  except g.SampleRejected:rejects+=1
 # Public reduced rational boundaries for every eligible family/profile.
 for level in g.LEVELS:
  for template,s in g.TEMPLATES.items():
   profiles=(['endpoints'] if s['unit']=='degree' else ['endpoints','outer_transform']) if s['response']=='range' else ['extrema']
   for profile in profiles:
    for a,d in ([('1','8'),('6','-8')] if level=='easy' else [('-1','8'),('-6','-8')] if level=='moderate' else [('-1/4','16/3'),('-11/2','-15/2')]):
     p=dict(A=a,D=d,B=1 if s['unit']=='degree' else 5,C=90 if s['unit']=='degree' else '-pi/6' if s['unit']=='radian' else -3)
     try:check_record(g.generate(level,parameters=p,template=template,profile=profile))
     except g.SampleRejected:pass
 # Same assessed task under incidental horizontal/function changes deduplicates.
 p=dict(A=3,B=2,C=0,D=4);r1=g.generate('easy',parameters=p,template='range_cos_linear',profile='endpoints');r2=g.generate('easy',parameters={**p,'B':5,'C':2},template='range_sin_linear',profile='endpoints')
 assert r1['generation']['parameter_fingerprint']==r2['generation']['parameter_fingerprint'];assert r1['question'][':question/id']!=r2['question'][':question/id']
 for level in g.LEVELS:
  for template,s in g.TEMPLATES.items():
   profiles=(['endpoints'] if s['unit']=='degree' else ['endpoints','outer_transform']) if s['response']=='range' else ['extrema']
   for profile in profiles:assert (level,template,profile) in coverage,(level,template,profile)
 # Native fixtures include every default family/profile plus all five complete raw banks.
 native=[]
 for idx,r in enumerate(records+[r for r in raw_records if all(':answer-field/correct' in f for f in r['question'].get(':question/answer-fields',[])) and ':question/answer-fields' in r['question']]):
  f=r['question'][':question/answer-fields'][0];native.append(dict(label=f'fixture/{idx}',record=r,checks=[dict(submitted_answer_id=a[':answer/id'],expected='accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected',purpose='Owned radio option, independently checked mathematics') for a in f[':answer-field/choices']]))
 (HERE/'native-input.json').write_text(json.dumps(native,indent=2)+'\n')
 res=subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-report.json')],capture_output=True,text=True);assert res.returncode==0,res.stderr
 native_report=json.loads((HERE/'native-report.json').read_text())
 # Actual adjacent raw slash pairs only occur as aligned row separators.
 anomaly=[]
 for sid,q in g.ORIGINALS.items():
  for key,val in q.items():
   if isinstance(val,str):
    for m in re.finditer(re.escape(chr(92)*2),val):
     if not (key==':question/worked-solution' and val[m.end():].startswith(' ')):anomaly.append(dict(source_id=sid,attribute=key,index=m.start()))
 assert not anomaly
 report=dict(status='passed',frozen_version=g.VERSION,python_version=sys.version.split()[0],sympy_version=sp.__version__,source_fidelity=dict(prompts=[9,9],stored_solutions=[solution_count,7],complete_banks=[bank_count,7],displayed_choices=[choice_count,35],stored_correct_designations=[designation_count,5],attribute_presence=[9,9]),source_anomalies=dict(missing_difficulty=['q-10249','q-40977'],missing_solutions=['q-10249','q-40977'],missing_correct_refs=['q-10249','q-40977'],fieldless=['q-25512','q-40908'],raw_math_error=['q-25512: 2x in scaled/shifted rows contradicts prompt 3x; retained evidence-only'],unexpected_adjacent_backslash_pairs=anomaly),normal_random_records=480,explicit_family_profile_records=len(records),explicit_invalid_rejections=rejects,meaningful_task_counts=task_counts,sampled_unique_task_counts=rng_counts,default_coverage=sorted(coverage),native=dict(accepted=native_report['accepted_checks'],rejected=native_report['rejected_checks'],unresolved=native_report['documented_unresolved_checks'],raw_incomplete_records_excluded=4,entry_point=native_report['entry_point'],binary_sha256=hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest()),database_writes=0,plots='none; no practice/canonical plot references')
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 (HERE/'review.json').write_text(json.dumps(dict(originals=raw_records,generated=records),indent=2)+'\n')
 (HERE/'review.md').write_text('# Range generator review\n\nFrozen basis 1356. Raw originals are evidence-only, including omissions and the identified q-25512 error. Generated variants are labeled separately.\n\n'+ '\n---\n'.join('### Original '+r['generation']['source_ids'][0]+'\n\n'+g.markdown(r) for r in raw_records)+'\n\n# Generated variants\n\n'+ '\n---\n'.join('### Generated '+r['question'][':question/difficulty'].split('/')[-1]+' / '+r['generation']['bank_profile']+'\n\n'+g.markdown(r) for r in records))
 print(json.dumps({k:report[k] for k in ('status','source_fidelity','meaningful_task_counts','native')},indent=2))
if __name__=='__main__':main()
