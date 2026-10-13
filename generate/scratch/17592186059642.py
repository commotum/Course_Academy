#!/usr/bin/env python3
"""Exact rational Pythagorean-identity practice; basis 1356. No EDB writes.

Observed templates are compiled mathematical-component masks, not source payload
returns. Their unit instances reproduce whole worked solutions byte-for-byte;
angle, mirrored functions and an outer positive scalar affect every complete
mathematical stage and whole answer. Captured banks are explicit evidence-only
profiles: scaling a captured affine distractor is a replay operation, not a claim
about its historical error intention. Normal practice uses complete authored
operation banks. Missing easy uses the canonical rational identity method with
only a numeric common factor and a first-power denominator. All levels are
unordered variants, never a progression. See 17592186059642/ evidence.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from functools import lru_cache
from pathlib import Path
import sympy as sp

KP_ID=17592186059642
KP_UUID='868125f0-22e0-57fc-9620-f3242419a689'
TITLE='Simplifying a Rational Expression Using the Pythagorean Identity'
VERSION='rational-pythagorean-v1'
EVIDENCE=Path(__file__).with_suffix('')
CAPTURE=json.loads((EVIDENCE/'source.json').read_text())
SOURCE=CAPTURE['record']
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions']}
LEVELS={q: ('moderate' if ':question/difficulty' not in v else v[':question/difficulty'][':db/ident'].split('/')[-1]) for q,v in QUESTIONS.items()}
ANGLES={q:('θ' if q=='q-65165' else r'\theta' if r'\theta' in v[':question/problem'] else 't' if q=='q-65246' else 'x') for q,v in QUESTIONS.items()}
TEMPLATES={q:{'level':LEVELS[q],'origin':'observed','source':q} for q in QUESTIONS}
TEMPLATES['easy_identity']={'level':'easy','origin':'authored','source':None}
T=sp.Symbol('u',real=True)
SIN=2*T/(1+T*T); COS=(1-T*T)/(1+T*T)
FUNC={'sin':SIN,'cos':COS,'tan':SIN/COS,'cot':COS/SIN,'sec':1/COS,'csc':1/SIN}
MIRROR={'sin':'cos','cos':'sin','tan':'cot','cot':'tan','sec':'csc','csc':'sec'}
MATH=re.compile(r'(\$\$[\s\S]*?\$\$|(?<!\$)\$(?!\$)[^$]*?\$(?!\$))')
NEXT='Next, we use the Pythagorean identity to rewrite the expression in the parentheses, and then we simplify the resulting expression as much as possible.'

# Shared complete-component masks. No short arithmetic substring replacement.
def transform(text,old_angle,p):
    # Angle tokens have distinct complete names; these strings contain no prose x/t.
    text=re.sub(r'(?<![A-Za-z])'+re.escape(old_angle)+r'(?![A-Za-z])',lambda m:'@ANGLE@',text) if old_angle in ('x','t') else text.replace(old_angle,'@ANGLE@')
    if p['mirror']:
        text=re.sub(r'(?<![A-Za-z])(sin|cos|tan|cot|sec|csc)(?![A-Za-z])',lambda m:MIRROR[m[1]],text)
    return text.replace('@ANGLE@',p['angle'])

def scale_component(s,k):
    if k==1:return s
    # Each side is a full expression, not a fraction component or prose fragment.
    lead=s[:len(s)-len(s.lstrip())]; tail=s[len(s.rstrip()):]
    core=s.strip()
    if core.endswith('.'):
        core=core[:-1].rstrip();tail='.'+tail
    simple=re.fullmatch(r'(-?)([0-9]*)(\\(?:operatorname\{(?:sin|cos|tan|cot|sec|csc)\}|sin|cos|tan|cot|sec|csc)|\{(?:sin|cos|tan|cot|sec|csc)\})(?:\^\{?[0-9]+\}?)?⁡?\s*(?:x|t|θ|\\theta|\\phi)\s*',core)
    if simple:
        n=(-1 if simple[1] else 1)*int(simple[2] or '1')*k
        term=core[len(simple[1])+len(simple[2]):]
        return lead+str(n)+term+tail
    return lead+str(k)+r'\cdot\left('+core+r'\right)'+tail

def scale_math(body,k):
    # Retain exact row/side ordering and alignment while scaling every complete side.
    chunks=re.split(r'(\\\\|=|&|\\begin\{aligned\}|\\end\{aligned\})',body)
    result=[]
    for chunk in chunks:
        if chunk in ('=', '&',r'\\',r'\begin{aligned}',r'\end{aligned}') or not chunk.strip():result.append(chunk)
        else:result.append(scale_component(chunk,k))
    return ''.join(result)

def render_mask(text,old_angle,p,scale=True):
    text=transform(text,old_angle,p)
    def slot(m):
        v=m[0];d='$$' if v.startswith('$$') else '$'
        # Inline prose names the factored object; it is not the entire expression.
        apply=scale and (d=='$$' or r'\frac' in v or r'\dfrac' in v)
        return d+scale_math(v[len(d):-len(d)],p['k'])+d if apply else v
    return MATH.sub(slot,text)

def atom(name,p,power=1):
    return chr(92)+name+('^{'+str(power)+'}' if power!=1 else '')+' '+p['angle']

def frac(n,d):return r'\frac{'+n+'}{'+d+'}'
def coeff(k,s):return s if k==1 else str(k)+r'\cdot\left('+s+r'\right)'

def check_parameters(p):
    if set(p)!={'k','angle','mirror'}:raise ValueError('parameters must be k, angle, mirror')
    if type(p['k']) is not int or not 1<=p['k']<=12:raise ValueError('k must be integer 1..12 at every level')
    if p['angle'] not in ('x','t',r'\theta',r'\phi','θ'):raise ValueError('unsupported angle')
    if type(p['mirror']) is not bool:raise ValueError('mirror must be boolean')

# A strict display parser: legacy and standard TeX, complete implicit products,
# fractions, cancel groups, powers and all six trig functions. Fails on unknowns.
@lru_cache(maxsize=10000)
def parse_math(raw, symbolic=False, reduce=True):
    raw=raw.strip().replace('.','').replace('⁡','').replace('−','-')
    raw=re.sub(r'\\operatorname\{(sin|cos|tan|cot|sec|csc)\}',r'\\\1',raw)
    raw=re.sub(r'\{(sin|cos|tan|cot|sec|csc)\}',r'\\\1',raw)
    raw=raw.replace(r'\dfrac',r'\frac').replace(r'\left','').replace(r'\right','').replace(r'\,','')
    pattern=r'\\(?:frac|cancel|sin|cos|tan|cot|sec|csc|cdot|theta|phi)|[xtθ]|\d+|[{}()^+\-]'
    tokens=re.findall(pattern,raw)
    if re.sub(pattern,'',raw).strip():raise ValueError('unparsed TeX '+raw)
    i=0
    def group():
        nonlocal i
        if i>=len(tokens) or tokens[i] not in ('{','('):raise ValueError('expected group '+raw)
        end='}' if tokens[i]=='{' else ')';i+=1;e=add()
        if i>=len(tokens) or tokens[i]!=end:raise ValueError('unbalanced group '+raw)
        i+=1;return e
    def primary():
        nonlocal i
        v=tokens[i];i+=1
        if v.isdigit():e=sp.Integer(v)
        elif v in ('{','('):i-=1;e=group()
        elif v==r'\frac':e=group()/group()
        elif v==r'\cancel':e=group()
        elif v.startswith('\\') and v[1:] in FUNC:
            f=v[1:];power=1
            if i<len(tokens) and tokens[i]=='^':
                i+=1
                if tokens[i]=='{':power=group()
                else:power=sp.Integer(tokens[i]);i+=1
            if i>=len(tokens) or tokens[i] not in ('x','t','θ',r'\theta',r'\phi'):raise ValueError('missing trig argument '+raw)
            i+=1;e=(sp.Symbol(f) if symbolic and f in ('sin','cos') else (dict(sin=sp.Symbol('sin'),cos=sp.Symbol('cos'),tan=sp.Symbol('sin')/sp.Symbol('cos'),cot=sp.Symbol('cos')/sp.Symbol('sin'),sec=1/sp.Symbol('cos'),csc=1/sp.Symbol('sin'))[f] if symbolic else FUNC[f]))**power
        else:raise ValueError('invalid atom '+v+' in '+raw)
        if i<len(tokens) and tokens[i]=='^':
            i+=1
            if tokens[i]=='{':power=group()
            else:power=sp.Integer(tokens[i]);i+=1
            e=e**power
        return e
    def unary():
        nonlocal i
        if tokens[i] in ('+','-'):
            v=tokens[i];i+=1;return unary()*(1 if v=='+' else -1)
        return primary()
    def mul():
        nonlocal i
        e=unary()
        while i<len(tokens) and tokens[i] not in ('+','-',')','}'):
            if tokens[i]==r'\cdot':i+=1
            e*=unary()
        return e
    def add():
        nonlocal i
        e=mul()
        while i<len(tokens) and tokens[i] in ('+','-'):
            op=tokens[i];i+=1;e+=mul()*(1 if op=='+' else -1)
        return e
    if not tokens:raise ValueError('empty expression')
    e=add()
    if i!=len(tokens):raise ValueError('unconsumed tokens '+raw)
    return sp.cancel(e) if reduce else e

def displayed_stages(solution):
    for m in MATH.finditer(solution):
        if not m[0].startswith('$$'):continue
        body=m[0][2:-2].replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
        for side in re.split(r'\\\\|=|&',body):
            if side.strip():yield side.strip()

def prompt_expr(prompt):
    parts=MATH.findall(prompt)
    if len(parts)!=1:raise ValueError('one prompt math component required')
    return parts[0].strip('$').rstrip('= ').rstrip('.')

def original_correct(qid,p):
    f=QUESTIONS[qid][':question/answer-fields'][0]
    if ':answer-field/correct' in f:v=f[':answer-field/correct'][':answer/value']
    else:v=r'\tan θ' if qid=='q-65165' else r'\sin x'
    return scale_component(transform(v,ANGLES[qid],p),p['k'])

def authored_easy(p):
    s=atom('cos' if p['mirror'] else 'sin',p);c=atom('sin' if p['mirror'] else 'cos',p)
    num=coeff(p['k'],s+'^2+'+c+'^2')
    # Standard function power is before its argument, never appended to angle.
    s2=atom('cos' if p['mirror'] else 'sin',p,2);c2=atom('sin' if p['mirror'] else 'cos',p,2)
    expr=frac(coeff(p['k'],s2)+'+'+coeff(p['k'],c2),s)
    fact=frac(str(p['k'])+r'\cdot('+s2+'+'+c2+')',s)
    identity=frac(str(p['k'])+r'\cdot 1',s); reduced=frac(str(p['k']),s)
    ans=coeff(p['k'],atom('sec' if p['mirror'] else 'csc',p))
    solution='First, we factor the numerator:\n\n$$\n'+expr+'='+fact+'\n$$\n\n'+NEXT+'\n\n$$\n'+r'\begin{aligned}'+fact+' & ='+identity+r' \\ & ='+reduced+r' \\ & ='+ans+r'\end{aligned}'+'\n$$\n\nHence, we conclude that\n\n$$\n'+expr+'='+ans+'.\n$$'
    return 'Simplify the trigonometric expression $'+expr+'.$',solution,ans

def inferred_solution(qid,p,prompt,ans):
    s=atom('cos' if p['mirror'] else 'sin',p);c=atom('sin' if p['mirror'] else 'cos',p)
    s2=atom('cos' if p['mirror'] else 'sin',p,2);c2=atom('sin' if p['mirror'] else 'cos',p,2)
    if qid=='q-65165':
        fact=frac(s2+'('+c2+'+'+s2+')',c+s)
        ident=frac(s2+r'\cdot 1',c+s)
        cancellation=frac(r'\cancel{'+s+'}'+s,c+r'\cancel{'+s+'}')
        reduced=frac(s,c);opening='First, we factor the numerator:'
    else:
        fact=frac(s2,s+'('+s2+'+'+c2+')')
        ident=frac(s2,s+r'\cdot 1')
        cancellation=frac(r'\cancel{'+s+'}'+s,r'\cancel{'+s+'}')
        reduced=frac(s,'1');opening='First, we factor the denominator:'
    rows=[scale_component(x,p['k']) for x in (fact,ident,cancellation,reduced)]
    return opening+'\n\n$$\n'+prompt_expr(prompt)+'='+rows[0]+'\n$$\n\n'+NEXT+'\n\n$$\n'+r'\begin{aligned}'+rows[0]+''.join(' & ='+x+r' \\' for x in rows[1:])+ ' & ='+ans+r'\end{aligned}'+'\n$$\n\nHence, we conclude that\n\n$$\n'+prompt_expr(prompt)+'='+ans+'.\n$$'

def authored_bank(correct,p,template):
    # Complete operations selected as one bank. These make concrete mistakes at
    # identity, sign, reciprocal and cancellation; no first-valid recipe pool.
    C=parse_math(correct)
    # Direct correct-function display transformations preserve normal trig notation.
    reciprocal=re.sub(r'(?<![A-Za-z])(sin|cos|tan|cot|sec|csc)(?![A-Za-z])',lambda m:{'sin':'csc','cos':'sec','tan':'cot','cot':'tan','sec':'cos','csc':'sin'}[m[1]],correct)
    if '+' in correct:
        # Hard additive families: altering the identity contribution affects first
        # term only; the separately added term is left unchanged.
        base=correct
        if p['k']!=1:base=base[len(str(p['k'])+r'\cdot\left('):-len(r'\right)')]
        first,last=base.split('+',1)
        values=[correct,coeff(p['k'],'-('+first+')+'+last),coeff(p['k'],'2('+first+')+'+last),reciprocal,coeff(p['k'],first+'+1')]
        recipes=['correct','negate_identity_contribution','use_identity_two','invert_ratio_and_reciprocal','drop_added_denominator']
    else:
        identity_wrong=frac(correct,'2') if template in ('q-65166','q-119387','q-65248','q-65249') else (frac('3('+correct+')','2') if template=='q-119381' else '2('+correct+')')
        values=[correct,'-('+correct+')',identity_wrong,reciprocal,'('+correct+')'+atom('sin' if not p['mirror'] else 'cos',p)]
        recipes=['correct','negate_factored_numerator','use_identity_two','invert_final_ratio','duplicate_factored_function']
    if len({sp.srepr(parse_math(v)) for v in values})!=5:raise ValueError('entire authored bank rejected for equivalence')
    return values,recipes

def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+':'+s))
def fingerprint(s):return hashlib.sha256(s.encode()).hexdigest()

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('invalid level')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('radio only')
    rng=random.Random(seed)
    raw=False;observed=False
    if profile:
        if profile=='authored':pass
        elif profile.startswith(('raw:','observed:')):
            raw=profile.startswith('raw:');observed=True;qid=profile.split(':',1)[1]
            if qid not in QUESTIONS:raise ValueError('unknown source profile')
            if template is not None and template!=qid:raise ValueError('profile/template mismatch')
            template=qid
        else:raise ValueError('unknown profile')
    eligible=[q for q,v in TEMPLATES.items() if v['level']==level]
    template=template or rng.choice(eligible)
    if template not in eligible:raise ValueError('template outside level')
    p=dict(parameters) if parameters is not None else {'k':rng.randint(1,12),'mirror':rng.choice([False,True]),'angle':rng.choice(['x','t',r'\theta',r'\phi'])}
    check_parameters(p)
    if template=='easy_identity':prompt,solution,correct=authored_easy(p);source=None
    else:
        source=QUESTIONS[template]
        prompt=render_mask(source[':question/problem'],ANGLES[template],p)
        correct=original_correct(template,p)
        solution=render_mask(source[':question/worked-solution'],ANGLES[template],p) if ':question/worked-solution' in source else inferred_solution(template,p,prompt,correct)
    if observed:
        f=source[':question/answer-fields'][0]
        values=[scale_component(transform(a[':answer/value'],ANGLES[template],p),p['k']) for a in f[':answer-field/choices']]
        recipes=['observed_component_scale_'+str(i) for i in range(5)]
        # Original missing designations are inferred only in completed presentation.
        matches=[i for i,v in enumerate(values) if parse_math(v)==parse_math(correct)]
        if len(matches)!=1:raise ValueError('ambiguous captured bank')
        ci=matches[0]
    else:values,recipes=authored_bank(correct,p,template);ci=0
    if len({sp.srepr(parse_math(v)) for v in values})!=5:raise ValueError('entire bank rejected')
    if parse_math(prompt_expr(prompt))!=parse_math(correct):raise ValueError('prompt answer disagreement')
    task=fingerprint(sp.srepr(parse_math(prompt_expr(prompt),symbolic=True)))
    # Identity includes actual complete displayed content; order, aliases and seed
    # are excluded. Canonical task separately excludes banks/variable aliases.
    shown_solution=None if raw and ':question/worked-solution' not in source else solution
    ident=fingerprint(json.dumps([VERSION,prompt,shown_solution,sorted(values)],ensure_ascii=False))
    fid=uid(ident+':selection')
    answers=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
    if not(raw and ':answer-field/correct' not in source[':question/answer-fields'][0]):field[':answer-field/correct']=[':answer/id',answers[ci][':answer/id']]
    rng.shuffle(answers)
    question={':question/id':uid(ident),':question/problem':prompt,':question/answer-fields':[field]}
    if not(raw and ':question/difficulty' not in source):question[':question/difficulty']=':question.difficulty/'+level
    if shown_solution is not None:question[':question/worked-solution']=shown_solution
    # Raw key-presence parity includes provenance IDs; no new MA IDs are authored.
    if raw:
        question[':db/id']=source[':db/id'];question[':question/math-academy-id']=source[':question/math-academy-id']
        field[':db/id']=source[':question/answer-fields'][0][':db/id']
        for a,old in zip(values,source[':question/answer-fields'][0][':answer-field/choices']):
            next(x for x in answers if x[':answer/value']==a)[':db/id']=old[':db/id']
    denominator=sp.denom(parse_math(prompt_expr(prompt)))
    # Original denominator restriction derived from source rational factors, not
    # reduced answer: cancellation must not enlarge the original expression domain.
    domains={'q-65165':['sin','cos'],'q-65166':['sin'],'q-119379':['sin','cos'],'q-119381':['sin','cos'],'q-119387':['sin'],'q-119392':['sin'],'q-65246':['cos'],'q-65248':['sin','cos'],'q-65249':['cos'],'q-72712':['cos'],'easy_identity':['sin']}
    functions=[MIRROR[x] if p['mirror'] else x for x in domains[template]]
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'seed':seed,'difficulty':level,'template':template,'profile':profile or 'authored','parameters':p,'source':{'database':'math','basis':1356,'lineage':CAPTURE['lineage'],'source_id':template if source else None},'recipes':recipes,'mathematical_fingerprint':task,'content_identity':ident,'domain':[atom(f,p)+' != 0' for f in functions],'evidence_only':observed,'eligible_for_learning':not observed,'raw_attribute_omissions':raw,'authored_level_assignment':template in ('q-65165','q-65166','easy_identity'),'inferred_correct_designation':source is not None and ':answer-field/correct' not in source[':question/answer-fields'][0] and not raw}}

# EASY: authored 24 meaningful tasks: k=1..12, sin/cos denominator. Identity
# collapse + reciprocal, no trig-monomial cancellation or extra sum.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: five rated + two unrated inferred moderate templates; one factoring
# site, identity and monomial cancellation, original powers <=5, scalar <=12.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: three observed numerator templates; same identity/cancellation method
# with an additional surviving term. No common-denominator combination or new
# alternate identity. k=1..12 varies exact simple coefficient arithmetic.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('hard',seed,template,field_type,parameters,profile)

def presentation_label(r):
    """Author-preview label; absent raw difficulty stays visibly unrated."""
    q=r['question'];g=r['generation']
    difficulty=q.get(':question/difficulty')
    level={'easy':'E','moderate':'M','hard':'H'}[difficulty.split('/')[-1]] if difficulty else 'unrated'
    if g['raw_attribute_omissions']:origin='original raw/evidence-only'
    elif g['evidence_only']:origin='observed completed evidence-only'
    else:origin='normal/authored'
    return level+' — '+origin

def markdown(r,include_label=True):
    q=r['question'];out=(['**'+presentation_label(r)+'**',''] if include_label else [])+[q[':question/problem']]
    for f in q.get(':question/answer-fields',[]):
        correct=f.get(':answer-field/correct')
        if correct is None:out += ['\nOriginal correct key absent; no option is designated.']
        for i,a in enumerate(f[':answer-field/choices']):
            mark=''
            if correct and a[':answer/id']==correct[1]:
                mark=' **✓ Correct (inferred)**' if r['generation']['inferred_correct_designation'] else ' **✓ Correct**'
            out.append('\n'+str(i+1)+'. $'+a[':answer/value']+'$'+mark)
    if ':question/worked-solution' in q:out+=['\nWorked solution\n',q[':question/worked-solution']]
    return '\n'.join(out)
def main():
    a=argparse.ArgumentParser();a.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',choices=['markdown','json'],default='markdown');a.add_argument('--template');a.add_argument('--profile');args=a.parse_args()
    levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in levels for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
