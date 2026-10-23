"""Executable regressions on CURRENT CLI output; no historical batch input default."""
import collections, copy, importlib.util, json, os, pathlib, re, subprocess, sys, tempfile
sys.dont_write_bytecode=True
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import retained_probe as old
W=pathlib.Path(__file__).resolve().parents[1]
JOB=W.parent
REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
E=W/'evidence';E.mkdir(exist_ok=True)
commands=[]
def read(p):return json.loads(pathlib.Path(p).read_text())
def save(name,d): (E/name).write_text(json.dumps(d,indent=2,ensure_ascii=False))
def run(args,stdout=None,env=None):
 commands.append([str(x) for x in args])
 p=subprocess.run(list(map(str,args)),cwd=W,text=True,capture_output=True,env=env)
 if stdout: (E/stdout).write_text(p.stdout)
 assert p.returncode==0,(args,p.stdout[-2000:],p.stderr[-2000:])
 return p.stdout
m=old.load(W)
def cli(count,seed,name):
 env=dict(os.environ,COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(E/'assets'))
 run([sys.executable,W/'17592186064206.py','--difficulty','easy','--count',count,'--seed',seed,'--format','json'],name,env)
 return read(E/name)
def field(r):return old.field(r)
def keyval(r):return next(c[':answer/value'] for c in field(r)[':answer-field/choices'] if c[':answer/id']==old.key(field(r)))
def norm(v):return re.sub(r'\s+','',v.replace(r'\ln',r'\operatorname{ln}').replace(r'\mid','|').replace('⁡',''))
def parts(v):
 p=re.fullmatch(r'(.*?)\\operatorname\{ln\}\|([^|]+)\|\+C',norm(v));assert p,v
 return old.coeff(p[1]),old.expr(p[2])
def validate(rs):
 rows=[];grader=[];x=sp.Symbol('x')
 for r in rs:
  q=r['question'];match=re.search(r'\\d?frac\{(\d+)\}\{([^}]+)\}',q[':question/problem']);assert match,q[':question/problem']
  integrand=sp.Integer(match[1])/old.expr(match[2]);checks=[];ncorrect=0
  for ch in field(r)[':answer-field/choices']:
   c,arg=parts(ch[':answer/value']);valid=sp.cancel(c*sp.diff(arg,x)/arg-integrand)==0
   assert valid==(ch[':answer/id']==old.key(field(r))),(q[':question/problem'],ch)
   ncorrect+=valid
   checks.append({'submitted_answer_id':ch[':answer/id'],'expected':'accepted' if valid else 'rejected','purpose':'independent derivative of visible option'})
  assert ncorrect==1
  assert norm(keyval(r)) in norm(q[':question/worked-solution']),q
  rows.append({'id':q[':question/id'],'integrand':str(integrand),'unique_correct':True,'solution_final_agrees':True})
  grader.append({'label':q[':question/id'],'record':r,'checks':checks})
 return rows,grader
source=read(JOB/'source/source.json')['material']['kp']
replays=[];replay_report=[]
for q in source[':knowledge-point/questions']:
 sid=q[':question/math-academy-id'];p=[2,3,5] if sid=='q-49511' else m.PROFILES[sid]['parameters']
 r=m.generate(template=sid,parameters=p,seed=8301);replays.append(r)
 assert r['question'][':question/problem']==q[':question/problem']
 assert sorted(c[':answer/value'] for c in field(r)[':answer-field/choices'])==sorted(c[':answer/value'] for c in q[':question/answer-fields'][0][':answer-field/choices'])
 if q.get(':question/worked-solution'):
  assert r['question'][':question/worked-solution']==q[':question/worked-solution']
  assert keyval(r)==q[':question/answer-fields'][0][':answer-field/correct'][':answer/value']
 else:assert parts(keyval(r))[0]==sp.Rational(2,3)
 replay_report.append({'source_id':q[':question/id'],'template':sid,'bank_matches':'5/5','prompt_exact':True,'solution':'exact' if q.get(':question/worked-solution') else 'reconstructed and differentiated'})
canonical=m.generate(template='e-449',parameters=[3,5,2],seed=8301);replays.append(canonical)
for k in [':question/problem',':question/worked-solution']:assert canonical['question'][k]==source[':knowledge-point/canonical-example'][k]
# Keep the precise reported positive-slope counterexample even though replay is separate.
replays.append(m.generate(template='q-15707',parameters=[3,5,2],seed=8301))
save('source-replay-records.json',replays);save('source-replay.json',replay_report)
prospective=cli(5,994860459,'prospective-batch.json')
assert prospective==m.batch('easy',5,994860459)
controls=cli(20,0,'control-0.json')+cli(20,1,'control-1.json')
for r in prospective+controls+replays:
 assert m.replay(r['generation'])==r
save('controls.json',controls)
boundaries=[m.generate(parameters=p,seed=8301) for p in [[1,1,-12],[9,1,12],[1,-9,-12],[9,-9,12],[1,9,0],[9,9,0],[3,5,2],[2,3,5]]]
# Explicit probes for both authored profiles at all supported slope signs/classes.
cf=[]
import random
for profile in ['coefficient-choice','argument-choice']:
 for a in [1,3,-3]:
  _,pars=m.candidates(random.Random(8301),[2,a,5],profile)
  group=[m.from_candidates(pars,i,8301,profile) for i in range(5)]
  assert len({keyval(r) for r in group})==5
  assert len({r['question'][':question/problem'] for r in group})==5
  assert len({r['question'][':question/worked-solution'] for r in group})==5
  for i,r in enumerate(group):
   shuffled=m.from_candidates(pars,i,8302,profile)
   assert keyval(shuffled)==keyval(r)
  cf.extend(group)
