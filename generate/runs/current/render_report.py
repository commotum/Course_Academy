"""Render the durable per-KP run state for user review."""
import json,collections
from pathlib import Path
R=Path(__file__).resolve().parent;m=json.loads((R/'manifest.json').read_text());jobs=m['jobs'];counts=collections.Counter(j['status'] for j in jobs)
lines=['# Generator creation progress','',f"Cumulative scope: **{m['topics']} topics, {m['knowledge_points']} knowledge points**. Approved sources retain their recorded per-KP bases; active-before-refresh sources use1356; refreshed queued sources: basis{m.get('latest_candidate_basis',1356)}.",'',
 'Per-KP workers use **gpt-6.1-sol / high**; parent QA checks fidelity, sufficient variation, and scope. All work remains local through step7; database writes: **0**.','',
 ', '.join(f'**{status}: {count}**' for status,count in sorted(counts.items()))+'.','',
 f"Latest query: **{m.get('latest_candidate_topics',m['topics'])} topics, {m.get('latest_candidate_knowledge_points',m['knowledge_points'])} KPs**; script ranking is retained in [updated candidates](candidates-2026-10-14.json). The [13 explicit user priorities](user-priorities-2026-10-14.md) supersede that dispatch order and the earlier coverage priority. Existing approved work is preserved; other ready drafts await QA until these13 pass. Then finish any coverage-report KPs and the remaining script-ranked candidates.",'',
 'Cumulative counts retain seven earlier KPs outside the latest list. Only qa_passed jobs have current parent verification; queued, working and needs_revalidation jobs are not complete. Captured counts can include independently authored inventory as well as original MA examples; per-KP evidence separates them. Source anomalies and authored missing-level designs are recorded with each KP.','',
 '| KP | Topic | Knowledge point | Captured E / M / H / unrated | Status | Parent QA |',
 '|---|---|---|---|---|---|']
for j in jobs:
 c=j['source_counts'];s=' / '.join(str(c.get(':question.difficulty/'+x,0)) for x in ('easy','moderate','hard'))+' / '+str(c.get('unrated',0))
 script='../../scratch/'+Path(j['script']).name
 label=f"[{j['kp_id']}]({script})" if Path(j['script']).exists() else str(j['kp_id'])
 qa=f"[Report](qa/{j['kp_id']}.json)" if j['qa'] else '—'
 lines.append(f"| {label} | {j['topic_title'].replace('|','/')} | {j['title'].replace('|','/')} | {s} | {j['status']} | {qa} |")
(R/'progress.md').write_text('\n'.join(lines)+'\n')
if m.get('explicit_user_priority_ids'):
 by={j['kp_id']:j for j in jobs}
 lines=['# Explicit user priorities','','Dispatch in the listed order; independently approve all13 before continuing other unfinished work. Completed work is preserved. All15 coverage-report priorities currently have QA approval.','','| Priority | KP | Knowledge point | Status | Parent QA |','|---:|---|---|---|---|']
 for i,k in enumerate(m['explicit_user_priority_ids'],1):
  j=by[k];q=f"[Report](qa/{k}.json)" if j.get('qa') else '—'
  lines.append(f"| {i} | {k} | {j['title']} | {j['status']} | {q} |")
 (R/'user-priorities-2026-10-14.md').write_text('\n'.join(lines)+'\n')
print(dict(counts))
