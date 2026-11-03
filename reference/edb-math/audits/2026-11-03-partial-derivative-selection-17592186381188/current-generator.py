#!/usr/bin/env python3
"""Seeded, relocatable first-partial difference-quotient practice. No I/O except stdout."""
import argparse
import hashlib
import json
import random
import re
import sys
import uuid
sys.dont_write_bytecode = True
from math_format import normalize_prose, normalize_tex, validate_generated_record

VERSION = 'partial-quotient-v6'
KP = {'db_id': 17592186124643, 'id': '59c3f441-0499-575c-af10-b597d61e6e35',
      'title': 'Partial Derivatives as Limits of Difference Quotients'}
FAMILIES = {
 'easy': ['monomial', 'exponential_linear', 'log_linear', 'variable_power', 'cosine', 'sine_product', 'log_factor', 'rational', 'root_product', 'structured_sum'],
 'moderate': ['rational', 'exponential_product', 'cube_root', 'log_product', 'root_product', 'structured_sum'],
 'hard': ['coordinated_rational']}
SOURCES = dict(zip(
 ['monomial','exponential_linear','log_linear','variable_power','cosine','sine_product',
  'rational','exponential_product','cube_root','log_product','root_product','structured_sum','coordinated_rational','log_factor'],
 ['b1789afc-331e-5614-8cc9-89f93ec40167','5c2bb34d-dbfd-5a5b-98f2-f7deb6f4851c',
  'fdf020b6-22cb-53d4-9f16-5ef52a2ed3d5','9785714b-27e4-57d0-bac5-65edf8d118a2',
  'ea65f87f-49a7-5b8c-93db-0d61d7663ef3','fab082ec-08e1-574d-8102-367e3c718114',
  '31a26b77-cde2-5225-9c1c-15176a7705f8','96b9d7fd-e6bd-5861-b4a2-0c2b1d143000',
  '53daed36-1f31-5b2b-8966-96a4d35c598d','1c0019cf-9f1b-5e4a-8594-fc0063073eea',
  '0b3ca695-bbf4-58d5-b3fd-5901b18ae41b','8ce7a70c-484e-561e-b846-c96b367f5a49',
  '8ce7a70c-484e-561e-b846-c96b367f5a49','a14d53ae-1922-531d-bb2a-bda9b4829f6e']))

# These same functions support two workloads. Keep both roles available, but
# rate the actual requested substitution rather than the unchanged wrapper.
ROLE_FAMILIES = ('rational', 'root_product', 'structured_sum')
def calibrated_level(family, p, target, default):
    if family not in ROLE_FAMILIES:
        return default
    repeated_or_nested = 'x' if p['swap'] else 'y'
    return 'moderate' if target == repeated_or_nested else 'easy'

def uid(*values):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, json.dumps(values, sort_keys=True, ensure_ascii=False)))

def replace_inputs(text, mapping):
    # Commands are atomic: the x in \\exp is never a variable.
    return re.sub(r'\\[A-Za-z]+|[xy]', lambda m: mapping.get(m[0], m[0]), text)

def function(family, p):
    a,b,c,d,e,n = [p[k] for k in ('a','b','c','d','e','n')]
    if family == 'monomial': f,domain = rf'{a}x^{{{n}}}y', ''
    elif family == 'exponential_linear': f,domain = rf'{b}^{{x+{c}y}}', ''
    elif family == 'log_linear': f,domain = rf'\log(x+{c}y)', rf'x+{c}y>0'
    elif family == 'log_factor': f,domain = rf'y^{{{n}}}\ln(x)', 'x>0'
    elif family == 'variable_power': f,domain = r'x^{y}', 'x>0'
    elif family == 'cosine': f,domain = rf'\cos(x-y^{{{n}}})', ''
    elif family == 'sine_product': f,domain = rf'\sin({a}xy)', ''
    elif family == 'rational': f,domain = rf'\frac{{x^{{{n}}}}}{{(y+{a})^{{{c}}}}}', rf'y+{a}\ne 0'
    elif family == 'exponential_product': f,domain = rf'{b}^{{xy}}', ''
    elif family == 'cube_root': f,domain = rf'\sqrt[3]{{x^{{{n}}}-y}}', rf'x^{{{n}}}-y\ne 0'
    elif family == 'log_product': f,domain = rf'\ln({a}xy)', 'xy>0'
    elif family == 'root_product': f,domain = r'x\sqrt{y}', 'y>0'
    elif family in ('structured_sum', 'coordinated_rational'):
        numerator = rf'{a}xy+{b}y^2'
        if family == 'structured_sum': f,domain = numerator, ''
        else: f,domain = rf'\frac{{{numerator}}}{{{d}x+{e}y}}', rf'{d}x+{e}y\ne 0'
    else: raise ValueError('Unknown family')
    if p['swap']:
        f = replace_inputs(f, {'x':'y','y':'x'})
        domain = replace_inputs(domain, {'x':'y','y':'x'})
    # Omit coefficient one without altering the mathematical grouping.
    f = re.sub(r'(?<![0-9])1(?=[xy])', '', f)
    domain = re.sub(r'(?<![0-9])1(?=[xy])', '', domain)
    return normalize_tex(f), normalize_tex(domain)

def quotient(first, second, plus=False):
    # The outer fence groups the whole numerator. Only a second additive
    # operand needs another fence when subtraction would distribute its sign.
    depth=0; additive=False
    for ch in second:
        if ch in '({[': depth+=1
        elif ch in ')}]': depth-=1
        elif ch in '+-' and depth==0: additive=True
    if additive and not plus: second=r'\left('+second+r'\right)'
    if additive:
        # A polynomial sum needs compact numerator typography in radio banks.
        return normalize_tex(r'\lim_{h\to 0}\frac{'+first+('+' if plus else '-')+second+'}{h}')
    # Keep nested rational inputs readable rather than shrinking them inside
    # another fraction numerator. The fence groups the entire subtraction.
    return normalize_tex(r'\lim_{h\to 0}\frac{1}{h}\left('+first+('+' if plus else '-')+second+r'\right)')

