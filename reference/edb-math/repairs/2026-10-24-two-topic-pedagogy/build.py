"""Build reviewable immutable replacement packages; install after publication."""
import argparse,importlib.util,json,re,shutil,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3]
sys.path.insert(0,str(ROOT/'generate'))
import substitution_pedagogy as model
from read_math import scalar,integral,source_prompt

def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def main():
 p=argparse.ArgumentParser();p.add_argument('--install',action='store_true');args=p.parse_args()
 for kp in model.CASES:
  d=H/str(kp);source=json.loads((d/'source/source.json').read_text());inv=json.loads((d/'inventory/inventory.json').read_text());record=source['material']['kp'];qs=inv['questions']+[inv['canonical_example']]
  excluded=[];limitations=[]
  for q in qs:
   try:
    text=q[':question/problem'].replace('z','x').replace('y','x')
    if r'\mathrm{d}x' in text:
     body,_,lo,hi=integral(re.findall(r'\$\$\s*(.*?)\s*\$\$',text,re.S)[0])
    else:body,lo,hi=source_prompt(text)
    excluded.append(model.fp(body,lo,hi))
   except Exception as exc:limitations.append({'entity':q[':db/id'],'source':q.get(':question/math-academy-id'),'error':str(exc)})
  assert not any(not a['source']for a in limitations),limitations
  counts={b:sum(bool(q.get(':question/math-academy-id'))and q.get(':question/difficulty',{}).get(':db/ident')==':question.difficulty/'+b for q in inv['questions'])for b in('easy','moderate','hard')}
  hard='Two small perfect-square normalizations; no irrational slope or fractional numerator.'if kp in(17592186064218,17592186064219)else 'Rewrite |x| in terms of |u|; keep the scale an integer.'if kp==17592186064250 else 'Evaluate from two nonzero transformed bounds; inverse endpoint facts supplied.'if kp==17592186064220 else 'Recognize a negative inner derivative; no extra fraction or larger powers.'if kp in model.EXP[:2]else 'Recognize one logarithmic derivative, including a composite denominator.'if kp==model.EXP[2]else 'Transform bounds for a logarithmic derivative; exponential endpoint facts supplied.'
  origins={'easy':'Authored supplied-u transformation stage, following imported q-49529/q-49532 scaffolding; own KP imports anchor the integrands.','moderate':'Authored supported full calculation using own imported families with small parameters and a supplied primitive.','hard':'Authored relative band: '+hard}
  evidence={'kp':{'db_id':kp,'id':record[':knowledge-point/id'],'title':record[':knowledge-point/title']},'basis':source['basis'],'excluded_tasks':sorted(set(excluded)),'exclusion_parse_limitations':limitations,'band_origin':origins,'source_counts':counts,'sources':[q[':question/math-academy-id']for q in qs if q.get(':question/math-academy-id')],'source_eligibility':source['material']['source_eligibility'],'benchmark_kp':17592186064172,'benchmark_report':'reference/edb-math/audits/2026-10-24-difficulty-pedagogy/README.md'}
  contract={'version':model.VERSION,'families':model.CASES[kp],'band_origin':origins,'calibration':'Source-informed authored task progression, not psychometric calibration or inherited source difficulty.','support':'Easy supplies u and asks only for the transformed integral. Full calculations supply primitives. Exact inverse/exponential endpoint facts are supplied when needed.','parameter_policy':'Integer amplitudes 1..4, inverse scale integers 2..5 or their ratios, perfect-square constants at most25; exponential slopes magnitude at most2 and powers at most3. Hard adds one target condition.','sampling':'Seeded family-first sampling; no duplicates within batch; exclude existing integrands for full calculations. Easy transformations are a distinct task and may share an imported full-calculation integrand.','answer_policy':'External C for indefinite blanks; all worked solutions finish with the exact key. No mandatory decimal padding.'}
  wrapper=f'''#!/usr/bin/env python3
"""KP {kp}: scaffolded substitution."""
import json
from pathlib import Path
import sys
LOCAL=Path(__file__).with_suffix('')
if not (LOCAL/'substitution_pedagogy.py').is_file():LOCAL=Path(__file__).resolve().parent
sys.path.insert(0,str(LOCAL))
import substitution_pedagogy as model
KP={kp}
EVIDENCE=json.loads((LOCAL/'source-evidence.json').read_text())
def generate(level,seed=0,template=None,**kwargs):return model.generate(KP,level,seed,template,evidence=EVIDENCE,**kwargs)
def batch(level,count=8,seed=0,template=None):return model.batch(KP,level,count,seed,evidence=EVIDENCE,template=template)
if __name__=='__main__':model.cli(KP,LOCAL)
'''
  targets=[d/'package']+([ROOT/f'generate/scratch/{kp}']if args.install else [])
  for target in targets:
   target.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/'generate/substitution_pedagogy.py',target/'substitution_pedagogy.py');save(target/'source-evidence.json',evidence);save(target/'band-contract.json',contract)
   (target/'generator.py'if target.name=='package'else ROOT/f'generate/scratch/{kp}.py').write_text(wrapper)
  if args.install:
   save(ROOT/f'generate/scratch/{kp}/capabilities.json',{'supported_levels':['easy','moderate','hard'],'implementation_version':model.VERSION,'band_contract':'band-contract.json','imported_source_counts':counts,'band_origin':origins,'maximum_records_per_call':100})
   (ROOT/f'generate/scratch/{kp}/README.md').write_text(f'# Scaffolded substitution — KP {kp}\n\nVersion {model.VERSION}; source/band contract is in `band-contract.json`.\n\nThe immutable live package and verification are recorded in `reference/edb-math/repairs/2026-10-24-two-topic-pedagogy/`. Older extraction/replay/validation files in this folder are historical evidence, not the current sampler. Imports and learner history are preserved.\n')
  print(kp,counts,'exclusions',len(excluded),'parse limitations',len(limitations),flush=True)
if __name__=='__main__':main()
