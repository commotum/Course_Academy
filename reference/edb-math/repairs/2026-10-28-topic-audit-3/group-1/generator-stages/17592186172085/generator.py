#!/usr/bin/env python3
"""Seeded 2D vector-field identification with a three-band checkbox progression.

Derived from the supplied 17592186172085.py: retains its eight formula/domain
recipes and source solution stages. See instructional-account.md for repairs.
No writes, generated images, network calls, or repository runtime imports.
"""
from __future__ import annotations
from audit_presentation import prose as _ca_prose, problem as _ca_problem, values as _ca_values, question as _ca_question, identity_material as _ca_material
import argparse, copy, hashlib, itertools, json, random, re, sys, uuid
from pathlib import Path
sys.dont_write_bytecode = True
from math_format import checked_math_content, normalize_prose

KP_ID = 17592186172085
KP_UUID = '019e5a17-1aab-565b-8881-447c86a9a7ec'
TITLE = 'Identifying Vector Fields on Two-Dimensions'
VERSION='vector-identification-3-checkbox-format-audit-9837-v1'
CAPTURE = json.loads(Path(__file__).with_name('source-data.json').read_text())
SOURCES = {q[':question/math-academy-id']:q for q in CAPTURE['kp'][':knowledge-point/questions']}
# Complete expression/domain slots; no replacement of isolated variable letters.
# Anchors are observed constants; each slot is evaluated for every ordinary call.
RECIPES={
 'q-122465': (r'\operatorname{ln}⁡y',lambda h:r'\operatorname{ln}⁡'+('y' if h==0 else '(y'+signed(-h)+')'),r'y>0',lambda h:'y>'+str(h)),
 'q-122643': (r'\frac{1}{{x}^{2}}',lambda h:r'\frac{1}{'+('{x}^{2}' if h==0 else '(x'+signed(-h)+')^{2}')+'}',r'x\ne 0',lambda h:r'x\ne '+str(h)),
 'q-122650': (r'\frac{1}{x+2}',lambda h:r'\frac{1}{x'+signed(h)+'}',r'x\ne -2,\,x-y\ge 0',lambda h:r'x\ne '+str(-h)+r',\,x-y\ge 0'),
 'q-122653': (r'\operatorname{ln}⁡(x+y)',lambda h:r'\operatorname{ln}⁡(x+y'+('' if h==0 else signed(-h))+')',r'x+y>0',lambda h:'x+y>'+str(h)),
 'q-122678': (r'\frac{{x}^{2}}{x-y}',lambda h:r'\frac{{x}^{2}}{x-y'+('' if h==0 else signed(-h))+'}',r'x\ne y',lambda h:r'x\ne y'+('' if h==0 else signed(h))),
 'q-122641': (r'{x}^{2}',lambda h:'{x}^{'+str(h)+'}',None,None),
 'q-122656': (r'\operatorname{cos}⁡y+1',lambda h:r'\operatorname{cos}⁡y'+signed(h),None,None),
 'q-122675': (r'\frac{1}{x+y}',lambda h:r'\frac{1}{x+y'+('' if h==0 else signed(-h))+'}',r'x+y\ne 0',lambda h:r'x+y\ne '+str(h)),
}
ANCHORS={s:0 for s in SOURCES};ANCHORS.update({'q-122650':2,'q-122641':2,'q-122656':1})
DIMENSIONS={
 'q-122465':[(2,2,'all'),(2,2,'log'),(3,3,'all')],
 'q-122643':[(2,2,'reciprocal'),(3,3,'all'),(1,2,'all')],
 'q-122650':[(2,2,'reciprocal+sqrt'),(2,2,'all'),(3,3,'all')],
 'q-122653':[(2,2,'log'),(3,3,'all'),(1,2,'all')],
 'q-122678':[(2,2,'reciprocal'),(3,3,'all'),(2,2,'all')],
 'q-122641':[(2,2,'all'),(1,2,'sqrt'),(3,3,'all')],
 'q-122656':[(2,3,'reciprocal'),(2,2,'all'),(1,2,'sqrt')],
 'q-122675':[(2,2,'reciprocal'),(2,2,'all'),(2,3,'all')],
}
LABELS={1:'I only',2:'II only',3:'I and II only',4:'III only',5:'I and III only',6:'II and III only',7:'I, II, and III'}
def signed(n): return ('+' if n>=0 else '')+str(n)
def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy/'+s))
def subset(ds):return sum(1<<i for i,(inp,out,_) in enumerate(ds) if inp==out==2)
def normal_repairs(s,text):
 if s=='q-122678':text=text.replace('$K(x,y,z)$','$V(x,y,z)$').replace('$V(x,y)$','$W(x,y)$')
 if s=='q-122675':text=text.replace('$E(x,y,z)$','$E(x,y)$')
 return text.replace('S={','S=\\{').replace('}\n$$','\\}\n$$')

ROMANS = ('I', 'II', 'III')
ORDERS = tuple(itertools.permutations(range(3)))

def h_values(template):
    return tuple(range(1, 5)) if template == 'q-122641' else tuple(range(-4, 5))


