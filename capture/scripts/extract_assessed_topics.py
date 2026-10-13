"""Freeze explicitly assessed topic IDs from saved question metadata and headers."""
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re


class TopicHeader(HTMLParser):
    def __init__(self):
        super().__init__()
        self.topics = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'a' and 'questionKP' in a.get('class', '').split():
            match = re.search(r'/topics/(\d+)(?:#|\?|$)', a.get('href', ''))
            if match:
                self.topics.add(match[1])


def extract(question):
    candidates = set()
    for node in (question, question.get('content', {}), question.get('history', {}),
                 question.get('before', {}), question.get('after', {})):
        topic = str(node.get('topic_id', ''))
        if topic.isdigit():
            candidates.add(topic)
        parser = TopicHeader()
        parser.feed(node.get('html', '') or node.get('raw_html', '') or '')
        candidates.update(parser.topics)
    return sorted(candidates)


def main():
    folder = Path('reference/mathacademy/encompassing-analysis-2026-10-11')
    output = {'method': 'Explicit numeric topic_id or questionKP header link; conflicting or missing identities remain unresolved.',
              'source_sha256': {}, 'accounts': {}}
    for account in ('foundations', 'linear', 'multivariable', 'differential'):
        report = json.loads((folder/(account+'.json')).read_text())
        tasks = {}
        for audit in report['activity_audit']:
            if audit['kind'] not in ('assessment', 'multistep'):
                continue
            path = Path(audit['path'])
            path = path.parent/'content.json' if audit['pipeline']=='current' else path.parents[1]/'state.json'
            raw = path.read_bytes()
            output['source_sha256'][str(path)] = hashlib.sha256(raw).hexdigest()
            data = json.loads(raw)
            qs = data.get('questions', [])
            qs = list(qs.values()) if isinstance(qs, dict) else qs
            questions = []
            for q in qs:
                ids = extract(q)
                questions.append({'question': q.get('math_academy_id') or q.get('dom_id') or q.get('before', {}).get('dom_id'),
                                  'topic': ids[0] if len(ids)==1 else None,
                                  'candidate_topics': ids,
                                  'grade': q.get('actual_result') or q.get('grade') or q.get('result') or q.get('history', {}).get('result')})
            tasks[audit['task_id']] = {'kind': audit['kind'], 'source': str(path), 'questions': questions,
                                       'topics': sorted({q['topic'] for q in questions if q['topic']}),
                                       'unresolved_questions': sum(q['topic'] is None for q in questions)}
        output['accounts'][account] = tasks
        print(account, 'tasks', len(tasks), 'questions', sum(len(t['questions']) for t in tasks.values()),
              'unresolved', sum(t['unresolved_questions'] for t in tasks.values()))
    output['script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (folder/'restoration-analysis/assessment-topics.json').write_text(json.dumps(output, indent=2)+'\n')


if __name__ == '__main__':
    main()
