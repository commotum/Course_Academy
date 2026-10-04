"""Course-qualified color observations; these are not exact FIRe state values."""
from datetime import datetime, timezone
from pathlib import Path

from core import atomic_json

COURSES = (113, 111, 136)
COLORS = {
    'white': 0, 'rgb(255, 255, 255)': 0,
    'rgb(210, 231, 249)': 1, 'rgb(165, 207, 243)': 2,
    'rgb(120, 182, 237)': 3, 'rgb(74, 158, 232)': 4,
    'rgb(29, 134, 226)': 5, 'rgb(23, 107, 181)': 6,
}
EXTRACT_PROGRESS = '''() => ({
  declared_topics:[...document.querySelectorAll('.unitNumTopics')].map(n=>n.textContent.trim()),
  units_html:document.querySelector('#units')?.outerHTML,
  rows:[...document.querySelectorAll('.moduleTopics tr')].map(r=>({
    module_id:r.closest('.moduleTopics').id,
    topic_number:r.querySelector('.topicNumber')?.textContent.trim(),
    title:r.querySelector('.topicLink')?.textContent.trim(),
    href:r.querySelector('.topicLink')?.getAttribute('href'),
    color:r.querySelector('.topicCircle')?.style.background,
    circle_style:r.querySelector('.topicCircle')?.getAttribute('style')
  }))
})'''


def now():
    return datetime.now(timezone.utc).isoformat()


def normalize_course(course_id, observed):
    import re
    counts = [re.fullmatch(r'(\d+) topics?', s) for s in observed['declared_topics']]
    if not counts or not all(counts) or sum(int(m[1]) for m in counts) != len(observed['rows']):
        raise ValueError('Incomplete course progress page: ' + str(course_id))
    topics, seen = [], set()
    for row in observed['rows']:
        match = re.fullmatch(r'/topics/(\d+)\?courseId=(\d+)', row.get('href') or '')
        if not match or int(match[2]) != course_id or not row.get('title'):
            raise ValueError('Unexpected topic identity in course progress: ' + str(course_id))
        topic_id = int(match[1])
        if topic_id in seen or row.get('color') not in COLORS:
            raise ValueError('Duplicate topic or unknown progress color: ' + str(topic_id))
        seen.add(topic_id)
        topics.append({**row, 'topic_id': topic_id, 'display_band': COLORS[row['color']]})
    if not observed.get('units_html'):
        raise ValueError('Missing course progress HTML')
    return topics


def changes(previous, current):
    def index(snapshot):
        return {(c['course_id'], t['topic_id']): t
                for c in snapshot.get('courses', []) for t in c['topics']}
    before, after = index(previous), index(current)
    return [{'course_id': key[0], 'topic_id': key[1],
             'title': (after.get(key) or before[key])['title'],
             'before_color': before.get(key, {}).get('color'),
             'after_color': after.get(key, {}).get('color'),
             'before_band': before.get(key, {}).get('display_band'),
             'after_band': after.get(key, {}).get('display_band')}
            for key in sorted(before.keys() | after.keys())
            if before.get(key, {}).get('color') != after.get(key, {}).get('color')]


def capture(reader, directory, event, task_id, course_ids=COURSES, previous=None, recovered=False):
    directory = Path(directory)
    snapshot = {'event': event, 'task_id': task_id, 'started_at': now(),
                'recovered_after_interruption': recovered,
                'scope': 'course-progress display colors',
                'mapping': 'White=0; blue bands=1-6; darkest=6 is a local initialization convention',
                'limitations': 'Not exact continuous repetitions, memory, intervals, ability, or complete internal MA state. Courses are read sequentially.',
                'courses': []}
    for course_id in course_ids:
        url = 'https://mathacademy.com/courses/' + str(course_id) + '/progress'
        started = now()
        reader.navigate(url, force=True)
        reader.page.locator('.moduleTopics .topicLink').first.wait_for(state='attached')
        reader.page.wait_for_timeout(reader.args.settle_ms)
        reader.check()
        observed = reader.page.evaluate(EXTRACT_PROGRESS)
        topics = normalize_course(course_id, observed)
        course = {'course_id': course_id, 'source_url': url, 'started_at': started,
                  'captured_at': now(), 'topics': topics, 'units_html': observed['units_html']}
        snapshot['courses'].append(course)
    snapshot['finished_at'] = now()
    snapshot['changes'] = changes(previous, snapshot) if previous else []
    snapshot['comparison_available'] = previous is not None
    # The complete file is published only after every requested course validates.
    atomic_json(directory / (event + '.json'), snapshot)
    return snapshot
