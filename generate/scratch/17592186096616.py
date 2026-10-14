#!/usr/bin/env python3
"""Basis-1356 logarithmic tangent slopes, source masks and authored M/H calibration.

Easy: all thirteen source-shaped families, with repaired/completed normal records.
Moderate: three terms ln + quadratic - linear, nonunit integer input (2..4).
Hard: three terms base logarithm + quadratic - linear, x=s/ln(b), s=2..4.
Every difficulty uses termwise differentiation followed by point evaluation.
Opaque raw banks are public evidence-only profiles, never sampled as normal banks.
"""
import argparse,hashlib,json,random,re,sys,uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186096616
KP_UUID='cef7fc21-23f4-5d6a-a208-9963ef23c784'
TITLE='Calculating the Slope of the Tangent Line of a Logarithmic Function at a Point'
VERSION='log-tangent-frozen1356-v2'
HERE=Path(__file__).with_suffix('')
CASES=json.loads((HERE/'source-cases.json').read_text())
MASKS=json.loads((HERE/'masks.json').read_text())
SOURCE=json.loads((HERE/'source.json').read_text())
X=sp.Symbol('x',positive=True)
SUPPORTED_LEVELS=('easy','moderate','hard')
TEMPLATES={c['template']:'easy' for c in CASES}
D=r'\frac{\text{d}}{\text{d}x}'
DY=r'\frac{\text{d}y}{\text{d}x}'
INTRO='To find the slope of the tangent at a given point, we have to find $'+DY+'$ at that point.\n\nTaking the derivative, we have\n\n'
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),v))
def tex(v):
    # Explicit multiplication prevents the engine reading 8e+4 as scientific notation.
    s=sp.latex(sp.sympify(v),ln_notation=True)
    return re.sub(r'(\d) e(?=[ +\-]|$)',r'\1\\cdot e',s)
def case(t):return next(c for c in CASES if c['template']==t)
def terms(t,p):
    a=p.get('a',1);c=p.get('c',1);k=p.get('k',1);b=p.get('b',2);lb=sp.log(X)/sp.log(b)
    return {
    'rational_ln_radio':[(-sp.Rational(p.get('n',1),p.get('d',1)),sp.log(X))],
    'two_logs_radio':[(1,lb),(c,sp.log(X))],
    'exp_base_log_fieldless':[(a,sp.exp(X)),(-c,lb)],
    'quadratic_ln_blank':[(a,X**2),(c,sp.log(X))],
    'ln_exp_base_blank':[(a,sp.log(X)),(-c,sp.Integer(b)**X)],
    'negative_exp_log_blank':[(-a,sp.exp(X)),(c,lb)],
    'log_exp_base_fieldless':[(a,lb),(1,sp.Integer(b)**X)],
    'linear_log_reciprocal_radio':[(a,X),(-k,sp.Integer(1)),(c,lb)],
    'ln_quadratic_linear_radio':[(a,sp.log(X)),(c,X**2),(-k,X)],
    'cubic_log_blank':[(a,X**3),(-c,lb)],
    'log_quadratic_linear_blank':[(a,lb),(c,X**2),(-k,X)],
    'exp_log_constant_blank':[(a,sp.exp(X)),(-c,lb),(k,sp.Integer(1))],
    'common_log_cubic_radio':[(a,lb),(1,X**3),(-k,sp.Integer(1))]}[t]
def data(t,p):
    parts=terms(t,p);f=sum(c*v for c,v in parts);d=sp.diff(f,X)
    x0=sp.Integer(p['s'])/sp.log(p['b']) if 's' in p else 1/sp.log(p['b']) if t=='linear_log_reciprocal_radio' else sp.sympify(p['t'])
    return parts,f,d,x0,sp.expand(d.subs(X,x0),log=False)
def bounds(level,t,p,raw=False):
    expected=set(case(t)['parameters'])
    if level=='hard' and not raw:expected.remove('t');expected.add('s')
    if set(p)!=expected or any(type(v)!=int for v in p.values()):raise ValueError('exact integer parameter keys required')
    if 'b' in p and not (p['b']>0 and p['b']!=1):raise ValueError('log base must be positive and not 1')
    for k,v in p.items():
        if k=='b':
            if t=='common_log_cubic_radio' and v!=10:raise ValueError('common log has base ten')
            if t!='common_log_cubic_radio' and not 2<=v<=9:raise ValueError('base 2..9')
        elif k in ('s','t'):
            if not 1<=v<=4:raise ValueError('positive point parameter 1..4')
        elif not 1<=v<=12:raise ValueError('positive coefficient 1..12')
    if t=='rational_ln_radio' and (sp.gcd(p['n'],p['d'])!=1 or p['n']==p['d']):raise ValueError('reduced nonunit rational')
    if raw or level=='easy':
        if t in ('rational_ln_radio','two_logs_radio','ln_quadratic_linear_radio','log_quadratic_linear_blank') and p['t']!=1:raise ValueError('easy source family point one')
    elif level=='moderate':
        if t!='ln_quadratic_linear_radio' or not 2<=p['t']<=4:raise ValueError('moderate three natural-log terms, point 2..4')
        if any(p[k]>9 for k in ('a','c','k')):raise ValueError('moderate coefficients 1..9')
    elif level=='hard':
        if t!='log_quadratic_linear_blank' or not 2<=p['s']<=4:raise ValueError('hard reciprocal-log point 2..4')
        if any(p[k]>9 for k in ('a','c','k')):raise ValueError('hard coefficients 1..9')
    if raw and t=='linear_log_reciprocal_radio' and p['k']<=p['a']:raise ValueError('raw negative historical slot requires k>a')
    if raw and t=='ln_quadratic_linear_radio' and p['a']+2*p['c']-p['k']<=0:raise ValueError('raw signed answer mask requires positive answer')
    if t=='log_quadratic_linear_blank' and level=='easy' and 2*p['c']-p['k']<=0:raise ValueError('positive source collected arithmetic slot')
