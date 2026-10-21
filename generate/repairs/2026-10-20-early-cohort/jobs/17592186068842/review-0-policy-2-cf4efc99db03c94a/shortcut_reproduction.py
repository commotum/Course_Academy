"""Reproduce prompt-blind answer selection. Run with the job's Python executable.
All generated artifacts are kept beside this script. Does not modify package/DB.
"""
import pathlib,sys,json,importlib.util,collections
sys.dont_write_bytecode=True
R=pathlib.Path(__file__).resolve().parent;PKG=R.parent/'workspace'
spec=importlib.util.spec_from_file_location('review_target',PKG/'17592186068842.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
D=r'\frac{\text{d}y}{\text{d}x}'
def probe(r):
 q=r['question'];f=q[':question/answer-fields'][0];cs=f[':answer-field/choices'];chosen=[a for a in cs if r'\frac' not in a[':answer/value'].replace(D,'D')]
 return {'question_id':q[':question/id'],'template':r['generation']['template'],'seed':r['generation']['seed'],'parameters':r['generation']['parameters'],'candidates':[a[':answer/value'] for a in chosen],'unique':len(chosen)==1,'correct':len(chosen)==1 and chosen[0][':answer/id']==f[':answer-field/correct'][1]}
records=[m.generate_easy(seed,t) for t in ['exp_quotient','simple_quotient'] for seed in [27011,27012,27013,27014,27015,27016]]
records.append(m.generate_easy(17,'simple_quotient',parameters={'n':1}))
(R/'shortcut-records.json').write_text(json.dumps(records,indent=2,ensure_ascii=False))
results={pool:[probe(r) for r in rs if r['generation']['template'] in ('exp_quotient','simple_quotient')] for pool,rs in [('fresh',records),('batch',json.load(open(R/'batch.json'))),('accepted_batch',json.load(open(R/'delivery-batch/accepted.json'))),('accepted_control',json.load(open(R/'delivery-control/accepted.json')))]}
# Also challenge raw TeX length without using the prompt: ancillary probe from independent_checks.
(R/'fraction-shortcut-results.json').write_text(json.dumps({'strategy':'Select the unique row with no fraction bar except dy/dx; do not inspect the prompt, variables, exponents, or values.','baseline':0.2,'pools':results},indent=2,ensure_ascii=False))
# Exact single minimal case, complete prompt/key/bank and generation metadata retained.
(R/'minimal-failing-record.json').write_text(json.dumps([records[-1]],indent=2,ensure_ascii=False))
print({p:{'correct':sum(v['correct'] for v in rs),'total':len(rs)} for p,rs in results.items()})

# Strict acceptance regression: a functioning distractor bank must defeat this prompt-blind cue.
vulnerable=[r for r in results["fresh"] if r["correct"]]
if vulnerable:
 raise SystemExit("FAIL: prompt-blind fractionless-choice strategy answers "+str(len(vulnerable))+" fresh quotient records. See fraction-shortcut-results.json.")
