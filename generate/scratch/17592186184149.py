#!/usr/bin/env python3
"""Phase identification for a given stretched tan/cot graph. Steps 3–7 only.

Frozen source basis 1356; source masks and complete opaque evidence banks are
parameterized in the private recipes.json. Observed profiles are explicitly
ineligible evidence (one cannot infer error intent from scalar distractors).
Normal banks implement sign/scale/zero-feature operations. No DB connections.
Principal phase contract: -pi/2<C<pi/2; equality of curves is modulo pi in C.
The graph's horizontal shift is -C/B modulo pi/B. The requested answer is C,
not a unique unconstrained horizontal translation. Explicit parameters use c=C/pi.
"""
from __future__ import annotations
import argparse,hashlib,json,random,re,subprocess,sys,uuid
from pathlib import Path
import sympy as sp
KP=17592186184149
HERE=Path(__file__).with_suffix('')
RAW=json.loads((HERE/'source.json').read_text())
RECIPES=json.loads((HERE/'recipes.json').read_text())
VERSION='phase-shift-v2'
X,C=sp.symbols('x C',real=True)

def rational(v):
    z=sp.sympify(v)
    if not z.is_Rational:raise ValueError('Exact rational required')
    return z

def tex(v):
    """Source number-form spelling: rational multiples of pi, rational scalars."""
    v=sp.sympify(v)
    if v==0:return '0'
    coeff=sp.cancel(v/sp.pi)
    if coeff.is_Rational:
        n,d=int(abs(coeff).p),int(abs(coeff).q);sgn='-' if coeff<0 else ''
        num=('' if n==1 else str(n))+r'\pi '
        return sgn+(num.rstrip() if d==1 else r'\frac{'+num+'}{'+str(d)+'}')
    if v.is_Rational:
        n,d=int(abs(v).p),int(abs(v).q);sgn='-' if v<0 else ''
        return sgn+(str(n) if d==1 else r'\frac{'+str(n)+'}{'+str(d)+'}')
    return sp.latex(v)

def times_symbol(v,symbol):
    v=rational(v)
    if v==1:return symbol
    if v.q==1:return str(v)+symbol
    return r'\frac{'+('' if v.p==1 else str(v.p))+symbol+'}{'+str(v.q)+'}'

def parse_scalar(t):
    """Independent narrow reader for displayed source-shaped scalar answer TeX."""
    t=t.strip().replace(' ','').replace(r'\pi','pi')
    t=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',t)
    t=re.sub(r'(?<=\d)pi','*pi',t)
    return sp.sympify(t,locals={'pi':sp.pi})

def phase_equivalent(a,b):return sp.simplify((a-b)/sp.pi).is_integer is True

def bank_valid(values):
    if len(values)!=5:raise ValueError('Complete five-option bank required')
    for i,a in enumerate(values):
        if not a.is_real or not a.is_finite:raise ValueError('Nonreal bank')
        for b in values[:i]:
            if phase_equivalent(a,b):raise ValueError('Whole bank rejected: periodic aliases')

def authored_bank(B,c,fn):
    a=c*sp.pi; h=-a/B; z=(sp.pi/2-a)/B
    # Complete operations: correct; reverse direction; omit B; use B inversely;
    # misidentify a zero as an asymptote (or vice versa), taking principal phase.
    feature=a-sp.pi/2 if a>0 else a+sp.pi/2
    vals=[a,-a,-h,-h/B,feature]
    bank_valid(vals)
    return vals,['correct','reverse_shift_sign','omit_stretch_factor','invert_stretch_factor','confuse_zero_and_asymptote']

def parameter_domain(level):
    if level=='easy':return [sp.Rational(2),sp.Rational(3),sp.Rational(1,2),sp.Rational(1,3)]
    if level=='moderate':return [sp.Rational(n) for n in range(2,6)]+[sp.Rational(1,n) for n in range(2,6)]
    if level=='hard':return sorted({sp.Rational(n,d) for n in range(2,6) for d in range(2,8) if sp.Rational(n,d).p>1 and sp.Rational(n,d).q>1 and sp.Rational(n,d)<2})
    raise ValueError('Unknown level')

