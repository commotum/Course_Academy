import sys
sys.dont_write_bytecode=True
import json,re,hashlib,subprocess,shutil,os
from pathlib import Path
from fractions import Fraction
from collections import Counter,defaultdict
from itertools import product
E=Path(__file__).resolve().parent
R=Path('/home/jake/Developer/Course_Academy')
P=R/'generate/scratch/17592186152131/repair-2026-10-18/pipeline/workspace'
B=P.parent
PYTHON=R/'.venv/bin/python'
sys.path.insert(0,str(P)); import generator as g

def save(name,x):
 (E/name).write_text(json.dumps(x,indent=2)+'\n')
def hashes():return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in P.iterdir() if p.is_file()}
if not (E/'package-before.json').exists():save('package-before.json',hashes())
def clean(s):return re.sub(r'[{}\s]','',s)
def factors(q):
 q=Fraction(q);out=Counter()
 for v,sign in [(q.numerator,1),(q.denominator,-1)]:
  k=2
  while k*k<=v:
   while v%k==0:out[k]+=sign;v//=k
   k+=1
  if v>1:out[v]+=sign
 return out

def value(s):
 s=s.strip()
 m=re.fullmatch(r'\{([\d.]+)\}\^\{(\d+)/(\d+)\}',s)
 if m:
  a,u,v=m.groups();return tuple(sorted((p,Fraction(k)*Fraction(int(u),int(v))) for p,k in factors(a).items() if k))
 m=re.fullmatch(r'\\frac\{(\d+)\}\{(\d+)\}',s)
 if m:s=str(Fraction(*map(int,m.groups())))
 return tuple(sorted((p,Fraction(k)) for p,k in factors(s).items() if k))
def inspect(r):
 q=r['question'];f=q[':question/answer-fields'][0];cs=f[':answer-field/choices']
 m=re.search(r'\\sqrt(?:\[(\d+)\])?\{([\d.]+)\}',q[':question/problem']);assert m,q
 n=int(m[1] or 2);x=Fraction(m[2]); expected=tuple(sorted((p,Fraction(k,n)) for p,k in factors(x).items() if k))
 vals=[value(a[':answer/value']) for a in cs];key=f[':answer-field/correct'][1]
 assert len(cs)==5 and len(set(vals))==5,(q[':question/problem'],[a[':answer/value'] for a in cs])
 hit=[a[':answer/id'] for a,v in zip(cs,vals) if v==expected]; assert hit==[key],(q[':question/problem'],hit,key)
 solution=q[':question/worked-solution'];final=solution.split('=')[-1].strip().removesuffix('$$').strip()
 assert value(final)==expected,(q[':question/problem'],final)
 assert f'x={m[2]},' in solution and f'n={n}.' in solution
 return {'x':str(x),'n':n,'key':key,'position':[a[':answer/id'] for a in cs].index(key),'template':r['generation']['template'],'profile':r['generation']['profile']}

