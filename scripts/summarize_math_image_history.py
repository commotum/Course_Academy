#!/usr/bin/env python3
"""Bind math-image findings to retained history and archived lesson identities.

Older text is a recovery candidate, not an automatically approved replacement:
later mathematical or editorial corrections can make wholesale rollback wrong.
"""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re


def summarize(findings_path, history_path, output, lessons):
    findings = json.loads(findings_path.read_text())
    grouped = defaultdict(list)
    with history_path.open() as stream:
        for line in stream:
            row = json.loads(line)
            if row['added']:
                grouped[row['e'], row['a']].append(row)
    cache, recovery, introductions = {}, [], Counter()
    for f in findings:
        history = sorted(grouped[f['e'], f['a']], key=lambda row: row['t'])
        earlier = [r for r in history if r['t'] < f['t'] and '$' in r['v']
                   and not re.search(r'images/|<img\b|<svg\b', r['v'])]
        image_history = [r for r in history if 'images/' in r['v']]
        first = image_history[0] if image_history else None
        if first:
            introductions[first['t']] += 1
        own = next(c for c in f['context'] if c['entity'] == f['e'])
        topics = [c for c in f['context'] if 'topic/math-academy-id' in c]
        cid = str(own.get('tutorial/math-academy-id', own.get('question/math-academy-id', ''))).removeprefix('e-')
        kind = 'tutorial' if 'tutorial/id' in own else 'example'
        archived = []
        for topic in topics:
            mid = topic['topic/math-academy-id']
            path = lessons / str(mid) / 'Source' / f'{mid}.json'
            if path not in cache:
                cache[path] = json.loads(path.read_text()) if path.is_file() else None
            source = cache[path]
            if source:
                for item in source['lesson']['items']:
                    if item.get('step_type') == kind and str(item.get('content_id')) == cid:
                        archived.append({'json':str(path), 'html':str(path.with_suffix('.html')),
                            'markdown':str(path.parent.parent / f'{mid}.md'),
                            'step_id':item['step_id'], 'content_id':cid, 'step_type':kind})
        recovery.append({'entity':f['e'], 'attribute':f['a'], 'current_value_sha256':f['value_sha256'],
            'current_t':f['t'], 'current_source':f['source'],
            'first_retained_image_assertion':first,
            'latest_prior_image_free_math':earlier[-1] if earlier else None,
            'matching_archived_lesson_sources':archived,
            'status':'history-and-archive' if earlier and archived else 'history-candidate' if earlier
                else 'archive-source' if archived else 'needs-source-recovery'})
    counts = Counter(r['status'] for r in recovery)
    summary = {'affected_attributes':len(recovery), 'recovery_by_status':dict(counts),
        'attributes_with_prior_image_free_math':sum(r['latest_prior_image_free_math'] is not None for r in recovery),
        'attributes_with_matching_archived_lesson_content':sum(bool(r['matching_archived_lesson_sources']) for r in recovery),
        'first_retained_image_assertion_by_t':dict(sorted(introductions.items())),
        'warning':'Earlier whole-field text requires source comparison; do not overwrite later corrections blindly.'}
    output.mkdir(parents=True,exist_ok=True)
    (output/'recovery-candidates.json').write_text(json.dumps(recovery,indent=2,ensure_ascii=False)+'\n')
    (output/'recovery-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k!='first_retained_image_assertion_by_t'},indent=2))


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('findings',type=Path);p.add_argument('history',type=Path);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--lessons',type=Path,default=Path('/home/jake/Developer/MA/DATA/Lessons'))
    a=p.parse_args();summarize(a.findings,a.history,a.output,a.lessons)
