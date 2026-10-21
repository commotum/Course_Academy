"""History f5bbcb9650d7b114e116: probe actual CLI and shared delivery.

Also independently construct five mathematical witnesses for each tested bank.
Never changes runtime package files, contacts services or accesses a database.
"""
import collections, copy, importlib.util, itertools, json, math, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode=True
from regressions import W, check_record, matrix, coords, ref_after, generator as g
from order_probe import probe
E=W/'evidence/repair2/regression'
REPO=Path('/home/jake/Developer/Course_Academy')

def save(n,x): (E/n).write_text(json.dumps(x,indent=2)+'\n')
def bank(r):
 f=r['question'][':question/answer-fields'][0]
 return [coords(a[':answer/value']) for a in f[':answer-field/choices']]
def ci(r):
 f=r['question'][':question/answer-fields'][0]
 return next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])
def tail(n,h,p=.2):return sum(math.comb(n,k)*p**k*(1-p)**(n-k) for k in range(h,n+1))
def cues(rs):
 groups=collections.defaultdict(list)
 for r in rs:
  m=matrix(r['question'][':question/problem']);b=bank(r)
  groups['all'].append(r)
  groups['size='+str(len(b[0]))].append(r)
  groups['zero_row='+str(any(not any(row) for row in m))].append(r)
  groups['size='+str(len(b[0]))+',zero_row='+str(any(not any(row) for row in m))].append(r)
 out={}
 for label,rr in groups.items():
  hits=collections.Counter();trial=collections.Counter();sole_noop=0
  for r in rr:
   b=bank(r);key=ci(r);m=matrix(r['question'][':question/problem']);ordered=sorted(range(5),key=lambda i:b[i])
   strategies={**{'rank'+str(k):ordered[k] for k in range(5)},**{'position'+str(k):k for k in range(5)}}
   flat=[[(4*i+j) for i,j in bb] for bb in b];freq=collections.Counter(c for bb in flat for c in bb)
   for name,scores in [('coordinate_frequency',[sum(freq[c] for c in bb) for bb in flat]),('coordinate_sum',[sum(bb) for bb in flat]),('first_row_count',[sum(c<4 for c in bb) for bb in flat]),('coordinate_span',[max(bb)-min(bb) for bb in flat])]:
    for side,fn in [('min',min),('max',max)]:
     extreme=fn(scores);tied=[i for i,s in enumerate(scores) if s==extreme]
     # Average over ties avoids accidental serialized-position effects.
     name2=name+'_'+side;hits[name2]+= (1/len(tied) if key in tied else 0);trial[name2]+=1
   # Encode sorted coordinate sets independently of their rendered ordering.
   # The old centered-neighborhood rule could also leave density/gap cues.
   numbers=[sum((c+1)*17**(len(bb)-1-k) for k,c in enumerate(bb)) for bb in flat]
   distances=[sum(abs(v-other) for other in numbers) for v in numbers]
   for side,fn in [('min',min),('max',max)]:
    tied=[i for i,v in enumerate(distances) if v==fn(distances)]
    name='coordinate_gap_'+side;hits[name]+=(1/len(tied) if key in tied else 0);trial[name]+=1
   for name,pred in strategies.items():hits[name]+=pred==key;trial[name]+=1
   z=[sum(m[i][j]==0 for i,j in bb) for bb in b]
   sole_noop += z[key]==min(z) and z.count(min(z))==1
  out[label]={'n':len(rr),'hits':dict(hits),'baseline':.2,'sole_fewest_noops_keys':sole_noop,
    'rank_position_binomial_tails':{name:tail(trial[name],int(h)) for name,h in hits.items() if name.startswith(('rank','position'))}}
  assert sole_noop==0, (label,'no-op counting alone identifies key')
  # A conservative family-wise alarm across 6 groups x 10 rank/position probes.
  assert all(p>=.01/60 for p in out[label]['rank_position_binomial_tails'].values()),out[label]
 return out

def witness_ref(mask,op):
 # Independent leading-column calculation over the visible operation; no
 # runtime predicates, support tables or generation parameters are used.
 cleared=mask
 for i,j in op:cleared &= ~(1<<(4*i+j))
 leading=[];zero=False
 for i in range(4):
  row=[j for j in range(4) if cleared & 1<<(4*i+j)]
  if not row:zero=True
  else:
   if zero:return False
   leading.append(row[0])
 return all(x<y for x,y in zip(leading,leading[1:]))

