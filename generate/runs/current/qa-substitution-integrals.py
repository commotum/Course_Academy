"""Parent independently reads displayed substitution-integral stages and full banks."""
import hashlib, importlib.util, itertools, json, re, sys
from pathlib import Path
import sympy as s

sys.dont_write_bytecode = True
R = Path(__file__).resolve().parent
ROOT = R.parents[2]

def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

P = module(R / 'ode-scalar-parser.py', 'root_integral_parser')
FID = module(R / 'root-source-fidelity.py', 'root_integral_fidelity')
DIFFERENTIAL = r'(?:\\(?:text|mathrm)\{d\}|d)\s*([xyzut])'

def scalar(text):
    text = text.strip().rstrip('.,')
    text = re.sub(r'\+\s*C\s*$', '', text)
    text = text.replace(r'\displaystyle', '').replace(r'\;', '')
    text = text.replace(r'\!', '').replace(r'\dfrac', r'\frac')
    return P.scalar(text)

def integral(text):
    text = re.sub(r'\(\s*-\s*(' + DIFFERENTIAL + r')\s*\)', r'(-1)\1', text)
    text = re.sub(r'\(([^()]*?)(' + DIFFERENTIAL + r')\s*\)', lambda m:'('+m[1]+')'+m[2], text)
    match = re.search(r'\\int\s*(.*?)\s*' + DIFFERENTIAL, text, re.S)
    assert match, ('No actual displayed integral', text)
    body = match[1].replace(r'\,', '').strip()
    # A printed dot multiplying the differential is legal: f(u) · du.
    # The differential becomes the measure here, leaving f(u) as integrand.
    if body.endswith(r'\cdot'): body = body[:-len(r'\cdot')].strip()
    return scalar(body), P.locals_[match[2]], match

def equal(a, b):
    return s.simplify(s.expand(a - b)) == 0

def factor(text):
    text = text.replace(r'\,', '').strip()
    return s.Integer(-1) if text == '-' else s.Integer(1) if text in ('', '+') else scalar(text)

