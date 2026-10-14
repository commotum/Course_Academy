#!/usr/bin/env python3
"""Frozen-basis general-base logarithm derivatives; local review only.

Observed prose/layout masks and complete banks precede authored extensions.
Raw evidence profiles retain missing attributes; normal records repair them.
No plots, EDB access, registrations or transactions.
"""
import argparse, copy, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).with_suffix('')
KP_ID=17592186096615
KP_UUID='5856f3cc-5423-5a97-b2fd-7f44e0797ec7'
TITLE='Differentiating a Logarithmic Function With a General Base'
VERSION='general-base-log-frozen1356-v2'
X=sp.Symbol('x',positive=True)
CAPTURE=json.loads((HERE/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in CAPTURE['record'][':knowledge-point/questions']}
# Template names retain distinct answer layouts and operative solution chains.
TEMPLATES={
 'linear-log-radio':('easy','q-11903'),
 'quadratic-log-radio':('easy','q-11907'),
 'constant-log-slope':('easy','q-101719'),
 'scaled-log':('easy','q-11900'),
 'exp-explicit-radio':('easy','q-105256'),
 'exp-common-radio':('easy','q-1921'),
 'quadratic-slope':('easy','q-339989'),
 'log-minus-ln':('easy','q-339997'),
 'cubic-slope':('easy','q-339994'),
 'exp-common-blank':('easy','q-340105'),
 'negative-exp-log':('easy','q-340106'),
 'log-ln-exp-derivative':('moderate',None),
 'log-ln-exp-slope':('hard','q-308866'),
}
PARAMETERS={
 'linear-log-radio':{'a':3,'base':5},
 'quadratic-log-radio':{'a':7,'base':9,'legacy_a':3,'legacy_base':5},
 'constant-log-slope':{'constant':7,'a':4,'base':3},
 'scaled-log':{'a':5,'base':4},
 'exp-explicit-radio':{'expbase':7,'base':5,'wrong_expbase':4},
 'exp-common-radio':{'expbase':2,'base':10,'wrong_expbase':4},
 'quadratic-slope':{'a':4,'b':6,'base':3,'point':1},
 'log-minus-ln':{'base':7,'b':3},
 'cubic-slope':{'a':2,'b':3,'base':6,'point':3},
 'exp-common-blank':{'expbase':3,'base':10},
 'negative-exp-log':{'a':3,'base':5},
 'log-ln-exp-derivative':{'a':2,'b':4,'c':5,'base':3},
 'log-ln-exp-slope':{'a':2,'b':4,'c':5,'base':3,'point':1},
}
OPAQUE={'quadratic-log-radio','exp-explicit-radio','exp-common-radio'}
RADIOS={'linear-log-radio','quadratic-log-radio','scaled-log','exp-explicit-radio','exp-common-radio'}

def tex(v): return sp.latex(v).replace(r'\log',r'\ln')
def frac(n,d): return r'\frac{'+str(n)+'}{'+str(d)+'}'
def normal_notation(s):
    """Presentation-only normalization; raw evidence remains byte-exact."""
    s=s.replace(r'\operatorname{log}',r'\log ').replace('⁡','').replace('{log}',r'\log ').replace('logx',r'\log x')
    s=re.sub(r'(?<![A-Za-z\\{])ln',lambda _:r'\ln ',s)
    s=s.replace(r'\log _',r'\log_')
    s=s.replace('Do not round the answer.','Give an exact answer.')
    s=re.sub(r'(?<![A-Za-z0-9])(\d+)\s*e(?![A-Za-z0-9^])',lambda m:m[1]+r'\cdot e',s)
    return s

def expressions(t,p):
    a,b,c,base=[sp.Integer(p.get(k,1)) for k in ('a','b','c','base')]
    lg=sp.log(X)/sp.log(base)
    if t=='scaled-log': f=a*lg
    elif t.startswith('exp-'): f=sp.Integer(p['expbase'])**X+lg
    elif t=='linear-log-radio': f=X-a*lg
    elif t=='quadratic-log-radio': f=X**2-a*lg
    elif t=='constant-log-slope': f=sp.Integer(p['constant'])-a*lg
    elif t=='quadratic-slope': f=a*X**2-b*lg
    elif t=='log-minus-ln': f=lg-b*sp.log(X)
    elif t=='cubic-slope': f=a*X**3+X-b*lg
    elif t=='negative-exp-log': f=-sp.exp(X)+a*lg
    elif t in ('log-ln-exp-slope','log-ln-exp-derivative'): f=a*lg-b*sp.log(X)+c*sp.exp(X)
    else: raise ValueError(t)
    derivative=sp.diff(f,X)
    point=1/sp.log(base) if t=='constant-log-slope' else p.get('point')
    answer=sp.expand(derivative.subs(X,point)) if point is not None else derivative
    return f,derivative,answer,point

def validate_parameters(p,level,t,profile=None):
    if t not in TEMPLATES or TEMPLATES[t][0]!=level: raise ValueError('Wrong template difficulty')
    if set(p)!=set(PARAMETERS[t]): raise ValueError('Exact declared parameter keys required')
    if any(not isinstance(v,int) or isinstance(v,bool) for v in p.values()): raise ValueError('Integer parameters required')
    # Domain guards run before logarithms/CAS. No chain-rule logarithm arguments.
    if not 2<=p['base']<=12: raise ValueError('Logarithm base must be in 2..12 (positive, not one)')
    for k in ('a','b','c','expbase','legacy_a','legacy_base','wrong_expbase'):
        if k in p and not 2<=p[k]<=12: raise ValueError('Coefficient/base slots must be in 2..12')
    if 'common' in t and p['base']!=10: raise ValueError('Common logarithm requires base10')
    if 'point' in p and p['point']!=PARAMETERS[t]['point']: raise ValueError('Retain observed evaluation point')
    if 'constant' in p and not 2<=p['constant']<=12: raise ValueError('Constant outside 2..12')
    if t=='scaled-log' and p['a']==p['base']: raise ValueError('Observed coefficient-as-base bank collision')
    if 'wrong_expbase' in p and p['expbase']==p['wrong_expbase']: raise ValueError('Altered-base replay bank collision')
    if t in ('log-ln-exp-slope','log-ln-exp-derivative') and p['c']<p['b']: raise ValueError('c>=b keeps native zero rejection reliable')
    if profile is not None and profile not in ('raw-source','observed-bank','authored-bank','normal'): raise ValueError('Unknown profile')
    if profile=='authored-bank' and t not in OPAQUE: raise ValueError('Authored bank applies only to radios')

def sample(t,rng):
    p=dict(PARAMETERS[t])
    for k in p:
        if k=='point' or k in ('legacy_a','legacy_base'):continue
        if k=='base' and 'common' in t:continue
        p[k]=rng.randint(2,12)
    return p

# Mask extraction: complete role-bearing fragments are replaced simultaneously.
# This is deliberately NOT a whole-string digit/function-name substitution.
def slots(t):
    """Return source-component -> named variable-slot masks for one backbone."""
    mid=TEMPLATES[t][1]
    if mid is None:return {}
    p=PARAMETERS[t];base=p['base'];a=p.get('a');b=p.get('b');c=p.get('c')
    mapping={}
    # Base-bearing logarithm components (not bare digits).
    for ln in ('ln⁡',r'\ln ',r'\ln',r'\operatorname{ln}⁡',r'\operatorname{ln}'):
        mapping[ln+str(base)]=ln+'@@base@@'
        mapping[ln+'('+str(base)+')']=ln+'(@@base@@)'
    mapping['{log}_{'+str(base)+'}']='{log}_{@@base@@}'
    mapping[r'\log_{'+str(base)+'}']=r'\log_{@@base@@}'
    if t in ('exp-explicit-radio','exp-common-radio','exp-common-blank'):
        eb=p['expbase']
        mapping['{'+str(eb)+'}^{x}']='{@@expbase@@}^{x}'
        for ln in ('ln⁡',r'\operatorname{ln}⁡',r'\operatorname{ln}'):
            mapping[ln+str(eb)]=ln+'@@expbase@@'
            mapping[ln+'('+str(eb)+')']=ln+'(@@expbase@@)'
        if t in RADIOS:mapping['{4}^{x}']='{@@wrong_expbase@@}^{x}'
    if t=='quadratic-log-radio':
        # Unrelated historical 3/(x ln5): evidence-only, independent explicit slots.
        mapping[r'\frac{3}{x\ln 5}']=r'\frac{@@legacy_a@@}{x\ln @@legacy_base@@}'
    coeff = b if t in ('quadratic-slope','cubic-slope','log-minus-ln') else a
    if coeff is not None:
        for fragment in (str(coeff)+'{log}',str(coeff)+r'\log',str(coeff)+r'\operatorname{ln}',str(coeff)+r'\frac',str(coeff)+r'\cdot',str(coeff)+'('+r'\frac'):
            mapping[fragment]='@@'+('b' if t in ('quadratic-slope','cubic-slope','log-minus-ln') else 'a')+'@@'+fragment[len(str(coeff)):]
        for prefix in (r'\frac{',r'-\frac{'):
            mapping[prefix+str(coeff)+'}{']=prefix+'@@'+('b' if t in ('quadratic-slope','cubic-slope','log-minus-ln') else 'a')+'@@}{'
    if t=='scaled-log':
        # Historical log5 is coefficient-as-base, not the supplied base4.
        mapping['ln⁡5']='ln⁡@@a@@'
        mapping[r'\frac{5}{4x}']=r'\frac{@@a@@}{@@base@@x}'
        mapping[r'\frac{5}{x}']=r'\frac{@@a@@}{x}'
    if t=='quadratic-slope':
        mapping['4{x}^{2}']='@@a@@{x}^{2}'
        mapping[r'4\cdot 2x']=r'@@a@@\cdot 2x'
        mapping['8x']='@@two_a@@x';mapping['8(1)']='@@two_a@@(1)'
        mapping['8-']='@@two_a@@-'
    if t=='cubic-slope':
        mapping.pop(r'3\cdot',None)
        mapping[r'3\cdot \frac{1}{xln⁡6}']=r'@@b@@\cdot \frac{1}{xln⁡@@base@@}'
        mapping['2{x}^{3}']='@@a@@{x}^{3}'
        mapping[r'2\cdot 3']=r'@@a@@\cdot 3'
        mapping['6{x}^{2}']='@@three_a@@{x}^{2}'
        mapping['6(3)^{2}']='@@three_a@@(3)^{2}'
        mapping['55-']='@@cubic_value@@-'
        for ln in ('ln⁡',r'\operatorname{ln}'):
            mapping[r'\frac{1}{'+ln+'6}']=r'\frac{@@bthird_num@@}{@@bthird_den@@'+ln+'@@base@@}'
    if t=='constant-log-slope':
        mapping['7-4']='@@constant@@-@@a@@'
        mapping[r'\frac{\text{d}}{\text{d}x}(7)']=r'\frac{\text{d}}{\text{d}x}(@@constant@@)'
        mapping['=-4.']='=-@@a@@.'
    if t=='log-ln-exp-slope':
        mapping[r'4\operatorname{ln}']=r'@@b@@\operatorname{ln}'
        mapping[r'\frac{4}{x}']=r'\frac{@@b@@}{x}'
        mapping[r'\frac{4}{1}']=r'\frac{@@b@@}{1}'
        mapping['-4+5e']='-@@b@@+@@c@@e'
        mapping['5{e}']='@@c@@{e}'
    return mapping

MASKS={}
for t,(level,mid) in TEMPLATES.items():
    if mid is None:continue
    replacements=slots(t)
    # Longest complete-component matches consume nested slots once, simultaneously.
    regex=re.compile('|'.join(re.escape(k) for k in sorted(replacements,key=len,reverse=True)))
    def mask(value):
        for _ in range(4):
            updated=regex.sub(lambda m:replacements[m[0]],value)
            if updated==value:return value
            value=updated
        return value
    source=SOURCES[mid]
    MASKS[t]={'problem':mask(source[':question/problem'])}
    if ':question/worked-solution' in source:MASKS[t]['solution']=mask(source[':question/worked-solution'])
    MASKS[t]['choices']=[mask(a[':answer/value']) for f in source.get(':question/answer-fields',[]) for a in f[':answer-field/choices']]

def render(s,t,p):
    v={**p,'two_a':2*p.get('a',1),'three_a':3*p.get('a',1),'cubic_value':27*p.get('a',1)+1}
    third=sp.Rational(p.get('b',3),3);v.update(bthird_num=third.p,bthird_den='' if third.q==1 else third.q)
    result=re.sub(r'@@([a-z_]+)@@',lambda m:str(v[m[1]]),s)
    if '@@' in result:raise ValueError('Unresolved variable mask')
    return result

FORMULA='To differentiate a logarithm with base $a,$ we use the formula\n\n$$\n'+r'\frac{\text{d}}{\text{d}x}(\log_a x)=\frac{1}{x\ln a}.'+'\n$$'
def authored_solution(t,p):
    """Missing solutions/level only; observed source chains use MASKS."""
    base,a,b,c=p['base'],p.get('a',1),p.get('b',1),p.get('c',1)
    if t=='linear-log-radio':
        f='x-'+str(a)+r'\log_{'+str(base)+'}x'
        operation='1-'+str(a)+r'\cdot '+frac(1,'x'+r'\ln '+str(base))
    elif t=='quadratic-log-radio':
        f='x^{2}-'+str(a)+r'\log_{'+str(base)+'}x'
        operation='2x-'+str(a)+r'\cdot '+frac(1,'x'+r'\ln '+str(base))
    elif t=='log-ln-exp-derivative':
        f=str(a)+r'\log_{'+str(base)+'}x-'+str(b)+r'\ln x+'+str(c)+'e^{x}'
        operation=frac(a,'x'+r'\ln '+str(base))+'-'+frac(b,'x')+'+'+str(c)+'e^{x}'
    else:raise ValueError(t)
    _,d,_,_=expressions(t,p)
    return FORMULA+'\n\nTherefore,\n\n$$\n'+r'\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}('+f+r') \\ & ='+operation+r' \\ & ='+tex(d)+r'.\end{aligned}'+'\n$$'

def authored_values(t,p):
    """Each complete bank follows the actual derivative operations."""
    _,d,_,_=expressions(t,p);a=sp.Integer(p.get('a',1));base=sp.Integer(p['base']);lg=a/(X*sp.log(base))
    if t=='quadratic-log-radio':values=[d,2*X-1/(X*sp.log(base)),X-lg,2*X+lg,2*X-a/X]
    elif t.startswith('exp-'):
        eb=sp.Integer(p['expbase']);ex=eb**X;term=1/(X*sp.log(base))
        values=[d,ex*sp.log(eb)+1/sp.log(base),ex+term,ex*sp.log(eb)+1/X,ex*sp.log(eb)-term]
    else:raise ValueError(t)
    return [tex(v) for v in values]

def complete_bank_math(t,p,profile):
    """Whole operation banks, constructed before displayed choices.

    Analytical base/coefficient guards and exact expanded pair differences
    reject the entire instance. Profiles never exchange individual members.
    """
    _,d,_,_=expressions(t,p)
    a=sp.Integer(p.get('a',1));B=sp.Integer(p['base']);L=1/(X*sp.log(B))
    if t=='linear-log-radio':bank=[-a*L,a*L,X-a*L,1-L,d]
    elif t=='quadratic-log-radio':
        bank=[d,2*X-L,X-a*L,2*X+a*L,2*X-a/X] if profile=='authored-bank' else [d,sp.Integer(p['legacy_a'])/(X*sp.log(p['legacy_base'])),2*X-L,X-L,X-a*L]
    elif t=='scaled-log':bank=[L,a/(B*X),a/(X*sp.log(a)),d,a/X]
    elif t in ('exp-explicit-radio','exp-common-radio'):
        E=sp.Integer(p['expbase']);C=E**X*sp.log(E)
        last=C-L if profile=='authored-bank' else sp.Integer(p['wrong_expbase'])**X*sp.log(E)+L
        bank=[d,C+1/sp.log(B),E**X+L,C+1/X,last]
    else:return []
    if len(bank)!=5 or any(sp.expand(sp.expand_log(bank[i]-bank[j],force=True))==0 for i in range(5) for j in range(i)):
        raise ValueError('Reject whole equivalent operation bank')
    return bank

def fingerprint(t,p):
    _,d,_,point=expressions(t,p)
    # Constants, raw layout, banks and legacy parameters do not create new tasks.
    data=[sp.srepr(sp.expand(sp.expand_log(d,force=True))),str(point) if point is not None else None]
    return hashlib.sha256(json.dumps(data).encode()).hexdigest()

def assemble(level,t,p,seed,profile):
    raw=profile=='raw-source';mid=TEMPLATES[t][1];source=SOURCES.get(mid)
    _,derivative,answer,point=expressions(t,p)
    if t=='log-ln-exp-derivative':
        prompt='Given that $y='+str(p['a'])+r'\log_{'+str(p['base'])+'}x-'+str(p['b'])+r'\ln x+'+str(p['c'])+r'e^{x}$, find $\frac{\text{d}y}{\text{d}x}.$'+'\n\n'+r'$\frac{\text{d}y}{\text{d}x}=$'+'\n{{field-1}}.'
        solution=authored_solution(t,p);values=[tex(answer)]
    else:
        prompt=render(MASKS[t]['problem'],t,p)
        solution=render(MASKS[t]['solution'],t,p) if 'solution' in MASKS[t] else None
        values=[render(s,t,p) for s in MASKS[t]['choices']]
        if not raw:
            if solution is None:solution=authored_solution(t,p)
            if not values:
                values=[tex(answer)];prompt+='\n\nThe instantaneous rate of change is\n{{field-1}}.'
            if profile=='authored-bank':values=authored_values(t,p)
    if not raw:
        prompt=normal_notation(prompt);solution=normal_notation(solution);values=[normal_notation(s) for s in values]
    # Exact output distinguishes bank/presentation; shuffling never changes IDs.
    attrs={'problem':prompt,'solution':solution,'values':sorted(values),'level':None if raw and ':question/difficulty' not in source else level,'raw_fields_present':not raw or ':question/answer-fields' in source,'raw_correct_present':not raw or bool(source.get(':question/answer-fields') and ':answer-field/correct' in source[':question/answer-fields'][0])}
    content=hashlib.sha256(json.dumps([VERSION,attrs],sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    qid=str(uuid.uuid5(uuid.UUID(KP_UUID),content));qid_uuid=uuid.UUID(qid)
    q={':question/id':qid,':question/problem':prompt}
    if solution is not None:q[':question/worked-solution']=solution
    if not raw or ':question/difficulty' in source:q[':question/difficulty']=':question.difficulty/'+level
    sf=source.get(':question/answer-fields',[None])[0] if source else None
    if not raw or sf is not None:
        kind='radio' if t in RADIOS else 'blank';key=sf[':answer-field/key'] if sf else 'field-1'
        fid=str(uuid.uuid5(qid_uuid,'field/'+key));choices=[]
        for index,value in enumerate(values):
            aid=str(uuid.uuid5(uuid.UUID(fid),value))
            choices.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':value})
        # All complete radio banks have their correct recipe at this index.
        correct_index=0 if profile=='authored-bank' else {
            'linear-log-radio':4,'quadratic-log-radio':0,'scaled-log':3,
            'exp-explicit-radio':0,'exp-common-radio':0}.get(t,0)
        correct=choices[correct_index][':answer/id']
        if kind=='radio':random.Random(seed).shuffle(choices)
        field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':choices}
        if not raw or ':answer-field/correct' in sf:field[':answer-field/correct']=[':answer/id',correct]
        q[':question/answer-fields']=[field]
    eligible=not raw and not (profile=='observed-bank' and t in OPAQUE)
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{
        'version':VERSION,'seed':seed,'template':t,'parameters':p,'bank_profile':profile,
        'parameter_fingerprint':fingerprint(t,p),'content_fingerprint':content,
        'source':{k:CAPTURE[k] for k in ('database','basis','lineage')},'source_question_ids':[mid] if mid else [],
        'authored_extension':t=='log-ln-exp-derivative' or profile=='authored-bank' or t in ('linear-log-radio','quadratic-log-radio','constant-log-slope'),
        'evidence_only':not eligible,'eligible_for_learning':eligible,
        'domain':'x>0; logarithm base positive and unequal to1; integer base2..12',
        'python_version':sys.version.split()[0],'sympy_version':sp.__version__,'plot_rating':'none',
        'repairs':[] if raw else ['source notation normalization']+(['visible multiplication in Euler scalar'] if t=='log-ln-exp-slope' else [])+(['exact-answer wording'] if 'Do not round' in (source or {}).get(':question/problem','') else []) + (['authored fields/level/solution/key from derivative'] if t in ('linear-log-radio','quadratic-log-radio','constant-log-slope') else []),
    }}

# EASY — observed source family masks plus explicit anomaly completion.
# MODERATE — authored three-rule symbolic derivative, without point evaluation.
# HARD — observed three-rule derivative and substitution at x=1.
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    rng=random.Random(seed)
    eligible=[t for t,(l,_) in TEMPLATES.items() if l==level and (field_type is None or field_type==('radio' if t in RADIOS else 'blank'))]
    if not eligible or template is not None and template not in eligible:raise ValueError('No eligible template/field type at this level')
    t=template or rng.choice(eligible)
    if profile is None:profile='authored-bank' if t in OPAQUE else 'normal'
    if profile=='normal' and t in OPAQUE:profile='authored-bank'
    if profile in ('raw-source','observed-bank') and TEMPLATES[t][1] is None:raise ValueError('Authored template has no observed source')
    for _ in range(128):
        p=dict(parameters) if parameters is not None else sample(t,rng)
        try:validate_parameters(p,level,t,profile)
        except ValueError:
            if parameters is not None:raise
            continue
        # Reject entire complete profile on any collision before assembly.
        if t in RADIOS:
            if t=='scaled-log' and p['a']==p['base']:continue
        try:complete_bank_math(t,p,profile)
        except ValueError:
            if parameters is not None:raise
            continue
        return assemble(level,t,p,seed,profile)
    raise ValueError('Whole-bank rejection exhausted bounded sampler')

def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
    q=r['question'];lines=[q[':question/problem'],'']
    for f in q.get(':question/answer-fields',[]):
        lines.extend('- $'+a[':answer/value']+'$'+(' **correct**' if f.get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else '') for a in f[':answer-field/choices'])
    if ':question/worked-solution' in q:lines+=['','**Worked solution**','',q[':question/worked-solution']]
    return '\n'.join(lines)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--field-type',choices=['radio','blank']);args=ap.parse_args()
    if args.count<1:ap.error('Positive count required')
    if args.template and args.difficulty=='all':ap.error('Template needs a specific difficulty')
    levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty];records=[]
    for level in levels:
        used=set();batch=[]
        for i in range(args.count*200):
            if len(batch)==args.count:break
            r=generate(level,args.seed+i,args.template,args.field_type,profile=args.profile);fp=r['generation']['parameter_fingerprint']
            if fp not in used:used.add(fp);batch.append(r)
        if len(batch)<args.count:raise ValueError('Requested count exceeds bounded meaningful task variety')
        records+=batch
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
