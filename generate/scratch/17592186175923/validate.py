"""Independently read rendered lines, all worked steps, and native grading."""
import hashlib
import importlib.util
import json
import re
import subprocess
from pathlib import Path
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec); spec.loader.exec_module(value)
    return value
g = module('perpendicular_generator', HERE.with_suffix('.py'))
reader = module('perpendicular_math', HERE/'math_parser.py')

def save(name, value):
    (HERE/name).write_text(json.dumps(value, indent=2, default=str)+'\n')

def parse(problem):
    coordinates = re.findall(r'\$\((-?\d+),\s*(-?\d+)\)', problem)
    if len(coordinates) != 3:
        raise ValueError('A referenced diagram or reference coordinates are missing')
    p, a, b = [sp.Matrix(list(map(int,z))) for z in coordinates]
    direction = b-a
    if direction[0] == 0 or direction[1] == 0:
        raise ValueError('Unsupported axis-parallel reference')
    # Reference direction is a normal of the required line.
    m = -direction[0]/direction[1]
    intercept = p[1]-m*p[0]
    return p, a, b, m, intercept

def fingerprint(problem):
    _, _, _, m, b = parse(problem)
    return g.digest({'slope': str(m), 'intercept': str(b)})

def scalar(text):
    text = text.strip().rstrip('.,').replace(r'\dfrac', r'\frac').replace(r'\text', '')
    return reader.scalar(text)

def bank_check(q):
    p, a, b, m, intercept = parse(q[':question/problem'])
    fields = q[':question/answer-fields']; assert len(fields) == 1
    field = fields[0]; correct = field[':answer-field/correct']
    cid = str(correct[':answer/id']) if isinstance(correct,dict) else correct[1]
    ftype = field[':answer-field/type']
    ftype = ftype[':db/ident'] if isinstance(ftype,dict) else ftype
    choices = field[':answer-field/choices']
    assert len(choices) == (1 if ftype.endswith('/blank') else 5)
    target = reader.y-m*reader.x-intercept
    valid = []
    objects = []
    for option in choices:
        value = option[':answer/value']
        if ftype.endswith('/blank'):
            assert '=' not in value and field[':answer-field/key'] == 'field-1'
            obj = reader.y-scalar(value)
        else:
            left, right = value.split('='); obj = scalar(left)-scalar(right)
        objects.append(obj)
        # Complete equations, normalized by their y coefficient.
        coefficient = sp.expand(obj).coeff(reader.y)
        valid.append(coefficient != 0 and sp.simplify(obj/coefficient-target) == 0)
    assert sum(valid) == 1
    assert str(choices[valid.index(True)][':answer/id']) == cid
    assert len({str(sp.expand(z/z.coeff(reader.y))) for z in objects}) == len(objects)
    return p, a, b, m, intercept

def solution_check(q):
    p, a, b, m, intercept = bank_check(q)
    reference = (b[1]-a[1])/(b[0]-a[0])
    solution = q[':question/worked-solution']
    blocks = re.findall(r'\$\$\n(.*?)\n\$\$', solution, re.S)
    assert len(blocks) == 3
    first = blocks[0].split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0].split(r'\\')
    for row in first[1:]:
        right = row.split('=')[1]
        assert sp.simplify(scalar(right)-reference) == 0, ('Incorrect slope step',row)
    middle = blocks[1]
    displayed_slopes = re.findall(r'\((.*?)\)', middle)
    assert len(displayed_slopes) == 1 and scalar(displayed_slopes[0]) == reference
    assert m*reference == -1
    assert scalar(middle.split('m=')[-1]) == m
    assert '=-1' in middle.replace(' ','')
    last = blocks[2].split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0].split(r'\\')
    for row in last[1:]:
        left, right = row.replace('&','').split('=')
        assert sp.simplify(scalar(left)-scalar(right)-(reader.y-m*reader.x-intercept)) == 0, ('Incorrect equation step',row)
    # Prose coordinates agree with the prompt in A,B,P order.
    prose = re.findall(r'\((-?\d+),\s*(-?\d+)\)', solution)
    assert [list(map(int,z)) for z in prose] == [list(a),list(b),list(p)]
    return {'slope_rows':len(first)-1,'point_slope_rows':len(last)-1}

def independent(rec):
    q = rec['question']; solution_check(q)
    assert fingerprint(q[':question/problem']) == rec['generation']['parameter_fingerprint']
    assert q[':question/difficulty'].split('/')[-1] in g.SUPPORTED_LEVELS
    field = q[':question/answer-fields'][0]
    assert field[':answer-field/type'] == ':answer-field.type/blank'
    assert q[':question/problem'].count('{{field-1}}') == 1
    assert ':question/math-academy-id' not in q
    assert len({q[':question/id'],field[':answer-field/id'],field[':answer-field/choices'][0][':answer/id']}) == 3