def fill(mask,p,ans,x0):
    env={k:sp.Integer(v) for k,v in p.items()};env.update(t=x0,answer=ans)
    return re.sub(r'@@(.*?)@@',lambda m:tex(sp.sympify(m[1],locals=env)),mask)
def block(rows):return '$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
def authored_missing(t,p,parts,d,x0,ans):
    if t=='rational_ln_radio':
        n=p['n'];den=p['d'];fs=rf'-\frac{{{n}}}{{{den}}}\ln x'
        rows=[DY+'&='+D+'('+fs+')','&='+rf'-\frac{{{n}}}{{{den}}}\cdot\frac{{1}}{{x}}','&='+rf'-\frac{{{n}}}{{{den}x}}']
    else:
        b=p['b'];c=p['c'];fs=rf'\log_{{{b}}}x+{c}\ln x'
        rows=[DY+'&='+D+'('+fs+')','&='+D+rf'(\log_{{{b}}}x)+{c}'+D+r'(\ln x)','&='+rf'\frac{{1}}{{x\ln {b}}}+\frac{{{c}}}{{x}}']
    return INTRO+block(rows)+'\n\nTherefore, the slope of the tangent at $x='+tex(x0)+'$ is\n\n'+block([DY+r'\big|_{x='+tex(x0)+'}&='+r'\left('+tex(d)+r'\right)\big|_{x='+tex(x0)+'}','&='+tex(ans)+r'\,.'])
def render(level,t,p,raw):
    parts,f,d,x0,ans=data(t,p);m=MASKS[case(t)['source_id']]
    problem=fill(m['prompt'],p,ans,x0)
    solution=fill(m['solution'],p,ans,x0) if m['solution'] else None
    if not raw:
        if not solution:solution=authored_missing(t,p,parts,d,x0,ans)
        if t=='common_log_cubic_radio':solution=solution.replace('at $x=1$','at $x='+tex(x0)+'$')
        if not m['presence'][':question/answer-fields']:problem+='\n\n{{field-1}}'
        if level=='hard':
            # Final collected row is a complete component, including both substituted terms.
            blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',solution,re.S)
            last=blocks[-1];pos=last.rfind('& =');end=last.rfind(r'\,.')
            changed=last[:pos]+'& ='+tex(ans)+last[end:]
            solution=solution.replace(last,changed)
    return problem,solution,f,d,x0,ans

def method_bank(t,p,ans,x0):
    """Complete profiles grounded in derivative/evaluation operations, chosen before params."""
    a=p.get('a',1);c=p.get('c',1);k=p.get('k',1);b=p.get('b',2)
    if t=='rational_ln_radio':
        r=sp.Rational(p['n'],p['d']);return [ans,1/r,-1/r,r,sp.Integer(0)]
    if t=='two_logs_radio':return [ans,1/(x0*sp.log(b)),c/x0,(sp.log(b)+c)/x0,c/(x0*sp.log(b))]
    if t=='linear_log_reciprocal_radio':return [ans,sp.Integer(a),sp.Integer(c),a+c*sp.log(b),a+c-k]
    if t=='ln_quadratic_linear_radio':return [ans,a/x0+2*c*x0+k,-a/x0+2*c*x0-k,a/x0+c*x0-k,2*c*x0-k]
    if t=='common_log_cubic_radio':return [ans,a/x0+3*x0**2,a/(x0*sp.log(b))+x0**2,a/sp.log(b)+3*x0**2,3*x0**2]
    return [ans]
