"""Current enrollment as displayed by Math Academy, independent of account keys."""
import re
import time
from .storage import atomic_json, read_json


def parse_current_course(html):
    from bs4 import BeautifulSoup
    page = BeautifulSoup(html, 'html.parser')
    link = page.select_one('a#courseNameLink[href], a.courseNameLink[href]')
    match = re.search(r'/courses/(\d+)(?:/|$|\?)', link.get('href', '')) if link else None
    name = link.get_text(' ', strip=True) if link else ''
    if match and name:
        return {'course_id': match[1], 'course_name': name}
    return {}


def record_current_course(config, html, source_url=None):
    course = parse_current_course(html)
    if course:
        course.update(observed_at=time.time(), source_url=source_url)
        atomic_json(config.state_root / 'current-course.json', course)
        config.course_id = course['course_id']
    return course


def current_course(config):
    try:
        value = read_json(config.state_root / 'current-course.json', {})
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError, UnicodeError):
        return {}


def course_label(config):
    return current_course(config).get('course_name') or 'Account: ' + config.account
