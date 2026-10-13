"""Independent rendered-equation validation, complete source replay and native grading."""
import hashlib
import importlib.util
import json
import re
import subprocess
import uuid
from pathlib import Path
import sympy as sp

D = Path(__file__).resolve().parent
ROOT = D.parents[2]
s = importlib.util.spec_from_file_location('generator', D.with_suffix('.py'))
g = importlib.util.module_from_spec(s); s.loader.exec_module(g)
x, y = sp.symbols('x y')

def math(text):
    text = text.replace(' ', '')
    text = re.sub(r'\\(?:d?frac)\{(-?\d+)\}\{(-?\d+)\}', r'(\1)/(\2)', text)
    if not re.fullmatch(r'[\d()+\-*/xy]+', text):
        raise ValueError('Unexpected notation ' + text)
    text = re.sub(r'(?<=[\d)xy])(?=[xy(])', '*', text)
    return sp.sympify(text, locals={'x':x, 'y':y}, rational=True)

def equation(text):
    parts = text.replace('&', '').replace(r'\,', '').replace(r'\times', '').replace('✓', '').split('=')
    assert len(parts) == 2
    return sp.expand(math(parts[0]) - math(parts[1]))

def equation_line(e):
    assert sp.Poly(e,x,y).total_degree() == 1 and e.coeff(y) != 0
    return sp.cancel(-e.coeff(x)/e.coeff(y)), sp.cancel(-e.subs({x:0,y:0})/e.coeff(y))

def parse(q):
    eqs = re.findall(r'(?m)^(?:I|II|III)\. \$(.*?)\$$', q[':question/problem'])
    if not eqs:
        eqs = re.findall(r'(?m)^- \*\*(?:I|II|III)\.\*\* \$(.*?)\$$', q[':question/problem'])
    assert len(eqs) == 3
    return [equation(z) for z in eqs]

def fingerprint(q):
    # Inspect graph references through retained source/asset manifests, not answer metadata.
    path = re.findall(r'!\[.*?\]\((.*?)\)', q[':question/problem'])[0]
    known = {'q-71837':('-3','6'), 'q-54293':('-1/2','2'), 'q-54285':('1/2','2'), 'q-59732':('-1','4')}
    for sid, record in g.PROFILES.items():
        if path in record[':question/problem']:
            return g.digest(list(known[sid]))
    files = sorted((D/'reference').glob('**/*generated.json')) + [D/'review-records.json']
    for file in files:
        if not file.exists(): continue
        for r in json.loads(file.read_text()):
            for a in r['generation']['assets']:
                if a['role'] == 'prompt' and a['path'] == path:
                    return g.digest(a['line'])
    raise ValueError('Unrecognized graph; cannot claim mathematical distinctness')

def structural(rec):
    q = rec['question']; md = rec['generation']; profile = md['bank_profile']; p = md['parameters']
    assert q[':question/difficulty'] == ':question.difficulty/hard'
    assert rec['knowledge_point']['db_id'] == g.KP_ID
    b, t = sp.Rational(p['b']), sp.Rational(p['t']); target = (-b/t, b)
    eqs = parse(q); truth = [equation_line(e) == target for e in eqs]
    assert truth == ([True]*3 if profile == 'q-71837' else [False,True,False])
    assert md['parameter_fingerprint'] == g.digest([str(z) for z in target])
    f = q[':question/answer-fields'][0]
    assert len(q[':question/answer-fields']) == 1 and f[':answer-field/key'] == 'selection'
    assert f[':answer-field/type'] == ':answer-field.type/radio'
    choices = f[':answer-field/choices']; assert len(choices) == len({a[':answer/value'] for a in choices}) == 5
    correct = f[':answer-field/correct'][1]
    for a in choices:
        labels = re.findall(r'\bI{1,3}\b', a[':answer/value'])
        selected = set(labels)
        assert (a[':answer/id'] == correct) == (selected == {label for label,v in zip(('I','II','III'),truth) if v})
        assert a[':answer/type'] == ':answer.type/text' and '$' not in a[':answer/value']
        uuid.UUID(a[':answer/id'])
    assert len({a[':answer/id'] for a in choices}) == 5
    uuid.UUID(q[':question/id']); uuid.UUID(f[':answer-field/id'])
    sol = q[':question/worked-solution']; blocks = re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)
    assert len(blocks) == 3
    # Each displayed numeric step must equal the original equation's residual at A or B.
    for idx,block in enumerate(blocks):
        point = {x:0,y:b}
        expected = eqs[idx].subs(point)
        for step in block.split(r'\\'):
            residual = equation(step)
            assert residual == expected, (profile,p,idx,step,residual,expected)
            if '✓' in step or r'\times' in step:
                assert (residual == 0) == ('✓' in step)
                point = {x:t,y:0}; expected = eqs[idx].subs(point)
    assert f'$(0,{b})$ and $({t},0)$' in sol
    for asset in md['assets']:
        assert asset['line'] == [str(z) for z in target]
        assert hashlib.sha256(Path(asset['local']).read_bytes()).hexdigest() == asset['sha256']
        if asset['role'] == 'solution':
            assert asset['points'] == [[0,int(b)],[int(t),0]]
    return target

def checks(rec):
    f = rec['question'][':question/answer-fields'][0]; cid = f[':answer-field/correct'][1]
    return [{'submitted_answer_id':a[':answer/id'], 'expected':'accepted' if a[':answer/id'] == cid else 'rejected', 'purpose':'complete source-profile field-owned radio bank'} for a in f[':answer-field/choices']]

def write(name,value):
    (D/name).write_text(json.dumps(value,indent=2)+'\n')