def sample(level,t,rng):
    p={k:(10 if t=='common_log_cubic_radio' else rng.randint(2,9)) if k=='b' else rng.randint(1,12 if level=='easy' else 9) for k in case(t)['parameters']}
    if 't' in p:p['t']=rng.randint(1,4)
    if t in ('rational_ln_radio','two_logs_radio','ln_quadratic_linear_radio','log_quadratic_linear_blank'):p['t']=1
    if level=='moderate':p['t']=rng.randint(2,4)
    if level=='hard':p.pop('t');p['s']=rng.randint(2,4)
    return p

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in SUPPORTED_LEVELS:raise ValueError('difficulty easy/moderate/hard required')
    rng=random.Random(seed);raw=bool(profile and profile.startswith('raw:'))
    if raw:
        sid=profile[4:];cs=next((c for c in CASES if c['source_id']==sid),None)
        if cs is None:raise ValueError('unknown raw profile')
        if template and template!=cs['template']:raise ValueError('profile/template mismatch')
        template=cs['template']
        if level!='easy':raise ValueError('raw observed/unrated sources replay via easy only')
    else:
        eligible=list(TEMPLATES) if level=='easy' else ['ln_quadratic_linear_radio'] if level=='moderate' else ['log_quadratic_linear_blank']
        eligible=[t for t in eligible if field_type is None or case(t)['field_type']==field_type]
        if not eligible:raise ValueError('unsupported field/level combination')
        template=template or rng.choice(eligible)
        if template not in eligible:raise ValueError('template outside difficulty scope')
        if profile not in (None,'method','method:'+template):raise ValueError('normal profile is method')
    c=case(template);m=MASKS[c['source_id']]
    if field_type and field_type!=c['field_type']:raise ValueError('field mismatch')
    selected_profile=profile if raw else 'method:'+template
    for _ in range(1000):
        p=dict(parameters) if parameters is not None else sample(level,template,rng)
        try:
            bounds(level,template,p,raw);problem,solution,f,d,x0,ans=render(level,template,p,raw)
            vals=[fill(v,p,ans,x0) for v in m['answers']] if raw else [tex(v) for v in method_bank(template,p,ans,x0)]
            if raw and c['field_type']=='radio':
                if str(HERE) not in sys.path:sys.path.insert(0,str(HERE))
                from scalar_parser import scalar,same
                vv=[scalar(v) for v in vals]
                if any(same(v,u) for i,v in enumerate(vv)for u in vv[i+1:]):raise ValueError('whole historical bank collision')
            if not raw and c.get('aliases')==2:vals.append(vals[0].replace(r'\ln',r'\operatorname{ln}'))
            if not raw and c['field_type']=='radio':
                mathvals=method_bank(template,p,ans,x0)
                if any(sp.simplify(u-v)==0 for i,u in enumerate(mathvals)for v in mathvals[i+1:]):raise ValueError('whole method bank collision')
            break
        except ValueError:
            if parameters is not None:raise
    else:raise ValueError('whole-bank sampling exhausted')
    presence=m['presence'] if raw else {k:True for k in m['presence']}
    # Raw unrated records intentionally retain omission; normal authored levels explicit.
    display={'problem':problem,'solution':solution,'values':sorted(vals),'difficulty':level if presence[':question/difficulty'] else None,'fields':presence[':question/answer-fields'],'correct':m['correct_present'] if raw else True}
    identity=digest([VERSION,display]);qid=uid('question/'+identity)
    q={':question/id':qid,':question/problem':problem}
    if presence[':question/worked-solution']:q[':question/worked-solution']=solution
    if presence[':question/difficulty']:q[':question/difficulty']=':question.difficulty/'+level
    if presence[':question/answer-fields']:
        fid=uid(qid+'/'+c['key']);answers=[{':answer/id':uid(fid+'/'+str(i)+'/'+v),':answer/type':':answer.type/math',':answer/value':v}for i,v in enumerate(vals)]
        fdict={':answer-field/id':fid,':answer-field/key':c['key'],':answer-field/type':':answer-field.type/'+c['field_type'],':answer-field/choices':answers}
        idx=m['correct_index'] if raw else 0
        if idx is not None:fdict[':answer-field/correct']=[':answer/id',answers[idx][':answer/id']]
        rng.shuffle(answers);q[':question/answer-fields']=[fdict]
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'generator_id':uid('generator'),'version':VERSION,'template':template,'profile':selected_profile,'parameters':p,'seed':seed,'source_ids':[c['source_id']],'source_basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'domain':'x>0; base>0 and base!=1','evidence_only':raw,'eligible_for_learning':not raw,'authored_level':level!='easy' or not c['observed_level'],'repairs':[] if raw else ['missing fields/solutions/correct refs completed when absent; q-70903 point prose corrected; opaque radio banks replaced by labeled method banks'],'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'mathematical_fingerprint':digest([sp.srepr(sp.simplify(d)),sp.srepr(sp.simplify(x0))]),'content_fingerprint':identity,'plots':[]}}
# Easy: observed source forms, completed fields and method banks.
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
# Moderate: three term natural logarithm, nonunit integer evaluation, coefficient <=9.
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
# Hard: three term general logarithm and reciprocal-log evaluation, coefficient <=9.
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*SUPPORTED_LEVELS,'all'),default='all');ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=('json','markdown'),default='json');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
    levels=SUPPORTED_LEVELS if a.difficulty=='all' else [a.difficulty]
    rs=[generate(l,a.seed+i,a.template,profile=a.profile)for l in levels for i in range(a.count)]
    if a.format=='json':print(json.dumps(rs,indent=2))
    else:
        for r in rs:
            q=r['question'];print(q[':question/problem']);print('\n'.join(v[':answer/value']for f in q.get(':question/answer-fields',[])for v in f[':answer-field/choices']));print(q.get(':question/worked-solution','[source solution absent]'))
