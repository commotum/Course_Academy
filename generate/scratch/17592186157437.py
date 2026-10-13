#!/usr/bin/env python3
"""Parameterized exponential common-factor equations. Steps 3–7, basis 1356.

Every observed display profile uses component masks and exact operation banks;
no source payload is returned. Underidentified scalar banks are explicit replay
profiles, never the authored default. Hard is authored: two primitive nonunit
linear factors, a quadratic already equal to zero, no rearrangement/logarithms.
One invalid or colliding bank member rejects the entire sampled instance.
"""
from __future__ import annotations
import argparse,hashlib,json,random,re,uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186157437
KP_UUID='3758cf02-ba4b-539a-bc61-8c2030ff6f6f'
TITLE='Solving an Exponential Equation by Factoring'
VERSION='exponential-factoring-1'
ROOT=Path(__file__).with_suffix('')
DISPLAYS=json.loads((ROOT/'display-profiles.json').read_text())
X=sp.Symbol('x',real=True)
TEMPLATES={s['template']:s['level'] for s in DISPLAYS.values()}
TEMPLATES.update(hard_leading_radio='hard',hard_leading_blank='hard')
DEFAULTS={t:next(k for k,s in DISPLAYS.items() if s['template']==t) for t in TEMPLATES if not t.startswith('hard')}
DEFAULTS.update(hard_leading_radio='q-88460',hard_leading_blank='q-264778')
PARAM_KEYS={'g','a','b','c','d','base','k','h'}

def tex(v):
    return sp.latex(sp.sympify(v)).replace('- ','-').replace(' + ','+').replace(' - ','-')
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(s):return str(uuid.uuid5(uuid.UUID(KP_UUID),s))
def term(n,m=''):
    if not n:return ''
    return ('-' if n<0 else '')+('' if abs(n)==1 and m else str(abs(n)))+m
def join_terms(parts):
    return ''.join(('+' if i and not s.startswith('-') else '')+s for i,s in enumerate(s for s in parts if s))
def poly(A,B,C):return join_terms([term(A,r'{x}^{2}'),term(B,'x'),term(C)])
def linear(a,b):return '('+join_terms([term(a,'x'),term(b)])+')'
def bounds(p,level,template):
    if set(p)!=PARAM_KEYS:raise ValueError('Require exactly g,a,b,c,d,base,k,h.')
    for k in PARAM_KEYS-{'base'}:
        if type(p[k]) is not int:raise ValueError('Integer parameters required.')
    if p['base']!='e' and (type(p['base']) is not int or not 2<=p['base']<=9):raise ValueError('Base e or integer 2..9 required.')
    if not 1<=p['g']<=3 or not 1<=p['a']<=4 or not 1<=p['c']<=4 or not 1<=abs(p['k'])<=9 or abs(p['h'])>4:raise ValueError('Common-factor/exponent bounds.')
    if not p['b'] or not p['d']:raise ValueError('Both roots nonzero.')
    if sp.Rational(-p['b'],p['a'])==sp.Rational(-p['d'],p['c']):raise ValueError('Two distinct roots required.')
    if level=='easy':
        if p['a']!=1 or p['c']!=1 or p['b']!=-p['d'] or abs(p['b'])>12:raise ValueError('Easy requires integer opposite roots <=12.')
    elif level=='moderate':
        if p['c']!=1 or p['a']>3 or max(abs(p['b']),abs(p['d']))>9:raise ValueError('Moderate one nonunit factor at most; constants <=9.')
        if p['a']==1 and p['b']==-p['d']:raise ValueError('Moderate requires nonzero linear term.')
    else:
        if not 2<=p['a']<=4 or not 2<=p['c']<=4 or p['g']!=1 or max(abs(p['b']),abs(p['d']))>9:raise ValueError('Hard primitive factors bounds.')
        if sp.gcd(p['a'],p['b'])!=1 or sp.gcd(p['c'],p['d'])!=1:raise ValueError('Hard factors must be primitive.')
    if 'difference' in template and (p['a']!=1 or p['c']!=1 or p['b']!=-p['d']):raise ValueError('Difference structure required.')
    if 'leading' in template and p['a']==1:raise ValueError('Leading coefficient required.')
    if 'leading' in template and sp.gcd(p['a'],p['b'])!=1:raise ValueError('Leading linear factor must be primitive.')
    if 'quadratic' in template and (p['a']!=1 or p['c']!=1 or p['b']==-p['d']):raise ValueError('Quadratic integer factor structure required.')
    if ('gcf' in template or 'scaled' in template) and p['g']==1:raise ValueError('Nonunit common scalar required.')
    if 'gcf' not in template and 'scaled' not in template and p['g']!=1:raise ValueError('Unit common scalar required for this layout.')
    A=p['g']*p['a']*p['c'];B=p['g']*(p['a']*p['d']+p['b']*p['c']);C=p['g']*p['b']*p['d']
    if not B and level!='easy':raise ValueError('Nonzero linear coefficient required.')
    if level=='moderate' and (A>3 or abs(B)>30 or abs(C)>72):raise ValueError('Moderate expanded workload bounds.')
    if level=='hard' and (A>16 or abs(B)>72 or abs(C)>81):raise ValueError('Hard expanded workload bounds.')

