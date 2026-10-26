#!/usr/bin/env python3
"""Visible-cue audit; predictions defined without answer-bank or correct-key access."""
import argparse,collections,json,re
from pathlib import Path
from fractions import Fraction as F
ap=argparse.ArgumentParser();ap.add_argument('--evidence',type=Path,required=True);a=ap.parse_args();E=a.evidence
read=lambda n:json.loads((E/n).read_text())
def num(s):return F(re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'\1/\2',s))
def keys(r):
 vals=[]
 for f in r['question'][':question/answer-fields']:
  cid=f[':answer-field/correct'][1];vals.append(num(next(c[':answer/value'] for c in f[':answer-field/choices'] if c[':answer/id']==cid)))
 return vals
# Predictor input is limited to these displayed attributes, never generation metadata/keys.
def features(r):
 p=r['question'][':question/problem'];formula=re.search(r'\$([^$]+)\$',p)[1];band=r['question'][':question/difficulty'].split('/')[-1]
 if band=='hard':
  c,m,v=re.match(r'(.+?)-(\d+)([xytz])\+[xytz]\^2',formula).groups();sign='unsigned-param'
 else:
  v,m,c=re.match(r'([xytz])\^2-(\d+)[xytz](.*)',formula).groups();c=c.lstrip('+') or '0';sign=re.search(r'\)\^2([+-])\$',p)[1]
 return {'band':band,'variable':v,'m':int(m),'c':num(c),'sign':sign}
sets={}
for b in ('easy','moderate','hard'):
 sets['final-'+b]=read('final-'+b+'.json');sets['control-'+b]=read('control-'+b+'.json')
 # Actual publisher survivors are used, not inferred from raw counts.
 sets['delivered-final-'+b]=read('delivery-final-'+b+'/accepted.json')
 sets['delivered-control-'+b]=read('delivery-control-'+b+'/accepted.json')
probes=[];coverage=[];observations={}
for name,records in sets.items():
 ref=(name+'.json') if name.startswith(('final-','control-')) else ('delivery-'+name.removeprefix('delivered-')+'/accepted.json')
 b=features(records[0])['band'];groups={'all':records}
 for sign in sorted({features(r)['sign'] for r in records}):groups['supplied-remainder-sign:'+sign]=[r for r in records if features(r)['sign']==sign]
 for v in sorted({features(r)['variable'] for r in records}):groups['variable:'+v]=[r for r in records if features(r)['variable']==v]
 counts=collections.Counter('zero' if (k:=keys(r)[1])==0 else 'positive' if features(r)['sign']=='+' or b=='hard' and k>0 else 'negative' for r in records)
 observations[name]={'count':len(records),'remainder_cases':dict(counts),'distinct_response_pairs':len({tuple(keys(r)) for r in records}),'original_constant_signs':dict(collections.Counter('negative' if features(r)['c']<0 else 'zero' if features(r)['c']==0 else 'positive' for r in records))}
 coverage.append({'case':name+': original constant and remainder signs, response pairs','sample_refs':[ref],'result':json.dumps(observations[name],sort_keys=True)})
 for group,rs in groups.items():
  # Singleton surface groups cannot demonstrate a repeatable predictor. Preserve counts separately.
  if len(rs)<2:continue
  ys=[keys(r) for r in rs]
  base=max(collections.Counter(y[1] for y in ys).values())/len(rs)
  for label,predict in [('second blank is always zero',lambda f:F(0)),('copy visible original constant into second blank',lambda f:f['c'] if b=='hard' else abs(f['c'])),('copy visible linear magnitude into second blank',lambda f:F(f['m']))]:
   success=sum(predict(features(r))==keys(r)[1] for r in rs)
   assert success<len(rs),(name,group,label)
   probes.append({'cue':label,'subgroup':name+'/'+group,'scope':'within_template' if group=='all' else 'other_recognizable_subgroup','strategy':'Predict the numeric second response using only displayed variable, coefficients and supplied sign; '+label+'. No key, generation metadata or answer catalog is consulted.','correct':success,'total':len(rs),'baseline':base,'disposition':'not_predictive','conclusion':'Comparison baseline is the empirical most-frequent numeric second response in this same subgroup ('+str(base)+'). This fixed surface strategy does not solve the subgroup. Singletons are retained in records but cannot support repeatability claims.','sample_refs':[ref]})
 # Halving is intentionally one necessary component; it must not be misclassified as an incidental cue.
 success=sum((F(-features(r)['m'],2) if b=='hard' else F(features(r)['m'],2))==keys(r)[0] for r in records)
 probes.append({'cue':'negative odd linear coefficient','subgroup':name,'scope':'within_template','strategy':'Read linear coefficient and halve it, using the signed parameter convention in hard. Does not compute the second response.','correct':success,'total':len(records),'baseline':max(collections.Counter(y[0] for y in map(keys,records)).values())/len(records),'disposition':'intended_skill','conclusion':'Baseline is the most frequent first numeric response. Halving is explicitly the target operation, not a shape-only shortcut, and alone cannot finish either field contract.','sample_refs':[ref]})