def check(k):
    D = ROOT / f'generate/scratch/{k}'
    G = module(D.with_suffix('.py'), 'root_integral_' + str(k))
    originals, source_counts = FID.check(G, k, D)
    source_cases = json.load(open(D / 'source-cases.json'))
    family_source = {case['template']: originals[case.get('source_ma_id', case.get('math_academy_id', case['source_id']))] for case in source_cases}
    def prose_mask(text):
        text = re.sub(r'\$\$[\s\S]*?\$\$|\$[^$]*\$', '<MATH>', text)
        return re.sub(r'\s+', ' ', text).strip()
    records = json.load(open(R / f'qa/{k}-sampled.json'))
    # Include every normal source-shaped family in review, beyond default sampling.
    for item in json.load(open(D / 'review.json')):
        record = item.get('record', item)
        if 'question' in record and not record['generation'].get('evidence_only', False):
            records.append(record)
    counts = dict(records=0, actual_integrands=0, substitutions=0,
                  differential_relations=0, operative_integral_rows=0,
                  primitive_rows=0, complete_choice_values=0, criterion_pairs=0, source_prose_masks=0)
    for record in records:
        question = record['question']
        prompt = question[':question/problem']
        solution = question[':question/worked-solution']
        original = family_source.get(record['generation']['template'])
        if original and ':question/worked-solution' in original:
            assert prose_mask(solution) == prose_mask(original[':question/worked-solution']), (k, 'Source solution prose/stage-mask mismatch', record['generation']['template'])
            counts['source_prose_masks'] += 1
        expected, variable, _ = integral(prompt)
        counts['actual_integrands'] += 1
        definitions = re.findall(r'(?<![A-Za-z}])u\s*=\s*([^$\n]+)', solution)
        # Definitions may occur in inline prose and in their own display.
        assert definitions, ('Missing displayed substitution', solution)
        inner = scalar(definitions[0])
        assert variable in inner.free_symbols
        derivative = s.diff(inner, variable)
        assert derivative != 0
        for definition in definitions:
            assert equal(scalar(definition), inner), ('Stale u definition', definition)
        counts['substitutions'] += len(definitions)
        derivative_relation = re.search(
            r'\\(?:frac|dfrac)\{\\(?:text|mathrm)\{d\}u\}'
            r'\{\\(?:text|mathrm)\{d\}' + str(variable) + r'\}\s*&?\s*=\s*(.*?)\s*(?:\\,)?⟹',
            solution, re.S)
        assert derivative_relation, ('Missing actual derivative relation', solution)
        assert equal(scalar(derivative_relation[1].replace('&', '')), derivative)
        counts['differential_relations'] += 1
        differential_block = next(block for block in re.findall(r'\$\$\s*(.*?)\s*\$\$', solution, re.S) if '⟹' in block)
        relation = re.sub(r'\\(?:begin|end)\{aligned\}', '', differential_block.split('⟹', 1)[1]).replace('&', '').strip().rstrip('.,')
        dm = re.fullmatch(r'(.*?)' + DIFFERENTIAL + r'\s*=\s*(.*?)' + DIFFERENTIAL + r'\s*,?', relation, re.S)
        assert dm and dm[2] == 'u' and dm[4] == str(variable), ('Malformed differential relation', relation)
        coefficient_text = dm[1].replace(r'\,', '').strip()
        coefficient = factor(coefficient_text)
        assert equal(coefficient * derivative, scalar(dm[3])), ('Wrong multiplier in displayed differential relation', relation)
        counts['differential_relations'] += 1
        # Read every operative aligned/equality side. Substituted integral sides
        # are converted back using du = inner'(x) dx; primitive sides are
        # differentiated after the SAME displayed substitution.
        blocks = re.findall(r'\$\$\s*(.*?)\s*\$\$', solution, re.S)
        before_primitives = counts['primitive_rows']
        for block in blocks:
            if r'\int' not in block:
                continue
            block = re.sub(r'\\(?:begin|end)\{aligned\}', '', block).replace('&', '')
            rows = block.split(chr(92) * 2)
            for row in rows:
                for side in row.split('='):
                    side = side.strip().rstrip('.,')
                    if not side:
                        continue
                    if r'\int' in side:
                        integrand, integration_variable, match = integral(side)
                        coefficient = factor(side[:match.start()])
                        actual = coefficient * integrand
                        if integration_variable == P.u:
                            actual = actual.subs(P.u, inner) * derivative
                        else:
                            assert integration_variable == variable
                        assert equal(actual, expected), (k, 'Wrong operative integral', side, actual, expected)
                        counts['operative_integral_rows'] += 1
                    else:
                        primitive = scalar(side).subs(P.u, inner)
                        assert equal(s.diff(primitive, variable), expected), (k, 'Wrong displayed primitive', side)
                        counts['primitive_rows'] += 1
        assert counts['primitive_rows'] > before_primitives
        for field in question[':question/answer-fields']:
            answers = field[':answer-field/choices']
            derivatives = [s.diff(scalar(answer[':answer/value']), variable) for answer in answers]
            for answer, actual in zip(answers, derivatives):
                assert equal(actual, expected) == (answer[':answer/id'] == field[':answer-field/correct'][1]), (k, 'Wrong key', answer)
                counts['complete_choice_values'] += 1
            for a, b in itertools.combinations(derivatives, 2):
                assert not equal(a, b), (k, 'Equivalent choices modulo integration constant', answers)
                counts['criterion_pairs'] += 1
        counts['records'] += 1
    result = dict(status='passed', kp_id=k, source=source_counts, readback=counts,
                  generator_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(), database_writes=0)
    (R / f'qa/{k}-root-readback.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))

if __name__ == '__main__':
    for kp in map(int, sys.argv[1:]):
        check(kp)
