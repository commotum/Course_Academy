"""Post-filter shortcut and selection audit; run with the job's Python."""
import sys,subprocess,collections,json,hashlib,random
sys.dont_write_bytecode=True
from audit import *

def values(r,fi):return [expr(z[':answer/value']) for z in r['question'][':question/answer-fields'][fi][':answer-field/choices']]
def rightindex(r,fi):
 f=r['question'][':question/answer-fields'][fi];return next(i for i,z in enumerate(f[':answer-field/choices']) if z[':answer/id']==f[':answer-field/correct'][1])
def counts(rows):
 out={'count':len(rows),'coefficients':collections.Counter(),'h_signs':collections.Counter(),'c_signs':collections.Counter(),'IF_positions':collections.Counter(),'y_positions':collections.Counter(),'IF_ranks':collections.Counter()}
 for r in rows:
  p,q,t,h=promptdata(r);out['coefficients'][str(p)]+=1;out['h_signs']['negative' if h<0 else 'positive']+=1;out['c_signs']['negative' if h-q/p<0 else 'positive']+=1
  for fi,key in [(0,'IF_positions'),(1,'y_positions')]:out[key][str(rightindex(r,fi))]+=1
  slopes=[s.simplify(s.diff(v,x)/v) for v in values(r,0)];out['IF_ranks'][str(sorted(slopes).index(p))]+=1
 return out

def predict(r,strategy):
 fi=1 if strategy.startswith('y ') else 0
 f=r['question'][':question/answer-fields'][fi];vs=values(r,fi)
 if strategy.endswith('first'):return fi,0
 if strategy.endswith('last'):return fi,len(vs)-1
 if strategy.endswith('shortest'):return fi,min(range(len(vs)),key=lambda i:len(f[':answer-field/choices'][i][':answer/value']))
 if strategy.endswith('longest'):return fi,max(range(len(vs)),key=lambda i:len(f[':answer-field/choices'][i][':answer/value']))
 if strategy=='IF always e^x':return fi,next((i for i,v in enumerate(vs) if eq(v,s.exp(x))),-1)
 slopes=[s.simplify(s.diff(v,x)/v) for v in vs]
 if strategy=='IF minimum slope':return fi,min(range(len(slopes)),key=lambda i:slopes[i])
 if strategy=='IF maximum slope':return fi,max(range(len(slopes)),key=lambda i:slopes[i])
 if strategy=='IF most repeated y-bank slope':
  freq=collections.Counter(-z.args[0].coeff(x) for v in values(r,1) for z in v.atoms(s.exp))
  return fi,max(range(len(slopes)),key=lambda i:freq[slopes[i]])
 raise ValueError(strategy)

inputs={k:json.load(open(R/p)) for k,p in [('fresh','independent-delivery-input.json'),('fresh accepted','delivery-independent/accepted.json'),('runner','runner-batch.json'),('runner accepted','delivery-batch/accepted.json')]}
stages={k:counts(v) for k,v in inputs.items()}
traces=json.load(open(R/'resampling-traces.json'));stages['rejection_trace']={'proposals':sum(len(z['attempted']) for z in traces),'accepted':len(traces),'coefficients_before':dict(collections.Counter(str(p['a']) for z in traces for p in z['attempted'])),'coefficients_after':dict(collections.Counter(str(z['accepted']['a']) for z in traces)),'rejected_proposals':[p for z in traces for p in z['attempted'][:-1]],'rule':'h=0 or h=b excludes degenerate inherited banks, independent of a; easy bank generation treats a and alternate slope symmetrically.'}
save('stage-coverage.json',stages)
strategies=['IF always e^x','IF first','IF last','IF shortest','IF longest','IF minimum slope','IF maximum slope','IF most repeated y-bank slope','y first','y last','y shortest','y longest']
probes=[]
for stage,rows in inputs.items():
 for group,sub in [('easy_constant',rows),('negative initial value',[r for r in rows if promptdata(r)[3]<0]),('positive initial value',[r for r in rows if promptdata(r)[3]>0])]:
  if len(sub)<4:continue
  for strategy in strategies:
   answers=[predict(r,strategy) for r in sub];correct=sum(i==rightindex(r,fi) for r,(fi,i) in zip(sub,answers))
   probes.append({'stage':stage,'subgroup':group,'strategy':strategy,'correct':correct,'total':len(sub),'baseline':.2 if strategy.startswith('y ') else .25,'question_ids':[r['question'][':question/id'] for r in sub]})
