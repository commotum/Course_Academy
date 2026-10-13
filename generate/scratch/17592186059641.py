#!/usr/bin/env python3
"""GCF factoring followed by sin²+cos²=1; math basis 1356, no EDB writes.

Observed source masks retain the complete prompt, bank and ordered solution;
their complete function atoms and argument slots support sine/cosine symmetry.
Raw profiles preserve missing attributes and source errors as evidence only.
Repaired profiles separately normalize function typography, correct two solution
errors, and explicitly infer the missing fields. Default banks are authored
operation banks, never a pooled selection of convenient wrong values.

Easy: one monomial GCF, degree 1–3, coefficient ±1–5, two terms.
Moderate: one GCF plus a residual term, coefficient ±1–4; three terms.
Hard (authored missing level): two disjoint GCF groups, odd degree 1 or 3,
coefficient ±1–4; four terms. No quotients, reciprocals or angle identities.
Independent displayed-math validation and native grading: 17592186059641/validate.py.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import random
import re
import uuid
import sympy as sp

KP_ID = 17592186059641
KP_UUID = '3332b534-bd04-5e86-995e-1e6d691d8e1b'
TITLE = 'Simplifying an Expression by Factoring and Using the Pythagorean Identity'
VERSION = 'factoring-pythagorean-1'
ROOT = Path(__file__).with_suffix('')
CAPTURE = json.loads((ROOT/'source.json').read_text())
SOURCES = {q[':question/math-academy-id']: q for q in CAPTURE['record'][':knowledge-point/questions']}
S, C = sp.symbols('S C')
ANGLES = (r'\theta', 'x', 't', r'\alpha')
COEFFICIENTS = (-4,-3,-2,-1,1,2,3,4)
MONOMIALS = ((1,0),(2,0),(3,0),(0,1),(0,2),(0,3),(1,1),(1,2),(2,1))
SOURCE_LEVELS = {k: q.get(':question/difficulty', {':db/ident': ':question.difficulty/easy'})[':db/ident'].split('/')[-1] for k,q in SOURCES.items()}
ERRORS = {'q-119362': 'Wrong cos exponent in the left side of the identity block: 2 should be 3.',
          'q-65229': 'Missing angle on cos squared in the identity block.'}

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',',':')).encode()).hexdigest()

def identity(value):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, VERSION+':'+value))

def source_slots(text, angle, swap):
    """Render whole function-name and argument slots, never numeric text fits.

    The source bank is a parameterized expression pattern; its error intention
    is not inferred. Angle aliases are presentation only; symmetry changes the
    assessed polynomial. Literal source whitespace survives raw replay.
    """
    old = r'\theta' if r'\theta' in text else ('θ' if 'θ' in text else 'x')
    if old == 'x':
        text = re.sub(r'(?<![A-Za-z\\])x(?![A-Za-z])', lambda _: angle, text)
    else:
        text = text.replace(old, angle)
    if swap:
        text = re.sub(r'(\\operatorname\{)(sin|cos)(\})|(\\)(sin|cos)(?![a-z])|(\{)(sin|cos)(\})',
                      lambda m: (m[1] or m[4] or m[6])+({'sin':'cos','cos':'sin'}[m[2] or m[5] or m[7]])+(m[3] or m[8] or ''), text)
    return text

ATOM = re.compile(r'(?:\\operatorname\{(sin|cos)\}|\\(sin|cos)|\{(sin|cos)\})(?:\^\{?(\d+)\}?)?[\s⁡]*(?:\{)?(\\theta|\\alpha|θ|x|t)(?:\})?')

def normalize(text):
    """Typography only. Missing arguments require a separate mathematical repair."""
    def render(m):
        name = m[1] or m[2] or m[3]
        power = '' if not m[4] or m[4]=='1' else '^{'+m[4]+'}'
        angle = r'\theta' if m[5]=='θ' else m[5]
        return '\\'+name+power+'{'+angle+'}'
    return ATOM.sub(render,text)

def source_text(text, source_id, p, repaired=False, solution=False):
    if repaired and solution:
        if source_id=='q-119362':
            text=text.replace(r'\begin{aligned}{cos}^{2}',r'\begin{aligned}{cos}^{3}')
        if source_id=='q-65229':
            text=text.replace('{cos}^{2})','{cos}^{2}⁡'+r'\theta )')
    text=source_slots(text,p['angle'],p['swap'])
    return normalize(text) if repaired else text

def monomial(p,q,angle):
    return ''.join('\\'+fn+('' if power==1 else '^{'+str(power)+'}')+'{'+angle+'}'
                   for fn,power in (('sin',p),('cos',q)) if power) or '1'

def term(a,p,q,angle):
    m=monomial(p,q,angle)
    if m=='1': return str(a)
    return ('' if a==1 else '-' if a==-1 else str(a))+m

def join(terms):
    return terms[0]+''.join(t if t.startswith('-') else '+'+t for t in terms[1:])

def tex_expr(e,angle):
    poly=sp.Poly(sp.expand(e),S,C)
    return join([term(int(a),p,q,angle) for (p,q),a in poly.terms()])

def build_authored(level,p):
    angle=p['angle']; a=p['a']; u=p['p']; v=p['q']; b=p.get('b',0)
    factor=term(a,u,v,angle)
    pair=monomial(2,0,angle)+'+'+monomial(0,2,angle)
    factored=factor+r'\cdot('+pair+')'
    substituted=factor+r'\cdot 1'
    F=a*S**u*C**v
    prompt_terms=[term(a,u+2,v,angle),term(a,u,v+2,angle)]
    stages=[]
    if level=='easy':
        answer=F; prompt_poly=F*(S*S+C*C)
        recipes=[answer,2*answer,-answer,answer*(S*S+C*C-1),F*(S*S-C*C)]
    elif level=='moderate':
        family=p['family']
        ru,rv=(v,u) if family=='opposite' else (u,v) if family=='same' else (v,u)
        residual=term(b,ru,rv,angle); R=b*S**ru*C**rv
        prompt_terms.append(residual); prompt_poly=F*(S*S+C*C)+R
        factored=join([factored,residual]); substituted=join([substituted,residual])
        collected=join([factor,residual]); stages.append(collected)
        answer=sp.Integer(a) if family=='complement' else F+R
        recipes=[answer,F-R,-F+R,F*(S*S-C*C)+R,2*F+R]
        if family=='same': recipes=[answer,F-R,-answer,F*(S*S-C*C)+R,F+2*R]
        if family=='complement': recipes=[answer,2*a,-a,0,F-R]
    else:
        n=p['n']; G=b*C**n; prompt_poly=F*(S*S+C*C)+G*(S*S+C*C)
        second=term(b,0,n,angle)
        prompt_terms += [term(b,2,n,angle),term(b,0,n+2,angle)]
        factored=join([factored,second+r'\cdot('+pair+')'])
        substituted=join([substituted,second+r'\cdot 1'])
        answer=F+G; recipes=[answer,F-G,-F+G,F*(S*S-C*C)+G,F+G*(S*S-C*C)]
    expr=join(prompt_terms); final=tex_expr(answer,angle)
    rows=[factored+' & ='+substituted]+[' & ='+r for r in stages]+[' & ='+final]
    solution='First, we factor the expression:\n\n$$\n'+expr+'='+factored+'\n$$\n\nThen, we use $'+pair+'=1$ to simplify the expression in the parentheses:\n\n$$\n'+r'\begin{aligned}'+' \\\\ '.join(rows)+r'\end{aligned}'+'\n$$\n\nHence, we conclude that\n\n$$\n'+expr+'='+final+'.\n$$'
    bank=[tex_expr(r,angle) for r in recipes]
    # Whole-bank rejection, including every complete trig polynomial value.
    basis=sp.groebner([S*S+C*C-1],S,C)
    if any(basis.reduce(sp.expand(x-y))[1]==0 for i,x in enumerate(recipes) for y in recipes[:i]):
        raise ValueError('Entire bank is ambiguous')
    return 'Simplify the trigonometric expression $'+expr+'.$',solution,bank,sp.expand(prompt_poly)

def guard(level,p):
    if p.get('angle') not in ANGLES: raise ValueError('Unsupported angle')
    required={'angle','a','p','q'} | ({'b','family'} if level=='moderate' else {'b','n'} if level=='hard' else set())
    if set(p)!=required: raise ValueError('Unexpected or missing parameters')
    for key in required-{'angle','family'}:
        if type(p[key]) is not int: raise ValueError('Integer parameters required')
    if level=='easy':
        if (p['p'],p['q']) not in MONOMIALS or not 1<=abs(p['a'])<=5: raise ValueError('Easy workload bounds')
    elif level=='moderate':
        if p['a'] not in COEFFICIENTS or p['b'] not in COEFFICIENTS: raise ValueError('Moderate coefficient bounds')
        if p['family'] in ('opposite','same'):
            if (p['p'],p['q']) not in ((1,0),(0,1)): raise ValueError('Moderate linear factor required')
            if p['family']=='same' and (p['a']+p['b']==0 or p['a']-p['b']==-(p['a']+p['b'])): raise ValueError('Canceled factor')
        elif p['family']=='complement':
            if (p['p'],p['q']) not in ((2,0),(0,2)) or p['a']!=p['b']: raise ValueError('Complement workload bounds')
        else: raise ValueError('Unknown moderate family')
    elif level=='hard':
        if p['a'] not in COEFFICIENTS or p['b'] not in COEFFICIENTS or p['p'] not in (1,3) or p['q']!=0 or p['n'] not in (1,3): raise ValueError('Hard two-factor workload bounds')
    else: raise ValueError('Unknown level')

def sample(level,rng):
    if level=='easy':
        u,v=rng.choice(MONOMIALS)
        return {'angle':rng.choice(ANGLES),'a':rng.choice(tuple(range(-5,0))+tuple(range(1,6))),'p':u,'q':v}
    if level=='moderate':
        family=rng.choice(('opposite','same','complement')); a=rng.choice(COEFFICIENTS)
        u,v=rng.choice(((2,0),(0,2)) if family=='complement' else ((1,0),(0,1)))
        b=a if family=='complement' else rng.choice(COEFFICIENTS)
        return {'angle':rng.choice(ANGLES),'a':a,'b':b,'p':u,'q':v,'family':family}
    return {'angle':rng.choice(ANGLES),'a':rng.choice(COEFFICIENTS),'b':rng.choice(COEFFICIENTS),'p':rng.choice((1,3)),'q':0,'n':rng.choice((1,3))}

def assemble(question,values,correct_index,field_type,meta,seed,has_correct=True):
    # Stable identities include the full fixed solution and complete unordered bank.
    content=digest({'question':question,'bank':sorted(values),'field_type':field_type,'correct':correct_index if has_correct else None})
    qid=identity(content); fid=identity(content+':selection')
    answers=[{':answer/id':identity(content+':selection:'+value),':answer/type':':answer.type/math',':answer/value':value} for value in values]
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/'+field_type,':answer-field/choices':answers}
    if has_correct: field[':answer-field/correct']=[':answer/id',answers[correct_index][':answer/id']]
    if field_type=='radio': random.Random(seed).shuffle(answers)
    question={**question,':question/id':qid,':question/answer-fields':[field]}
    meta.update({'version':VERSION,'seed':seed,'content_hash':content,'evidence_only':meta.get('evidence_only',False),'eligible_for_learning':not meta.get('evidence_only',False),
                 'source':{k:CAPTURE[k] for k in ('database','basis','lineage')},'dependencies':{'sympy':sp.__version__},'domain':'All real angles; sin²(angle)+cos²(angle)=1.', 'plots':'none'})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':meta}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'): raise ValueError('Unknown difficulty')
    if profile and profile.startswith(('raw:','repaired:')):
        mode,sid=profile.split(':',1)
        if sid not in SOURCES or SOURCE_LEVELS[sid]!=level: raise ValueError('Source level/profile mismatch')
        if template not in (None,'source_'+sid) or field_type not in (None,'radio'): raise ValueError('Source template/layout mismatch')
        src=SOURCES[sid]; original_angle=r'\theta' if r'\theta' in src[':question/problem'] else ('θ' if 'θ' in src[':question/problem'] else 'x')
        p={'angle':original_angle,'swap':False} if parameters is None else dict(parameters)
        if set(p)!={'angle','swap'} or p['angle'] not in ANGLES+('θ',) or type(p['swap']) is not bool: raise ValueError('Source symbol slots')
        repaired=mode=='repaired'
        q={':question/problem':source_text(src[':question/problem'],sid,p,repaired)}
        if not repaired:q[':question/math-academy-id']=src[':question/math-academy-id']
        if ':question/difficulty' in src or repaired: q[':question/difficulty']=':question.difficulty/'+level
        if ':question/worked-solution' in src:
            q[':question/worked-solution']=source_text(src[':question/worked-solution'],sid,p,repaired,True)
        f=src[':question/answer-fields'][0]
        values=[source_text(a[':answer/value'],sid,p,repaired) for a in f[':answer-field/choices']]
        has_correct=':answer-field/correct' in f
        if has_correct:
            index=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][':answer/id'])
        else: index=0 if sid=='q-65163' else 4
        if repaired and ':question/worked-solution' not in src:
            authored={'angle':r'\theta' if p['angle']=='θ' else p['angle'],'a':1,'p':0,'q':1} if sid=='q-65163' else {'angle':p['angle'],'a':1,'p':2,'q':1}
            if p['swap']: authored['p'],authored['q']=authored['q'],authored['p']
            _,q[':question/worked-solution'],_,_=build_authored('easy',authored)
        # Mathematical-task key reads the actual displayed expression independently.
        from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
        def polynomial(text):
            text=ATOM.sub(lambda m: (m[1] or m[2] or m[3])[0].upper()+'**'+(m[4] or '1')+' ',text).replace('s','S').replace('c','C')
            return sp.expand(parse_expr(text.strip().rstrip('.'),local_dict={'S':S,'C':C}, transformations=standard_transformations+(implicit_multiplication_application,)))
        poly=polynomial(q[':question/problem'].split('$')[1])
        return assemble(q,values,index,'radio',{'template':'source_'+sid,'profile':profile,'bank_profile':profile,'parameters':p,'source_ids':[sid],
                        'mathematical_fingerprint':digest(str(poly)),'evidence_only':not repaired,'raw_source_errors':[ERRORS[sid]] if sid in ERRORS and not repaired else [],
                        'repairs':([ERRORS[sid]] if sid in ERRORS else [])+(['Inferred missing correct value, easy level and authored solution'] if not has_correct else []) if repaired else [],
                        'interpretation_limit':'Complete bank symmetry is observed-pattern algebra, not recovered distractor intentions.'},seed,has_correct or repaired)
    expected={'easy':'one_gcf','moderate':'gcf_residual','hard':'two_gcf'}[level]
    if template not in (None,expected) or profile not in (None,'authored_operations'): raise ValueError('Unknown template/profile')
    kind=field_type or 'radio'
    if kind not in ('radio','blank'): raise ValueError('Unsupported field type')
    rng=random.Random(seed)
    for attempt in range(1000):
        p=dict(parameters) if parameters is not None else sample(level,rng)
        try:
            guard(level,p); prompt,solution,values,poly=build_authored(level,p)
        except ValueError:
            if parameters is not None: raise
            continue
        if kind=='blank': prompt+='\n\n{{selection}}'; values=values[:1]
        operations=['F','2F','-F','F*(sin²+cos²-1)','F*(sin²-cos²)']
        if level=='moderate':
            operations={'opposite':['F+R','F-R','-F+R','F*(sin²-cos²)+R','2F+R'],
                        'same':['F+R','F-R','-(F+R)','F*(sin²-cos²)+R','F+2R'],
                        'complement':['a','2a','-a','0','F-R']}[p['family']]
        elif level=='hard':operations=['F+G','F-G','-F+G','F*(sin²-cos²)+G','F+G*(sin²-cos²)']
        return assemble({':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level},values,0,kind,
                        {'template':expected,'profile':'authored_operations','bank_profile':'authored_operations' if kind=='radio' else None,'parameters':p,
                         'source_ids':list(SOURCES),'mathematical_fingerprint':digest(str(poly)),'authored':True,
                         'recipe_operations':operations[:1] if kind=='blank' else operations,
                         'recipe_definitions':'F=a sin^p(angle) cos^q(angle); R=b times the stated residual monomial; G=b cos^n(angle).'},seed)
    raise RuntimeError('No eligible complete bank')

# Easy: a single monomial GCF and one Pythagorean substitution.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('easy',seed,template,field_type,parameters,profile)

# Moderate: source-supported third residual term, collection or complementary squares.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('moderate',seed,template,field_type,parameters,profile)

# Hard: authored same-KP double GCF, with two identity substitutions.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
    q=record['question']; f=q[':question/answer-fields'][0]
    difficulty=q.get(':question/difficulty','unrated (original difficulty absent)').split('/')[-1]
    meta=record['generation']
    origin='raw source evidence' if meta.get('evidence_only') else ('repaired source' if meta['template'].startswith('source_') else 'authored extension')
    correct=f.get(':answer-field/correct',[None,None])[1]
    rows=['**'+difficulty+' · '+origin+' · '+meta['template']+'**','',q[':question/problem']]
    rows+=['- $'+a[':answer/value']+'$'+(' **(correct)**' if a[':answer/id']==correct else '') for a in f[':answer-field/choices']]
    if correct is None:rows+=['','Original correct designation: **absent**.']
    if ':question/worked-solution' in q: rows+=['',q[':question/worked-solution']]
    return '\n'.join(rows)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--difficulty',choices=('easy','moderate','hard','all'),default='all')
    ap.add_argument('--seed',type=int,default=0); ap.add_argument('--count',type=int,default=1)
    ap.add_argument('--format',choices=('json','markdown'),default='markdown'); ap.add_argument('--template'); ap.add_argument('--profile'); ap.add_argument('--field-type',choices=('radio','blank'))
    args=ap.parse_args(); levels=('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,)
    records=[generate(l,args.seed+i,args.template,args.field_type,profile=args.profile) for l in levels for i in range(args.count)]
    print(json.dumps(records,ensure_ascii=False,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__': main()
