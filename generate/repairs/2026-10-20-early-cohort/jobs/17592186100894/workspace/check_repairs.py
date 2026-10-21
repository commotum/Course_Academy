"""Executable retained findings; reads visible records and invokes native tools offline."""
from audit_support import *
import collections
E.mkdir(exist_ok=True)
def require(ok, why):
 if not ok:raise AssertionError(why)
def cue(r):
 options=[a for a in field(r)[':answer-field/choices'] if ('\\ln' in a[':answer/value'] or '\\operatorname{ln}' in a[':answer/value']) and '\\pi' not in a[':answer/value']]
 return len(options)==1 and options[0][':answer/id']==field(r)[':answer-field/correct'][1]
def measurements(rs):
 ts=[r for r in rs if r['generation']['template']=='q-104065'];keys=[correct(r) for r in ts]
 return {'total':len(rs),'trig':len(ts),'old_symbol_cue_successes':sum(map(cue,ts)),'key_with_pi':sum('\\pi' in k for k in keys),'key_without_pi':sum('\\pi' not in k for k in keys),'correct_positions':dict(collections.Counter(next(i for i,a in enumerate(field(r)[':answer-field/choices']) if a[':answer/id']==field(r)[':answer-field/correct'][1]) for r in ts)),'constants':dict(collections.Counter(str(r['generation']['parameters'].get('c')) for r in ts))}
# Complete source replay, including the two formerly missing profiles.
source=json.loads((JOB/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions'];replays=[];fidelity=[]
for q in source:
 mid=q[':question/math-academy-id']
 if mid=='q-104058':
  # Read the singular initial equation directly; no solution at its stated IC.
  require('y(1)=1' in q[':question/problem'],'source changed: re-evaluate singular IC')
  continue
 r=g.generate(q[':question/difficulty'][':db/ident'].split('/')[-1],template=mid,replay=True);replays.append(r);sf=q[':question/answer-fields'][0]
 expected=collections.Counter(g.normalize_tex(a[':answer/value']) for a in sf[':answer-field/choices']);actual=collections.Counter(a[':answer/value'] for a in field(r)[':answer-field/choices'])
 require(expected==actual,mid+' complete bank mismatch');require(correct(r)==g.normalize_tex(sf[':answer-field/correct'][':answer/value']),mid+' key mismatch')
 fidelity.append({'template':mid,'source_id':q[':question/id'],'bank_count':sum(actual.values()),'full_bank_equal':True,'correct_equal':True})
save('source-replay-records.json',replays);save('source-replay.json',{'profiles':fidelity,'supported':len(fidelity),'excluded':{'q-104058':'0*yprime=2 at the given IC'},'corrections':'See instructional-account.md and preserved prior REPAIRS; sine equation and local branch restored from worked solution.'})
# Exact old failure, all old shifts, and small factorial decision sample.
trig=[g.generate('easy',847003,'q-104065',{'h':h}) for h in (-4,-3,-2,-1,1,2,3,4)]
trig += [g.generate('easy',8100+5*i+j,'q-104065',{'h':(-4,1,4)[i],'a':a,'c':c}) for i,a in enumerate((2,4,6)) for j,c in enumerate(('-pi^2','-1','0','1','pi^2'))]
require(not any(map(cue,trig)),'retained symbol shortcut persists')
require(all(len(field(r)[':answer-field/choices'])==5 for r in trig),'bank width changed')
# Math witnesses use the prompt's ODE and IC, not generator models/metadata.
rad=[g.generate('moderate',43+i,'q-128199',{'h':1,'b':b}) for i,b in enumerate((-2,-1,1,2))]
native_families=[g.generate(g.level(mid),91+i,mid,{'h':h}) for i,mid in enumerate(('q-355559','q-355577','q-355582','q-350957')) for h in (-4,1,4)]
small=[g.generate(g.level(mid),320+i,mid,{'h':1}) for i,mid in enumerate(g.MODELS) if mid not in ('q-104065','q-126765','q-128199','q-355559','q-355577','q-355582','q-350957')]
# Two relevant changes holding all other data fixed, plus irrelevant seed/order changes.
cf=[g.generate('easy',67,'q-104065',{'h':1,'a':4,'c':c}) for c in ('0','1','pi^2')]
for a,b in zip(cf,cf[1:]):
 require(a['question'][':question/problem']!=b['question'][':question/problem'],'IC prompt stale');require(correct(a)!=correct(b),'constant key stale');require(a['question'][':question/worked-solution']!=b['question'][':question/worked-solution'],'solution stale')
 require(simplify(explicit(a,correct(a))-explicit(b,correct(b)))!=0,'constant response unchanged')
ir=g.generate('easy',68,'q-104065',{'h':1,'a':4,'c':'0'});require(simplify(explicit(ir,correct(ir))-explicit(cf[0],correct(cf[0])))==0,'seed changes mathematical response')
records=trig+rad+native_families+small+cf+[ir];save('current-records.json',records)
math=[]
for r in records:
 print('math',r['generation']['template'],r['generation']['parameters'],flush=True)
 result=math_check(r);require(result['passed'] and result['valid_choice_count']==1,str(result));math.append(result)
save('math-results.json',math)
# Repaired incomplete source: check visible equation, branch condition and full scaffold.
sine=next(r for r in replays if r['generation']['template']=='q-126765');p=sine['question'][':question/problem'];require("y'=2x" in p and 'sqrt{1-y^2}' in p and 'pi/2' in p,'sine restoration/branch missing');require(simplify(expr(correct(sine))-x*x)==0,'sine fragment wrong')
# Independent symbolic differentiation on a local branch where cos(x²+C)>0.
c=S.symbols('C',real=True);zz=S.sin(x*x+c);require(simplify(S.diff(zz,x)-2*x*S.cos(x*x+c))==0,'sine branch derivative wrong')
# Actual learner grade: all current choices; blank key, alternate notation and wrong zero.
cases=[]
for r in records+[sine]:
 f=field(r);checks=[]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected'} for a in f[':answer-field/choices']]
 else:
  v=correct(r);checks=[{'submitted':v,'expected':'accepted'},{'submitted':str(expr(v)).replace('**','^').replace('log(', 'ln(').replace('E','e'),'expected':'accepted','purpose':'independently parsed plain algebra equivalent'},{'submitted':'0','expected':'rejected'},{'submitted':'('+v+')+1','expected':'accepted' if r['generation']['template']=='q-126765' else 'rejected','purpose':'Arbitrary C absorbs constant shifts only in the sine solution-family scaffold'}]
  if r['generation']['template']=='q-128199':checks.append({'submitted':'-('+v+')','expected':'rejected','purpose':'opposite branch has same squared relation but violates IC'})
 cases.append({'label':r['generation']['template']+' '+str(r['generation']['parameters']),'record':r,'checks':checks})
save('grader-input.json',cases)
proc=subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(E/'grader-input.json'),str(E/'grader-report.json')],capture_output=True,text=True);(E/'grader-console.txt').write_text(proc.stdout+proc.stderr);require(proc.returncode==0,'native grader failed: '+proc.stderr)
# Shared filters and same probes AFTER normalization, rejection and inventory deduplication.
stages={}
for difficulty in ('easy','moderate'):
 rs=[r for r in records+[sine] if r['question'][':question/difficulty'].endswith('/'+difficulty)];inp=E/(difficulty+'-input.json');inp.write_text(json.dumps(rs));out=E/('delivery-'+difficulty)
 cmd=[sys.executable,str(ROOT/'generate/pipeline/check_delivery.py'),'--input',str(inp),'--source',str(JOB/'source/source.json'),'--inventory',str(JOB/'source/inventory.json'),'--difficulty',difficulty,'--output',str(out),'--asset-root',str(E),'--math-root','/media/jake/SSD/EDB/math']
 result=subprocess.run(cmd,capture_output=True,text=True);(E/(difficulty+'-delivery-console.txt')).write_text(result.stdout+result.stderr);require(result.returncode==0,result.stdout+result.stderr)
 accepted=json.loads((out/'accepted.json').read_text());stages[difficulty]={'raw':measurements(rs),'accepted':measurements(accepted)}
 if difficulty=='easy':
  m=stages[difficulty]['accepted'];require(m['trig']>0 and m['old_symbol_cue_successes']==0,'delivery shortcut persists');require(m['key_with_pi']>0 and m['key_without_pi']>0,'decision cases lost in filtering')