PHASES=sorted({sp.Rational(s*n,d) for d in [5,7,8,9,10,11,12] for n in range(1,d//2+1) for s in [-1,1] if sp.Rational(n,d)<sp.Rational(1,2)})

def check_parameters(level,p,observed=False):
    if set(p)!={'B','c','fn'}:raise ValueError('Parameters require exactly B,c,fn')
    B,c=rational(p['B']),rational(p['c']);fn=p['fn']
    if B<=0 or fn not in ['tan','cot'] or not -sp.Rational(1,2)<c<sp.Rational(1,2) or c==0:raise ValueError('Invalid phase/scale/family')
    if not observed and (B not in parameter_domain(level) or c not in PHASES):raise ValueError('Outside documented same-level workload bounds')
    return B,c,fn

def functions(B,fn):
    op=r'\operatorname{'+fn+'}\u2061'.replace('\\u2061','\u2061')
    arg=times_symbol(B,'x');factor='x+'+times_symbol(1/B,'C')
    coeff=tex(B)
    formula='y='+op+'('+arg+'+C)'
    factored='y='+op+'('+coeff+'('+factor+'))'
    baseline='y='+op+'('+arg+')'
    return formula,factored,baseline,factor,op

def source_component(spec,B,c,fn,level):
    form,fact,base,factor,op=functions(B,fn);a=c*sp.pi;h=-a/B
    z0=0 if fn=='tan' else sp.pi/(2*B);z=z0+h
    distance=tex(abs(h))
    if spec['subtraction']:
        left,right=(z,z0) if h>0 else (z0,z)
        distance=tex(left)+'-'+('('+tex(right)+')' if right<0 else tex(right))+'='+distance
    calc=times_symbol(1/B,'C')+'='+tex(-h)
    if level=='hard':calc+=r'\,⟹\,C=('+tex(-h)+')('+tex(B)+')'
    calc+=r'\,⟹\,C='+tex(a)
    block=r'\begin{aligned}y & ='+form[2:]+r' \\  & ='+fact[2:]+r'\end{aligned}'
    body={'formula':form,'factored':fact,'baseline':base,'factor':factor,'constant':'C','bound':r'-\frac{\pi }{2}<C<\frac{\pi }{2}','distance':distance,'answer':tex(a),'calculation':calc,'factor_block':block}[spec['tag']]
    if spec['bare_baseline']:body='y='+fn+r'\,('+times_symbol(B,'x')+')'
    original=spec['original'];stripped=original.strip()
    punctuation=stripped[-1] if stripped[-1:] in ['.',',','?'] else ''
    body+=punctuation
    if spec['display']:body='\n'+body+'\n'
    return body

def render_source(cfg,B,c,fn,level,assets):
    slots={'prompt_plot':assets['prompt'],'solution_plot':assets['solution'],'direction':'right' if c<0 else 'left'}
    for i,spec in enumerate(cfg['math_components']):slots['math_'+str(i)]=source_component(spec,B,c,fn,level)
    def fill(mask):return re.sub(r'\{\{(.*?)\}\}',lambda m:slots[m[1]],mask)
    return fill(cfg['problem_mask']),fill(cfg['worked-solution_mask'])

def render_plots(B,c,fn,level):
    key=hashlib.sha256(json.dumps([str(B),str(c),fn,level,VERSION]).encode()).hexdigest()[:24]
    out=HERE/'plots';out.mkdir(exist_ok=True)
    targets={r:str(out/(key+'-'+r+'.png')) for r in ['prompt','solution']}
    if not all(Path(f).exists() and Path(f).with_suffix('.json').exists() for f in targets.values()):
        import tempfile,os
        with tempfile.NamedTemporaryFile(mode='w',suffix='.json',prefix='render-',dir=out,delete=False) as f:
            json.dump({'B':str(B),'c':str(c),'fn':fn,'level':level,'targets':targets},f);input_path=f.name
        try:subprocess.run([sys.executable,str(HERE/'render.py'),input_path],check=True,capture_output=True,text=True)
        finally:os.unlink(input_path)
    return targets

def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,str(KP)+':'+v))

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ['easy','moderate','hard']:raise ValueError('Unknown difficulty')
    if field_type not in [None,'radio',':answer-field.type/radio']:raise ValueError('Observed radio layout required')
    cfg=None;observed=bool(profile and profile.startswith('observed:'))
    if observed:
        sid=profile.split(':',1)[1];cfg=RECIPES[sid]
        if level!=cfg['level']:raise ValueError('Observed level mismatch')
        if parameters is None:parameters={k:cfg[k] for k in ['B','c','fn']}
    elif profile not in [None,'authored-method']:raise ValueError('Unknown profile')
    rng=random.Random(seed)
    family=template.removesuffix('_shift') if template else (parameters['fn'] if parameters else (cfg['fn'] if cfg else rng.choice(['tan','cot'])))
    if family not in ['tan','cot']:raise ValueError('Unknown template')
    if parameters is None:
        for attempt in range(2000):
            parameters={'B':str(rng.choice(parameter_domain(level))),'c':str(rng.choice(PHASES)),'fn':family}
            B,c,fn=check_parameters(level,parameters)
            try:authored_bank(B,c,fn);break
            except ValueError:parameters=None
        else:raise RuntimeError('No eligible whole bank')
    B,c,fn=check_parameters(level,parameters,observed)
    if observed and fn!=cfg['fn']:raise ValueError('Observed profile family mismatch')
    if fn!=family:raise ValueError('Template/family mismatch')
    if observed:
        # Parameterized scalar-pattern replay, deliberately opaque/ineligible.
        c0=rational(cfg['c']);vals=[sp.simplify(parse_scalar(t)*c/c0) for t in cfg['banks']]
        recipes=['opaque_scaled_source_pattern_'+str(i) for i in range(5)]
        correct=sp.simplify(parse_scalar(cfg['correct'])*c/c0)
        eligible=False;bank_issue=None
        try:bank_valid(vals)
        except ValueError as e:bank_issue=str(e)
        same=B==rational(cfg['B']) and c==c0 and fn==cfg['fn']
        assets={role:cfg[key].removeprefix('/media/jake/SSD/EDB/math/') for role,key in [('prompt','problem_asset'),('solution','worked-solution_asset')]} if same else render_plots(B,c,fn,level)
        prompt,solution=render_source(cfg,B,c,fn,level,assets)
    else:
        vals,recipes=authored_bank(B,c,fn);correct=c*sp.pi;eligible=True;bank_issue=None
        assets=render_plots(B,c,fn,level)
        form,fact,base,factor,op=functions(B,fn);h=-correct/B;z0=0 if fn=='tan' else sp.pi/(2*B);z=z0+h
        prompt='![]('+assets['prompt']+')\n\nThe graph above shows the function $'+form+',$ where $C$ is a constant. Given that $-\\frac{\\pi }{2}<C<\\frac{\\pi }{2},$ what is the value of $C?$'
        if level=='easy':prompt+=' The dashed curve is $'+base+'.$ The horizontal displacement between the two marked zeros is $'+tex(abs(h))+'$ units to the '+('right' if h>0 else 'left')+'.'
        spec={'tag':'factor_block','original':'\nblock\n','display':True,'bare_baseline':False,'subtraction':False}
        solution='The parameter $C$ determines a horizontal shift of $-'+times_symbol(1/B,'C')+'$ units, modulo the period $'+tex(sp.pi/B)+'$.\n\nFirst, we rewrite the function by factoring the horizontal stretch factor, as follows:\n\n$$'+source_component(spec,B,c,fn,level)+'$$\n\nThe factor $'+factor+'$ indicates that the graph of $'+fact+'$ is a horizontal translation of $'+base+'.$ Comparing the two graphs below allows us to determine the amount of this shift.\n\n![]('+assets['solution']+')\n\nFrom the diagram, we see that our curve has been obtained by shifting $'+base+'$ by $'
        spec.update(tag='distance',display=False,original='distance',subtraction=level!='easy')
        solution+=source_component(spec,B,c,fn,level)+'$ units to the '+('right' if h>0 else 'left')+'. Therefore:\n\n$$\n'
        spec.update(tag='calculation',original='calculation',subtraction=False)
        solution+=source_component(spec,B,c,fn,level)+'\n$$\n\nSince $-\\frac{\\pi }{2}<C<\\frac{\\pi }{2}$ and $'+tex(correct)+'$ is in this interval, the value of $C$ is $'+tex(correct)+'.$'
    bank=[tex(v) for v in vals]
    if observed:
        # Preserve the source's negative-numerator notation as a component style,
        # rather than replacing a generated answer with a source literal.
        bank=[(t[1:].replace(r'\frac{',r'\frac{-',1) if original.startswith(r'\frac{-') and t.startswith(r'-\frac{') else t) for t,original in zip(bank,cfg['banks'])]
    # Presentation and task identities deliberately exclude source/profile aliases.
    fingerprint=hashlib.sha256(json.dumps([fn,str(B),str(c),level,'given-displacement' if level=='easy' else 'read-zero-coordinates']).encode()).hexdigest()
    identity=hashlib.sha256(json.dumps([VERSION,level,prompt,solution,sorted(bank)]).encode()).hexdigest()
    field_id=uid(identity+':selection');choices=[{':answer/id':uid(field_id+':'+str(sp.simplify(v))),':answer/type':':answer.type/math',':answer/value':t} for v,t in zip(vals,bank)]
    corr=next(a[':answer/id'] for a,v in zip(choices,vals) if sp.simplify(v-correct)==0)
    rng.shuffle(choices)
    question={':question/id':uid(identity),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':field_id,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',corr]}]}
    return {'knowledge_point':{'db_id':KP,'id':RAW['record'][':knowledge-point/id'],'title':RAW['record'][':knowledge-point/title']},'question':question,'generation':{'version':VERSION,'template':fn+'_shift','profile':profile or 'authored-method','bank_profile':profile or 'authored-method','seed':seed,'parameters':{'B':str(B),'c':str(c),'fn':fn},'mathematical_fingerprint':fingerprint,'content_identity':identity,'eligible_for_learning':eligible,'evidence_only':not eligible,'source_bank_issue':bank_issue,'recipes':recipes,'source':{k:RAW[k] for k in ['database','basis','lineage']},'domain':{'phase':'-pi/2<C<pi/2','curve_phase_equivalence':'C1-C2 in pi*Z','shift_equivalence':'h1-h2 in (pi/B)*Z','response_contract':'exact scalar C in principal open interval; no aliases accepted as representative'},'plot_assets':assets,'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

# EASY — authored scaffold: B integer/reciprocal; supplied displacement and overlay.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# MODERATE — observed workload: B integer/reciprocal, read actual shifted zero.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# HARD — observed workload: reduced nonunit rational B, subtract then multiply.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
    records=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
    if a.format=='json':print(json.dumps(records,indent=2,ensure_ascii=False))
    else:
        for r in records:
            q=r['question'];g=r['generation'];raw=g['evidence_only'];level=q[':question/difficulty'].split('/')[-1]
            def preview(z):return re.sub(r'(!\[[^]]*\]\()(images/[^)]+)(\))',lambda m:m[1]+'/media/jake/SSD/EDB/math/'+m[2]+m[3],z)
            print('## '+('ORIGINAL SOURCE / EVIDENCE VARIANT' if raw else 'GENERATED VARIANT')+' — '+level+'\n\n'+g['profile']+'; '+('evidence only' if raw else 'eligible authored bank'))
            print(preview(q[':question/problem']));print('\nChoices:\n')
            f=q[':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
            print('\n'.join('- $'+x[':answer/value']+'$'+(' **designated correct**' if x[':answer/id']==correct else '') for x in f[':answer-field/choices']))
            print('\nWorked solution:\n'+preview(q[':question/worked-solution']))
