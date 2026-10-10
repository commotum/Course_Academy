"""Cache displayed course completion and today's task XP at normal queue reads."""
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from core import ROOT, atomic_json

LOCAL_TIMEZONE=ZoneInfo('America/Los_Angeles')
EXTRACT_STATS=r'''() => ({
  percent:document.querySelector('#coursePercentComplete')?.textContent.trim(),
  course_href:document.querySelector('a#courseNameLink, a.courseNameLink')?.getAttribute('href'),
  completed:[...document.querySelectorAll('#completedTasks .taskCompleted')].map(e=>({
    task_id:e.id.match(/^task-(\d+)$/)?.[1],
    day:e.querySelector('.taskCompletedDate')?.value,
    kind:e.querySelector('.taskTypeLocked')?.textContent.trim().toLowerCase(),
    title:e.querySelector('.taskNameUnlocked, .taskNameLocked')?.textContent.trim(),
    completed_time:e.querySelector('.taskTimeCompleted')?.textContent.trim(),
    points:e.querySelector('.taskPoints')?.textContent.trim()
  }))
})'''


def local_date():
    return datetime.now(LOCAL_TIMEZONE).date().isoformat()


def xp_pair(text):
    match=re.fullmatch(r'(-?[\d,]+)\s*(?:/\s*([\d,]+))?\s*XP',text or '',re.I)
    if not match:return None
    earned=int(match[1].replace(',',''))
    # Fixed awards, such as placement exams, display a single full award.
    base=int(match[2].replace(',','')) if match[2] else max(0,earned)
    return {'earned':earned,'base':base}


def record(state_dir, observed):
    state_dir=Path(state_dir)
    ledger_file=state_dir/'daily-xp.json'
    try:ledger=json.loads(ledger_file.read_text())
    except (OSError,ValueError):ledger={}
    day=local_date();tasks=ledger.setdefault(day,{})
    for item in observed.get('completed',[]):
        pair=xp_pair(item.get('points'))
        if item.get('day')=='Today' and item.get('task_id') and pair is not None:
            tasks[str(item['task_id'])]={**pair,'kind':item.get('kind'),'source_text':item['points']}
    atomic_json(ledger_file,ledger)
    recent_file=state_dir/'recent-activities.json'
    try:recent=json.loads(recent_file.read_text())
    except (OSError,ValueError):
        # Older XP ledgers already contain authentic completed activity points.
        recent=[{'task_id':mid,'date':date,**task} for date in sorted(ledger)
                for mid,task in reversed(list(ledger[date].items()))]
    known={str(t['task_id']):t for t in recent}
    observed_ids=[]
    for item in observed.get('completed',[]):
        pair=xp_pair(item.get('points'))
        if not item.get('task_id') or pair is None:continue
        mid=str(item['task_id']);observed_ids.append(mid)
        label=item.get('day')
        date=day if label=='Today' else (datetime.fromisoformat(day)-timedelta(days=1)).date().isoformat() if label=='Yesterday' else None
        known[mid]={**known.get(mid,{}),**item,**pair,'task_id':mid,'date':date,'source_text':item['points']}
    # CompletedTasks is newest first; retain older cached rows if it is truncated.
    order=[str(t['task_id']) for t in recent if str(t['task_id']) not in observed_ids]
    order.extend(reversed(list(dict.fromkeys(observed_ids))))
    recent=[known[mid] for mid in order][-20:]
    atomic_json(recent_file,recent)
    percent=re.search(r'(\d+(?:\.\d+)?)\s*%',observed.get('percent') or '')
    course=re.fullmatch(r'/courses/(\d+)/progress',observed.get('course_href') or '')
    stats={'observed_at':datetime.now(LOCAL_TIMEZONE).isoformat(),
           'course_id':int(course[1]) if course else None,
           'course_percent_text':observed.get('percent'),
           'percent_complete':float(percent[1]) if percent else None,
           'daily_xp':{'date':day,'earned':sum(t['earned'] for t in tasks.values()),
                       'base':sum(t['base'] for t in tasks.values()),'tasks':len(tasks)}}
    stats.update(activity_counts=activity_counts(tasks.values()),recent_activities=recent)
    atomic_json(state_dir/'dashboard.json',stats)
    return stats


def capture(page,state_dir):
    return record(state_dir,page.evaluate(EXTRACT_STATS))


KINDS=('lesson','review','quiz','multistep','diagnostic')


def activity_counts(tasks):
    counts={kind:0 for kind in KINDS}
    for task in tasks:
        kind=re.sub(r'[\s_-]+','',task.get('kind') or '')
        kind={'assessment':'quiz','test':'quiz','exam':'quiz','quizretake':'quiz',
              'assessmentretake':'quiz','testretake':'quiz'}.get(kind,kind)
        if kind in counts:counts[kind]+=1
    return counts


def receipt_new_ids(directory):
    """Count actual question identity assertions, using saved receipts only."""
    from edn import loads
    root=Path(directory)/'edb-import-math'
    if not root.is_dir():root=Path(directory)/'edb-import'
    try:
        attributes=loads((root/'attributes.edn').read_text())
        identity=next(a for a,name in attributes if str(name)==':question/math-academy-id')
        receipt=loads((root/'commit.edn').read_text())
        if not receipt.get(':edb/committed'):return []
        return sorted({str(d[2]) for d in receipt.get(':edb/tx-data',[]) if d[1]==identity and d[-1] is True})
    except (OSError,ValueError,StopIteration,KeyError,TypeError):return []


def import_totals(state_dir):
    """Daily unique questions added/refreshed, cached without any EDB queries."""
    state_dir=Path(state_dir);source=state_dir/'journal.jsonl';cache=state_dir/'dashboard-imports.json'
    day=local_date()
    try:stamp=[source.stat().st_mtime_ns,source.stat().st_size]
    except OSError:stamp=None
    try:saved=json.loads(cache.read_text())
    except (OSError,ValueError):saved={}
    if saved.get('schema')==2 and saved.get('date')==day and saved.get('stamp')==stamp:return saved['totals']
    imported=set();added=set();directories=set()
    try:lines=source.read_text().splitlines()
    except OSError:lines=[]
    for line in lines:
        try:event=json.loads(line)
        except ValueError:continue
        if event.get('event')!='content_imported' or not event.get('timestamp'):continue
        if datetime.fromtimestamp(event['timestamp'],LOCAL_TIMEZONE).date().isoformat()!=day:continue
        directory=event.get('directory')
        if directory:directory=str((ROOT/Path(directory)).resolve())
        if not directory or directory in directories:continue
        directories.add(directory)
        ids=event.get('imported_question_ids')
        if ids is None:
            try:
                content=json.loads((Path(directory)/'content.json').read_text())
                ids=[q['math_academy_id'] for q in content['questions']+content.get('canonical_examples',[])]
            except (OSError,ValueError,KeyError):ids=[]
        imported.update(ids)
        added.update(event.get('new_question_ids') if 'new_question_ids' in event else receipt_new_ids(directory))
    totals={'added':len(added),'updated':len(imported-added),'imported':len(imported)}
    atomic_json(cache,{'schema':2,'date':day,'stamp':stamp,'totals':totals})
    return totals