def bank(profile,p,roots):
    u,v=roots; z=u*v;r=abs(u)
    if profile in ('q-100785','q-88454','q-88412'):return [('product',z),('opposite_product',-z),('lower_root',u),('upper_root',v),('false_exponential_root',sp.Integer(0))]
    if profile=='q-110801':return [('double_upper_root',2*v),('opposite_product',-z),('false_exponential_root',sp.Integer(0)),('product',z),('double_lower_root',2*u)]
    if profile=='q-100781':return [('upper_root',v),('sum_roots',u+v),('lower_root',u),('double_product',2*z),('product',z)]
    # Underidentified banks retain explicit scale patterns; no intent claim.
    if profile=='q-88458':return [('half_product',z/2),('negative_double_upper',-2*v),('negative_upper',-v),('product',z),('double_upper',2*v)]
    if profile=='q-88459':return [('negative_product',-z),('double_product',2*z),('negative_double_product',-2*z),('triple_product',3*z),('product',z)]
    if profile=='q-88460':return [('negative_triple_product',-3*z),('three_eighths_product',3*z/8),('one_sixteenth_product',z/16),('negative_eighth_product',-z/8),('product',z)]
    if profile!='authored':raise ValueError('Unknown bank profile.')
    if p['b']==-p['d'] and p['a']==p['c']==1:
        if r==1:return [('product',z),('opposite_product',-z),('double_lower_root',2*u),('double_upper_root',2*v),('false_exponential_root',sp.Integer(0))]
        return [('product',z),('opposite_product',-z),('lower_root',u),('upper_root',v),('false_exponential_root',sp.Integer(0))]
    return [('product',z),('sum_instead_of_product',u+v),('lower_root_only',u),('upper_root_only',v),('unscaled_constant',p['g']*p['b']*p['d']) if p['g']*p['a']*p['c']!=1 else ('opposite_product',-z)]

def components(p,s):
    g,a,b,c,d,base,k,h=(p[z] for z in ['g','a','b','c','d','base','k','h'])
    A=g*a*c;B=g*(a*d+b*c);C=g*b*d;pol=poly(A,B,C)
    exponent=join_terms([term(k,'x'),term(h)])
    if k==-1 and h:exponent=str(h)+'-x'
    E='{'+str(base)+'}^{'+exponent+'}'
    dot=r'\cdot ' if s['dot'] else ''
    eq=join_terms([term(A,r'{x}^{2}')+dot+E,term(B,'x')+dot+E if B else '',term(C)+dot+E])
    # Omit coefficient 1 on constant times the exponential.
    if C in (1,-1):eq=join_terms([term(A,r'{x}^{2}')+dot+E,term(B,'x')+dot+E if B else '',('-' if C<0 else '')+E])
    f=(str(g) if g!=1 else '')+linear(a,b)+linear(c,d)
    roots=sorted([sp.Rational(-b,a),sp.Rational(-d,c)]);u,v=map(tex,roots)
    prod=tex(roots[0]*roots[1]);
    factors=[u,v]
    if s['product_parens']:factors=['('+v+')' if z<0 else v for z,v in zip(roots,factors)]
    equation=eq+'=0'+('?' if s['prompt_question_inside'] else '')
    if s['legacy_prompt']:
        equation='x^{2}e^{'+exponent+'} - '+str(-C)+'e^{'+exponent+'} = 0'
    first=r'\begin{aligned}'+eq+r' & =0 \\ ('+pol+')'+(r'\cdot ' if s['factor_dot'] and s['dot'] else '')+E+r' & =0\end{aligned}'
    factor=f+'=0,'
    if s['two_rows']:factor=r'\begin{aligned}'+str(g)+'('+poly(a*c,a*d+b*c,b*d)+r') & =0 \\ '+f+r' & =0,\end{aligned}'
    inline=lambda v:'$'+v+'$';display=lambda v:'$$\n'+v+'\n$$'
    return {'equation':inline(equation),'prompt_x':'$x=$','prompt_space':r'$\,$','prompt_x2':r'$\,x=$',
      'first':display(first),'zp_product':'$ab=0$','zp_a':'$a=0$','zp_b':'$b=0.$',
      'split':display(pol+r'=0\,\text{and}\,'+E+'=0.'),'polynomial':inline(pol+'=0'),
      'factor':display(factor),'roots_dot':inline('x='+u+','+v+'.'),'gcf_false':inline(str(g)+'=0'),
      'exp_zero':inline(E+'=0'),'exp':inline(E),'x_dot':'$x.$','roots_comma':inline('x='+u+','+v+','),
      'final_blanks':display('x='+u+r'\,\text{and}\,x='+v+'.'),
      'product':inline(factors[0]+r'\cdot '+factors[1]+'='+prod+'.')},roots

