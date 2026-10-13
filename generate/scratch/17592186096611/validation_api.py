"""Frozen mathematical QA plus current native grading input; scoped to this KP."""
import importlib.util
from pathlib import Path
import copy, json
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('mathematical_validation', HERE/'validate.py')
v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
g = v.g
cases = json.loads((HERE/'source-cases.json').read_text())
native = []

def validate(rec):
    assert rec['knowledge_point']['db_id'] == g.KP_ID
    assert rec['knowledge_point']['id'] == g.KP_UUID
    gen = rec['generation']
    assert gen['version'] == g.VERSION
    expected = g.generate(rec['question'][':question/difficulty'].split('/')[-1], gen['seed'], gen['template'], parameters=gen['parameters'], profile=gen['profile'])
    def ordered(q):
        q = copy.deepcopy(q)
        for f in q[':question/answer-fields']:
            f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
        return q
    assert ordered(expected['question']) == ordered(rec['question'])
    assert expected['generation']['math_fingerprint'] == gen['math_fingerprint']
    v.check_record(rec)
    fld=rec['question'][':question/answer-fields'][0]
    if fld[':answer-field/type'].endswith('/radio'):
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==fld[':answer-field/correct'][1] else 'rejected','purpose':'Owned radio choice native designation'} for a in fld[':answer-field/choices']]
    else:
        correct=next(a for a in fld[':answer-field/choices'] if a[':answer/id']==fld[':answer-field/correct'][1])
        checks=[{'submitted':correct[':answer/value'],'expected':'accepted','purpose':'Canonical fragment'}, {'submitted':v.equivalent_entry(rec),'expected':'accepted','purpose':'Independently unreduced equivalent'}, {'submitted':g.sp.latex(v.displayed_reference(rec)[2]+1),'expected':'rejected','purpose':'Incorrect fragment'}]
    native.append({'label':rec['question'][':question/id'],'record':rec,'checks':checks})