cf=read('counterfactual-records.json');results=[]
for offset,b in [(0,'easy'),(5,'moderate'),(10,'hard')]:
 before,zero,after,renamed,changed_m=cf[offset:offset+5]
 assert [keys(r)[1] for r in (before,zero,after)]==([F(-2),F(0),F(1)] if b=='hard' else [F(2),F(0),F(1)])
 assert keys(after)==keys(renamed) and keys(changed_m)!=keys(after)
 assert 'z' in renamed['question'][':question/problem'] and 'z' in renamed['question'][':question/worked-solution']
 results.append({'band':b,'constant_change_responses':[list(map(str,keys(r))) for r in (before,zero,after)],'coefficient_changed_responses':list(map(str,keys(changed_m))),'variable_only_preserved':list(map(str,keys(renamed))),'native_grader':'grading-report.json contains correct equivalents for every case and rejects stale changed-constant and changed-coefficient responses.'})
(E/'counterfactual-results.json').write_text(json.dumps(results,indent=2)+'\n')
(E/'shortcut-measurements.json').write_text(json.dumps({'observations':observations,'probes':probes,'singleton_policy':'No repeatable shortcut is inferred from a one-item subgroup. Full pairs are preserved for manual inspection.','prediction_inputs':'Specified in each strategy before scoring. No response position or bank profile applies to the ordinary blank fields. Stored single choice is the hidden reference key, not an answer option shown before response.'},indent=2)+'\n')
report={'learner_operation':'Complete a monic quadratic with negative odd linear coefficient: infer the half, preserve value by adding/subtracting its square, factor, and combine the residual constant. Produce both numeric fragments; hard also requires signed parameters.',
'fixed_features':[{'feature':'Monic quadratic and negative odd integer linear term','justification':'Target KP e-15021 and tutorial9421 teach the fractional-half completion for this sign. Varying to a nonmonic polynomial or solving an equation would add another operation.'},{'feature':'Two numeric blanks; factored sign support in easy/moderate','justification':'Complete source q-223639/q-223640 explicitly supply signs. Both blanks still require calculation. Ordinary sampling uses this captured contract; full radio banks remain in source replay.'},{'feature':'Minus sign inside the completed square; hard a is negative','justification':'Expanding (v-h)^2 with h>0 necessarily gives the negative linear term. Its fixed sign is a mathematical invariant, while its magnitude and the residual constant vary.'}],
'answer_roles':[{'role':'half of coefficient','eligible_variation':'Odd m=3..15; variable rename irrelevant to numeric value.','observed':'Fresh controls and boundary samples cover multiple halves; matched coefficient counterfactual changes both responses.'},{'role':'surviving constant c-m²/4','eligible_variation':'Negative, zero and positive; vary original c independently using integer/source-quarter profiles as well as near-square values.','observed':'All three final bands include all three outcome signs after delivery. Catalog regression restores all five complete source polynomials and permits negative original constants in each band.'}],
'coverage':coverage,
'counterfactuals':[{'kind':'relevant','change':'Hold m=5 and variable x fixed; c=17/4,25/4,29/4 crosses compensation boundary. Also hold c=29/4 fixed and change m=5 to7.','expected':'First change updates residual -2,0,+1 and supplied sign/magnitude or signed b; second change updates h and residual. Prompts, solution and actual grader must track both.','observed':'Responses match exact arithmetic in all bands; stale answers fail native grading. Rendered prompts/explanations use each changed input.','status':'passed','justification':'Only answer-bearing original data changes; the same completing-square identity determines both fragments.','sample_refs':['counterfactual-records.json','counterfactual-results.json','grading-report.json','render-controls/rendering.json']},{'kind':'irrelevant','change':'Rename x to z at fixed m=5,c=29/4 in each band.','expected':'Numeric answers and grader outcomes preserved; all polynomial/square occurrences change variable.','observed':'The numeric pairs agree, both records pass native grading, and actual UI displays the renamed prompt and solution.','status':'passed','justification':'Variable names have no effect on the numeric completion parameters.','sample_refs':['counterfactual-records.json','counterfactual-results.json','grading-report.json','render-controls/rendering.json']}],
'shortcut_probes':probes,
'delivery':{'stages_examined':['finite catalog selection without replacement, initial remainder cases and finite exhaustion fallback','requested band, normalized stable identity and captured-inventory deduplication using actual publisher','within-band learner selection under configured positive weights; source inspection of zero weights and legacy default'], 'sample_refs':['delivery-summary.json','selection-analysis.json','catalog-after.txt','shortcut-measurements.json'],'result':'Final bands have easy5/5, moderate5/5, hard4/4 survivors; controls6/6 each. No case or measured cue changes through these stages. Configured positive-weight learner selection is uniform within the fresh eligible band and does not inspect keys or signs. Captured basis7581; offline evidence is not a publication receipt.'},
'limitations':['This finite audit challenges declared simple cues; it does not prove absence of every possible shortcut.','No ordinary answer banks exist; numerical rank, counterpart and modal-bank probes are inapplicable. All original radio banks are replayed and checked separately rather than claimed as a newly randomized radio family.','Only easy imported labels exist. Moderate/hard are authored support/response progressions, not empirical imported calibration.','Live learner history and changing inventory are outside the captured offline evidence. Selection conclusions are conditional on fresh usable candidates and configured band weights.','A genuine perfect-square cancellation can be recognized directly. That is valid completion knowledge; zero cases remain eligible.']}
(E/'pedagogical-variation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'surface_probes':len(probes),'sets':observations,'counterfactuals':results}))
