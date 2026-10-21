#!/usr/bin/env python3
"""Compare decision cases and simple within-template cues across real delivery stages."""
import collections, json, pathlib, sys
sys.dont_write_bytecode=True
from validate_repair import inspect,semantic,ROOT,OUT

def audit(records):
 groups=collections.defaultdict(list)
 for r in records:
  d=inspect(r,solution=False)
  groups[('plain-dy-fraction' if r['generation']['template']=='parity_numbered' else 'text-dy-fraction',d['powers'])].append(d)
 report={}
 for (template,powers),ds in sorted(groups.items()):
  masks={d['mask'] for d in ds}
  # The controlled cohort holds the actual equation and quadrant order fixed.
  # Each supported presentation/parity family must change the true subset.
  assert len(masks)>1,(template,powers,masks)
  cues={}
  for label,key in [('coefficient_sign',lambda d:d['coefficient_sign']),('statement_quadrants',lambda d:tuple(q for q,_ in d['statements']))]:
   cue_groups=collections.defaultdict(set)
   for d in ds:cue_groups[str(key(d))].add(d['mask'])
   tested={k:sorted(v) for k,v in cue_groups.items() if len(v)>1}
   assert tested,(template,powers,label)
   cues[label]={'observed_responses':tested,'singletons_in_sparse_seeded_cases':sum(len(v)==1 for v in cue_groups.values()),'maximum_fixed_response_success_on_controlled_eight_subsets':'1/8'}
  # Unique masks, rather than repeats/seeds/UUIDs, measure eligible response variety.
  label_truths=collections.defaultdict(set)
  for d in ds:
   for label,truth in zip(d['statements'],d['truths']):label_truths[str(label)].add(truth)
  repeated_labels={label:sorted(values) for label,values in label_truths.items() if len(values)>1}
  assert repeated_labels,(template,powers,'no tested label reversals')
  positional={str(i+1):sorted({bool(m&(1<<i)) for m in masks}) for i in range(3)}
  assert all(v==[False,True] for v in positional.values())
  assert masks==set(range(8)),(template,powers,masks)
  counts=sorted({m.bit_count() for m in masks});assert counts==[0,1,2,3]
  report[template+':'+str(powers)]={'records':len(ds),'truth_subsets':sorted(masks),'correct_ordinary_counts':counts,'position_can_be_true_or_false':positional,'cue_probes':cues,'exact_quadrant_claim_labels_can_be_true_or_false':repeated_labels,'labels_with_one_truth_only_in_sparse_seeded_extra_cases':sum(len(v)==1 for v in label_truths.values()),'fixed_subset_strategy_best_success_over_distinct_masks':'1/8','fixed_count_strategy_best_success_over_distinct_masks':'3/8','none_always_present':'Newly generated items always include None; its truth varies (true only on mask 0).'}
 return {'records':len(records),'semantic_instances':len({(d['coefficient_sign'],d['powers'],tuple(sorted(d['statements']))) for d in (inspect(r,solution=False) for r in records)}),'groups':report}

def main():
 result={'before':{},'after':{},'grouping':'Groups use the learner-visible fraction notation and exponent pair. Open/closed/thin templates differ only in hidden worked-solution prose, so they cannot be prompt cues. Their duplicate response structures collapse at delivery. Implementation-template coverage is separately tested before filtering.','generator_rejection':'All eight truth subsets allowed with source-backed explicit None. No truth-mask rejection; legacy profile restrictions apply only to requested historical radio-bank replay. Invalid parameter boundary checks are retained in validation.json.','selection_limit':'The shared helper tests captured-inventory and within-batch deduplication. Learner history/weights and database identity collisions are not simulated. question_selection.rs selects by configured difficulty, then within band; no truth-mask-specific rule was observed.','semantic_domain':'64 easy, 64 moderate, 192 hard possible tasks from 2 coefficient signs, 4 omitted quadrants, 8 claim assignments, and 1/1/3 exponent pairs. This audit samples semantic instances and is not an exhaustive-domain run.'}
 for level in ['easy','moderate','hard']:
  raw=json.loads((OUT/('records-'+level+'.json')).read_text());accepted=json.loads((OUT/('delivery-'+level)/'accepted.json').read_text())
  implementation=collections.defaultdict(set)
  for r in raw:
   d=inspect(r,solution=False);implementation[r['generation']['template']+str(d['powers'])].add(d['mask'])
  assert all(v==set(range(8)) for v in implementation.values())
  result['before'][level]=audit(raw);result['before'][level]['implementation_template_subsets']={k:sorted(v) for k,v in implementation.items()};result['after'][level]=audit(accepted)
  result['after'][level]['delivery_stage_counts']=json.loads((OUT/('delivery-'+level)/'delivery.json').read_text())
  removed=set(result['before'][level]['groups'])-set(result['after'][level]['groups'])
  result['after'][level]['deduplicated_presentations']=sorted(removed)
  # Duplicate wording/layout variants are not meaningful lost decision cases.
  assert {x for group in result['before'][level]['groups'].values() for x in group['truth_subsets']}=={x for group in result['after'][level]['groups'].values() for x in group['truth_subsets']}
 (OUT/'pedagogical-variation.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({level:{'before':result['before'][level]['records'],'after':result['after'][level]['records'],'semantic_before':result['before'][level]['semantic_instances'],'semantic_after':result['after'][level]['semantic_instances'],'all_eight_subsets_per_surviving_group':True} for level in result['before']}))
if __name__=='__main__':main()
