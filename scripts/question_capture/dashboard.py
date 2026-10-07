"""Cache displayed course completion and today's task XP at normal queue reads."""
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from core import atomic_json

LOCAL_TIMEZONE=ZoneInfo('America/Los_Angeles')
EXTRACT_STATS=r'''() => ({
  percent:document.querySelector('#coursePercentComplete')?.textContent.trim(),
  course_href:document.querySelector('a#courseNameLink, a.courseNameLink')?.getAttribute('href'),
  completed:[...document.querySelectorAll('#completedTasks .taskCompleted')].map(e=>({
    task_id:e.id.match(/^task-(\d+)$/)?.[1],
    day:e.querySelector('.taskCompletedDate')?.value,
    kind:e.querySelector('.taskTypeLocked')?.textContent.trim().toLowerCase(),
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
    import json
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
    percent=re.search(r'(\d+(?:\.\d+)?)\s*%',observed.get('percent') or '')
    course=re.fullmatch(r'/courses/(\d+)/progress',observed.get('course_href') or '')
    stats={'observed_at':datetime.now(LOCAL_TIMEZONE).isoformat(),
           'course_id':int(course[1]) if course else None,
           'course_percent_text':observed.get('percent'),
           'percent_complete':float(percent[1]) if percent else None,
           'daily_xp':{'date':day,'earned':sum(t['earned'] for t in tasks.values()),
                       'base':sum(t['base'] for t in tasks.values()),'tasks':len(tasks)}}
    atomic_json(state_dir/'dashboard.json',stats)
    return stats


def capture(page,state_dir):
    return record(state_dir,page.evaluate(EXTRACT_STATS))
