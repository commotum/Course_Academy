"""Read-only first-observed review offers, frozen to encompassing manifests.

Run: PYTHONPATH=capture python3 reference/analysis/review-threshold-2026-10-11/offers/analyze.py
Only writes outputs beside this script. Active capture files are never mutated.
"""
import csv
import hashlib
import html
import json
import re
import statistics
from bisect import bisect_right
from collections import Counter, defaultdict
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path

from scripts.analyze_encompassing import timestamp
from scripts.progress import color_observation

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
FROZEN = ROOT / 'reference/mathacademy/encompassing-analysis-2026-10-11'
ACCOUNTS = ['foundations', 'linear', 'multivariable', 'differential']


def read(path):
    return json.loads(Path(path).read_text())


def rel(path):
    return str(Path(path).relative_to(ROOT))


@lru_cache(maxsize=256)
def band_from_style(color, style):
    return color_observation(dict(color=color,circle_style=style))['display_band']


def cards_from_html(path):
    """Parse only unlocked task fragments, never completed history cards."""
    raw = Path(path).read_text()
    starts = list(re.finditer(r'<div\b[^>]*(?:class="taskUnlocked"[^>]*id="task-\d+"|id="task-\d+"[^>]*class="taskUnlocked")[^>]*>', raw))
    records = []
    for i, m in enumerate(starts):
        stop = starts[i+1].start() if i+1 < len(starts) else len(raw)
        completed = raw.find('id="completedTasks"', m.end())
        if completed >= 0:
            stop = min(stop, completed)
        part = raw[m.start():stop]
        tid = re.search(r'id="task-(\d+)"', m[0])[1]
        kind = re.search(r'taskTypeUnlocked[^>]*>\s*([^<]+)', part)
        route = re.search(r'/tasks/'+tid+r'/topics/(\d+)/(lesson|review)', part)
        topic = route[1] if route else None
        if not topic:
            link = re.search(r'<a\b(?=[^>]*id="taskTopicLink-'+tid+r'")(?=[^>]*href="/topics/(\d+))[^>]*>', part)
            topic = link[1] if link else None
        records.append({'task_id':tid, 'topic_id':topic,
            'kind':kind[1].strip().lower() if kind else route[2] if route else 'unknown'})
    return records


def distribution(values):
    values = sorted(x for x in values if x is not None)
    if not values:
        return {'n': 0}
    return dict(n=len(values), min=values[0], q25=values[int((len(values)-1)*.25)],
        median=statistics.median(values), q75=values[int((len(values)-1)*.75)], max=values[-1])


