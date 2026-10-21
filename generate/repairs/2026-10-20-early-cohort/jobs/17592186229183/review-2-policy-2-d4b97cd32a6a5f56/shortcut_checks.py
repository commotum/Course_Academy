#!/usr/bin/env python3
"""Strict independent acceptance regression for the fixed-radius bank bypass.
Run: <job python> shortcut_checks.py [--package PATH]
Exit 1 means the demonstrated shortcut persists. Writes only this evidence root.
"""
import sys
sys.dont_write_bytecode=True
import json,re,argparse,importlib.util
from fractions import Fraction
from pathlib import Path
R=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--package',type=Path,default=R.parent/'workspace');a=ap.parse_args()
spec=importlib.util.spec_from_file_location('shortcut_candidate',a.package/'17592186229183.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(n,x):(R/n).write_text(json.dumps(x,indent=2,default=str)+'\n')
def probe(r):
 f=r['question'][':question/answer-fields'][0];choices=f[':answer-field/choices'];key=f.get(':answer-field/correct');key=key.get(':answer/id') if isinstance(key,dict) else key[1] if key else None
 vals=[Fraction(re.search(r'\d+(?:\.\d+)?',x[':answer/value'])[0]) for x in choices]
 eligible=[i for i,v in enumerate(vals) if all(abs(v-u)<=2 for u in vals)]
 return {'question_id':r['question'][':question/id'],'template':r['generation']['template'],'seed':r['generation']['seed'],'sorted_choices':[f'{float(v):.1f}' for v in sorted(vals)],'eligible_values':[f'{float(vals[i]):.1f}' for i in eligible],'singleton':len(eligible)==1,'success':len(eligible)==1 and choices[eligible[0]][':answer/id']==key,'selected_id':choices[eligible[0]][':answer/id'] if len(eligible)==1 else None}
p={'H':'20','v':'10','q':'1','c':'0.4','rin':'6','rout':'4'}
minimal=g.generate('easy',seed=41072,template='q-336506',parameters=p);m=probe(minimal);save('minimal-records.json',[minimal])
# Independently solve from physical mass balance: Q(to)=cH+(q-cv)*(v/H)^2=7.25 -> 7.3 lb.
assert Fraction(2,5)*20+(1-Fraction(2,5)*10)*Fraction(10,20)**2==Fraction(29,4)
sets={'minimal':[minimal],'sample before':json.load(open(R/'sample-records.json')),'sample after':json.load(open(R/'delivery-sample/accepted.json')),'batch before':json.load(open(R/'batch-records.json')),'batch after':json.load(open(R/'delivery-batch/accepted.json'))}
results={k:{'total':len(v),'singleton_count':sum(probe(r)['singleton'] for r in v),'correct_singletons':sum(probe(r)['success'] for r in v),'rows':[probe(r) for r in v]} for k,v in sets.items()}
failed=m['singleton'] and m['success']
save('shortcut-results.json',{'command':sys.argv,'parameters':p,'minimal':m,'results':results,'historical_family_wide_proof_not_current':'method_bank samples every nonzero distractor offset from 1..width tenths, where width<=20. Thus the key always lies within 2 lb of every other choice. Whenever only one displayed choice has this property, the key is determined by that geometry. Random rank, offset magnitudes, option shuffle and delivery normalization do not change this implication.','source_contrast':'Original q-336451 correct 207.6 lb has distractor 201.0 lb, 6.6 lb away; the uniform 2 lb radius is authored, incidental and unnecessary for mixture modeling.','passed':not failed,'failure':'Singleton fixed-radius center answers an instance without reading its physical quantities.' if failed else None,'acceptance_condition':'The fixed 2 lb radius must not reliably single out the correct choice. Retain all source profiles and eligible numerical ranks; fix the full bank construction rather than suppress the demonstrated parameters.'})
cases=[]
for label,rs in [('minimal',[minimal]),('actual post-delivery batch',sets['batch after'])]:
 for r in rs:
  z=probe(r)
  if z['singleton']:
   cases.append({'label':label+' / solve using only option distances','record':r,'checks':[{'field_index':0,'submitted_answer_id':z['selected_id'],'expected':'accepted' if z['success'] else 'rejected','purpose':'Select sole option whose maximum distance to all displayed values is at most 2 lb; no prompt quantities used.'}]})
save('shortcut-grader-input.json',cases)
print(json.dumps({'passed':not failed,'minimal':m,'sample_singleton_success':results['sample after']['correct_singletons'],'batch_singleton_success':results['batch after']['correct_singletons']}));sys.exit(1 if failed else 0)