save('counterfactual-records.json',cf);save('boundary-records.json',boundaries)

def bank_report(rs):
 groups=collections.defaultdict(list)
 for r in rs:
  signature=tuple(sorted(norm(c[':answer/value']) for c in field(r)[':answer-field/choices']))
  groups[signature].append(r)
 result=[]
 for sig,group in groups.items():
  keys={norm(keyval(r)) for r in group}
  assert len(keys)>1,('bank still has invariant answer',sig,len(group))
  # No argument that occurs only once can leak its identity as a privileged option.
  args=collections.Counter(str(parts(c[':answer/value'])[1]) for c in field(group[0])[':answer-field/choices'])
  assert min(args.values())>=2
  result.append({'count':len(group),'distinct_correct_values':len(keys),'argument_multiplicities':sorted(args.values()),'bank':list(sig)})
 probe=old.probe(rs)
 assert probe['correct']<probe['total']
 return {'groups':result,'historical_shortcut':probe,'bank_only_best_possible':sum(max(collections.Counter(norm(keyval(r)) for r in group).values()) for group in groups.values()),'total':len(rs)}

stages={}
for name,rs in [('batch',prospective),('controls',controls),('counterfactual',cf)]:
 raw='prospective-batch.json' if name=='batch' else 'controls.json' if name=='controls' else 'counterfactual-records.json'
 run([sys.executable,REPO/'generate/pipeline/check_delivery.py','--input',E/raw,'--source',JOB/'source/source.json','--inventory',JOB/'source/inventory.json','--difficulty','easy','--output',E/('delivery-'+name),'--asset-root',E/'assets','--math-root','/media/jake/SSD/EDB/math'])
 accepted=read(E/('delivery-'+name)/'accepted.json')
 stages[name]={'raw':bank_report(rs),'delivered':bank_report(accepted),'delivery':read(E/('delivery-'+name)/'delivery.json')}
save('decision-variation.json',stages)
# Within each recognizable authored profile, keys must span coefficient ranks and positions.
coverage={}
for profile in ['coefficient-choice','argument-choice']:
 subset=[r for r in controls+cf if r['generation']['profile']==profile]
 positions=collections.Counter(next(i for i,c in enumerate(field(r)[':answer-field/choices']) if c[':answer/id']==old.key(field(r))) for r in subset)
 assert len(positions)==5
 coverage[profile]={'records':len(subset),'correct_positions':dict(positions),'slope_cases':sorted(set('negative' if r['generation']['parameters'][1]<0 else 'unit' if r['generation']['parameters'][1]==1 else 'positive_nonunit' for r in subset))}
save('coverage.json',coverage)
rows,grader=validate(prospective+controls+cf+boundaries+replays)
save('math.json',rows);save('grader-input.json',grader)
run([REPO/'generate/runs/current/check-engine',E/'grader-input.json',E/'grader-report.json'])
# Relocation uses only declared runtime files and compares CURRENT output byte-for-byte.
import shutil
with tempfile.TemporaryDirectory(dir=E) as tmp:
 root=pathlib.Path(tmp)
 for f in read(W/'package.json')['files']:
  dest=root/f;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/f,dest)
 relocated=json.loads(run([sys.executable,root/'17592186064206.py','--difficulty','easy','--count',5,'--seed',994860459,'--format','json']))
 assert relocated==prospective
for difficulty in ['moderate','hard']:
 try:m.batch(difficulty,5,1)
 except ValueError:pass
 else:raise AssertionError('unsupported difficulty accepted')
inv=read(JOB/'source/inventory.json');source_ids={q[':question/id'] for q in source[':knowledge-point/questions']}
assert all(q[':question/id'] in source_ids for q in inv['questions'])
save('affected-inventory.json',{'affected_questions':[]})
save('inventory-review.json',{'basis':inv['basis'],'stored_count':len(inv['questions']),'source_original_count':len(inv['questions']),'generated_count':0,'conclusion':'Verified all captured inventory IDs are original source questions. No stored generated records to repair. q-49511 lacks key and difficulty; no original is marked generated.','records':[{'id':q[':question/id'],'entity_id':q[':db/id'],'has_key':bool(q[':question/answer-fields'][0].get(':answer-field/correct')),'has_difficulty':bool(q.get(':question/difficulty')),'retired':q.get(':question/retired',False)} for q in inv['questions']]})
# Rendering is a separate final command, not repeated by every preflight.
render=[canonical,replays[1],cf[0],cf[5],cf[10],cf[15],cf[20],cf[25]]
save('render-records.json',render)
save('commands.json',commands)
save('validation-summary.json',{'source_banks':6,'source_choices':30,'canonical_replay':True,'math_records':len(rows),'native_grader_checks':len(grader)*5,'prospective_count':len(prospective),'historical_shortcut':stages['batch']['delivered']['historical_shortcut']['correct'],'deterministic_and_relocated':True,'inventory_generated_records':0,'passed':True})
print(json.dumps(read(E/'validation-summary.json')))
