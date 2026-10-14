"""Render the durable per-KP run state for user review."""
import json,collections
from pathlib import Path
R=Path(__file__).resolve().parent;m=json.loads((R/'manifest.json').read_text());jobs=m['jobs'];counts=collections.Counter(j['status'] for j in jobs)
lines=['# Generator creation progress','',f"Cumulative scope: **{m['topics']} topics, {m['knowledge_points']} knowledge points**. Approved sources retain their recorded per-KP bases; active-before-refresh sources use1356; refreshed queued sources: basis{m.get('latest_candidate_basis',1356)}.",'',
 'Per-KP workers use **gpt-6.1-sol / high**; parent QA checks fidelity, sufficient variation, and scope. All work remains local through step7; database writes: **0**.','',
 ', '.join(f'**{status}: {count}**' for status,count in sorted(counts.items()))+'.','',
 f"Latest query: **{m.get('latest_candidate_topics',m['topics'])} topics, {m.get('latest_candidate_knowledge_points',m['knowledge_points'])} KPs**; script ranking is retained in [updated candidates](candidates-2026-10-14.json). Finish existing workers, then follow updated ranks; coverage-report priorities remain first and are already approved.",'',
 'Cumulative counts include previously approved KPs and two active KPs that left the latest list; their work is retained. Queued and working KPs are not complete. Source anomalies and authored missing-level designs are recorded with each KP.','',
 '| KP | Topic | Knowledge point | Source E / M / H / unrated | Status | Parent QA |',
 '|---|---|---|---|---|---|']
for j in jobs:
 c=j['source_counts'];s=' / '.join(str(c.get(':question.difficulty/'+x,0)) for x in ('easy','moderate','hard'))+' / '+str(c.get('unrated',0))
 script='../../scratch/'+Path(j['script']).name
 label=f"[{j['kp_id']}]({script})" if Path(j['script']).exists() else str(j['kp_id'])
 qa=f"[Report](qa/{j['kp_id']}.json)" if j['qa'] else '—'
 lines.append(f"| {label} | {j['topic_title'].replace('|','/')} | {j['title'].replace('|','/')} | {s} | {j['status']} | {qa} |")
(R/'progress.md').write_text('\n'.join(lines)+'\n')
print(dict(counts))