def graded(label,r):
 f=r['question'][':question/answer-fields'][0];key=f[':answer-field/correct'][1]
 return {'label':label,'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key else 'rejected','purpose':'Independent exact prime-exponent arithmetic determines equivalence to prompt.'} for a in f[':answer-field/choices']]}

batch=json.loads((B/'samples.json').read_text());save('runner-batch.json',batch)
# Fresh small batches, plus exhaustive semantic-capacity boundary runs.
seeds=[82371,946217,540823,829301,750117,838251,387341,1000039,131101,524309,20261019,251051]
records=[];runs=[]
for seed in seeds:
 a=g.generate_batch(count=5,seed=seed);assert a==g.generate_batch(count=5,seed=seed)
 records+=a;runs.append({'seed':seed,'count':5,'records':a})
capacity=len({(str(x),n) for t in g.TEMPLATES for x,n in g.domain(t)})
for seed in [870031,891207]:
 a=g.generate_batch(count=capacity,seed=seed);assert len({(str(r['generation']['parameters']['x']),r['generation']['parameters']['n']) for r in a})==capacity
 records+=a;runs.append({'seed':seed,'count':capacity,'records':a})
save('sample-runs.json',runs);save('samples.json',records)

# Reconstruct source from immutable capture, not author's source-case file.
src=json.loads((B/'source/source.json').read_text())['material']['kp']
replay=g.source_replay();replay_results=[]
for old,new in zip(src[':knowledge-point/questions'],replay):
 q=new['question']; f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
 assert clean(q[':question/problem'])==clean(old[':question/problem'])
 assert sorted(clean(a[':answer/value']) for a in f[':answer-field/choices'])==sorted(clean(a[':answer/value']) for a in of[':answer-field/choices'])
 if ':question/worked-solution' in old:assert clean(q[':question/worked-solution'])==clean(old[':question/worked-solution'])
 inspect(new)
 replay_results.append({'source_id':old[':question/id'],'ma_id':old[':question/math-academy-id'],'prompt':True,'complete_bank':True,'choice_count':len(f[':answer-field/choices']),'solution':'matched after insignificant braces/whitespace normalization' if ':question/worked-solution' in old else 'missing in capture; inferred from tutorial, explicitly identified by author','key':'verified with independent arithmetic; captured q-69158 key absent'})
canonical=g.generate(4,5,'indexed-equation');inspect(canonical)
save('source-replay.json',{'records':replay,'checks':replay_results,'canonical':canonical,'canonical_check':'4^(1/5) and identity/substitution stages match e-4959. Canonical worked example has no captured answer bank; ordinary equation wording is not a claim to reproduce a fourth question bank.'})

# Controlled complete-bank target swaps, and irrelevant choice reordering.
cf=[];pairs=[]
for t in ['indexed-equation','indexed-what']:
 for u,v in [(2,3),(15,10)]:
  group=[]
  for x,n in product([2,15],[3,10]):
   group.append(g.generate(x,n,t,indexed_bank={'bases':(2,15),'indices':(3,10),'foil_numerator':u,'foil_denominator':v},order_seed=70091))
  assert len({r['question'][':question/answer-fields'][0][':answer-field/correct'][1] for r in group})==4
  assert len({tuple(sorted(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])) for r in group})==1
  cf+=group;pairs.append({'kind':'relevant','label':f'{t} fixed bank foil {u}/{v}, all four targets','indices':list(range(len(cf)-4,len(cf))),'expected':'same five mathematical choices; radicand/index changes must change key value and final equation'})
