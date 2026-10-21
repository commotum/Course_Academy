import sys
sys.dont_write_bytecode=True
import json,re,hashlib,importlib.util
from pathlib import Path
from collections import Counter,defaultdict
from fractions import Fraction
E=Path(__file__).resolve().parent
R=Path('/home/jake/Developer/Course_Academy');B=R/'generate/scratch/17592186152131/repair-2026-10-18/pipeline';P=B/'workspace'
sys.path.insert(0,str(P));import generator as g
sys.path.insert(0,str(R))
spec=importlib.util.spec_from_file_location('shared_check_delivery',R/'generate/pipeline/check_delivery.py');delivery=importlib.util.module_from_spec(spec);spec.loader.exec_module(delivery)
inventory=json.loads((B/'source/inventory.json').read_text());source=json.loads((B/'source/source.json').read_text())

def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
def inspect(r):
 q=r['question'];f=q[':question/answer-fields'][0];cs=f[':answer-field/choices'];k=f[':answer-field/correct'][1];key=next(c[':answer/value'] for c in cs if c[':answer/id']==k)
 return cs,key

def score(rs):
 # Shortcut reads only the answer bank, with no radical or generation metadata.
 out=Counter(); refs=[]
 for i,r in enumerate(rs):
  if 'captured_inventory_question' in r: continue
  cs,key=inspect(r);v=[c[':answer/value'] for c in cs]
  half=sorted(s for s in v if s in ('{2}^{1/2}','{3}^{1/2}'))
  if len(half)==2:
   out['total']+=1;out['correct']+=key=='{2}^{1/2}';refs.append(i)
 return dict(out)|{'indices':refs}
# Five-question independent prospective publications against same captured inventory.
# Each call uses the actual supplied adapter, so independent batches are not deduplicated against each other.
runs=[];raw=[];accepted=[];stage=Counter()
for seed in range(461003,461515):
 rs=g.generate_batch(count=5,seed=seed)
 out=E/'trial-delivery'
 report=delivery.audit(rs,inventory,source,'easy',out,E,Path('/media/jake/SSD/EDB/math'))
 ac=json.loads((out/'accepted.json').read_text());runs.append({'seed':seed,'count':5,'input':rs,'accepted':ac,'stage_counts':{k:report[k] for k in ('input_count','duplicate_count','accepted_count')}})
 raw+=rs;accepted+=ac
 stage.update({k:report[k] for k in ('input_count','duplicate_count','accepted_count')})
save('shortcut-trials.json',runs);save('shortcut-raw.json',raw);save('shortcut-accepted.json',accepted)
# One complete-bank target quartet makes clear whether a cue is essential or incidental.
# Square index2 identity is intended; preference for base2 in bank {2,3} is incidental.
raw_score=score(raw);accepted_score=score(accepted)
# Faithful read-only learner selection: all newly accepted questions easy; if easy
# weight positive, select uniformly from this available band using digest bytes8..16.
# No history, and a history excluding all earlier selections, are both evaluated.
def select_indices(n,seed):
 digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
 u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53)
 return min(int(u*n),n-1)
selected=[];with_history=[]
captured=[{'captured_inventory_question':q[':question/id'],'question':q} for q in inventory['questions'] if q.get(':question/difficulty',{}).get(':db/ident')==':question.difficulty/easy' and all(':answer-field/correct' in f for f in q[':question/answer-fields'])]
for run in runs:
 ac=captured+run['accepted']
 for trial in range(16):
  if ac:selected.append(ac[select_indices(len(ac),f'review/{run["seed"]}/{trial}')])
 pool=ac.copy()
 for trial in range(len(ac)):
  idx=select_indices(len(pool),f'review-history/{run["seed"]}/{trial}');with_history.append(pool.pop(idx))
save('selection-records.json',{'without_history':selected,'with_history':with_history})
selection_score=score(selected);history_score=score(with_history)
# Mathematical exact first-item branch probability from the observed generator code.
# direction +: x=n branch picks2 with 1/3; direction -: x>n branch picks3 among17 with1/2.
exact={'p_base2_bank_given_square':str(Fraction(1,2)*Fraction(1,3)),
       'p_base3_bank_given_square':str(Fraction(1,2)*Fraction(1,2)*Fraction(1,17)),
       'conditional_choose_base2':str(Fraction(34,37)),
       'explanation':'For the first square item, direction+ includes x<n,x=n,x>n; x=n is exactly2. Direction- excludes x=n, leaving two cases, and x>n has17 radicands including3. No-replacement effects in later items are measured in actual count5 trials.'}
# Other standard superficial strategies, including within each recognizable template.
probes=[]
for name,rs in [('raw',raw),('accepted',accepted),('runner',json.loads((E/'runner-batch.json').read_text()))]:
 for t in g.TEMPLATES:
  sub=[r for r in rs if r['generation']['template']==t]
  positions=Counter();unitfoil=Counter()
  for r in sub:
   cs,key=inspect(r);positions.update([next(i for i,c in enumerate(cs) if c[':answer/value']==key)])
   foil=next((re.fullmatch(r'\{1\}\^\{(\d+)/(\d+)\}',c[':answer/value']) for c in cs if c[':answer/value'].startswith('{1}^')),None)
   if foil:unitfoil['total']+=1;unitfoil['correct']+=key==f'{{{foil[1]}}}^{{1/{foil[2]}}}'
  if sub:
   probes.append({'stage':name,'template':t,'position_counts':dict(positions),'choose_first':positions[0],'total':len(sub),'old_base1_foil_strategy':dict(unitfoil),'position_baseline':0.2,'foil_strategy_baseline':0.25})
result={'commands':['.venv/bin/python -B shortcut_audit.py'],'seeds':{'start':461003,'stop_exclusive':461515,'batch_size':5},'captured_basis':inventory['basis'],'stage_counts':dict(stage),'raw':raw_score,'accepted':accepted_score,'learner_no_history':selection_score,'learner_progressive_history':history_score,'first_square_exact':exact,'other_probes':probes,'selection_model':'Faithful select() SHA256 uniform-within-easy rule. Includes the two usable captured easy inventory questions; incomplete unrated q-69158 excluded. Ordering treated as ordinal surrogate for unknown future DB IDs; uniform no-history trials and progressive history exclusion. Positive easy weight assumed; all-easy pool means other weights irrelevant. Zero easy weight returns no rated questions; unconfigured policy chooses smallest DB ID whose future assignment cannot be determined.','conclusion':'Evaluate statistical answer-only base preference against 50% after intended identification of square index, or20% blind five choices. Conditioning on the base pair is recognizable from choices, does not inspect the radical, and is not a mathematical necessity: both targets are supported by identical banks.'}
save('shortcut-results.json',result)
print(json.dumps({k:v for k,v in result.items() if k in ('stage_counts','first_square_exact')}));print('scores',[(k,v['correct'],v['total']) for k,v in result.items() if k in ('raw','accepted','learner_no_history','learner_progressive_history')])