def main():
    ledger=[]; all_records=[]; native=[]; distinct=set(); replay_records=[]
    for profile,p in g.SOURCE_CASES.items():
        rec=g.generate('hard',parameters=p,profile=profile); structural(rec)
        old=g.PROFILES[profile]; q=rec['question']; expected=old[':question/worked-solution']
        correction=[]
        if profile=='q-54293':
            expected=expected.replace(r'(2) & =-1(0)',r'(2) & =-2(0)')
            correction=['Source Equation I substitution uses -1 instead of displayed -2; corrected generated coefficient. Source unchanged.']
        assert q[':question/problem']==old[':question/problem']
        assert q[':question/worked-solution']==expected
        old_f=old[':question/answer-fields'][0];new_f=q[':question/answer-fields'][0]
        assert {(a[':answer/type'][':db/ident'],a[':answer/value']) for a in old_f[':answer-field/choices']}=={(a[':answer/type'],a[':answer/value']) for a in new_f[':answer-field/choices']}
        correct=lambda f: next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
        old_correct=old_f[':answer-field/correct'][':answer/value'];assert correct(new_f)==old_correct
        ledger.append({'profile':profile,'parameters':p,'prompt_exact':True,'solution_exact_with_documented_correction':True,'matched_values':5,'matched_distractors':4,'complete_bank_matched':True,'correct_designation_matched':True,'missing_or_extra':[],'corrections':correction})
        replay_records.append(rec)
    coverage={}
    for profile in g.SUPPORTED:
        coverage[profile]=0
        for p in g.candidates(profile):
            rec=g.generate('hard',seed=17,parameters=p,profile=profile);structural(rec)
            assert rec==g.generate('hard',seed=17,parameters=p,profile=profile)
            assert rec['question']==g.generate('hard',seed=23,parameters=p,profile=profile)['question']
            coverage[profile]+=1;distinct.add(rec['generation']['parameter_fingerprint']);all_records.append(rec)
            native.append({'label':profile+'/'+str(p),'record':rec,'checks':checks(rec)})
    for level in ('easy','moderate','unclassified'):
        try:g.batch(level,1,0)
        except ValueError:pass
        else:raise AssertionError('Unsupported level accepted')
    assert len(g.batch('hard',len(distinct),4))==len(distinct)
    try:g.batch('hard',len(distinct)+1,4)
    except ValueError:pass
    else:raise AssertionError('Finite limit not enforced')
    for sid in g.SUPPORTED:
        try:g.generate('hard',profile=sid,parameters={'b':0,'t':0})
        except ValueError:pass
        else:raise AssertionError('Invalid boundary accepted')
    # The unrated checkbox source profiles remain explicit exclusions; their keys are verified.
    unrated=[]
    for sid,target in (('q-54285',(sp.Rational(1,2),sp.Integer(2))),('q-59732',(sp.Integer(-1),sp.Integer(4)))):
        q=g.PROFILES[sid]; truth=[equation_line(e)==target for e in parse(q)]
        fields={f[':answer-field/key']:f for f in q[':question/answer-fields']}
        for label,correct in zip(('I','II','III'),truth):
            f=fields[label]; assert {a[':answer/value'] for a in f[':answer-field/choices']}=={'false','true'}
            assert f[':answer-field/correct'][':answer/value']==str(correct).lower()
        unrated.append({'profile':sid,'truth':truth,'complete_boolean_banks_verified':3,'generation_supported':False,'reason':'Difficulty absent; no source-rated easy or moderate template'})
    write('source-replay.json',{'supported':ledger,'unrated_exclusions':unrated})
    write('review-records.json',all_records)
    write('source-replay-records.json',replay_records)
    samples=[g.generate('hard',parameters={'b':12,'t':3},profile='q-71837'),g.generate('hard',parameters={'b':3,'t':6},profile='q-54293')]
    write('visual-review.json',samples)
    (D/'review.md').write_text('\n\n---\n\n'.join('## '+r['generation']['template']+' '+str(r['generation']['parameters'])+'\n\n'+g.markdown(r) for r in replay_records+samples)+'\n')
    write('engine-input.json',native)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
    report=json.loads((D/'engine-report.json').read_text());assert report['documented_unresolved_checks']==0
    sha=lambda path:hashlib.sha256(Path(path).read_bytes()).hexdigest()
    write('validation.json',{'status':'pass','source_basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],
        'source_fidelity':{'complete_banks_matched':2,'complete_banks_total':2,'matched_values':10,'matched_distractors':8,'missing_or_extra':[],'exact_prompt_and_solution_replay':True,'source_corrections':ledger[1]['corrections'],'unrated_profiles_excluded':unrated},
        'mathematics':{'displayed_instances_checked':len(all_records),'complete_profile_coverage':coverage,'finite_distinct_tasks':len(distinct),'deterministic_replay':True,'whole_equations_and_all_numeric_worked_steps_checked':True},
        'native_grading':{k:report[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},
        'hashes':{str(D.with_suffix('.py').relative_to(ROOT)):sha(D.with_suffix('.py')),'validator':sha(__file__),'source':sha(D/'source.json'),'grader':sha(ROOT/'generate/runs/current/check-engine')},
        'limitations':['Hard only; easy/moderate remain unsupported bounded capability exceptions.','36 profile instances yield 35 distinct lines; duplicate graph across profiles counted once.','The two unrated source questions remain unrated and unchanged.','Axis ranges adapt to intercepts; exact source assets reused for source replay.']})
    print(json.dumps(json.loads((D/'validation.json').read_text()),indent=2))

if __name__=='__main__':main()