# Position, pi/log membership, expression-length and coefficient/constant rank probes per trig template.
probes=measurements(trig);require(probes['key_with_pi']>0 and probes['key_without_pi']>0,'constant cases absent');require(len(probes['correct_positions'])>1,'fixed key position')
ranks=collections.defaultdict(collections.Counter)
for r in trig:
 opts=field(r)[':answer-field/choices'];values=[explicit(r,a[':answer/value']) for a in opts];j=next(i for i,a in enumerate(opts) if a[':answer/id']==field(r)[':answer-field/correct'][1]);h=r['generation']['parameters']['h'];coeffs=[S.expand(v-S.log(S.sin(x-h))).coeff(x,2) for v in values];consts=[simplify(v.subs(x,h+S.pi/2)) for v in values]
 for name,arr in [('coefficient',coeffs),('initial_value',consts),('text_length',[len(a[':answer/value']) for a in opts])]:
  below=sum(float(S.N(z-arr[j]))<0 for z in arr);equal=sum(simplify(z-arr[j])==0 for z in arr);ranks[name][str((below,equal))]+=1
require(all(len(c)>1 for c in ranks.values()),'fixed rank cue within trig bank')
save('shortcut-results.json',{'before':'before-shortcut.json','current':probes,'delivery':stages,'rank_counts':ranks,'exact_old_counterexample_now_success':cue(trig[4]),'counterfactuals':[{'parameters':r['generation']['parameters'],'key':correct(r)} for r in cf],'irrelevant_seed_preserved_answer':True,'claims':'No tested universal symbol, position, coefficient rank, IC rank or text-length rank cue; finite audit does not prove absence of every shortcut.'})
# Captured inventory check: original questions are not generated.
inv=json.loads((JOB/'source/inventory.json').read_text());qs=inv['questions'];generated=[q for q in qs if any('generat' in k for k in q)]
require(not generated,'generated inventory requires reproduction and record-matching audit')
save('inventory-audit.json',{'basis':inv['basis'],'records':len(qs),'generated_records':len(generated),'source_ids_match':set(q[':question/id'] for q in qs)==set(q[':question/id'] for q in source),'result':'All captured records are original supplied sources; none is represented as generated. No affected stored generated instance demonstrated; live inventory/history not queried.'})
save('affected-inventory.json',{'affected_questions':[]})
save('repair-results.json',{'findings':['eb86c81d41054c769ae2','6ffd6956bea7b22e14eb','f3b35aaeab20566aa269'],'source_replay':len(replays),'math_records':len(math),'native_cases':len(cases),'shortcut_probes':probes,'status':'passed'})
print(json.dumps({'source_replay':len(replays),'math_records':len(math),'native_cases':len(cases),'delivery':stages,'passed':True}))
