"""Strict acceptance regressions: current package is expected to fail both cases."""
import sys,importlib.util,argparse,json
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--case',choices=['source-five-components','bank-cue'],required=True);ap.add_argument('--package',type=Path,default=R.parent/'workspace');args=ap.parse_args()
sys.path.insert(0,str(args.package));s=importlib.util.spec_from_file_location('generator_under_test',args.package/'17592186184171.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def answer(r):
 f=r['question'][':question/answer-fields'][0];return int(next(c[':answer/value'] for c in f[':answer-field/choices'] if c[':answer/id']==f[':answer-field/correct'][1]))
if args.case=='source-five-components':
 # Source q-142489 / 5e7c8be1-d271-506d-bfc9-fbf1881a88d8.
 p={'matrix':[[1,0],[0,0],[1,1],[0,0],[0,0]],'indices':[1,2]}
 r=g.generate('moderate',seed=802103,parameters=p,profile='one-through5',template='null-space-inline')
 assert answer(r)==3
 assert sorted(int(c[':answer/value']) for c in r['question'][':question/answer-fields'][0][':answer-field/choices'])==[1,2,3,4,5]
else:
 # The same recognizable positive consecutive bank must not always identify its key.
 rs=[g.generate('easy',seed=1,parameters={'m':2,'n':n,'k':1},profile='offset-minus1') for n in [4,5,6]]
 predictions=[sorted(int(c[':answer/value']) for c in r['question'][':question/answer-fields'][0][':answer-field/choices'])[1] for r in rs]
 assert not all(pred==answer(r) for pred,r in zip(predictions,rs)), 'Incidental shortcut: second-smallest option answers every varied positive consecutive bank.'
print('Acceptance regression passed')
