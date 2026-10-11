import collections,json,re,time
from pathlib import Path
from bs4 import BeautifulSoup
from scripts.browser.parsing import parse_dashboard
from scripts.progress import compare_progress
ROOT=Path('/home/jake/Developer/Course_Academy')
report=json.loads(Path('/tmp/capture-completeness-inventory.json').read_text())
body_gaps, historical_progress, omitted = [], [], []
for row in report['captures']:
 d=ROOT/'reference/mathacademy/capture'/row['account']/row['task_id']
 c=json.loads((d/'content.json').read_text()); cp=json.loads((d/'checkpoint.json').read_text())
 history=cp.get('history',{}).get('questions',[])
 for source in history:
  markup=source.get('html') or (Path(source['html_path']).read_text() if source.get('html_path') else '')
  soup=BeautifulSoup(markup,'html.parser');body=soup.select_one('.questionBody')
  if not body or not body.get_text(strip=True): continue
  q=next((q for q in c.get('questions',[]) if q.get('math_academy_id')==source.get('math_academy_id')),None)
  if q and q.get('problem') == source.get('problem'):
   live=[r['question'] for r in cp['presentations'].values() if r['question'].get('math_academy_id')==source.get('math_academy_id') or str(r['question'].get('dom_id','')).endswith(str(source.get('math_academy_id','')).removeprefix('q-'))]
   body_gaps.append({'account':row['account'],'task_id':row['task_id'],'title':row['title'],'question':source.get('math_academy_id'),
                    'problem':q['problem'],'saved_problem_length':len(q['problem']),'live_problem_lengths':[len(q['problem']) for q in live],
                    'field_count':len(q.get('answer_fields',q.get('fields',[]))),'placeholder_count':len(re.findall(r'\{\{field-\d+\}\}',q['problem'])),
                    'source_file':source.get('html_path'),'missing_html_section':'.questionBody',
                    'body_visible_text':body.get_text(' ',strip=True),'answer_fields_complete':q.get('answer_fields_complete')})
 p=json.loads((d/'post-activity.json').read_text()); obs=p['observations']; dashboard=obs.get('dashboard',{})
 if not (d/'progress-comparison.json').is_file() or not dashboard.get('course_progress'):
  f=dashboard.get('html_path'); source=Path(f) if f else None
  course= parse_dashboard(source.read_text(),row['task_id'])['course_progress'] if source and source.is_file() else None
  baseline=json.loads((d/'progress-before.json').read_text()) if (d/'progress-before.json').is_file() else {}
  comparison=compare_progress(baseline,obs)
  historical_progress.append({'account':row['account'],'task_id':row['task_id'],'course_progress_recovered_from_html':course,
                             'source_file':f,'comparison_available_from_saved_observations':comparison['comparison_available'],
                             'compared_topic_count':comparison['compared_topic_count'],'change_count':len(comparison['changes']),
                             'uncompared_topic_count':len(comparison['uncompared_topics']),
                             'baseline_observed_at':comparison['baseline_observed_at'],'observed_at':comparison['observed_at']})
 for om in row['omissions']: omitted.append({'account':row['account'],'task_id':row['task_id'],**om})
report.update(prompt_body_gaps=body_gaps,historical_progress_recovery=historical_progress,omitted_records=omitted)
report['extended_summary']={'truncated_prompts':len(body_gaps),'captures_with_truncated_prompts':len({(q['account'],q['task_id']) for q in body_gaps}),
 'captures_with_import_omissions':len({(q['account'],q['task_id']) for q in omitted}), 'omission_records':len(omitted),
 'missing_normalized_progress_records':len(historical_progress),'raw_course_percentages_recoverable':sum(bool(r['course_progress_recovered_from_html'] and r['course_progress_recovered_from_html']['displayed_progress']) for r in historical_progress),
 'topic_comparisons_recoverable':sum(r['comparison_available_from_saved_observations'] for r in historical_progress)}
Path('/tmp/new-capture-completeness-extended.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report['extended_summary'],indent=2))