def checks(rec):
    q = rec['question']; _, _, _, m, b = parse(q[':question/problem'])
    correct = q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']
    mn,md = m.as_numer_denom(); bn,bd = b.as_numer_denom()
    return [{'submitted':correct,'expected':'accepted','purpose':'Canonical RHS'},
            {'submitted':f'({mn}/{md})*x+({bn}/{bd})','expected':'accepted','purpose':'Equivalent explicit rational form'},
            {'submitted':g.tex(sp.factor(m*g.X+b)),'expected':'accepted','purpose':'Equivalent factored RHS'},
            {'submitted':g.tex(m*g.X+b+1),'expected':'rejected','purpose':'Wrong intercept'},
            {'submitted':g.tex(-m*g.X+b),'expected':'rejected','purpose':'Wrong slope sign'}]

def main():
    replay = []; records = []
    for mid, level in g.TEMPLATES.items():
        original = g.SOURCES[mid]
        solution_check(original)
        rec = g.generate(level,template=mid,parameters=g.source_parameters(mid))
        independent(rec)
        original_values = [a[':answer/value'] for a in original[':question/answer-fields'][0][':answer-field/choices']]
        generated_values = [a[':answer/value'] for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']]
        assert all(sp.simplify(scalar(a)-scalar(b)) == 0 for a,b in zip(original_values,generated_values))
        assert rec['question'][':question/problem'] == original[':question/problem']
        # Preserve source prose and sequence, report notation separately.
        before = re.sub(r'\$\$.*?\$\$', '',original[':question/worked-solution'],flags=re.S)
        after = re.sub(r'\$\$.*?\$\$', '',rec['question'][':question/worked-solution'],flags=re.S)
        assert before == after
        replay.append({'source':mid,'matched_values':1,'total_values':1,'complete_bank':True,
                       'prompt_exact':True,'prose_exact':True,'solution_sequence_preserved':True,
                       'solution_notation_exact':rec['question'][':question/worked-solution']==original[':question/worked-solution'],
                       'distractors':0,'source':mid})
        records.append(rec)
    for mid, level in g.TEMPLATES.items():
        for rec in g.batch(level,40,seed=1966,template=mid):
            independent(rec); records.append(rec)
    # Boundary/sign/zero tests, with every source layout exercised.
    for mid,level in g.TEMPLATES.items():
        for py in (-8,0,8):
            for ax,ay,bx,by in ((-8,-8,8,8),(8,8,-8,-8),(-8,8,8,-8),(8,-8,-8,8)):
                for px in ([0] if level=='easy' else [-8,8]):
                    rec=g.generate(level,template=mid,parameters={'P':[px,py],'A':[ax,ay],'B':[bx,by]})
                    independent(rec); records.append(rec)
    native = [{'label':str(i),'record':r,'checks':checks(r)} for i,r in enumerate(records)]
    save('engine-input.json',native)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    engine = json.loads((HERE/'engine-report.json').read_text()); assert engine['documented_unresolved_checks']==0
    for level in g.SUPPORTED_LEVELS:
        assert g.batch(level,10,178)==g.batch(level,10,178)
        assert len({r['generation']['parameter_fingerprint'] for r in g.batch(level,100,178)})==100
    a={'P':[0,1],'A':[0,0],'B':[2,3]}; b={'P':[0,1],'A':[1,1],'B':[3,4]}
    assert g.task_key(a)==g.task_key(b)
    try:g.generate('hard')
    except ValueError:pass
    else:raise AssertionError('Hard must remain unsupported')
    save('source-replay.json',{'supported_complete_banks':4,'matched_complete_banks':4,'matched_answers':4,'source_answers':4,'distractors':0,'cases':replay,'excluded_banks':'See choice-ledger.json; no radio profile is claimed supported'})
    previews=[g.generate(level,seed=88+i) for i in range(3) for level in g.SUPPORTED_LEVELS]
    (HERE/'review.md').write_text('\n\n---\n\n'.join(['Original '+mid+'\n\n'+g.SOURCES[mid][':question/problem']+'\n\n'+g.SOURCES[mid][':question/worked-solution']+'\n\nReplayed\n\n'+g.markdown(g.generate(level,template=mid,parameters=g.source_parameters(mid))) for mid,level in g.TEMPLATES.items()]+[g.markdown(r) for r in previews]))
    hashes = {str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest() for path in (HERE.with_suffix('.py'),HERE/'source.json',HERE/'math_parser.py',HERE/'validate.py',HERE/'capabilities.json')}
    save('validation.json',{'status':'pass','instances_checked':len(records),'supported_source_banks':4,'matched_source_banks':4,'native_accepted':engine['accepted_checks'],'native_rejected':engine['rejected_checks'],'native_unresolved':0,'hashes':hashes,'correctness':'Independent parsed prompt, complete equation bank and every numerical solution row','fidelity':'Exact prompt/prose, same source step sequence, mathematical answer match; display spacing/sign normalization reported separately','grading':'Actual course_academy_engine::learning::grade_field; canonical/equivalent/factored correct and two incorrect entries per instance','hard_supported':False})
    print(json.dumps(json.loads((HERE/'validation.json').read_text()),indent=2))

if __name__=='__main__':main()