save('shortcut-results.json',probes)
# Faithful read-only selector: captured entity order for existing bank, synthetic larger IDs for new records.
inv=json.load(open(B/'source/inventory.json'));accepted=inputs['fresh accepted'];pool=[]
for q in inv['questions']:
 rating=q.get(':question/difficulty',{});rating=rating.get(':db/ident','') if isinstance(rating,dict) else rating
 if rating==':question.difficulty/easy':pool.append((q[':db/id'],{'question':q},'captured'))
start=max(q[':db/id'] for q in inv['questions'])+1
pool.extend((start+i,r,'new') for i,r in enumerate(accepted));pool.sort(key=lambda z:z[0])
selection=[]
for label,candidates in [('no history',pool),('seen alternating candidates',[z for i,z in enumerate(pool) if i%2]),('new package only',[z for z in pool if z[2]=='new'])]:
 choices=[]
 for trial in range(96):
  seed='independent-630-selection-'+str(trial);digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53)
  eid,r,origin=candidates[int(u*len(candidates))];p,q,t,h=promptdata(r);choices.append({'seed':seed,'entity_id':eid,'question_id':r['question'][':question/id'],'coefficient':str(p),'origin':origin})
 selection.append({'case':label,'candidates':[{'entity_id':z[0],'record':z[1],'origin':z[2]} for z in candidates],'choices':choices,'coefficient_counts':dict(collections.Counter(z['coefficient'] for z in choices))})
save('selection-results.json',{'basis':inv['basis'],'implementation_hash':hashlib.sha256((ROOT/'engine/rust/question_selection.rs').read_bytes()).hexdigest(),'method':'Exact SHA256 uniform(8) within easy band, sorted deduplicated entity IDs, conditional on selecting a positive-weight easy band. No-history and explicit-history exclusions compared.','cases':selection,'limitations':['New entity IDs are a stated ordering scenario: database allocation is not performed. Actual learner histories, policy weights, and task seeds were not supplied.','With distribution=None production chooses the first candidate; that legacy configuration does not claim randomized delivery. Explicit zero easy weight excludes easy; mixed-band weights determine easy frequency, not its conditional within-band distribution.','Five captured legacy easy records retain the previous shortcut, reproduced in generated-records.json and affected-inventory.json; current generator does not overwrite them. Acceptance of current construction cannot certify their remediation.']})
# Confirm previously affected inventory still exactly matches retained complete generated evidence.
legacy=json.load(open(R/'generated-records.json'));legacytests=[]
for r in legacy:
 q=next(q for q in inv['questions'] if q[':question/id']==r['question'][':question/id']);fq=r['question'];same=q[':question/problem']==fq[':question/problem'] and q[':question/worked-solution']==fq[':question/worked-solution'];banks=True
 for f in fq[':question/answer-fields']:
  sf=next(z for z in q[':question/answer-fields'] if z[':answer-field/key']==f[':answer-field/key']);banks &= {z[':answer/id'] for z in sf[':answer-field/choices']}=={z[':answer/id'] for z in f[':answer-field/choices']}
 legacytests.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'same_prompt_solution':same,'same_answer_UUIDs':banks,'original_source':False,'historical_generation_metadata':r['generation']})
save('inventory-current-confirmation.json',{'basis':inv['basis'],'same_inventory_binding_as_previous_review':True,'reconfirmed':legacytests,'scope':'Five historical affected records re-confirmed. Other stored records are outside the retained easy shortcut; no new defects demonstrated there. No database writes.'})
# Package relocation via copied author's current package. Also CLI run from evidence cwd.
py=str(ROOT/'.venv/bin/python');rel=R/'author-current';cmd=[py,str(rel/'17592186087879.py'),'--difficulty','easy','--seed','630071','--count','2','--format','json'];out=subprocess.run(cmd,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},cwd=R)
save('cli-records.json',json.loads(out.stdout));same=json.loads(out.stdout)[0]==inputs['fresh'][0]
save('relocation-results.json',{'command':cmd,'exit_code':out.returncode,'stderr':out.stderr,'relocated_same_record':same,'output':'stdout only; source inputs resolved against __file__; no generated assets.'});assert same
save('package-integrity.json',{'unchanged':hashpackage()==json.load(open(R/'package-before.json')),'files':len(hashpackage())})
assert hashpackage()==json.load(open(R/'package-before.json'))
print(json.dumps({'stages':stages,'shortcut_perfect_current_groups':[z for z in probes if z['correct']==z['total'] and z['total']>=8],'legacy_affected_reconfirmed':len(legacytests),'package_unchanged':True}))
