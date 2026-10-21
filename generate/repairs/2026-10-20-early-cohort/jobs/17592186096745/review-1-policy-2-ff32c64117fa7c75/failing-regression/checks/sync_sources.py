"""Build-time capture sync; runtime reads only its bundled source snapshot.

Iterate every supplied assessed case, preserving equivalent existing captures.
This script is not a regression (it deliberately updates the runtime snapshot).
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=ROOT.parent / 'source/source.json')
    args = parser.parse_args()
    source = json.loads(args.source.read_text())
    target = ROOT / 'source-data.json'
    old = json.loads(target.read_text())
    old_by_id = {q[':question/id']: q for q in old['questions']}
    supplied = source['material']['kp'][':knowledge-point/questions']
    # Only q-74629 has a capture presentation difference: (-1/4) versus
    # \left(-1/4\right). Preserve the completed formatter repair in the snapshot.
    def normalized(q):
        value = json.loads(json.dumps(q))
        value[':question/worked-solution'] = value[':question/worked-solution'].replace(r'\left(', '(').replace(r'\right)', ')')
        return value
    result = []
    for question in supplied:
        prior = old_by_id.get(question[':question/id'])
        if prior is not None:
            assert normalized(prior) == normalized(question), f'Changed source needs review: {question[":question/id"]}'
        result.append(prior if prior is not None else question)
    assert len({q[':question/math-academy-id'] for q in result}) == len(supplied)
    target.write_text(json.dumps({'basis': source['basis'],
                                 'kp_title': source['material']['kp'][':knowledge-point/title'],
                                 'questions': result}, indent=2) + '\n')
    print(json.dumps({'before': len(old['questions']), 'after': len(result),
                      'retained': len(old_by_id), 'basis': source['basis']}))


if __name__ == '__main__':
    main()
