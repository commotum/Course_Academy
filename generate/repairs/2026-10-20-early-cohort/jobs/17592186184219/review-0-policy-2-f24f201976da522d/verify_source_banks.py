import sys,json
sys.dont_write_bytecode=True
from review_generator import E,JOB,W,loadg,save,read
G=loadg(W/'17592186184219.py');src=json.loads((JOB/'source/source.json').read_text());rows=[]
for q in src['material']['kp'][':knowledge-point/questions']:
 mid=q[':question/math-academy-id']
 if mid in G.PROFILES:continue
 d=read(q);p={k:d[k] for k in ('m','n','k','target')};trials=[]
 for profile in G.PROFILES:
  if G.ORIGINAL[profile]['target']!=p['target']:continue
  try:r=G.generate('easy',profile=profile,template=p['target'],parameters=p)
  except ValueError as exc:trials.append({'profile':profile,'result':'rejected','error':str(exc)})
  else:trials.append({'profile':profile,'result':'emitted','values':read(r)['values'],'full_bank_matches':sorted(read(r)['values'])==sorted(d['values'])})
 assert not any(t.get('full_bank_matches') for t in trials)
 rows.append({'source_id':q[':question/id'],'source_ma_id':mid,'parameters':p,'source_values':d['values'],'trials':trials,'conclusion':'No currently supported bank profile can replay the complete source bank at its original parameters.'})
save('missing-bank-exhaustion.json',rows)
print('Verified absent bank recipes for',len(rows),'current source cases')