def make(level, family, p, target, profile, bank_seed=0):
    if family not in FAMILIES[level] or target not in ('x','y') or profile not in ('reverse','addition'):
        raise ValueError('Unsupported construction')
    if calibrated_level(family,p,target,level) != level:
        raise ValueError('Difficulty must follow the requested substitution role')
    if level=='hard' and p['b']*p['d']==p['a']*p['e']:
        raise ValueError('Canceled variable denominator belongs outside the hard coordination band')
    f, domain = function(family,p)
    shifted = {v: replace_inputs(f,{v:'('+v+'+h)'}) for v in ('x','y')}
    both = replace_inputs(f,{'x':'(x+h)','y':'(y+h)'})
    values = [quotient(shifted[v], f) for v in ('x','y')] + [quotient(both, f)]
    values += [quotient(f, shifted[v]) if profile=='reverse' else quotient(shifted[v], f, True) for v in ('x','y')]
    if len(set(values)) != 5: raise ValueError('Degenerate bank')
    correct = values[0 if target=='x' else 1]
    held = 'y' if target=='x' else 'x'
    pair = 'x+h,y' if target=='x' else 'x,y+h'
    lhs = rf'\frac{{\partial f}}{{\partial {target}}}'
    prompt = 'Given that $f(x,y)='+f+'$'
    if domain: prompt += ' on the domain $'+domain+'$'
    prompt += ', which limit of a difference quotient represents $'+lhs+'$?'
    formal = r'\lim_{h\to 0}\frac{f('+pair+r')-f(x,y)}{h}'
    solution = ('Hold $'+held+'$ constant. The definition gives\n\n$$\n'+lhs+'='+formal+'.\n$$\n\n'
                'Replace every occurrence of $'+target+'$ by $('+target+'+h)$ in the function, preserving each operator and its input:\n\n$$\n'
                'f('+pair+')='+shifted[target]+'.\n$$\n\nSubtract the entire original function value and divide by $h$:\n\n$$\n'
                +lhs+'='+correct+'\n$$\n\nOnly $'+target+'$ changes, and $h\\ne 0$ before taking the limit.')
    if domain: solution += ' The stated domain places the inputs in a differentiable interior region; sufficiently small increments keep the function defined.'
    prompt,solution = normalize_prose(prompt),normalize_prose(solution)
    # Normalize all prose before identities. Seed and parameters are not identities.
    qid = uid(KP['id'], level, prompt, solution, sorted(values), correct)
    fid = uid(qid,'selection')
    choices = [{':answer/id':uid(fid,v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    correct_id = choices[0 if target=='x' else 1][':answer/id']
    random.Random(bank_seed).shuffle(choices)
    q = {':question/id':qid, ':question/difficulty':':question.difficulty/'+level,
         ':question/problem':prompt, ':question/worked-solution':solution,
         ':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',
           ':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,
           ':answer-field/correct':[':answer/id',correct_id]}]}
    record = {'knowledge_point':dict(KP),'question':q,'generation':{
       'version':VERSION,'template':family,'profile':profile,'parameters':dict(p),
       'target_variable':target,'source_question_ids':[SOURCES[family]],
       'authored_bank':True,'domain':domain,'bank_seed':bank_seed}}
    validate_generated_record(record)
    return record

def parameters(rng):
    return {'a':rng.randint(1,5),'b':rng.randint(2,5),'c':rng.randint(2,4),
            'd':rng.randint(1,3),'e':rng.randint(1,3),'n':rng.choice([2,3]),'swap':bool(rng.getrandbits(1))}

def generate_batch(level, count, seed):
    if level not in FAMILIES or count < 1: raise ValueError('Invalid level/count')
    rng = random.Random(seed)
    families = list(FAMILIES[level]); rng.shuffle(families)
    phase = rng.randrange(2); profile_phase = rng.randrange(2)
    output,seen = [],set()
    for attempt in range(max(1000,count*100)):
        i=len(output)
        # Family cycles and coordinate cycles are independent, including at count=5.
        family=families[i%len(families)]
        target=('x','y')[(i//len(families)+i%len(families)+phase)%2]
        profile=('reverse','addition')[(i//2+profile_phase)%2]
        p=parameters(rng)
        if family in ROLE_FAMILIES:
            # Either physical target is available. Orient the function so its
            # requested role realizes this band's workload; the other role is
            # served by the other band, not discarded.
            p['swap'] = (target == ('x' if level == 'moderate' else 'y'))
        if level=='hard' and p['b']*p['d']-p['a']*p['e'] == 0:
            continue  # A globally canceled denominator removes this band's coordination task.
        record=make(level,family,p,target,profile,rng.getrandbits(64))
        identity=record['question'][':question/id']
        if identity in seen:
            # Advance a saturated finite family instead of pinning the whole batch.
            families=families[1:]+families[:1]
            continue
        seen.add(identity);output.append(record)
        if len(output)==count: return output
    raise ValueError('Requested batch exceeds supported semantic capacity')

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--difficulty',choices=[*FAMILIES,'unclassified'],default='easy')
    parser.add_argument('--count',type=int,default=1)
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=['json'],default='json')
    a=parser.parse_args()
    try: records=generate_batch('easy' if a.difficulty=='unclassified' else a.difficulty,a.count,a.seed)
    except ValueError as error: parser.error(str(error))
    print(json.dumps(records,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
