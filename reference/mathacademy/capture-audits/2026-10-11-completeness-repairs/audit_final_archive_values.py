"""Compare final authored records with their normal pinned import readbacks."""
from pathlib import Path
import hashlib, json
from scripts.config import Config
from scripts.storage import atomic_json, read_json
from scripts.database.edn import loads
from scripts.database.evidence import authoritative_question
from scripts.database.images import ImageLibrary
from scripts.database.text import markdown

ROOT = Path(__file__).resolve().parent
rows = []
def ident(value):
    return str(value.get(':db/ident', '') if isinstance(value, dict) else value).rsplit('/', 1)[-1]
for candidate in read_json(ROOT/'literal-brace-final-apply-candidates.json'):
    directory = Path(candidate['directory']).parents[1]
    content = read_json(directory/'content.json')
    result = read_json(directory/'database/result.json')
    basis = result['basis']
    observed = {}
    def collect(value):
        if isinstance(value, dict):
            if value.get(':question/math-academy-id'):
                observed[value[':question/math-academy-id']] = value
            for child in value.values(): collect(child)
        elif isinstance(value, list):
            for child in value: collect(child)
    for path in (directory/'database'/f'snapshot-{basis}').glob('questions-*.edn'):
        if '-inputs' not in path.name and '-query' not in path.name:
            collect(loads(path.read_text()))
    library = ImageLibrary(Config(account=candidate['account']).math_root, directory)
    checks = []
    for bucket in ['questions', 'canonical_examples']:
        for original in content.get(bucket, []):
            record = {'id': original.get('math_academy_id'), 'bucket': bucket}
            try:
                question = library.question(authoritative_question(original, example=bucket=='canonical_examples'))
                db = observed[record['id']]
                record['text'] = {key: markdown(question.get(key, ''))==db.get(':question/'+key.replace('_', '-'), '')
                                  for key in ['problem', 'worked_solution']}
                actual = {field[':answer-field/key']: field for field in db.get(':question/answer-fields', [])}
                fields = []
                for field in question.get('answer_fields', []):
                    pinned = actual.get(field['key'], {})
                    wanted = {(choice['type'], choice['value']) for choice in field['choices']}
                    choices = {(ident(choice.get(':answer/type')), choice.get(':answer/value'))
                               for choice in pinned.get(':answer-field/choices', [])}
                    correct = pinned.get(':answer-field/correct', {})
                    fields.append({'key': field['key'], 'type': ident(pinned.get(':answer-field/type'))==field['type'],
                                   'choices': wanted<=choices if field['type']=='blank' else wanted==choices,
                                   'correct': (ident(correct.get(':answer/type')), correct.get(':answer/value'))==
                                              (field['correct_type'], field['correct_value'])})
                record['fields'] = fields
                record['matches'] = all(record['text'].values()) and all(all(f[k] for k in ['type','choices','correct']) for f in fields)
            except Exception as error:
                record.update(matches=False, error=str(error))
            checks.append(record)
    rows.append({'account': candidate['account'], 'task_id': directory.name, 'basis': basis,
                 'terminal': result.get('status') in ('verified','no_changes'), 'omissions': result.get('omissions', []),
                 'records': checks, 'all_values_match': all(r['matches'] for r in checks)})
output = {'text_sha256': hashlib.sha256(Path(markdown.__code__.co_filename).read_bytes()).hexdigest(),
          'captures': rows, 'all_values_match': all(r['terminal'] and not r['omissions'] and r['all_values_match'] for r in rows)}
atomic_json(ROOT/'final-archive-authored-pinned-values.json', output)
print(json.dumps({'captures': len(rows), 'all_values_match': output['all_values_match'],
                  'failures': [{'task_id': r['task_id'], 'records': [v for v in r['records'] if not v['matches']]} for r in rows if not r['all_values_match']]}))
