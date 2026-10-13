from pathlib import Path
from scripts.browser.adapter import EXTRACT
import hashlib,json
R=Path(__file__).resolve().parent;rows=json.loads((R/'later-source-candidates.json').read_text());rows.append({'account':'multivariable','task_id':'14120884'})
affected=json.loads((R/'later-ordered-list-affected-packages.json').read_text());h=hashlib.sha256(EXTRACT.encode()).hexdigest();out=[]
for row in affected:
 d=R.parents[1]/'capture'/row['account']/row['task_id'];c=json.loads((d/'content.json').read_text());records=c['questions']+c.get('canonical_examples',[]);selected=[q for q in records if q.get('math_academy_id',q.get('id')) in row['question_or_example_ids']];stale=[q.get('math_academy_id',q.get('id')) for q in selected if q.get('recovery',{}).get('extractor_sha256')!=h];out.append({**row,'offset':next(i for i,r in enumerate(rows) if r['account']==row['account'] and (r.get('task_id') or Path(r['directory']).parents[1].name)==row['task_id']),'current_extractor_sha256':h,'stale_ids':stale,'all_affected_records_found':len(selected)==len(row['question_or_example_ids'])})
(R/'later-ordered-list-refresh-audit.json').write_text(json.dumps(out,indent=2)+'\n');print([{k:v for k,v in x.items() if k not in ['question_or_example_ids','current_extractor_sha256','stale_ids']}|{'stale_count':len(x['stale_ids'])} for x in out])