def analyze(account):
    report_path = FROZEN / (account+'.json')
    report = read(report_path)
    events = sorted(report['activity_audit'], key=lambda e:e['time'])
    begin, end = events[0]['time'], max(e['finished_at'] for e in events)
    event_by_id = {e['task_id']:e for e in events}
    sources = {s['task_id']:s for s in report['sources']}
    band_records, queues, assessments = [], [], []
    journal = ROOT / ('.local/question_capture/journal.jsonl' if account=='foundations' else f'.local/question_capture-workers/{account}/journal.jsonl')
    journal_raw = journal.read_bytes()
    candidate_topics = {e['source'] for e in events if e['source']}
    for line in journal_raw.decode().splitlines():
        try:
            row=json.loads(line)
        except json.JSONDecodeError:
            continue
        if row.get('event') in ('queue_observed','queue_observation_corrected') and begin<=row.get('timestamp',0)<=end:
            candidate_topics.update(str(c['topic_id']) for c in row.get('queue',[]) if c.get('topic_id'))
    seen_snapshots, seen_dashboards = set(), set()
    direct, all_direct = defaultdict(list), defaultdict(list)
    def snapshot(data, path):
        for course in data.get('courses') or data.get('progress') or []:
            at = timestamp(course.get('captured_at') or course.get('observed_at') or data.get('observed_at') or data.get('finished_at'))
            if at is None or at > end:
                continue
            for topic in course.get('topics', []):
                if str(topic['topic_id']) not in candidate_topics:
                    continue
                band_records.append((at, str(course['course_id']), str(topic['topic_id']),
                    band_from_style(topic.get('color'),topic.get('circle_style')), rel(path)))
    ledger_path = ROOT / ('.local/question_capture/daily-xp.json' if account=='foundations' else f'.local/question_capture-workers/{account}/daily-xp.json')
    ledger = {str(tid):xp.get('earned') for tasks in read(ledger_path).values() for tid,xp in tasks.items()}
    for event_index,event in enumerate(events):
        tid = event['task_id']
        source = sources[tid]
        path = Path(source['path'])
        data = read(path)
        before = source.get('before_path')
        if before and before not in seen_snapshots and Path(before).exists():
            seen_snapshots.add(before)
            snapshot(read(before), before)
        if event['pipeline']=='legacy':
            snapshot(data, path)
            content = read(path.parents[1]/'state.json') if event['kind']=='assessment' else {}
        else:
            content = read(path.parent/'content.json') if event['kind']=='assessment' else {}
            histories = [h['observations'] for h in data.get('observation_history', []) if h.get('observations')]
            histories.append(data.get('observations', {}))
            for obs in histories:
                snapshot(obs, path)
                dash = obs.get('dashboard') or {}
                dp, dt = dash.get('html_path'), timestamp(dash.get('captured_at'))
                if dp and dt and dt<=end and dp not in seen_dashboards and Path(dp).exists():
                    seen_dashboards.add(dp)
                    queues.append(dict(time=dt, after_task_id=tid, cards=cards_from_html(dp), source=rel(dp), source_record=rel(path), origin='post_activity_dashboard'))
        if event['kind'] in ('lesson','review') and event['source']:
            xp = event.get('earned_xp')
            if xp is None:
                xp = ledger.get(tid)
            record = dict(time=event['time'], task_id=tid, kind=event['kind'], outcome=event['outcome'],
                observed_end=event['finished_at'], earned_xp=xp, source=rel(path), late=bool(data.get('recovered_after_interruption')))
            all_direct[event['source']].append(record)
            if event['outcome']=='passed':
                direct[event['source']].append(record)
        if event['kind']=='assessment':
            questions = content.get('questions', {})
            questions = list(questions.values()) if isinstance(questions,dict) else questions
            topics, missed, unknown = set(), set(), 0
            for q in questions:
                topic = q.get('topic_id') or q.get('content',{}).get('topic_id')
                grade = q.get('actual_result') or q.get('grade') or q.get('result') or q.get('after',{}).get('result')
                if topic:
                    topics.add(str(topic))
                    if grade in ('Incorrect','Skipped Question','Skipped'):
                        missed.add(str(topic))
                else:
                    unknown += 1
            assessments.append(dict(time=event['time'], task_id=tid, topics=topics, missed=missed, unknown_questions=unknown, source=rel(path)))
        if event_index%250==0:
            print(account,'read',event_index+1,'activities',flush=True)
    for line_number,line in enumerate(journal_raw.decode().splitlines(), 1):
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue # Active writer can leave a trailing partial record.
        if row.get('event') not in ('queue_observed','queue_observation_corrected') or not begin<=row.get('timestamp',0)<=end:
            continue
        cards = [dict(task_id=str(c['task_id']), topic_id=str(c['topic_id']) if c.get('topic_id') else None,
            kind=c.get('task_type')) for c in row.get('queue',[]) if c.get('task_id')]
        queues.append(dict(time=row['timestamp'], after_task_id=str(row['after_task_id']) if row.get('after_task_id') else None,
            cards=cards, source=rel(journal), source_line=line_number, origin='legacy_journal'))
    queues.sort(key=lambda q:q['time'])
    band_records.sort()
    band_cursor, band_state, offered = 0, {}, set()
    band_changes = defaultdict(list)
    rows = []
    previous_queue = None
    for queue in queues:
        at = queue['time']
        while band_cursor<len(band_records) and band_records[band_cursor][0]<=at:
            br = band_records[band_cursor]
            old = band_state.get((br[1],br[2]))
            if old and old[3] is not None and br[3] is not None and old[3]!=br[3]:
                band_changes[br[2]].append(dict(at=br[0],course=br[1],before=old[3],after=br[3],source=br[4]))
            band_state[br[1],br[2]] = br
            band_cursor += 1
        for card in queue['cards']:
            tid, topic = card['task_id'], card['topic_id']
            if card['kind']!='review' or tid in offered:
                continue
            offered.add(tid)
            topic = topic or event_by_id.get(tid,{}).get('source')
            eligible = [x for x in direct[topic] if x['time']<at and x['task_id']!=tid]
            all_previous = [x for x in all_direct[topic] if x['time']<at and x['task_id']!=tid]
            prior = eligible[-1] if eligible else None
            latest = all_previous[-1] if all_previous else None
            bs = [x for (course,t),x in band_state.items() if t==topic]
            known = {x[3] for x in bs if x[3] is not None}
            band = next(iter(known)) if len(known)==1 else None
            previous = previous_queue
            absent = previous if previous and tid not in {c['task_id'] for c in previous['cards']} else None
            assessments_before = [a for a in assessments if a['time']<at]
            missed_since_prior = [a for a in assessments_before if topic in a['missed'] and (prior is None or a['time']>prior['time'])]
            after = event_by_id.get(queue['after_task_id'],{})
            immediate_assessment = after.get('kind')=='assessment'
            negative_previous = latest and latest.get('earned_xp') is not None and latest['earned_xp']<0
            failed_previous = latest and latest.get('outcome')=='failed'
            status = ('negative_xp_or_failed_repeat' if negative_previous or failed_previous else
                'assessment_miss_since_last_pass' if missed_since_prior else
                'immediately_after_assessment_unresolved' if immediate_assessment else
                'no_captured_remediation_trigger')
            changes = [c for c in band_changes[topic] if prior and c['at']>prior['observed_end']]
            # Same activity's several course reads can show one shared topic rise.
            rises = {c['source'] for c in changes if c['after']>c['before']}
            rows.append(dict(account=account, task_id=tid, topic_id=topic, first_offer_at=at,
                first_offer_utc=datetime.fromtimestamp(at,timezone.utc).isoformat(),
                first_offer_source=queue['source'], first_offer_source_line=queue.get('source_line'),
                first_offer_origin=queue['origin'], after_task_id=queue['after_task_id'],
                last_absent_at=absent['time'] if absent else None, last_absent_source=absent['source'] if absent else None,
                offer_bracket_seconds=at-absent['time'] if absent else None,
                classification=status, prior_direct_task=prior['task_id'] if prior else None,
                prior_direct_kind=prior['kind'] if prior else None,
                prior_direct_source=prior['source'] if prior else None,
                prior_direct_time_recovered_late=prior['late'] if prior else None,
                hours_since_last_pass=(at-prior['time'])/3600 if prior else None,
                latest_same_topic_task=latest['task_id'] if latest else None,
                latest_same_topic_earned_xp=latest['earned_xp'] if latest else None,
                assessment_missed_tasks=[a['task_id'] for a in missed_since_prior],
                visible_rise_sources_since_last_pass=len(rises),
                visible_changes_since_last_pass=changes,
                band=band, band_conflict=len(known)>1,
                band_age_hours=(at-max(x[0] for x in bs))/3600 if bs else None,
                band_evidence=[dict(course=x[1],band=x[3],at=x[0],source=x[4]) for x in bs],
                observed_completion=tid in event_by_id))
        previous_queue = queue
    def summarise(subset):
        return dict(n=len(subset), by_band=dict(Counter(str(r['band']) for r in subset)),
            with_last_absent=sum(r['last_absent_at'] is not None for r in subset),
            prior_direct_age_hours=distribution([r['hours_since_last_pass'] for r in subset]),
            band_age_hours=distribution([r['band_age_hours'] for r in subset]),
            by_band_age={str(b):distribution([r['hours_since_last_pass'] for r in subset if r['band']==b]) for b in range(7)})
    summary = dict(account=account, frozen_activities=len(events), queue_observations=len(queues),
        first_offer_count=len(rows), kinds=dict(Counter(r['classification'] for r in rows)),
        all=summarise(rows), by_classification={s:summarise([r for r in rows if r['classification']==s]) for s in sorted({r['classification'] for r in rows})},
        no_trigger_fresh_band=summarise([r for r in rows if r['classification']=='no_captured_remediation_trigger' and r['band_age_hours'] is not None and r['band_age_hours']<=1 and not r['prior_direct_time_recovered_late']]),
        sources=dict(report=rel(report_path),report_sha256=hashlib.sha256(report_path.read_bytes()).hexdigest(), journal=rel(journal),journal_prefix_sha256=hashlib.sha256(journal_raw).hexdigest(), journal_bytes_read=len(journal_raw)),
        window=dict(begin=begin,end=end))
    print(account, json.dumps({k:summary[k] for k in ['frozen_activities','queue_observations','first_offer_count','kinds']}),flush=True)
    (OUT/(account+'.json')).write_text(json.dumps(dict(summary=summary,offers=rows),indent=2)+'\n')
    return rows,summary


all_rows,summaries=[],[]
for account in ACCOUNTS:
    rows,summary=analyze(account)
    all_rows.extend(rows)
    summaries.append(summary)
fields=[k for k in all_rows[0] if k not in ('band_evidence','visible_changes_since_last_pass')]
with (OUT/'first-review-offers.csv').open('w') as file:
    writer=csv.DictWriter(file,fieldnames=fields)
    writer.writeheader()
    writer.writerows({k:r[k] for k in fields} for r in all_rows)
(OUT/'summary.json').write_text(json.dumps(summaries,indent=2)+'\n')
import runpy
runpy.run_path(str(OUT/'finalize.py'),run_name='__main__')
