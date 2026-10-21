"""Run the native learner grader and the unchanged learner rendering UI."""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]

def enum(value):
    return str(value.get(':db/ident') if isinstance(value, dict) else value).split('/')[-1]

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

if sys.argv[1] == 'grade':
    records = json.loads((HERE / 'grading-records.json').read_text())
    questions = []
    for record in records:
        q = record['question']
        fields = []
        for f in q[':question/answer-fields']:
            ref = f[':answer-field/correct']
            aid = ref[':answer/id'] if isinstance(ref, dict) else ref[1]
            correct = next(a for a in f[':answer-field/choices'] if a[':answer/id'] == aid)
            fields.append({'key': f[':answer-field/key'], 'type': enum(f[':answer-field/type']),
                           'correct_value': correct[':answer/value'],
                           'choices': [{'type': enum(a[':answer/type']), 'value': a[':answer/value']}
                                       for a in f[':answer-field/choices']]})
        questions.append({'math_academy_id': q[':question/id'], 'problem': q[':question/problem'],
                          'knowledge_point': 'Systems of Linear Equations', 'answer_fields': fields})
    out = HERE / 'native-grading'
    out.mkdir(exist_ok=True)
    (out / 'questions.json').write_text(json.dumps({'questions': questions}) + '\n')
    grader = load('historical_grader', ROOT / 'scripts/prepare_historical_questions.py')
    result = grader.runtime_check(out)
    assert result['current_engine_ready_count'] == len(questions)
    print(json.dumps({'passed': True, 'questions': len(questions), 'database_writes': 0}))
elif sys.argv[1] == 'render':
    renderer = load('learner_renderer', ROOT / 'generate/pipeline/render_preview.py')
    config = json.loads((ROOT / 'reference/mathacademy/repairs/2026-10-19-fraction-fences-corpus/generator-ui/browser-config.json').read_text())
    records = json.loads((HERE / 'render-records.json').read_text())
    renderer.render(records, HERE / 'ui', [ROOT, '/'], config['browser'], config['playwright'], config['node'])
else:
    raise ValueError('Choose grade or render')
