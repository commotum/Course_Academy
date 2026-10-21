#!/usr/bin/env python3
"""Independent displayed-data checks, exact source fidelity, native grader and review."""
import importlib.util,json,re,subprocess,hashlib,sys,math
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
D=Path(__file__).parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('equal_flow',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
src=json.loads((D/'source.json').read_text())['record'];cases=json.loads((D/'source-cases.json').read_text());t=sp.Symbol('t',real=True)
def parse_num(s):
 s=s.rstrip('.')
 m=re.fullmatch(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',s)
 return sp.Rational(m[1])/sp.Rational(m[2]) if m else sp.Rational(s)
def fn(s):
 s=s.replace(' ','').replace('{e}','e');s=s.split('=')[-1]
 m=re.fullmatch(r'(-?\d+(?:\.\d+)?)([+-])(\d+(?:\.\d+)?)?e\^\{(-?)([\dt.]+)/([\d.]+)\}',s)
 assert m,s
 E=sp.Rational(m[1]);A=sp.Rational(m[3] or 1)*(1 if m[2]=='+' else -1);ind=t if m[5]=='t' else sp.Rational(m[5]);k=sp.Rational(1)/sp.Rational(m[6])*(-1 if m[4] else 1)
 return E+A*sp.exp(k*ind)
def prompt_math(q):
 blocks=re.findall(r'\$([^$]+)\$',q[':question/problem'])
 start_number=r'(\\frac\{[\d.]+\}\{[\d.]+\}|[\d.]+)'
 nums=[parse_num(re.match(start_number,x)[1]) for x in blocks[:5]]
 tail=[parse_num(re.match(start_number,blocks[-1])[1])] if 'Find, rounded' in q[':question/problem'] else []
 V,q0,c,r,rout=nums
 assert r==rout and V>0 and r>0
 hard=r'\text{g/L}' in q[':question/problem'];c=c/1000 if hard else c
 return V,q0,c,r,(tail[0] if tail else None),hard
checks=[];reviews=[];rows=[];originals=[];coverage=[]
for case,q in zip(cases,src[':knowledge-point/questions']):
 rec=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);rr=rec['question'];sf=q[':question/answer-fields'][0];rf=rr[':question/answer-fields'][0]
 assert set(g.__dict__['LEVELS'])=={'easy','moderate','hard'}
 for key in (':question/problem',':question/worked-solution'):
  assert (key in q)==(key in rr);assert q.get(key)==rr.get(key),(case,key)
 assert (':question/difficulty' in q)==(':question/difficulty' in rr)
 assert (':answer-field/correct' in sf)==(':answer-field/correct' in rf)
 assert sf[':answer-field/key']==rf[':answer-field/key'];assert rf[':answer-field/type']==sf[':answer-field/type'][':db/ident']
 assert sorted(a[':answer/value'] for a in sf[':answer-field/choices'])==sorted(a[':answer/value'] for a in rf[':answer-field/choices'])
 if ':answer-field/correct' in sf:
  cv=next(a[':answer/value'] for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1]);assert cv==sf[':answer-field/correct'][':answer/value']
 V,q0,c,r,time,_=prompt_math(rr);expected=V*c+(q0-V*c)*sp.exp(-r*t/V)
 vals=rf[':answer-field/choices'];correct_indices=[]
 for i,a in enumerate(vals):
  v=a[':answer/value'];vexpr=fn(v) if time is None else sp.Rational(re.match(r'[\d.]+',v)[0]);target=expected if time is None else sp.Rational(g.rounded(expected.subs(t,time)))
  if sp.expand(vexpr-target)==0:correct_indices.append(i)
 assert len(correct_indices)==1,(case,correct_indices)
 if ':answer-field/correct' in rf:assert vals[correct_indices[0]][':answer/id']==rf[':answer-field/correct'][1]
 assert rec['generation']['evidence_only'] and not rec['generation']['eligible_for_learning'];json.dumps(rec)
 originals.append(rec);coverage.append({'source_id':case['source_id'],'bank_values_matched':5,'prompt_exact':True,'solution_exact_or_omitted':True,'designation_matched':':answer-field/correct' in sf,'difficulty_present':':question/difficulty' in q,'independent_correct_value':vals[correct_indices[0]][':answer/value']})
 # Changed dimensional-similarity variants exercise all seven masks and original banks.
 changed=g.generate(case['level'],71,case['template'],parameters={'mass_scale':'2','flow_scale':'2'},profile=case['bank_profile']);reviews.append(changed)
 vv,qq,cc,rate,tm,_=prompt_math(changed['question']);assert (vv,qq,cc,rate)==(2*V,2*q0,c,2*r)
 if ':question/worked-solution' in rr:
  assert changed['question'][':question/worked-solution']!=rr[':question/worked-solution']
  cs=changed['question'][':question/worked-solution'];assert '$'+g.num(rate)+r'\,\text{L/min}' in cs
  e2=vv*cc;b2=qq-e2;k2=rate/vv
  cmatches=re.findall(r'\\alpha =([\d.]+)\.(?=\n)',cs);assert cmatches and all(parse_num(v)==e2 for v in cmatches)
  finals=re.findall(r'^Q\(t\)=([0-9][^\n]+)',cs,re.M);assert len(finals)==1 and sp.expand(fn('Q(t)='+finals[0].rstrip('.'))-(e2+b2*sp.exp(-k2*t)))==0
  irow=re.search(r'A & =(-?[\d.]+)\\end',cs);assert irow and parse_num(irow[1])==b2

