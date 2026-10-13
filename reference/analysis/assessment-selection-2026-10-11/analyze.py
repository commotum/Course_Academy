"""Audit assessment sources against EDB, and measure observable topic selection."""
from pathlib import Path
import collections, csv, json, re, sys
from datetime import datetime, timezone
ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
PREVIOUS = ROOT / 'reference/analysis/question-difficulty-2026-10-11'
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from edn import loads
BANDS = ['easy', 'moderate', 'hard']
def read(name): return loads((OUT / (name + '.edn')).read_text())
def dist(rows, field):
    c = collections.Counter(r[field] for r in rows if r.get(field) in BANDS)
    n = sum(c.values())
    return {'n': n, 'counts': {b: c[b] for b in BANDS}, 'percent': {b: 100*c[b]/n if n else None for b in BANDS}}
def write_csv(name, rows):
    with (OUT / name).open('w') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
tasks = [t for t in json.loads((PREVIOUS / 'source-tasks.json').read_text()) if t['activity_type'] == 'assessment']
source_rows = [json.loads(s) for s in (PREVIOUS / 'source-appearances.jsonl').read_text().splitlines() if json.loads(s)['activity_type'] == 'assessment']
db = {r[0][':question/math-academy-id']: r[0] for r in read('assessment-questions')}
topics = {e: (str(mid), title) for e, mid, title in read('topics')}
topic_by_mid = {mid: (e, title) for e, (mid, title) in topics.items()}
kptopic = {kp: topics[t][0] for t, kp in read('knowledge-point-topics') if t in topics}
qtopics = collections.defaultdict(set)
for kp, q in read('assessment-memberships'):
    if kp in kptopic: qtopics[q].add(kptopic[kp])
courses = {r[0][':db/id']: r[0] for r in read('courses')}
course_by_code = {c.get(':course/code'): c for c in courses.values()}
course_by_mid = {str(c[':course/math-academy-id']): c for c in courses.values() if ':course/math-academy-id' in c}
units = collections.defaultdict(set); modules = collections.defaultdict(set)
for u,m in read('unit-modules'): units[u].add(m)
for m,t in read('module-topics'): modules[m].add(topics[t][0])
course_topics = collections.defaultdict(set)
for c,u in read('course-units'):
    for m in units[u]: course_topics[c].update(modules[m])
progress = {r['task-id']: r for r in csv.DictReader((ROOT/'reference/progress.csv').open())}
observations = {r['task_id']:r for r in json.loads((ROOT/'reference/assessment-topic-observations-2026-09-28.json').read_text())['summary']}
task_meta = {}; question_meta = {}
for task in tasks:
    p = Path(task['source_file']); d = json.loads(p.read_text())
    meta = {'task_id': task['task_id'], 'stream':task['stream'], 'account_group':'', 'source_file':str(p.relative_to(ROOT)), 'title':'', 'course_id':'', 'course_title':'', 'course_evidence':'unknown', 'completed_at':'', 'advertised_questions':'', 'time_limit_minutes':'', 'source_question_count':task['question_count']}
    course = None
    if task['stream'] == 'human-history':
        pr = progress[task['task_id']]
        course = course_by_code.get(pr['course-code'])
        meta.update(title=pr['topic-name'], completed_at=pr['completed-at'], account_group='human-history', course_evidence='progress.csv course label (may be inferred)')
    elif task['course_id'] is not None:
        course = course_by_mid[str(task['course_id'])]
        meta.update(title=d.get('title',''), completed_at=d.get('captured_at',''), account_group='automated-'+p.parent.parent.name, course_evidence='capture activity course_id; blank quiz course labels can fall back to current capture course')
        details = d.get('activity',{}).get('details',{})
        meta['advertised_questions'] = details.get('question_count','')
        tl = details.get('time_limit','')
        if re.search(r'\d+',str(tl)): meta['time_limit_minutes'] = int(re.search(r'\d+',str(tl))[0])
    else:
        meta['account_group'] = 'automated-'+p.parent.parent.name if 'question-capture-workers' in p.parts else 'automated-foundations' if 'question-capture' in p.parts else 'manual'
        queue = p.parent/'assessment-queue.json'
        if queue.exists():
            a=json.loads(queue.read_text());meta['title']=a.get('title','')
        details = d.get('assessment_details',{})
        if re.search(r'\d+',str(details.get('Questions',''))): meta['advertised_questions']=int(re.search(r'\d+',str(details['Questions']))[0])
        if re.search(r'\d+',str(details.get('Time Limit',''))): meta['time_limit_minutes']=int(re.search(r'\d+',str(details['Time Limit']))[0])
        state = p.parent/'state.json'
        if state.exists():
            s=json.loads(state.read_text());meta['completed_at']=s.get('knowledge_snapshots',{}).get('assessment-completed',{}).get('finished_at','')
    if isinstance(meta['completed_at'], (int,float)):
        meta['completed_at'] = datetime.fromtimestamp(meta['completed_at'], timezone.utc).isoformat()
    if course:
        meta.update(course_id=str(course.get(':course/math-academy-id','')),course_title=course[':course/title'])
    task_meta[task['task_id']]=meta
    for q in d['questions']:
        qid=q.get('math_academy_id') or q.get('id') or q.get('dom_id')
        qid='q-'+re.sub(r'^(?:question-|q-)', '',str(qid))
        href=q.get('kp_href') or q.get('provenance',{}).get('knowledge_point_href','')
        m=re.search(r'/topics/(\d+)(?:#(\d+))?',str(href))
        tid=str(q.get('topic_id') or (m[1] if m else ''))
        assert tid and tid in topic_by_mid, (task['task_id'],qid,tid)
        question_meta[task['task_id'],qid]={'topic_mid':tid,'kp_href':href,'kp_title':q.get('kp_title') or q.get('knowledge_point','')}
