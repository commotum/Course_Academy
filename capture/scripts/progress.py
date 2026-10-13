"""Course-qualified display-color observations, never exact FIRe proficiency."""
import re


PALETTE = {
    (255, 255, 255): 0,
    (210, 231, 249): 1,
    (165, 207, 243): 2,
    (120, 182, 237): 3,
    (74, 158, 232): 4,
    (29, 134, 226): 5,
    (23, 107, 181): 6,
}
LIMITATIONS = ('Display colors and local bands are observations, not exact FIRe repetitions, '
              'memory, intervals, ability, or proficiency. Unchanged bands do not establish '
              'unchanged internal state. Courses are read sequentially; late reads can include '
              'changes after the activity completed.')


def style_color(style):
    """Retain the authored background value, respecting declaration precedence."""
    selected, important = None, False
    for declaration in str(style or '').split(';'):
        name, separator, value = declaration.partition(':')
        if not separator or name.strip().lower() not in ('background', 'background-color'):
            continue
        value = value.strip()
        priority = bool(re.search(r'!\s*important\s*$', value, re.I))
        if priority or not important:
            selected, important = value, priority
    return selected


def color_observation(topic):
    color = topic.get('color')
    if color is None:
        color = style_color(topic.get('circle_style'))
    value = re.sub(r'!\s*important\s*$', '', str(color or ''), flags=re.I).strip().lower()
    rgb = None
    if value == 'white':
        rgb = (255, 255, 255)
    match = re.fullmatch(r'rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', value)
    if match:
        rgb = tuple(map(int, match.groups()))
    elif re.fullmatch(r'#[0-9a-f]{3}(?:[0-9a-f]{3})?', value):
        digits = value[1:]
        if len(digits) == 3:
            digits = ''.join(char * 2 for char in digits)
        rgb = tuple(int(digits[index:index + 2], 16) for index in (0, 2, 4))
    band = PALETTE.get(rgb)
    return {'color': color, 'display_band': band,
            'color_status': 'known' if band is not None else 'unknown' if value else 'missing'}


def _index(snapshot):
    courses = snapshot.get('progress') or snapshot.get('courses') or []
    if not isinstance(courses, list):
        return {}, []
    rows, duplicates, issues = {}, set(), []
    for course in courses:
        if not isinstance(course, dict) or course.get('course_id') is None:
            continue
        issues.extend({**issue, 'course_id': str(course['course_id'])}
                      for issue in course.get('parse_issues', []) if isinstance(issue, dict))
        observed_at = course.get('captured_at')
        if observed_at is None:
            observed_at = course.get('observed_at', snapshot.get('observed_at'))
        for topic in course.get('topics') or []:
            if not isinstance(topic, dict) or topic.get('topic_id') is None:
                continue
            key = (str(course['course_id']), str(topic['topic_id']))
            if key in rows:
                duplicates.add(key)
            rows[key] = {**topic, **color_observation(topic),
                         'observed_at': observed_at}
    for key in duplicates:
        rows.pop(key, None)
    return rows, issues + [{'course_id': course, 'topic_id': topic, 'reason': 'duplicate_topic_identity'}
                          for course, topic in sorted(duplicates)]


def compare_progress(baseline, observation, *, activity_kind=None):
    """Compare only source topics present in both reads; absences are not losses."""
    before, before_issues = _index(baseline)
    after, after_issues = _index(observation)
    result = {'scope': 'course-qualified topic display colors',
              'mapping': 'White=0; known blue bands=1–6; darkest=6 is a local display convention',
              'limitations': LIMITATIONS,
              'baseline_observed_at': baseline.get('observed_at'),
              'observed_at': observation.get('observed_at'),
              'late_read': bool(observation.get('late_read')),
              'comparison_available': False, 'compared_topic_count': 0, 'changes': [],
              'uncompared_topics': ([{**item, 'side': 'baseline'} for item in before_issues]
                                    + [{**item, 'side': 'current'} for item in after_issues])}
    for key in sorted(before.keys() | after.keys()):
        identity = {'course_id': key[0], 'topic_id': key[1]}
        if key not in before or key not in after:
            result['uncompared_topics'].append({**identity,
                'reason': 'missing_in_baseline' if key not in before else 'missing_in_current'})
            continue
        old, new = before[key], after[key]
        if old['color_status'] == 'missing' or new['color_status'] == 'missing':
            result['uncompared_topics'].append({**identity, 'reason': 'missing_color',
                'before_color': old['color'], 'after_color': new['color']})
            continue
        result['compared_topic_count'] += 1
        # Equivalent known RGB/hex/white spellings denote the same display band.
        same = old['display_band'] == new['display_band'] if (
            old['color_status'] == new['color_status'] == 'known') else old['color'] == new['color']
        if not same:
            result['changes'].append({**identity, 'title': new.get('title') or old.get('title'),
                'before_color': old['color'], 'after_color': new['color'],
                'before_band': old['display_band'], 'after_band': new['display_band'],
                'before_color_status': old['color_status'], 'after_color_status': new['color_status'],
                'before_observed_at': old['observed_at'], 'after_observed_at': new['observed_at']})
    result['comparison_available'] = result['compared_topic_count'] > 0
    if not result['comparison_available']:
        result['unavailable_reason'] = ('no_baseline_topics' if not before else
                                        'no_current_topics' if not after else 'no_comparable_topic_colors')
    result['anomalies'] = []
    elapsed = (observation.get('observed_at') or 0) - (baseline.get('observed_at') or 0)
    prior_percentage = baseline.get('dashboard_course_progress',{})
    current_percentage = observation.get('dashboard',{}).get('course_progress',{})
    def percentage(value):
        match = re.fullmatch(r'\s*(\d+(?:\.\d+)?)\s*%\s*',str(value.get('displayed_progress') or ''))
        return float(match[1]) if match else None
    previous, current = percentage(prior_percentage),percentage(current_percentage)
    if activity_kind in ('lesson','review','multistep') and 0 <= elapsed <= 3600:
        for course in sorted({key[0] for key in before.keys() & after.keys()}):
            compared = sum(key[0] == course for key in before.keys() & after.keys())
            changes = [change for change in result['changes'] if change['course_id'] == course]
            # Generalization can legitimately change many prerequisite colors.
            # Flag the combined abrupt percentage/color switch for this same
            # enrolled course, rather than assuming every large propagation is bad.
            if (str(prior_percentage.get('course_id')) == str(current_percentage.get('course_id')) == course
                    and previous is not None and current is not None and abs(current-previous)>=20
                    and len(changes) >= 50 and len(changes) >= compared * .25):
                result['anomalies'].append({'course_id':course,'changed_topics':len(changes),
                    'compared_topics':compared,'elapsed_seconds':elapsed,
                    'previous_percentage':previous,'current_percentage':current,
                    'reason':'Abrupt Math Academy percentage switch with widespread topic-color changes'})
    result['attribution_available'] = result['comparison_available'] and not result['anomalies'] and not result['late_read']
    return result
