"""Read-only candidate finder; a notation difference is not a proven defect."""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import re

FUNCTIONS = r'sin|cos|tan|sec|csc|cot|sinh|cosh|tanh|ln|log'


def normalize(text):
    text = re.sub(r'\\operatorname\{(' + FUNCTIONS + r')\}', r'\\\1 ', text)
    text = re.sub(r'\{(' + FUNCTIONS + r')\}', r'\\\1 ', text)
    return text.replace('\u2061', '').replace(r'\left', '').replace(r'\right', '')


def calls(text):
    """Read visible trig arguments, including bare source notation sin 2t."""
    text = normalize(text)

    def atom(i):
        while i < len(text) and text[i].isspace():
            i += 1
        start = i
        if i == len(text):
            return '', i
        if text[i] in '({[':
            close = {'(': ')', '{': '}', '[': ']'}[text[i]]
            depth = 1
            i += 1
            while i < len(text) and depth:
                depth += (text[i] == text[start]) - (text[i] == close)
                i += 1
        else:
            m = re.match(r'\\[A-Za-z]+|\d+|[A-Za-z]', text[i:])
            if not m:
                return '', i
            i += len(m[0])
        return text[start:i], i

    result = []
    for match in re.finditer(r'\\(' + FUNCTIONS + r')\b\s*', text):
        i = match.end()
        if i < len(text) and text[i] == '^':
            _, i = atom(i + 1)  # Function power, distinct from argument power.
        argument, end = atom(i)
        if not argument:
            continue
        if argument.isdigit():
            other, end = atom(end)
            argument += other
        if end < len(text) and text[end] == '^' and not argument.startswith('('):
            power, end = atom(end + 1)
            argument += '^' + power
        argument = re.sub(r'[\s{}]', '', argument)
        while argument.startswith('(') and argument.endswith(')'):
            depth = 0
            for pos, char in enumerate(argument):
                depth += (char == '(') - (char == ')')
                if depth == 0:
                    break
            if pos != len(argument) - 1:
                break
            argument = argument[1:-1]
        result.append((match[1], argument))
    return result


def candidates(entities):
    owners = defaultdict(list)
    for eid, record in entities.items():
        for question in record.get('knowledge-point/questions', []) + record.get('knowledge-point/canonical-example', []):
            owners[str(question)].append({'kp': int(eid), 'title': record.get('knowledge-point/title', [''])[0]})
    found = []
    questions = generated = 0
    for eid, question in entities.items():
        if 'question/problem' not in question:
            continue
        questions += 1
        generated += not bool(question.get('question/math-academy-id'))
        solution = question.get('question/worked-solution', [''])[0]
        solution_calls = calls(solution)
        for fid in question.get('question/answer-fields', []):
            field = entities[str(fid)]
            for aid in field.get('answer-field/correct', []):
                answer = entities[str(aid)].get('answer/value', [''])[0]
                missing = [call for call in calls(answer) if call not in solution_calls]
                if missing and solution:
                    found.append({'question': int(eid), 'answer_entity': aid,
                        'source': question.get('question/math-academy-id'), 'owners': owners[eid],
                        'prompt': question['question/problem'][0], 'answer': answer,
                        'solution': solution, 'unmatched': missing, 'solution_calls': solution_calls})
    return {'questions_scanned': questions, 'without_source_id': generated,
            'candidate_count': len(found), 'candidates': found,
            'limitations': ['Heuristic candidate discovery, not prerequisite or mathematical certification.',
                           'Only keyed answers with nonempty worked solutions and recognized function notation.',
                           'No automatic repair; candidate differences require contextual review.']}


def snapshot_index(path):
    """Accept the project's current-value JSONL exports without querying storage."""
    attributes = {'knowledge-point/title', 'knowledge-point/questions', 'knowledge-point/canonical-example',
                  'question/problem', 'question/worked-solution', 'question/math-academy-id',
                  'question/answer-fields', 'answer-field/correct', 'answer/value'}
    entities = defaultdict(lambda: defaultdict(list))
    with path.open() as stream:
        for line in stream:
            row = json.loads(line)
            if row['a'] not in attributes:
                continue
            value = row['v'] if 'v' in row else row['ref_eid'] if row.get('ref_eid') is not None else row['raw_string']
            entities[str(row['e'])][row['a']].append(value)
    return entities


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--index', type=Path)
    source.add_argument('--snapshot', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    entities = json.loads(args.index.read_text()) if args.index else snapshot_index(args.snapshot)
    report = candidates(entities)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'candidates'}))
