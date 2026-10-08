"""Course-qualified color observations; these are not exact FIRe state values."""
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import re

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
EXTRACT_SIDEBAR = '''() => ({
  enrolled:document.querySelector('a#courseNameLink, a.courseNameLink')?.getAttribute('href'),
  links:[...document.querySelectorAll('#sequenceUnits a.courseUnitLink[href]')].map(a=>a.getAttribute('href')),
  html:document.querySelector('#sequenceUnits')?.outerHTML
})'''


def sidebar_courses(observed):
    """Deduplicate the sidebar's unit links into complete course pages."""
    urls=[]
    for href in [observed.get('enrolled'),*observed.get('links',[])]:
        if not href:continue
        scope=target('https://mathacademy.com'+href if href.startswith('/') else href)
        url='https://mathacademy.com/courses/'+str(scope['course_id'])+'/progress'
        if url not in urls:urls.append(url)
    return urls


def now():
    return datetime.now(timezone.utc).isoformat()


def target(value):
    if isinstance(value,int):value='https://mathacademy.com/courses/'+str(value)+'/progress'
    url=urlparse(str(value))
    match=re.fullmatch(r'/courses/([1-9]\d*)/progress',url.path)
    query=parse_qs(url.query,keep_blank_values=True)
    if (url.scheme!='https' or url.netloc!='mathacademy.com' or not match or url.fragment or
            set(query)-{'unitId'} or ('unitId' in query and
            (len(query['unitId'])!=1 or not re.fullmatch(r'[1-9]\d*',query['unitId'][0])))):
        raise ValueError('Expected a Math Academy course progress URL with optional unitId: '+str(value))
    source='https://mathacademy.com'+url.path
    result={'course_id':int(match[1]),'source_url':source}
    if 'unitId' in query:
        result['selected_unit_id']=int(query['unitId'][0])
        result['source_url']+='?unitId='+query['unitId'][0]
    return result


def targets(args,state=None):
    state=state or {}
    return tuple(state.get('progress_urls') or state.get('progress_course_ids') or
                 getattr(args,'progress_urls',None) or getattr(args,'progress_course_ids',COURSES))


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


def capture(reader, directory, event, task_id, course_ids=COURSES, previous=None, recovered=False, *, start_url=None):
    directory = Path(directory)
    snapshot = {'event': event, 'task_id': task_id, 'started_at': now(),
                'recovered_after_interruption': recovered,
                'scope': 'course-progress display colors',
                'mapping': 'White=0; blue bands=1-6; darkest=6 is a local initialization convention',
                'limitations': 'Not exact continuous repetitions, memory, intervals, ability, or complete internal MA state. Courses are read sequentially.',
                'courses': []}
    loaded=None
    if course_ids is None:
        # The sequence sidebar is on Learn; individual progress pages omit it.
        discovery_url='https://mathacademy.com/learn'
        reader.navigate(discovery_url, force=True)
        reader.page.locator('a#courseNameLink, a.courseNameLink').first.wait_for(state='attached')
        observed=reader.page.evaluate(EXTRACT_SIDEBAR)
        course_ids=sidebar_courses(observed) or [target(start_url)['source_url']]
        snapshot['scope_source']='account sidebar'
        snapshot['sidebar_html']=observed.get('html')
        snapshot['discovery_start_url']=discovery_url
    for value in course_ids:
        scope=target(value)
        course_id=scope['course_id'];url=scope['source_url']
        started = now()
        if url!=loaded:reader.navigate(url, force=True)
        loaded=None
        reader.page.locator('.moduleTopics .topicLink').first.wait_for(state='attached')
        reader.page.wait_for_timeout(reader.args.settle_ms)
        reader.check()
        observed = reader.page.evaluate(EXTRACT_PROGRESS)
        topics = normalize_course(course_id, observed)
        course = {**scope, 'started_at': started,
                  'captured_at': now(), 'topics': topics, 'units_html': observed['units_html']}
        snapshot['courses'].append(course)
    snapshot['finished_at'] = now()
    snapshot['changes'] = changes(previous, snapshot) if previous else []
    snapshot['comparison_available'] = previous is not None
    # The complete file is published only after every requested course validates.
    atomic_json(directory / (event + '.json'), snapshot)
    return snapshot