for level in g.LEVELS:
 for seed in range(65):
  rec=g.generate(level,seed);q=rec['question'];p=rec['generation']['parameters'];V,q0,c,r,time,hard=prompt_math(q);k=r/V;E=V*c;A=q0-E;expected=E+A*sp.exp(-k*t)
  assert hard==(level=='hard');assert level!='easy' or time is None
  f=q[':question/answer-fields'][0];answers=f[':answer-field/choices'];assert len(answers)==5
  assert set(rec['knowledge_point'])=={'db_id','id','title'};assert len({a[':answer/id'] for a in answers})==5
  correct=next(a for a in answers if a[':answer/id']==f[':answer-field/correct'][1]); models=[expected,E/2+(q0-E/2)*sp.exp(-2*k*t),2*E+(q0-2*E)*sp.exp(-k*t/2),r*c+(q0-r*c)*sp.exp(-k*t),E-A*sp.exp(-k*t)]
  observed=[fn(a[':answer/value']) if time is None else sp.Rational(re.match(r'[\d.]+',a[':answer/value'])[0]) for a in answers]
  computed=models if time is None else [sp.Rational(g.rounded(x.subs(t,time))) for x in models]
  assert all(any(sp.expand(a-b)==0 for b in computed) for a in observed)
  assert len(set(observed))==5
  assert sp.expand(fn(correct[':answer/value'])-expected)==0 if time is None else sp.Rational(re.match(r'[\d.]+',correct[':answer/value'])[0])==computed[0]
  assert sp.expand(sp.diff(expected,t)-(r*c-r*expected/V))==0 and expected.subs(t,0)==q0
  # Read actual displayed rates, equation and primitive/initial-value stages.
  sol=q[':question/worked-solution'];num=r'[\d.]+'
  rates=re.findall(r'\$('+num+r')\\,\\text\{L/min\}',sol);assert len(rates)==2 and all(parse_num(x)==r for x in rates),(level,seed,rates,r)
  conc=re.findall(r'\$('+num+r')\\,\\text\{kg/L\}',sol);assert conc and all(parse_num(x)==c for x in conc)
  assert r'\frac{Q}{'+g.num(V)+'}' in sol
  ode=re.search(r'\\frac\{dQ\}\{dt\}\+\\frac\{1\}\{('+num+r')\}Q=([^\n]+)\.',sol);assert ode and parse_num(ode[1])==V/r and parse_num(ode[2])==r*c,(level,seed,ode.group() if ode else sol)
  eqs=re.findall(r'\\alpha =('+num+r')\.(?=\n)',sol);assert eqs and all(parse_num(x)==E for x in eqs),(level,seed,eqs,E)
  part=re.search(r'\{Q\}_\{p\}\(t\)=('+num+r')\.\$',sol);assert part and parse_num(part[1])==E
  ic=re.search(r'A & =(-?'+num+r')\\end',sol);assert ic and parse_num(ic[1])==A,(level,seed,ic.group() if ic else sol,A)
  general=re.search(r'Q\(t\)=\{Q\}_\{c\}\(t\)\+\{Q\}_\{p\}\(t\)=A\{e\}\^\{-t/('+num+r')\}\+('+num+r')\.',sol);assert general and parse_num(general[1])==V/r and parse_num(general[2])==E
  final=re.findall(r'^Q\(t\)=([0-9][^\n]+)',sol,re.M);assert len(final)==1 and sp.expand(fn('Q(t)='+final[0].rstrip('.'))-expected)==0
  if time is not None:
   ev=re.search(r'^Q\(('+num+r')\)=([^≈\n]+)≈('+num+r')',sol,re.M);assert ev and parse_num(ev[1])==time and sp.expand(fn('Q(t)='+ev[2])-expected.subs(t,time))==0 and sp.Rational(ev[3])==computed[0]
   assert '$'+g.num(time)+'$ minutes after pumping begins' in sol
  assert 'supplements' not in sol if 'supplement' not in q[':question/problem'] else True
  assert sol.count('**Step ')==4 and sol.count('\\begin{aligned}')==4
  assert '**Step 4**: Integrate the equation.' in sol and 'first-order linear equation with constant coefficients' in sol
  assert 'additives enter' not in sol and 'additives exit' not in sol
  # Balanced delimiters/groups and absence of stale masks/unsupported doubled commands.
  for content in [q[':question/problem'],sol]+[a[':answer/value'] for a in answers]:
   assert content.count('$')%2==0 and content.count('{')==content.count('}') and '⟦' not in content
   assert r'\\text' not in content and not re.search(r'\+\-|\-\-',content)
  json.loads(json.dumps(rec))
  assert rec['question'][':question/id']==g.generate(level,seed+500,parameters=p)['question'][':question/id']
  if seed<2:reviews.append(rec)
  rows.append(rec)
  checks.append({'label':f'{level}-{seed}','record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct[':answer/id'] else 'rejected','purpose':'native owned choice grading'} for a in answers]})
# Exercise every permitted dimensional source profile, including fraction concentrations.
for case in cases:
 for mass in range(1,5):
  for flow in range(1,4):
   raw=g.generate(case['level'],template=case['template'],profile=case['bank_profile'],parameters={'mass_scale':str(mass),'flow_scale':str(flow)})
   q=raw['question'];f=q[':question/answer-fields'][0];assert len({a[':answer/value'] for a in f[':answer-field/choices']})==5
   V,q0,c,r,tm,_=prompt_math(q)
   if tm is not None:
    target=g.rounded(V*c+(q0-V*c)*sp.exp(-r*tm/V));matching=[a for a in f[':answer-field/choices'] if re.match(r'[\d.]+',a[':answer/value'])[0]==target];assert len(matching)==1
    if ':answer-field/correct' in f:assert matching[0][':answer/id']==f[':answer-field/correct'][1]

# Explicit invalid inputs must fail without resampling.
for level in g.LEVELS:
 p=rows[g.LEVELS.index(level)*65]['generation']['parameters'].copy();p['V']='1200'
 try:g.generate(level,parameters=p)
 except ValueError:pass
 else:raise AssertionError('explicit invalid volume accepted')
# Raw source grading only where captured correct references exist.
for rec in originals:
 f=rec['question'][':question/answer-fields'][0]
 if ':answer-field/correct' in f:
  checks.append({'label':'raw-'+rec['generation']['template'],'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'raw captured radio grading; mathematical/TeX eligibility separate'} for a in f[':answer-field/choices']]})
(D/'engine-input.json').write_text(json.dumps(checks,indent=2)+'\n');result=subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(D/'engine-input.json'),str(D/'engine.json')],capture_output=True,text=True);assert result.returncode==0,result.stderr
(D/'review.json').write_text(json.dumps({'original_replays':originals,'generated_variants':reviews},indent=2,ensure_ascii=False)+'\n')
(D/'review.md').write_text('\n\n'.join([g.markdown(x,'ORIGINAL PROFILE REPLAY') for x in originals]+[g.markdown(x,'GENERATED VARIANT — '+('OBSERVED EVIDENCE BANK' if x['generation']['evidence_only'] else x['generation']['origin'].upper())) for x in reviews])+'\n')
cli=subprocess.run([sys.executable,str(D.with_suffix('.py')),'--difficulty','all','--count','2','--format','json'],capture_output=True,text=True);assert cli.returncode==0 and len(json.loads(cli.stdout))==6
md=subprocess.run([sys.executable,str(D.with_suffix('.py')),'--difficulty','easy','--profile','raw_17592186229724'],capture_output=True,text=True);assert md.returncode==0 and 'ORIGINAL PROFILE REPLAY' in md.stdout and 'omitted' in md.stdout
engine=json.loads((D/'engine.json').read_text());report={'status':'pass','database_writes':0,'source_questions':7,'source_banks_matched':7,'source_values_matched':35,'present_source_designations_matched':5,'absent_source_designations':2,'source_solutions_exact':5,'source_solutions_absent':2,'raw_presentation_anomalies':{'doubled_backslash_numeric_banks':sum(any(chr(92)*2 in a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']) for q in src[':knowledge-point/questions']),'ineligible_raw_profiles':7},'raw_dimensional_boundary_checks':84,'normal_math_checks':195,'sampled_unique_tasks':{l:len({r['generation']['mathematical_fingerprint'] for r in rows if r['question'][':question/difficulty'].endswith('/'+l)}) for l in g.LEVELS},'source_coverage':coverage,'native':{k:engine[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'engine_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'authored_extension':'hard g/L to kg conversion before same constant-volume IVP and finite-time evaluation; method-derived complete banks at all levels','plots':'none','stop_step':7}
# Enumerate the finite default sampler without counting context aliases or bank order.
family={'easy':set(),'moderate':set(),'hard':set()}
for rr in [10,12,15,20,25,30,40,50]:
 for tau in [10,12,14,15,16,20,24,25,30,35,40,50,60,70,80]:
  vv=rr*tau
  if not 300<=vv<=1000:continue
  for cent in range(1,7):
   e=sp.Rational(vv*cent,100);forcing=sp.Rational(rr*cent,100)
   for qq in range(1,26):
    if qq==e or qq>=2*e:continue
    if qq==e/2 or qq==2*e or qq==forcing:continue
    family['easy'].add((str(e),str(sp.Rational(1,tau)),qq))
    for tm in range(2,13):
     aa=float(qq-e);ef=float(e);ff=float(forcing);dec=math.exp(-tm/tau)
     options=[ef+aa*dec,ef/2+(qq-ef/2)*dec**2,2*ef+(qq-2*ef)*math.exp(-tm/(2*tau)),ff+(qq-ff)*dec,ef-aa*dec]
     opts=[format(x,'.2f') for x in options]
     if len(set(opts))!=5 or min(options)<=0 or len({len(v.split('.')[0]) for v in opts})!=1:continue
     task=(str(e),str(sp.Rational(1,tau)),qq,tm)
     family['moderate'].add(task);family['hard'].add(task)
report['default_sampler_meaningful_tasks']={k:len(v) for k,v in family.items()}
(D/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