def main():
 E.mkdir(parents=True,exist_ok=True)
 raw=json.loads(subprocess.check_output([sys.executable,str(W/'generator.py'),'--difficulty','moderate','--seed','932611','--count','64','--format','json'],text=True));save('cli-records.json',raw)
 # Reproduce actual CLI semantic rejection/resampling, using its current
 # fingerprint only for its declared deduplication contract, not correctness.
 last=raw[-1]['generation']['seed'];seen=set();kept=[];skipped=[]
 for seed in range(932611,last+1):
  r=g.generate('moderate',seed);check_record(r);fp=r['generation']['mathematical_fingerprint']
  if fp in seen:skipped.append(seed)
  else:seen.add(fp);kept.append(r)
 assert kept==raw
 minimal=g.generate('moderate',431440325);check_record(minimal);save('reported-seed-current.json',[minimal])
 # Four recognizable groups, each with all five supported successful roles.
 examples={}
 for r in raw:
  m=matrix(r['question'][':question/problem']);b=bank(r);group=(len(b[0]),any(not any(row) for row in m))
  examples.setdefault(group,r)
 assert len(examples)==4
 controls=[];witness_reports=[]
 for group,r in examples.items():
  b=bank(r);found={}
  for mask in range(65536):
   if (mask>>12==0)!=group[1]:continue
   if sum(bool((mask>>(4*i))&15) for i in range(4))<3:continue
   good=[k for k,op in enumerate(b) if witness_ref(mask,op)]
   if len(good)!=1 or good[0] in found:continue
   key=good[0];after=mask
   for i,j in b[key]:after &= ~(1<<(4*i+j))
   if sum(bool((after>>(4*i))&15) for i in range(4))<2:continue
   z=[sum(not mask & 1<<(4*i+j) for i,j in op) for op in b]
   if sum(v<=z[key] for v in z)<2:continue
   m=[[int(bool(mask & 1<<(4*i+j))) for j in range(4)] for i in range(4)]
   rr=g.generate('moderate',8000+len(controls),parameters={'matrix':m,'bank':b});check_record(rr)
   assert ci(rr)==key and bank(rr)==b
   found[key]=rr;controls.append(rr)
   if len(found)==5:break
  assert len(found)==5,(group,list(found))
  witness_reports.append({'group':list(group),'bank':b,'keys_witnessed':sorted(found),'visible_question_ids':[found[k]['question'][':question/id'] for k in range(5)]})
 save('counterfactual-records.json',controls);save('bank-witnesses.json',witness_reports)
 report={'cli_resampling':{'candidates':last-932611+1,'survivors':len(raw),'skipped_fingerprint_seeds':skipped},'before_delivery':probe(raw),'cue_before':cues(raw),'fixed_bank_controls':witness_reports}
 assert report['before_delivery']['all']['median_binomial_tail']>=.01
 for label,rs in [('cli',raw),('controls',controls)]:
  inp=E/(label+'-input.json');inp.write_text(json.dumps(rs,indent=2)+'\n')
  cmd=[sys.executable,str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(inp),'--source',str(W.parent/'source/source.json'),'--inventory',str(W.parent/'source/inventory.json'),'--difficulty','moderate','--output',str(E/('delivery-'+label)),'--math-root','/media/jake/SSD/EDB/math']
  p=subprocess.run(cmd,capture_output=True,text=True);(E/(label+'-delivery-log.txt')).write_text(p.stdout+p.stderr);assert p.returncode==0,p.stderr
  accepted=json.loads((E/('delivery-'+label)/'accepted.json').read_text())
  for r in accepted:check_record(r)
  assert len(accepted)==len(rs),(label,len(rs),len(accepted))
  if label=='cli':
   report['after_delivery']=probe(accepted);report['cue_after']=cues(accepted)
   assert report['after_delivery']==report['before_delivery']
   assert report['cue_before']==report['cue_after']
  else:
   assert collections.Counter(ci(r) for r in accepted)=={k:4 for k in range(5)}
 report['median_regression_passed']=True;save('results.json',report)
 print(json.dumps({'cli':report['cli_resampling'],'median':report['after_delivery']['all'],'fixed_banks':4,'all_five_keys_per_bank':True,'delivery_preserved_cues':True}))
if __name__=='__main__':main()
