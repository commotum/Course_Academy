import sys,json
from pathlib import Path
from collections import defaultdict,Counter
sys.dont_write_bytecode=True
import regressions as t
v=t.v

def summarize(records):
 groups=defaultdict(list)
 for r in records:
  v.inspect(r)
  groups[(r['generation']['bank_profile'],r['generation']['seed'])].append(r)
 controlled=[]
 for (profile,seed),rs in groups.items():
  if 730000<=seed<730000+len(t.m.PROFILES):
   assert len(rs)==5
   banks=[tuple(a[':answer/value'] for a in v.field(r)[':answer-field/choices']) for r in rs]
   assert len(set(banks))==1 and {v.correct_index(r) for r in rs}==set(range(5))
   controlled.append(dict(profile=profile,seed=seed,positions=[v.correct_index(r) for r in rs],choice_only_ceiling='1/5'))
 assert len(controlled)==12
 probes=[]
 for profile in t.m.PROFILES:
  rs=[r for r in records if r['generation']['bank_profile']==profile]
  applicable=[r for r in rs if v.shortcut(r)!=None]
  probes.append(dict(profile=profile,records=len(rs),correct_positions=dict(Counter(v.correct_index(r) for r in rs)),singleton_shortcut_attempts=len(applicable),singleton_shortcut_correct=sum(v.shortcut(r)==v.correct_index(r) for r in applicable)))
 return dict(count=len(records),controlled=controlled,by_profile=probes)

if __name__=='__main__':
 before=json.load(open(t.OUT/'delivery-input.json'));after=json.load(open(t.OUT/'delivery/accepted.json'))
 report=dict(before=summarize(before),after=summarize(after),decision='All 12 identical-bank five-answer groups survive. Whole-bank rejection happens before answer-role selection; incidental row resampling retains bank and key.',selection=dict(source='engine/rust/question_selection.rs:105-198',assumptions='Fresh usable delivered questions; moderate policy weight positive; no learner history exclusions.',result='Within the moderate band selection is uniform over eligible entity IDs. Every surviving five-member bank group has each response correct once. Band weights cannot prefer a bank member; entity order only permutes uniform candidates.',limits=['Future entity IDs, actual learner history and current policy are not supplied.','History may remove individual members. A zero moderate weight selects none; an unconfigured policy chooses the first entity, so no live distribution guarantee is claimed.','No database connection or selection mutation was performed.']))
 t.save('delivery-probes.json',report)
 print(json.dumps({'input':len(before),'accepted':len(after),'identical_bank_groups_preserved':12,'members_per_group':5}))
