"""Strict acceptance regressions. Current generator is expected to fail both cases."""
import argparse,json
import review as v
p=argparse.ArgumentParser();p.add_argument('--case',choices=['shortcut','sources'],default='shortcut');args=p.parse_args()
m=v.load_generator(v.JOB/'workspace/17592186161966.py')
if args.case=='shortcut':
 r=m.generate(seed=1118318699,bank_profile='q-130619');v.inspect(r)
 print(json.dumps({'seed':1118318699,'profile':'q-130619','choice_coefficients':v.coefficients(r),'predicted_index':v.shortcut(r),'correct_index':v.correct_index(r)}))
 # This is an acceptance requirement on the family, not on arithmetic correctness.
 rs=[m.generate(seed=731100+i,bank_profile='q-130619') for i in range(12)]
 assert not all(v.shortcut(x)==v.correct_index(x) for x in rs), 'FAIL: choice-only singleton-swap cue predicts 12/12 independently varied answers'
else:
 cases=json.load(open(v.ROOT/'source-replay.json'))
 for row in cases:
  if row.get('profile') in ['q-130617','q-130630']:
   print('Replaying rated source',row['source_id'],flush=True)
   rec=m.generate(bank_profile=row['profile'],parameters=row['parameters']);v.inspect(rec)