def render(mask,values):
    return re.sub(r'\{\{([a-z_0-9]+)\}\}',lambda m:values.get(m[1],m[0]),mask)

def sample(level,template,rng):
    p={'g':rng.choice([2,3]) if 'gcf' in template or 'scaled' in template else 1,'a':1,'c':1,'base':rng.choice(['e',2,3,4,5,6,7,8,9]),'k':rng.choice([-3,-2,-1,1,2,3]),'h':rng.randint(-3,3)}
    if level=='easy':p.update(b=rng.randint(1,12),d=0);p['d']=-p['b']
    else:
        p.update(a=rng.choice([2,3,4]) if level=='hard' else rng.choice([2,3]) if 'leading' in template else 1,c=rng.choice([2,3,4]) if level=='hard' else 1,b=rng.choice([i for i in range(-9,10) if i]),d=rng.choice([i for i in range(-9,10) if i]))
    return p

# Easy: a difference of squares after taking out a strictly positive exponential.
# Moderate: monic/GCF or one nonunit linear factor after that same operation.
# Hard: authored two primitive nonunit factors; no rearranging or new function.
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty.')
    rng=random.Random(seed)
    if profile and profile!='authored':
        if profile not in DISPLAYS:raise ValueError('Unknown observed profile.')
        s=DISPLAYS[profile]
        if template and template!=s['template']:raise ValueError('Profile/template mismatch.')
        template=s['template']
        if level!=s['level']:raise ValueError('Profile/level mismatch.')
    eligible=[t for t,l in TEMPLATES.items() if l==level and (not field_type or t.endswith('_'+field_type))]
    template=template or rng.choice(eligible)
    if template not in eligible:raise ValueError('Template/difficulty/field mismatch.')
    chosen=profile or 'authored';s=DISPLAYS[profile if profile and profile!='authored' else DEFAULTS[template]].copy()
    blank=template.endswith('_blank')
    if profile in (None,'authored'):
        s['legacy_prompt']=False
        if blank:s['field_order']=['field-1','field-2']
    for _ in range(2000):
        p=dict(parameters) if parameters is not None else sample(level,template,rng)
        if parameters is None and s['legacy_prompt']:p['base']='e'
        try:
            if s['legacy_prompt'] and p['base']!='e':raise ValueError('Legacy exponential display requires base e.')
            bounds(p,level,template);values,roots=components(p,s)
            entries=[] if blank else bank(chosen,p,roots)
            if entries and len({sp.Rational(v) for _,v in entries})!=5:raise ValueError('Whole bank has equivalent choices.')
            if entries and sum(v==roots[0]*roots[1] for _,v in entries)!=1:raise ValueError('Ambiguous bank.')
            break
        except ValueError:
            if parameters is not None:raise
    else:raise ValueError('Sampler exhausted whole-instance rejection.')
    prompt=render(s['prompt_mask'],values);solution=render(s['solution_mask'],values)
    # Hard uses the same stage/response layout as observed leading quadratics.
    field_values={f'field-{i+1}':[('root',r)] for i,r in enumerate(roots)} if blank else {'selection':entries}
    correct={f'field-{i+1}':r for i,r in enumerate(roots)} if blank else {'selection':roots[0]*roots[1]}
    content={'version':VERSION,'level':level,'template':template,'parameters':p,'prompt':prompt,'solution':solution,'banks':{k:sorted(tex(v) for _,v in arr) for k,arr in field_values.items()}}
    fingerprint=digest({'polynomial':tex(sp.Poly(p['g']*(p['a']*X+p['b'])*(p['c']*X+p['d']),X).monic().as_expr()),'nonunit_scalar_extraction':p['g']!=1,'response':'roots' if blank else 'product'})
    cid=digest(content);qid=ident(cid);fields=[]
    for key in s['field_order']:
        arr=field_values[key];fid=ident(cid+'/'+key);answers=[{':answer/id':ident(fid+'/'+tex(v)),':answer/type':':answer.type/math',':answer/value':tex(v)} for _,v in arr]
        correct_id=ident(fid+'/'+tex(correct[key]));rng.shuffle(answers)
        fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/blank' if blank else ':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':fields},'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':p,'profile':chosen,'display_profile':profile if profile and profile!='authored' else DEFAULTS[template],'origin':'authored hard extension' if level=='hard' else 'observed display; authored default bank' if chosen=='authored' else 'observed replay profile','source':{'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'},'domain':'x real; exponential base positive; distinct nonzero roots','mathematical_fingerprint':fingerprint,'content_fingerprint':cid,'recipes':[(name,tex(v)) for name,v in entries]}}

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in levels for i in range(args.count)]
    if args.format=='json':print(json.dumps(records,indent=2))
    else:
        for r in records:
            q=r['question'];print('\n'+q[':question/problem'])
            for f in q[':question/answer-fields']:print(f[':answer-field/key']+': '+', '.join(a[':answer/value'] for a in f[':answer-field/choices']))
            print('\n'+q[':question/worked-solution'])
if __name__=='__main__':main()