# Hold c (the inverted-power distractor base) fixed while exchanging target bases.
for bases in [(2,3),('1.8','2.5')]:
 for foil in [1,3,4,5]:
  a=g.generate(bases[0],2,'square-equation',foil_index=foil,base_direction=1,inverted_base='target',order_seed=70091)
  b=g.generate(bases[1],2,'square-equation',foil_index=foil,base_direction=-1,inverted_base='other',order_seed=70091)
  assert sorted(c[':answer/value'] for c in a['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(c[':answer/value'] for c in b['question'][':question/answer-fields'][0][':answer-field/choices'])
  cf += [a,b];pairs.append({'kind':'relevant','label':f'square targets {bases} foil {foil}','indices':[len(cf)-2,len(cf)-1],'expected':'same bank; target base and correct expression change'})
a=g.generate(9,7,'indexed-what',order_seed=51)
b=g.generate(9,7,'indexed-what',order_seed=52)
cf += [a,b];pairs.append({'kind':'irrelevant','label':'reorder same choices only','indices':[len(cf)-2,len(cf)-1],'expected':'prompt, solution, answer value and accepted choice UUID preserved; visual position changes'})
assert a['question'][':question/problem']==b['question'][':question/problem']
assert a['question'][':question/worked-solution']==b['question'][':question/worked-solution']
assert a['question'][':question/answer-fields'][0][':answer-field/correct']==b['question'][':question/answer-fields'][0][':answer-field/correct']
save('counterfactual-records.json',cf);save('counterfactual-pairs.json',pairs)

errors=[];summary=Counter()
for i,r in enumerate(records+batch+cf):
 try:info=inspect(r);summary.update([info['template']])
 except Exception as e:errors.append({'index':i,'error':str(e)})
save('math-results.json',{'method':'Parse served prompt and choices independently of metadata. Exact prime-exponent vectors of positive rationals certify equality of roots and powers; check every bank has exactly five distinct values and one matching key, final solution expression and x/n substitutions.','records':len(records+batch+cf),'template_counts':summary,'failures':errors})
assert not errors,errors[:3]
# True invalid-input contract and capacity boundaries.
bounds=[]
for label,kw,expect in [('zero',{'count':0},False),('negative',{'count':-1},True),('capacity-plus-one',{'count':capacity+1},True),('moderate',{'difficulty':'moderate'},True),('hard',{'difficulty':'hard'},True)]:
 try:g.generate_batch(**kw);raised=False
 except ValueError:raised=True
 assert raised==expect;bounds.append({'case':label,'arguments':kw,'rejected':raised})
for x,n,t in [(1,3,'indexed-equation'),(-2,3,'indexed-equation'),(3,1,'indexed-what'),(3,2,'indexed-equation'),(3,3,'indexed-equation'),(2,4,'indexed-equation'),(16,3,'indexed-equation')]:
 try:g.generate(x,n,t);raised=False
 except ValueError:raised=True
 bounds.append({'case':'parameter-domain','arguments':[x,n,t],'rejected':raised});assert raised
save('boundary-results.json',{'capacity':capacity,'tests':bounds,'construction':'Code constructs eligible complete profiles and unused targets directly, rather than rejecting emitted questions. Full-capacity runs exercise exhaustion/direction fallback.'})

# Native grader cases: all counterfactual choices, all replay choices, actual batch, boundary sample.
graders=[graded('cf-'+str(i),r) for i,r in enumerate(cf)]+[graded('source-'+str(i),r) for i,r in enumerate(replay)]+[graded('runner-'+str(i),r) for i,r in enumerate(batch)]+[graded('sample-'+str(i),r) for i,r in enumerate(records[:10])]
save('grader-input.json',graders)
# Render all controlled pairs; choose a compact source and runner representation too.
save('render-records.json',[cf[i] for i in [0,1,2,3,16,17,24,25,32,33]]+replay+batch)
# Relocate declared runtime files and run from an unrelated working directory.
manifest=json.loads((P/'package.json').read_text());rel=E/'relocated';rel.mkdir(exist_ok=True)
for f in manifest['files']:shutil.copy2(P/f,rel/f)
env=os.environ|{'PYTHONDONTWRITEBYTECODE':'1'}
res=subprocess.run([str(PYTHON),'-B',str(rel/'generator.py'),'--count','5','--seed','82371'],cwd=E,capture_output=True,text=True,env=env)
assert res.returncode==0,res.stderr
assert json.loads(res.stdout)==json.loads(json.dumps(runs[0]['records']))
save('relocation-sample.json',json.loads(res.stdout))
save('packaging-results.json',{'manifest':manifest,'runtime_python':sys.version.split()[0],'relocation_returncode':res.returncode,'relocation_matches':True,'external_outputs':[],'third_party_imports':'none; stdlib plus declared math_format.py','before':hashes(),'boundary_file':'boundary-results.json'})
assert sys.version.split()[0]==manifest['dependencies']['python'];assert manifest['dependencies']['packages']=={}
(E/'session-state.md').write_text('Completed source replay, fresh seeded sampling, full semantic-capacity runs, independent exact arithmetic, controlled pairs, rejection boundaries, deterministic replay and package relocation. Saved grader and renderer inputs. Next: native grading, delivery filters, learner-selection/shortcut analysis, actual UI inspection.\n')
print(json.dumps({'samples':len(records),'capacity':capacity,'counterfactuals':len(cf),'replay':len(replay),'math_failures':len(errors),'grading_records':len(graders)}))
