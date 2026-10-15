"""Independent printed-content, finite slots, field contracts and unchanged native grading."""
from pathlib import Path
import importlib.util,sys,json,hashlib,subprocess,copy,itertools,time,re
sys.dont_write_bytecode=True
D=Path(__file__).parent;ROOT=D.parents[2]
def module(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
g=module('kp68915_draft',D.with_suffix('.py'));v=module('kp68915_readback',D/'readback.py');s=g.s
ENGINE=ROOT/'generate/runs/current/check-engine';ENGINE_SHA='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,z):(D/n).write_text(json.dumps(z,indent=2,ensure_ascii=False)+'\n')
def invalid(fn):
 try:fn()
 except (ValueError,AssertionError,TypeError):return
 raise AssertionError('invalid public input accepted')
def check(r):
 g.fmt.validate_generated_record(r);q=r['question'];assert len(q[':question/answer-fields'])==1
 for t in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value']for a in q[':question/answer-fields'][0][':answer-field/choices']]:assert not any(ord(c)<32 and c not in '\n\t\r'for c in t)
 given,_=v.validate(q);v.structure(q,r['generation']['template'])
 # Read each numerical slot from actual displayed substitution/integrand/limits,
 # independent of generator model metadata; stale but internally consistent math
 # must not masquerade as sampled slot coverage.
 meta=r['generation'];p=meta['parameters'];conf=g.CONFIG[meta['template']]
 arg=v.scalar(re.search(r'If we let \$u=(.*?),\$',q[':question/worked-solution'])[1])
 a=g.rat(p['a'])*(s.pi if conf[3]else 1);b=g.rat(p['b'])*(s.pi if conf[4]else 1)
 assert v.zero(s.diff(arg,v.x)-a) and v.zero(arg.subs(v.x,0)-b),'stale displayed slope/shift'
 assert v.zero(given['body']-p['c']*getattr(s,conf[2])(arg)),'stale displayed coefficient or trig operand'
 if 'lo'in p:
  assert given['bounds'] and all(v.zero(arg.subs(v.x,z)-g.rat(p[k])*s.pi)for z,k in zip(given['bounds'],('lo','hi'))),'stale displayed endpoints'
  assert given['bounds'][0]<given['bounds'][1]
 else:assert given['bounds']is None
 assert meta['mathematical_fingerprint']==g.digest([str(given['body']),None if given['bounds']is None else list(map(str,given['bounds']))]),'actual printed task fingerprint differs'

assert sha(ENGINE)==ENGINE_SHA
assert json.loads((D/'source.json').read_text())==json.loads((ROOT/'generate/runs/current/refresh-2026-10-14/sources/17592186068915.json').read_text())
baseline=json.loads((D/'registration-baseline.json').read_text())['files'];numeric=ROOT/'generate/scratch/17592186068915';now={str(p.relative_to(ROOT)):sha(p)for p in [numeric.with_suffix('.py')]+sorted(p for p in numeric.rglob('*')if p.is_file())};assert now==baseline,'registered numeric script/evidence/caches changed'
started=time.monotonic();source_results=[];native=[];records=[];coverage={};capacities={};blank_reps={};level_fingerprints={level:set()for level in ('easy','moderate','hard')}
for case in json.loads((D/'source-cases.json').read_text()):
 sid=case['source_id'];c=g.CONFIG[sid];r=g.generate(c[0],template=sid,parameters=case['parameters'],profile='observed');check(r);n,d=v.fidelity(g.QS[sid],r['question']);records.append(r)
 assert r['generation']['evidence_only']==(sid=='q-2204') and r['generation']['eligible_for_learning']==(sid!='q-2204')
 sf=g.QS[sid][':question/answer-fields'][0];df=r['question'][':question/answer-fields'][0];assert sf[':answer-field/key']==df[':answer-field/key']
 source_results.append({'source_id':sid,'matched_choices':n,'matched_distractors':d,'complete_bank':True,'solution':'missing original; authored completion'if sid=='q-2204'else'normalized source prose, ordered stages and every formal operand matched','key':'missing original; independently completed'if sid=='q-2204'else'observed key matched'})
 if c[1]=='radio':native.append({'label':sid+'-source-owned-IDs','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==df[':answer-field/correct'][1]else'rejected','purpose':'field-owned radio selection; independent math bank checked separately'}for a in df[':answer-field/choices']]})
 other=g.generate(c[0],999,template=sid,parameters=case['parameters'],profile='observed');assert other['question'][':question/id']==r['question'][':question/id'];assert other['generation']['parameters']==r['generation']['parameters']
 for seed in (321,654):
  r=g.generate(c[0],seed,template=sid);check(r);records.append(r)
 print('Source and variants',sid,'passed',flush=True)
# Full bounded banks and real mathematical task fingerprints; source identity,
# field format, seed and option order do not add capacity. Select coverage cases
# greedily, then independently read every declared slot value in actual content.
for sid,conf in g.CONFIG.items():
 allp=list(g.instances(sid));valid=[];rejected=0;slots={k:set()for k in conf[-1]};covered={k:set()for k in conf[-1]};selected=[]
 for p in allp:
  try:out=g.core(sid,p,'method')
  except ValueError:rejected+=1;continue
  valid.append((p,g.digest([out[4]['integrand'],out[4]['bounds']])));level_fingerprints[conf[0]].add(valid[-1][1])
  for k,z in p.items():slots[k].add(str(z))
  if any(str(z)not in covered[k]for k,z in p.items()):
   selected.append(p)
   for k,z in p.items():covered[k].add(str(z))
  if conf[1]=='blank':
   # Independent exact scalar target; native grouping by identical canonical value.
   a=g.rat(p['a'])*(s.pi if conf[3]else 1);c=s.Integer(p['c']);lo=g.rat(p['lo'])*s.pi;hi=g.rat(p['hi'])*s.pi
   z=s.simplify(c/a*((s.cos(lo)-s.cos(hi))if conf[2]=='sin'else(s.sin(hi)-s.sin(lo))))
   blank_reps.setdefault((sid,str(z)),(p,z))
 for p in selected:
  r=g.generate(conf[0],template=sid,parameters=p);check(r);records.append(r)
 assert covered==slots
 coverage[sid]={'candidate_tuples':len(allp),'valid_complete_banks':len(valid),'whole_bank_rejections':rejected,'meaningful_capacity':len({fp for _,fp in valid}),'printed_content_slot_covering_cases':len(selected),'slot_values':{k:sorted(z)for k,z in slots.items()}}
 print('Finite slots',sid,len(valid),'valid',rejected,'colliding banks;',len(selected),'independently printed cases',flush=True)
# Capacity uses actual integrand+bounds, excluding labels/profiles and metadata.
for level in ('easy','moderate','hard'):capacities[level]=len(level_fingerprints[level])
# Every unique finite blank result goes through canonical, genuine equivalent and
# ordinary valid wrong submissions in the frozen real application grader.
for (sid,_),(p,expected)in blank_reps.items():
 r=g.generate(g.CONFIG[sid][0],template=sid,parameters=p);f=r['question'][':question/answer-fields'][0];canonical=f[':answer-field/choices'][0][':answer/value'];assert v.zero(v.scalar(canonical)-expected)
 checks=[{'submitted':canonical,'expected':'accepted','purpose':'canonical bounded blank target'},{'submitted':r'\frac{2('+canonical+r')}{2}','expected':'accepted','purpose':'valid unsimplified equivalent'},{'submitted':'('+canonical+r')\sin(\frac{\pi}{2})','expected':'accepted','purpose':'valid equivalent finite trig expression'}]
 for wrong in ('0','1','-1','17','100','-100',g.tex(expected+1),g.tex(expected-1)):
  if not v.zero(v.scalar(wrong)-expected):checks.append({'submitted':wrong,'expected':'rejected','purpose':'ordinary valid mathematical wrong value'})
 native.append({'label':sid+'-full-output-'+str(expected),'record':r,'checks':checks})
for sid in ('q-350040','q-346081'):
 r=g.generate(g.CONFIG[sid][0],template=sid,parameters=g.CONFIG[sid][-1],profile='observed');z=r['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']
 native.append({'label':sid+'-observed-wording-policy','record':r,'checks':[{'submitted':z,'expected':'accepted','purpose':'observed wording canonical'},{'submitted':r'\frac{2('+z+r')}{2}','expected':'rejected','mathematical_expected':'accepted','purpose':'valid math rejected: observed Do not round triggers format policy'}]})
r=g.generate('moderate',template='q-346081');native.append({'label':'malformed-diagnostic-separate','record':r,'checks':[{'submitted':r'\unsupported{!}','expected':'unresolved','purpose':'malformed notation diagnostic, separate from valid math'}]})
runner=module('kp68915_native_runner',D/'run_native.py');proc,native_limits=runner.run(native);print(proc.stdout,flush=True)
# Strict public API and exact metadata replay independent of option RNG.
for z in (True,None,1.5,'1'):invalid(lambda z=z:g.generate('easy',z))
for z in (True,0,-1,1.5,'2'):invalid(lambda z=z:g.batch('easy',count=z))
for sid,c in g.CONFIG.items():
 for key in c[-1]:
  p=dict(c[-1]);p[key]=True;invalid(lambda p=p,sid=sid,c=c:g.generate(c[0],template=sid,parameters=p))
 p=dict(c[-1]);p['extra']=1;invalid(lambda:g.generate(c[0],template=sid,parameters=p))
 p=dict(c[-1]);p['a']='17';invalid(lambda:g.generate(c[0],template=sid,parameters=p))
for level in capacities:
 rs=g.batch(level,seed=42,count=3);assert len(rs)==3 and len({v.read_integral(r['question'][':question/problem'])['raw']for r in rs})==3
 invalid(lambda level=level:g.batch(level,count=capacities[level]+1))
 r=rs[0];m=r['generation'];replay=g.generate(level,m['seed'],template=m['template'],parameters=m['parameters'],profile=m['bank_profile']);assert r==replay
 for r in rs:check(r)
# CLI exactly three per level, flat JSON and rendered Markdown.
for form in ('json','markdown'):
 p=subprocess.run([sys.executable,'-B',str(D.with_suffix('.py')),'--difficulty','all','--count','3','--seed','8','--format',form],capture_output=True,text=True);assert p.returncode==0,p.stderr
 if form=='json':
  rs=json.loads(p.stdout);assert len(rs)==9;assert all(type(z)is dict for z in rs);assert {lev:sum(z['question'][':question/difficulty']==':question.difficulty/'+lev for z in rs)for lev in capacities}=={lev:3 for lev in capacities}
 else:assert p.stdout.count('If we let $u=')==9
# Fail-closed mutation checks on displayed math, operators, table endpoints,
# component contributions, bank values and key ownership.
base=g.generate('moderate',template='q-10574',parameters=g.CONFIG['q-10574'][-1]);mutations=[]
for old,new in [(r'\text{d}u',r'\text{d}x'),(r'\frac{1}{3}\text{d}u',r'\frac{1}{2}\text{d}u'),('| $u$ | $', '| $u$ | $1+'),(r'\cos(\frac{2 \pi}{3})',r'\cos(\frac{\pi}{3})')]:
 q=copy.deepcopy(base['question']);assert old in q[':question/worked-solution'],old;q[':question/worked-solution']=q[':question/worked-solution'].replace(old,new,1);invalid(lambda q=q:v.validate(q));mutations.append(old)
q=copy.deepcopy(base['question']);q[':question/answer-fields'][0][':answer-field/correct'][1]='not-owned';invalid(lambda:v.validate(q));mutations.append('key ownership')
# Preservation rechecked after all imports/CLI; none points into numeric evidence.
now={str(p.relative_to(ROOT)):sha(p)for p in [numeric.with_suffix('.py')]+sorted(p for p in numeric.rglob('*')if p.is_file())};assert now==baseline
save('capacity.json',{'basis':2275,'meaningful_tasks_per_level':capacities,'overlap':'Authored hard shares the moderate q10574 task domain; cross-level capacity must not be summed.','coverage':coverage})
engine=json.loads((D/'engine-validation.json').read_text());report={'status':'passed independent mathematics and fidelity; documented native limits','basis':2275,'source_fidelity':{'ma_records':len(source_results),'complete_banks':len(source_results),'matched_choices':sum(z['matched_choices']for z in source_results),'matched_distractors':sum(z['matched_distractors']for z in source_results),'sources':source_results},'independent_printed_records':len(records),'coverage':coverage,'capacity':capacities,'native':{k:engine[k]for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'ordinary_valid_math_native_unresolved':len(native_limits),'engine_sha256':ENGINE_SHA,'api':'strict builtin int seed/count/c, reduced rational strings; full finite explicit parameter bounds; exact replay; flat all count3 JSON+Markdown; finite overflow rejection','mutation_checks':mutations,'registered_pathset_and_hashes_preserved':True,'limits':['No observed hard source; provisional authored rating shares moderate workload.','q2204 original key/solution/rating absent and independently completed.','Observed Do not round wording rejects valid unsimplified equivalents; normal wording repaired.','Three valid ordinary wrong submissions 1 against 4/pi,2sqrt(3)/pi,3/pi are unresolved by unchanged native rules. All mathematically valid outputs remain in ordinary scope. See native-mathematical-limits.json.','One intentionally malformed diagnostic unresolved, separated from valid math.'],'elapsed_seconds':round(time.monotonic()-started,2),'database_writes':0}
save('validation.json',report);print(json.dumps({k:report[k]for k in ('status','capacity','native','elapsed_seconds')},indent=2),flush=True)
