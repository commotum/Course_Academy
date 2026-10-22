#!/usr/bin/env python3
"""Prepare the single native-grader batch and three affected UI cases."""
import json
import validate as v


def main():
    records = json.loads((v.OUT/'single-witness-records.json').read_text())
    cases = json.loads((v.OUT/'grader-input.json').read_text())
    for i,r in enumerate(records):
        q = r['question']; expected = v.expected(v.matrix(q[':question/problem']))
        cases.append({'label': 'sparse-'+str(i), 'record': r, 'checks': [
            {'field_index': 0, 'submitted_answer_id': a[':answer/id'],
             'expected': 'accepted' if a[':answer/value'] == expected else 'rejected',
             'purpose': 'canonical and moved single-witness classification'}
            for a in q[':question/answer-fields'][0][':answer-field/choices']]})
    v.save('grader-all-input.json', cases)
    v.save('render-input.json', [records[0], records[1], records[-2]])
    print(json.dumps({'native_grader_cases': len(cases), 'render_cases': 3}))


if __name__ == '__main__': main()
