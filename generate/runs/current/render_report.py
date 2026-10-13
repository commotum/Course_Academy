"""Render the durable per-KP run state for user review."""
import json,collections
from pathlib import Path
R=Path(__file__).resolve().parent;m=json.loads((R/'manifest.json').read_text());jobs=m['jobs'];counts=collections.Counter(j['status'] for j in jobs)
lines=['# Generator creation progress','',f"Captured scope: **{m['topics']} topics, {m['knowledge_points']} knowledge points**, {m['source_questions']} practice questions; math basis {m['basis']}.",'',
 'Per-KP workers use **gpt-6.1-sol / high**; parent QA checks fidelity, sufficient variation, and scope. All work remains local through step7; database writes: **0**.','',
 ', '.join(f'**{status}: {count}**' for status,count in sorted(counts.items()))+'.','',
 'Dispatch priority: the 15 KPs in `coverage-report.md`, while already-started workers finish.','',
 'Counts describe reviewed work; queued and working KPs are not complete. Source anomalies and authored missing-level designs are recorded with each KP.','',
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
