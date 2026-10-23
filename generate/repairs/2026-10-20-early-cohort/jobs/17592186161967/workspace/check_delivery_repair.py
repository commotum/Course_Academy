"""Check repaired bank evidence after the actual delivery filter."""
import collections,json
from check_repair import OUT,save,inspect,groups_report
raw=json.loads((OUT/'fixed-bank-records.json').read_text())
accepted=json.loads((OUT/'delivery/accepted.json').read_text())
def signature(r):
 q=r['question']
 return (q[':question/problem'],tuple(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']))
lookup={signature(r):r for r in accepted}
matched=[lookup[signature(r)] for r in raw if signature(r) in lookup]
assert len(matched)==len(raw),(len(matched),len(raw))
groups=collections.defaultdict(list)
for r in matched:
 p=r['generation']['parameters'];bank,ci=inspect(r)
 # Group by unchanged entries, profile and exact ordered choices, not expected keys.
 A=p['A'];tag=(r['generation']['bank_profile'],A[1][1],A[2][1],tuple(bank))
 groups[tag].append((bank,ci))
assert len(groups)==52
for tag,rows in groups.items():
 assert len(rows)==4 and len({bank[ci] for bank,ci in rows})==4
summary=groups_report(matched)
for tag,s in summary.items():
 for coord in ('first','second'):
  if s[coord+'_mode_attempts']:
   assert s[coord+'_mode_success']*2==s[coord+'_mode_attempts'],(tag,s)
# Report source replay deduplication separately; these are explicit validation artifacts.
replays=json.loads((OUT/'source-replays.json').read_text())
source_survivors=sum(signature(r) in lookup for r in replays)
# Controlled witnesses already exercise every sign, extra-role and profile
# after actual deduplication; additionally report the natural sample honestly.
natural=json.loads((OUT/'fresh-records.json').read_text())
natural_survivors=[lookup[signature(r)] for r in natural if signature(r) in lookup]
assert len(natural_survivors)==len(natural)
report={'status':'pass','controlled_input':len(raw),'controlled_survivors':len(matched),'identical_bank_groups_surviving':len(groups),'controlled_groups':summary,'fresh_survivors':len(natural_survivors),'fresh_groups':groups_report(natural_survivors),'source_replays_surviving':source_survivors,'source_replay_limit':'Normalized source replay text survives delivery. These explicit-parameter fidelity artifacts are not produced by the CLI sampler.','selection_limits':'Shared delivery uses captured basis 5580. question_selection.rs selects among already-fresh usable questions by difficulty then seeded uniform index; it does not inspect bank features. Live learner history and database publication are outside this author check.'}
save('post-delivery-report.json',report)
print(json.dumps({k:v for k,v in report.items() if k not in ('controlled_groups','fresh_groups')}))