def semantic_key(template, h):
    # Permutations and harmless coefficient/exponent changes do not add coverage.
    return (template, h if RECIPES[template][2] is not None else None)


@checked_math_content
def source_generate(level='easy', seed=0, template=None, parameters=None):
    if level != 'easy':
        raise ValueError('Only easy is supported by the supplied source evidence')
    rng = random.Random(seed)
    template = template or rng.choice(tuple(SOURCES))
    if template not in SOURCES:
        raise ValueError('Unknown source template')
    p = copy.deepcopy(parameters) if parameters is not None else {
        'h': rng.choice(h_values(template)), 'order': list(rng.choice(ORDERS))}
    if (set(p) != {'h', 'order'} or type(p['h']) is not int
            or p['h'] not in h_values(template) or not isinstance(p['order'], (list, tuple))
            or len(p['order']) != 3 or any(type(i) is not int for i in p['order'])
            or tuple(p['order']) not in ORDERS):
        raise ValueError('Expected permitted integer h and permutation order of 0,1,2')
    h, order = p['h'], p['order']
    source = SOURCES[template]
    anchor, calculate, domain, domain_calculate = RECIPES[template]
    problem = source[':question/problem']
    if problem.count(anchor) != 1:
        raise ValueError('Formula anchor must occur exactly once')
    problem = problem.replace(anchor, calculate(h))
    solution = source[':question/worked-solution']
    if domain:
        if solution.count(domain) != 1:
            raise ValueError('Domain anchor must occur exactly once')
        solution = solution.replace(domain, domain_calculate(h))
    head, body = problem.split('\n\n- ', 1)
    formulas = [re.sub(r'^\*\*[IV]+\.\*\* ', '', line)
                for line in body.split('\n- ')]
    if len(formulas) != 3:
        raise ValueError('Source must have three candidate functions')
    problem = head + '\n\n' + '\n'.join(
        f'- **{ROMANS[j]}.** {formulas[i]}' for j, i in enumerate(order))
    intro, *bullets = solution.split('\n\n- ')
    bullets[-1] = bullets[-1].split('\n\nTherefore,')[0]
    ds = [DIMENSIONS[template][i] for i in order]
    selection = LABELS[subset(ds)]
    solution = intro + '\n\n' + '\n\n'.join('- ' + bullets[i] for i in order)
    solution += '\n\nTherefore, the correct answer is "' + selection + '."'
    problem = normalize_prose(problem)
    solution = normalize_prose(normal_repairs(template, solution))
    values = []
    source_fields = {f[':answer-field/key']: f for f in source[':question/answer-fields']}
    for i in order:
        bank = sorted(a[':answer/value'] for a in source_fields[ROMANS[i]][':answer-field/choices'])
        if bank != ['false', 'true']:
            raise ValueError('Unexpected source bank')
        values.append(bank)
    canonical = {'version': VERSION, 'problem': problem, 'solution': solution,
                 'banks': values, 'difficulty': 'easy'}
    ident = digest(canonical)
    qid = uid(ident)
    fields = []
    for j, (inp, out, _) in enumerate(ds):
        key = ROMANS[j]
        fid = uid(ident + '/' + key)
        correct = str(inp == out == 2).lower()
        choices = [{':answer/id': uid(fid + '/' + v), ':answer/type': ':answer.type/text',
                    ':answer/value': v} for v in values[j]]
        fields.append({':answer-field/id': fid, ':answer-field/key': key,
                       ':answer-field/type': ':answer-field.type/checkbox',
                       ':answer-field/choices': choices,
                       ':answer-field/correct': [':answer/id', uid(fid + '/' + correct)]})
    return {
        'knowledge_point': {'db_id': KP_ID, 'id': KP_UUID, 'title': TITLE},
        'question': {':question/id': qid, ':question/difficulty': ':question.difficulty/easy',
                     ':question/problem': problem, ':question/worked-solution': solution,
                     ':question/answer-fields': fields},
        'generation': {'version': VERSION, 'template': template, 'seed': seed, 'parameters': p,
                       'bank_profile': 'three-boolean-checkboxes',
                       'source': {'database': CAPTURE['database'], 'basis': CAPTURE['basis'],
                                  'lineage': CAPTURE['lineage'], 'question_id': source[':db/id'],
                                  'math_academy_id': template,
                                  'difficulty': source[':question/difficulty'][':db/ident']},
                       'dimensions': ds, 'semantic_key': semantic_key(template, h),
                       'content_fingerprint': ident, 'plot_rating': 'none',
                       'dependencies': {'python': sys.version.split()[0], 'packages': {}}}}


def replay(template):
    """Original parameters and complete banks, with documented source repairs."""
    return source_generate('easy', template=template,
                    parameters={'h': ANCHORS[template], 'order': [0, 1, 2]})


from practice import generate, batch


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', default='easy', choices=['easy', 'moderate', 'hard'])
    parser.add_argument('--count', type=int, default=5)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=['json'], default='json')
    args = parser.parse_args()
    try:
        records = batch(args.difficulty, args.count, args.seed)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(records, ensure_ascii=False, indent=2))



# Every learner-facing checkbox question has a nonempty correct selection.
from generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['batch', 'generate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__ == '__main__':
    main()
