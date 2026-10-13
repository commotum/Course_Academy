"""Read rendered calculus independently; exhaust the bounded banks and real grader."""
import hashlib
import importlib.util
import json
import re
import subprocess
from pathlib import Path
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module
g = load(HERE.with_suffix('.py'), 'negative_affine_generator')
reader = load(HERE/'math_parser.py', 'negative_affine_reader')
x, u, C = reader.x, reader.u, reader.z
DER = r'\frac{\text{d}}{\text{d}x}'
def save(name, value):
    (HERE/name).write_text(json.dumps(value, indent=2)+'\n')

def group(text, start):
    op = text[start]; close = {'[':']', '(' : ')', '{':'}'}[op]
    depth = 1; end = start+1
    while depth:
        assert end < len(text)
        depth += (text[end] == op) - (text[end] == close); end += 1
    return text[start+1:end-1], end

def scalar(text):
    text = text.strip().rstrip('.,').replace('✓', '').replace('C', 'z')
    while DER in text:
        at = text.index(DER)
        arg, end = group(text, at+len(DER))
        d = sp.diff(scalar(arg), x)
        text = text[:at] + '(' + sp.latex(d) + ')' + text[end:]
    return reader.scalar(text)

def equal(a, b):
    return sp.cancel(a-b) == 0

def value(text, affine):
    text = text.strip().rstrip('.,').replace('✓', '')
    if r'\int ' in text:
        prefix, body = text.split(r'\int ', 1)
        # A missing differential is never silently accepted in production.
        match = re.search(r'\\text\{d\}([ux])$', body)
        assert match, ('missing differential', text)
        var = u if match[1] == 'u' else x
        body = body[:match.start()].replace(r'\,', '').strip()
        if body.endswith(r'\cdot'): body = body[:-len(r'\cdot')]
        prefix = prefix.strip()
        if prefix.endswith(r'\cdot'): prefix = prefix[:-len(r'\cdot')].strip()
        coeff = sp.Integer(-1 if prefix == '-' else 1) if prefix in ('','-','+') else scalar(prefix)
        expr = coeff * sp.integrate(scalar(body), var)
    else:
        expr = scalar(text)
    return expr.subs(u, affine)

def prompt_parameters(q):
    match = re.search(r'\\frac\{(\d+)\}\{\(([^()]+)\)\^\{(\d+)\}\}', q[':question/problem'])
    assert match, q[':question/problem']
    n = int(match[1])
    if q[':question/problem'][match.start()-1] == '-': n = -n
    poly = sp.Poly(scalar(match[2]), x); assert poly.degree() == 1
    return [n, int(poly.coeff_monomial(x)), int(poly.coeff_monomial(1)), int(match[3])]

def fingerprint(q):
    # Accept source/canonical spelling too. Full current source prompts contain
    # only these rational affine integrands, including the incomplete legacy.
    if q.get(':question/math-academy-id') == 'q-12499':
        return g.fingerprint([1,1,-3,8])
    if q.get(':question/math-academy-id') == 'e-447':
        return g.fingerprint([2,-1,1,3])
    return g.fingerprint(prompt_parameters(q))

def check(rec):
    meta, q = rec['generation'], rec['question']
    parameters = prompt_parameters(q); assert parameters == meta['parameters']
    assert rec == g.generate(q[':question/difficulty'].split('/')[-1], meta['seed'], meta['template'], parameters)
    n, a, b, m = parameters; affine = a*x+b; integrand = sp.cancel(n/affine**m)
    fs = q[':question/answer-fields']; assert len(fs) == 1
    f = fs[0]; assert f[':answer-field/key'] == 'selection' and f[':answer-field/type'] == ':answer-field.type/radio'
    bank = f[':answer-field/choices']; assert len(bank) == 5
    assert all('$' not in answer[':answer/value'] for answer in bank)
    primitives = [scalar(answer[':answer/value']) for answer in bank]
    derivatives = [sp.cancel(sp.diff(expr,x)) for expr in primitives]
    assert len(set(derivatives)) == 5, 'Bank equivalent modulo constants'
    correct = [i for i, answer in enumerate(bank) if answer[':answer/id'] == f[':answer-field/correct'][1]]
    assert len(correct) == 1
    assert equal(derivatives[correct[0]],integrand)
    assert all(not equal(d,integrand) for i,d in enumerate(derivatives) if i != correct[0])
    sol = q[':question/worked-solution']
    sub = re.search(r'Let \$u=([^$]+)\.\$', sol); assert sub and equal(scalar(sub[1]), affine)
    jac = re.search(r'\\frac\{\\text\{d\}u\}\{\\text\{d\}x\}=(-?\d+)', sol); assert jac and int(jac[1]) == a
    dx = re.search(r'⟹\\,\\text\{d\}x=(.*?)\\text\{d\}u',sol)
    assert dx and equal(scalar(dx[1]) if dx[1] not in ('','-') else sp.Integer(-1 if dx[1]=='-' else 1),sp.Rational(1,a))
    blocks = re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S); assert len(blocks) == 4
    assert equal(sp.diff(value(blocks[0],affine),x),integrand)
    count = 0
    for index, block in enumerate(blocks[2:]):
        block = block.removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}')
        for row in block.split(r'\\'):
            for expression in row.split('& ='):
                if not expression.strip(): continue
                z = value(expression,affine)
                assert equal(sp.diff(z,x),integrand) if index == 0 else equal(z,integrand), (meta['template'], expression, z, integrand)
                count += 1
    assert meta['mathematical_fingerprint'] == g.fingerprint(parameters)
    assert equal(sp.sympify(meta['primitive'],locals={'x':x}), primitives[correct[0]]-C)
    return count