rows=[]; conflicts=[]; topic_conflicts=[]
for r in source_rows:
    t=task_meta[r['task_id']]; q=question_meta[r['task_id'],r['question_mid']]; d=db.get(r['question_mid'],{}); band=str(d.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
    if band and band!=r['source_difficulty']: conflicts.append((r['task_id'],r['question_mid']))
    qt=qtopics.get(d.get(':db/id'),set())
    if qt and qt!={q['topic_mid']}: topic_conflicts.append((r['task_id'],r['question_mid'],qt,q['topic_mid']))
    c=course_by_mid.get(t['course_id']); inside=q['topic_mid'] in course_topics[c[':db/id']] if c else None
    rows.append({'task_id':r['task_id'],'question_mid':r['question_mid'],'position':r['task_position'],'stream':r['stream'],'account_group':t['account_group'],'source_difficulty':r['source_difficulty'],'database_entity':d.get(':db/id',''),'database_difficulty':band if band in BANDS else '', 'topic_mid':q['topic_mid'],'topic_title':topic_by_mid[q['topic_mid']][1],'kp_href':q['kp_href'],'kp_title':q['kp_title'],'grade':r['grade'],'course_id':t['course_id'],'course_title':t['course_title'],'course_evidence':t['course_evidence'],'inside_course':inside,'title':t['title'],'completed_at':t['completed_at'],'source_file':t['source_file']})
assert not conflicts and not topic_conflicts, (conflicts,topic_conflicts)
assert len({(r['task_id'],r['question_mid']) for r in rows})==len(rows)
task_rows=[]
for t in task_meta.values():
    rs=[r for r in rows if r['task_id']==t['task_id']];ds=dist(rs,'source_difficulty'); rated=dist(rs,'database_difficulty');known=[r for r in rs if r['inside_course'] is not None]
    task_rows.append({**t,'distinct_topics':len({r['topic_mid'] for r in rs}),'database_rated_questions':rated['n'], 'inside_course_questions':sum(r['inside_course'] is True for r in known) if known else '', 'outside_course_questions':sum(r['inside_course'] is False for r in known) if known else '', **{b:ds['counts'][b] for b in BANDS}, 'retake':'retake' in t['title'].lower()})
assert all(t['distinct_topics']==t['source_question_count'] for t in task_rows)
assert all(not t['advertised_questions'] or t['advertised_questions']==t['source_question_count'] for t in task_rows)
# Repetition across quizzes: same capture account, ordered by source completion time.
history=[]; seen_by_account=collections.defaultdict(set)
for t in sorted(task_rows,key=lambda t:(t['account_group'],t['completed_at'] or str(t['task_id']))):
    old=seen_by_account[t['account_group']]; ts={r['topic_mid'] for r in rows if r['task_id']==t['task_id']}
    history.append({'task_id':t['task_id'],'account_group':t['account_group'],'title':t['title'],'completed_at':t['completed_at'],'topics':len(ts),'previously_captured_assessment_topics':len(ts&old),'not_previously_captured_assessment_topics':len(ts-old),'retake':t['retake'],'history_limit':'captured history only; older unseen assessments remain unknown'})
    old.update(ts)
# How many human quiz questions came from topics taught since the prior same-course quiz?
recent_learning=[]
for t in sorted([t for t in task_rows if t['stream']=='human-history'],key=lambda t:t['completed_at']):
    prior=[p for p in task_rows if p['stream']=='human-history' and p['course_id']==t['course_id'] and p['completed_at']<t['completed_at']]
    if not prior:continue
    previous=max(prior,key=lambda p:p['completed_at']); lesson_topics={p['topic-id'] for p in progress.values() if p['activity-type']=='Lesson' and previous['completed_at']<p['completed-at']<t['completed_at']}
    ts={r['topic_mid'] for r in rows if r['task_id']==t['task_id']}
    recent_learning.append({'task_id':t['task_id'],'title':t['title'],'previous_same_course_quiz':previous['task_id'],'retake':t['retake'],'questions':len(ts),'topics_with_recorded_intervening_lesson':len(ts&lesson_topics),'topics_without_recorded_intervening_lesson':len(ts-lesson_topics),'limit':'incomplete completion feed, not proof of no lesson'})
retakes=[]
for t in task_rows:
    if not t['retake']:continue
    base=t['title'].split(' (Retake)')[0]; prior=[p for p in task_rows if p['account_group']==t['account_group'] and p['course_id']==t['course_id'] and p['title']==base and p['completed_at']<t['completed_at']]
    if not prior:continue
    original=max(prior,key=lambda p:p['completed_at']); a=[r for r in rows if r['task_id']==original['task_id']];b=[r for r in rows if r['task_id']==t['task_id']];missed={r['topic_mid'] for r in a if str(r['grade']).lower() not in ['correct','true']}
    retakes.append({'original':original['task_id'],'retake':t['task_id'],'original_topics':len(a),'retake_topics':len(b),'shared_topics':len({r['topic_mid'] for r in a}&{r['topic_mid'] for r in b}),'shared_question_ids':len({r['question_mid'] for r in a}&{r['question_mid'] for r in b}),'original_missed_topics':len(missed),'missed_topics_retested':len(missed & {r['topic_mid'] for r in b})})
known=[r for r in rows if r['inside_course'] is not None]
rated=[r for r in rows if r['database_difficulty']]
summary={'snapshot':json.loads((OUT/'snapshot.json').read_text()),'source_assessments':len(tasks),'source_questions':len(rows),'source_unique_questions':len({r['question_mid'] for r in rows}),'source_unique_topics':len({r['topic_mid'] for r in rows}),'database_rated_assessments':len({r['task_id'] for r in rated}),'database_rated_unique_questions':len({r['question_mid'] for r in rated}),'database_rated_distribution':dist(rated,'database_difficulty'),'all_source_distribution':dist(rows,'source_difficulty'),'source_by_stream':{s:dist([r for r in rows if r['stream']==s],'source_difficulty') for s in sorted({r['stream'] for r in rows})},'rated_by_stream':{s:dist([r for r in rated if r['stream']==s],'database_difficulty') for s in sorted({r['stream'] for r in rows})},'question_counts':dict(sorted(collections.Counter(t['source_question_count'] for t in task_rows).items())),'assessments_with_repeated_topics':0,'difficulty_disagreements':conflicts,'topic_disagreements':topic_conflicts,'rated_questions_with_current_db_topic_membership':sum(bool(qtopics.get(r['database_entity'])) for r in rated),'capture_context_course_id_questions':len([r for r in known if r['stream']=='recent-automated']),'known_or_csv_inferred_course_questions':len(known),'inside_course_questions':sum(r['inside_course'] is True for r in known),'outside_course_questions':sum(r['inside_course'] is False for r in known),'outside_course_examples':[r for r in known if r['inside_course'] is False][:8],'course_membership_limit':'Capture course IDs may be current-course fallbacks, and CSV enrollment labels may be inferred. This is a context comparison, not proof of the quiz creation course or an estimate of course preference strength. Membership uses the current EDB curriculum.','previously_captured_topics_by_stream':{},'time_limits':dict(sorted(collections.Counter(t['time_limit_minutes'] for t in task_rows if t['time_limit_minutes']).items())),'retakes':retakes,'recent_learning':recent_learning,'assessment_engine_weights':[50,40,10],'current_policy_activity_types':[str(c[':question-weights/activity-type'][':db/ident']) for c in read('policy')[0][0][':policy/question-selection-weights']]}
summary['previously_captured_topics_by_stream'] = {s:{'questions':sum(h['topics'] for h in history if task_meta[h['task_id']]['stream']==s),'previously_assessed':sum(h['previously_captured_assessment_topics'] for h in history if task_meta[h['task_id']]['stream']==s)} for s in sorted({r['stream'] for r in rows})}
summary['regular_quiz_repeat_counts'] = {'questions':sum(h['topics'] for h in history if not h['retake']), 'previously_captured_assessment_topics':sum(h['previously_captured_assessment_topics'] for h in history if not h['retake']), 'human_questions':sum(h['topics'] for h in history if not h['retake'] and task_meta[h['task_id']]['stream']=='human-history'), 'human_previously_captured_assessment_topics':sum(h['previously_captured_assessment_topics'] for h in history if not h['retake'] and task_meta[h['task_id']]['stream']=='human-history')}
write_csv('assessment-questions.csv',rows);write_csv('assessment-tasks.csv',task_rows);write_csv('topic-repetition.csv',history);write_csv('human-recent-learning.csv',recent_learning)
(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ['outside_course_examples','recent_learning']},indent=2))
