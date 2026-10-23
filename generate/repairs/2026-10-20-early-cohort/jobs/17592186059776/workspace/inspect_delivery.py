"""Inspect visible banks before/after the actual shared delivery filters."""
import json
from pathlib import Path
import check_repair as c
root=c.ROOT
report={}
for level in ['easy','moderate']:
    before=json.loads((root/'evidence/validation'/f'{level}-delivery-input.json').read_text())
    after=json.loads((root/f'evidence/delivery-{level}/accepted.json').read_text())
    summaries={'before':c.summarize(before),'after':c.summarize(after)}
    for sid,s in summaries['after'].items():
        assert len(s['ranks'])>1 and len(s['positions'])>1,(level,sid,s)
        assert s['second_smallest_hits']<s['n']
    report[level]={'counts':{'input':len(before),'accepted':len(after)},'families':summaries,
        'accepted_source_replays':[r['generation']['template'] for r in after if r['generation']['parameters']==[0,0]],
        'semantic_instances_after':len({c.g.task_key(r['question']) for r in after})}
report['limits']=['Captured inventory basis 5576 contains only ten original source records.',
 'Generator batch conservatively deduplicates solution vectors; delivery additionally deduplicates normalized content against captured inventory.',
 'question_selection.rs select assumes freshness/usability are already checked, then weights difficulty bands and samples candidates. This offline audit does not simulate individual learner history or live reservations.',
 'All source replays retain their observed banks. Non-source variant summaries deliberately separate these exact source instances.',
 'Numerical-rank and authored-position witnesses test these cues, not every possible learned strategy.']
(root/'evidence/delivery-comparison.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:{'counts':v['counts'],'families':len(v['families']['after']),'all_families_vary_ranks_and_positions':True,'accepted_source_replays':v['accepted_source_replays']} for k,v in report.items() if k!='limits'}))
