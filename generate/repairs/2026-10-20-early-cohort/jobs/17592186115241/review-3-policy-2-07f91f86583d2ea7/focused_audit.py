"""Independent repair-3 controls. Only this directory receives output."""
import sys,pathlib,json,importlib.util,copy,random,collections,subprocess,hashlib
sys.dont_write_bytecode=True
from independent_math import *
from reproduce_unit_shortcut import probe
E=pathlib.Path(__file__).resolve().parent;J=E.parent;P=J/'workspace';sys.path.insert(0,str(P))
def dump(n,x):(E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
g=load(P/'17592186115241.py','focused_current')
old=load(J/'review-2-policy-2-4257d0679a900030/relocated/17592186115241.py','focused_old_unit')
records=[];measure=[]
# Supplied-coordinate construction changed. Check fresh source-profile draws,
# exact retained seed, and homogeneous source edge with independent visible math.
for profile in sorted(g.QUESTIONS):
 for seed in (95321,95322):records.append(g.generate_easy(seed=seed,profile=profile))
records += [g.generate_easy(seed=71383,profile='q-32244'),g.generate_easy(seed=71574,profile='q-32244')]
for a in (-1,1):
 records.append(g.generate_easy(seed=95323,parameters={'free_coefficients':[a],'constants':[0],'mix':[1,-2,2],'decision_case':'rank_one'}))
for r in records:
 result=mathcheck(r);assert result['pass'],result
 M=system(r['question'][':question/problem']);piv=M.rref()[1];fc=next(j for j in range(M.cols-1) if j not in piv);t=v[fc];cs=field(r)[':answer-field/choices'];xs=[vec(c[':answer/value']) for c in cs];key=next(i for i,c in enumerate(cs) if c[':answer/id']==correct(r));unit=probe(r)
 assert not unit['shortcut_correct']
 slopes=[str(sp.diff(x[0],t)) for x in xs];intercepts=[str(x[0].subs(t,0)) for x in xs]
 measure.append({'id':r['question'][':question/id'],'seed':r['generation']['seed'],'profile':r['generation']['bank_profile'],'math':result,'unit_probe':unit,'first_slopes':slopes,'first_intercepts':intercepts,'key_position':key+1})
dump('focused-records.json',records);dump('focused-results.json',measure)
# Keep a default candidate bank unchanged while changing which line satisfies
# the printed system. In-memory RNG intervention changes only the first role draw.
base=g.random.Random;roles=[];role_results=[]
try:
 fresh=json.load(open(E/'fresh.json'))
 for case in g.EASY_CASES:
  seed=next(r['generation']['seed'] for r in fresh if r['generation']['decision_case']==case)
  group=[]
  for role in range(5):
   class RoleRandom(base):
    def __init__(self,*args,**kw):super().__init__(*args,**kw);self.forced=False
    def randrange(self,*args,**kw):
     z=super().randrange(*args,**kw)
     if args==(5,) and not kw and not self.forced:self.forced=True;return role
     return z
   g.random.Random=RoleRandom
   r=g.generate_easy(seed=seed);assert mathcheck(r)['pass'];group.append(r)
  banks=[sorted(str(vec(c[':answer/value'])) for c in field(r)[':answer-field/choices']) for r in group]
  keys=[str(vec(next(c[':answer/value'] for c in field(r)[':answer-field/choices'] if c[':answer/id']==correct(r)))) for r in group]
  assert all(x==banks[0] for x in banks) and len(set(keys))==5
  assert len({r['question'][':question/problem'] for r in group})==5
  assert len({r['question'][':question/worked-solution'] for r in group})==5
  role_results.append({'case':case,'seed':seed,'fixed_bank':banks[0],'five_distinct_keys':keys,'distinct_prompts_and_solutions':True});roles+=group
finally:g.random.Random=base
dump('role-records.json',roles);dump('role-results.json',role_results)
# Both author executable predicates and strict independent regressions must fail
# on the precise historical witness. Do not weaken them to obtain current passes.
sys.path.insert(0,str(E/'author-checks'))
ar=load(E/'author-checks/unit_support.py','author_unit_predicate')
rr=load(E/'author-checks/rational_support.py','author_fraction_predicate')
original=load(pathlib.Path('/home/jake/Developer/Course_Academy/generate/scratch/17592186115241.py'),'baseline_v1')
frac_old=load(J/'review-1-policy-2-64575e53a5a82ae1/relocated/17592186115241.py','baseline_fraction')
au=old.generate_easy(seed=71383,profile='q-32244');cu=g.generate_easy(seed=71383,profile='q-32244')
failures=[]
for label,module,rrr in [('unit',ar,au),('fraction',rr,frac_old.generate_easy(seed=71381,profile='q-32244'))]:
 try:module.inspect([rrr]);raise RuntimeError('Known failing witness unexpectedly passed')
 except AssertionError as ex:failures.append({'predicate':label,'historical_rejection':str(ex)})
ar.inspect([cu]);rr.inspect([g.generate_easy(seed=71381,profile='q-32244')])
runs=[]
for name,exitcode in [('strict_prior_unit.py',1),('reproduce_unit_shortcut.py',0),('strict_prior_fraction.py',1),('reproduce_shortcut.py',0)]:
 cp=subprocess.run([sys.executable,'-B',str(E/name)],capture_output=True,text=True);assert cp.returncode==exitcode,(name,cp.stderr)
 runs.append({'command':cp.args,'exit':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr})
pre=json.load(open(J/'repair-preflight.json'))
for c in pre['checks']:assert hashlib.sha256((P/c['script']).read_bytes()).hexdigest()==c['sha256']
dump('repair-verification.json',{'retained_finding_count':len(json.load(open(J/'repair-history.json'))['findings']),'preflight':pre,'predicate_tests':failures,'current_author_predicates':'same inspect calls pass on the current exact seeds','strict_before_after':runs,'earlier_failures':'strict-regressions.json','current_author_suites':{n:(E/('author-'+n+'-console.txt')).read_text() for n in ['validate','rational','unit']},'author_script_changes':'Only copied filesystem/output paths changed; originals not executed with package output directories.'})
# Actual radio grader: all five choices, plus before/after historical witness.
grades=[{'label':'focused-'+str(i),'record':r,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==correct(r) else 'rejected','purpose':'Independent full-solution check; changed bank or fixed-bank role control'} for c in field(r)[':answer-field/choices']]} for i,r in enumerate(records+roles+[au])]
dump('focused-grader-input.json',grades)
dump('focused-render-records.json',[records[-4],records[-3],records[-2],records[-1],roles[0],roles[1]])
(E/'session-state.md').write_text('Completed 14-bank source replay, 126 exact math/solution checks, 36 fresh default samples, delivery of exact five batch records and source/control samples, 634 native grader checks, all retained historical counterexamples, author suites redirected here, fresh supplied-coordinate and 30 fixed-bank role controls. Actual UI first six inspected; remaining rendering and focused grader/renderer pending. Package still unchanged.\n')
print(json.dumps({'changed_records':len(records),'fixed_bank_role_records':len(roles),'historical_predicates_failed_as_expected':len(failures),'strict_regression_runs':[(x['command'][-1],x['exit']) for x in runs]}))