def native(label, rec):
    f = rec['question'][':question/answer-fields'][0]
    return {'label':label, 'record':rec, 'checks':[{'submitted_answer_id':answer[':answer/id'],
        'expected':'accepted' if answer[':answer/id']==f[':answer-field/correct'][1] else 'rejected',
        'purpose':'actual application radio ID grading'} for answer in f[':answer-field/choices']]}

def main():
    source = json.loads((HERE/'source.json').read_text())
    qs = {q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
    all_records, inputs, replay, review, recipes = [], [], [], [], {}
    count = 0
    for sid,t in g.PROFILES.items():
        rec = g.generate(t['level'],0,sid,t['parameters']); count += check(rec)
        q, old = rec['question'], qs[sid]; f = q[':question/answer-fields'][0]; of = old[':question/answer-fields'][0]
        assert q[':question/problem'] == old[':question/problem']
        expected_solution = old[':question/worked-solution']
        if t['source_correction']:
            correction = t['source_correction']; expected_solution = expected_solution.replace(correction['old'].replace('@@L@@',t['affine']),correction['new'].replace('@@L@@',t['affine']))
        assert q[':question/worked-solution'] == expected_solution
        assert sorted(answer[':answer/value'] for answer in f[':answer-field/choices']) == sorted(answer[':answer/value'] for answer in of[':answer-field/choices'])
        new_correct = next(answer[':answer/value'] for answer in f[':answer-field/choices'] if answer[':answer/id']==f[':answer-field/correct'][1])
        assert new_correct == of[':answer-field/correct'][':answer/value']
        recipe = []
        n,a,b,m = t['parameters']
        for option in t['bank']:
            expr = sp.cancel((scalar(option['source_value'])-C).subs(x,(u-b)/a))
            power = expr.as_powers_dict()[u]; coefficient = sp.cancel(expr/u**power)
            assert coefficient.is_Rational and power.is_Integer and power < 0
            recipe.append({**option,'recipe':'c*(a*x+b)^(-k)+C','c':str(coefficient),'k':int(-power),'complete_value_reproduced':True,'interpretation':'Observed coefficient/exponent recipe; misconception not inferred.'})
        recipes[sid] = recipe
        replay.append({'source':sid,'template':sid,'profile':sid,'matched_choices':5,'matched_distractors':4,'complete_bank_match':True,'prompt_exact':True,'solution_exact':not bool(t['source_correction']),'solution_supported_correction':t['source_correction']})
        review.append('## '+sid+'\n\nOriginal\n\n'+old[':question/problem']+'\n\n'+old[':question/worked-solution']+'\n\nReplay\n\n'+g.markdown(rec)+'\n\nVariant\n\n'+g.markdown(g.generate(t['level'],42,sid)))
        for b in range(t['bounds'][0],t['bounds'][1]+1):
            p = list(t['parameters']); p[2] = b
            r = g.generate(t['level'],0,sid,p); count += check(r)
            assert r['question'] == g.generate(t['level'],987,sid,p)['question']
            all_records.append(r); inputs.append(native(sid+' '+str(p),r))
    for level,limit in [('easy',60),('moderate',36)]:
        rows = g.batch(level,limit,22); assert len({r['generation']['mathematical_fingerprint'] for r in rows})==limit
        try: g.batch(level,limit+1,22)
        except ValueError: pass
        else: raise AssertionError('Finite limit bypassed')
    for args in [('hard',0,None,None),('easy',0,'q-113511',[1,5,0,6]),('moderate',0,'q-12019',[3,3,1,3])]:
        try: g.generate(*args)
        except ValueError: pass
        else: raise AssertionError('Parameter/level bound bypassed')
    assert g.fingerprint([1,1,-2,3]) == g.fingerprint([8,2,-4,3])
    excluded = qs['q-12499']; assert ':question/difficulty' not in excluded and ':question/worked-solution' not in excluded
    save('choice-recipes.json',recipes)
    save('source-replay.json',{'passed':True,'complete_banks_matched':8,'complete_banks_total':8,'distractors_matched':32,'distractors_total':32,'profiles':replay,'excluded_incomplete_sources':['q-12499']})
    save('native-input.json',inputs)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
    save('previews.json',{level:g.batch(level,5,1920) for level in ('easy','moderate')})
    (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
    save('validation.json',{'passed':True,'source_basis':source['basis'],'supported_levels':['easy','moderate'],
        'mathematical_checks':'independent rendered prompt/choice derivatives, all substitution/Jacobian values, every displayed integration and derivative equality',
        'printed_solution_expressions':count,'exhaustive_instances':len(all_records),
        'distinct_bounded_integrands':{level:len({r['generation']['mathematical_fingerprint'] for r in all_records if r['question'][':question/difficulty'].endswith('/'+level)}) for level in ('easy','moderate')},
        'source_fidelity':'8/8 complete banks and 32/32 distractors; exact prompts; 7 exact solutions and 1 documented missing-differential correction',
        'native_grading':'all five selections for all 96 bounded instances',
        'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'contract.json',HERE/'validate.py',HERE/'math_parser.py')}})

if __name__ == '__main__': main()
