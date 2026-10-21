"""Visible-choice policies, before/after the shared delivery filters."""
import collections,json
from pathlib import Path
import audit as a
W=Path(__file__).resolve().parent.parent;E=W/'evidence'
def value_key(r):return next(z[':answer/value'] for z in a.field(r)[':answer-field/choices'] if z[':answer/id']==a.answer_id(a.field(r)))
def bank(r):return tuple(z[':answer/value'] for z in a.field(r)[':answer-field/choices'])
def report(rs):
 out=[]
 for t in sorted({r['generation']['template'] for r in rs}):
  sub=[r for r in rs if r['generation']['template']==t]
  hits=sum(a.shortcut(r)==[a.answer_id(a.field(r))] for r in sub)
  groups=collections.defaultdict(list)
  for r in sub:groups[tuple(sorted(bank(r)))].append(r)
  complete=[g for g in groups.values() if len({value_key(r) for r in g})==5]
  assert complete,('no complete counterfactual group after filtering',t)
  policies={}
  for name,select in [('first',lambda b:b[0]),('last',lambda b:b[-1]),('shortest',lambda b:min(b,key=len)),('longest',lambda b:max(b,key=len)),('lexicographically_first',min),('lexicographically_last',max)]:
   # The matched groups use the same order. Test each policy's actual predictions.
   attempts=0;success=0
   for group in complete:
    # Controlled representatives selected by the fixed generation seed and roles;
    # duplicate random samples are excluded from the matched-group comparison.
    matched=[next(r for r in group if r['generation']['parameters']['c']==c) for c in (-2,-1,1,2,3)]
    assert len({bank(r) for r in matched})==1
    attempts+=5;success+=sum(select(bank(r))==value_key(r) for r in matched)
   assert success*5==attempts,(t,name,success,attempts)
   policies[name]={'correct':success,'attempts':attempts}
  out.append({'template':t,'records':len(sub),'old_unique_sign_double_shortcut_hits':hits,'complete_matched_banks':len(complete),'choice_only_policies':policies,'correct_coefficients':sorted({r['generation']['parameters']['c'] for r in sub}),'natural_and_controlled_correct_positions':dict(collections.Counter(bank(r).index(value_key(r)) for r in sub))})
  assert hits==0
 return out
before=json.loads((E/'delivery-input.json').read_text());after=json.loads((E/'delivery/accepted.json').read_text())
samples=json.loads((E/'samples.json').read_text());accepted_ids={r['generation']['content_fingerprint'] for r in after}
assert all(r['generation']['content_fingerprint'] in accepted_ids for r in samples)
result={'before':report(before),'after':report(after),'five_sample_records_survive':True,'stage_counts':{k:json.loads((E/'delivery/delivery.json').read_text())[k] for k in ('input_count','duplicate_count','accepted_count')},'family_wide_argument':'Within each fixed bank group every coefficient is correct once. Thus any choice-only deterministic policy (including sign, coefficient rank, length, layout, or a template lookup) has accuracy 1/5. The observed old attack selects multiple candidates and no longer resolves a key.','selection_limits':'Shared prepare_records was executed read-only. Generator has no resampling/rejection branch for valid parameters. The source has no diagrams. The difficulty-first selector is uniform within an eligible band when configured; captured inventory is available but live learner history and policy weights are not, so exact live mixtures are untested.'}
(E/'shortcut-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':True,'before':len(before),'after':len(after),'families':len(result['after']),'five_sample_records_survive':True}))
