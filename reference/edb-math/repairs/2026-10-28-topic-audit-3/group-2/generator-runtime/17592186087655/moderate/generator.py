#!/usr/bin/env python3
"""Given a labeled center and radius, construct the full standard circle equation.

Math database basis 4711. Self-contained source evidence and generator.
Observed easy graph radio banks and blank template are parameterized faithfully.
Two unrated raw profiles retain absent difficulty, solution and correct refs.
Their completed profiles infer center/radius directly from inspected labeled plots.
Two stripped blank diagrams are raw evidence only; completed replay restores input.
Normal delivery is easy radio only; moderate/hard are unsupported.
No center extraction, distance formula, midpoint, expansion or database writes.
"""
from __future__ import annotations

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186087655-source-policy.json'))
    raise SystemExit(0)

import argparse, copy, hashlib, json, os, random, re, sys, uuid
from math_format import normalize_prose, normalize_tex, checked_math_content
from pathlib import Path
import sympy as sp

KP_ID=17592186087655
KP_UUID='82d6988b-3220-578f-ba1c-cd86b9e3dbf9'
TITLE='Finding the Equation of a Circle Given the Center and the Radius'
VERSION='circle-given-center-radius-3'
HERE=Path(__file__).resolve().parent
SOURCE=json.loads((HERE/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['material']['kp'][':knowledge-point/questions']}
X,Y=sp.symbols('x y',real=True)
# Recipes are complete banks. Coordinates specify the proposed center; last
# component specifies the proposed squared radius. Interpretations are hypotheses.
BANKS={
 'q-54187': [('h','k','r'),('h','k','r2'),('-h','-k','r'),('-h','-k','r2'),('h','-k','r2')],
 'q-54210': [('-h','-k','r2'),('-h','-k','r'),('h','-k','r2'),('h','k','r2'),('h','k','r')],
 'q-116929':[('-h','-k','sqrt_r'),('h','-k','r'),('h','k','r2'),('-h','k','r'),('-h','-k','r2')],
 'q-117077':[('-h','k','r'),('h','-k','r2'),('h','k','r2'),('-h','-k','r2'),('-h','-k','r')],
 'q-117081':[('-h','k','r'),('h','k','r2'),('zero','zero','r2'),('h','k','r'),('-h','k','r2')],
 'q-70896':[('-h','k','r2'),('k','h','r2'),('h','k','r2'),('-h','-k','r2'),('-k','-h','r2')],
 'q-70898':[('-k','-h','r2'),('-h','k','r2'),('-h','-k','r2'),('k','h','r2'),('h','k','r2')],
 'blank':[('h','k','r2')],
}
ORIGINAL={
 'q-54187':{'h':1,'k':3,'r':3,'orientation':'horizontal'},
 'q-54210':{'h':-2,'k':5,'r':7,'orientation':'vertical'},
 'q-167948':{'h':0,'k':6,'r':6,'orientation':'vertical'},
 'q-167932':{'h':3,'k':0,'r':3,'orientation':'horizontal'},
 'q-116929':{'h':-4,'k':-3,'r':6,'orientation':'horizontal'},
 'q-117077':{'h':2,'k':-3,'r':4,'orientation':'vertical'},
 'q-117081':{'h':-5,'k':0,'r':7,'orientation':'vertical'},
 'q-70896':{'h':1,'k':2,'r':5,'orientation':'horizontal'},
 'q-70898':{'h':-2,'k':-3,'r':8,'orientation':'vertical'},
}

def digest(obj): return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(s): return str(uuid.uuid5(uuid.UUID(KP_UUID),s))
def exact(v):
    if isinstance(v,bool) or isinstance(v,float): raise ValueError('Use exact rational or algebraic numbers, not floats/bools.')
    z=sp.sympify(v)
    if not z.is_number or z.is_real is not True or not z.is_finite: raise ValueError('Finite real exact number required.')
    return z

def tex(z): return sp.latex(sp.sympify(z))
def shifted(v,c):
    c=sp.sympify(c)
    if c==0:return '{'+v+'}^{2}'
    return '('+v+('+' if c<0 else '-')+tex(abs(c))+')^{2}'
def equation(h,k,q): return shifted('x',h)+'+'+shifted('y',k)+'='+tex(q)
def subterm(v,c): return '('+v+'-'+('('+tex(c)+')' if c<0 else tex(c))+')^{2}'
def substitute(h,k):return subterm('x',h)+'+'+subterm('y',k)
def squared_radius(r):return ('{'+tex(r)+'}' if r.is_Integer else '('+tex(r)+')')+'^{2}'

def parse_expr(s):
    """Independent displayed-expression reader for our restricted circle LaTeX."""
    from sympy.parsing.sympy_parser import parse_expr as parse, standard_transformations, implicit_multiplication_application
    s=s.strip().rstrip('.')
    s=s.replace('\\left','').replace('\\right','').replace('\\dfrac','\\frac')
    # Innermost command groups first; arbitrary nesting in rational centers.
    for _ in range(15):
        old=s
        s=re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',r'((\1)/(\2))',s)
        s=re.sub(r'\\sqrt\{([^{}]*)\}',r'sqrt(\1)',s)
        s=re.sub(r'\{([^{}]*)\}',r'(\1)',s)
        if s==old:break
    return parse(s.replace('^','**'),local_dict={'x':X,'y':Y,'sqrt':sp.sqrt},transformations=standard_transformations+(implicit_multiplication_application,))
def polynomial(eq):
    a,b=eq.split('=');return sp.Poly(sp.expand(parse_expr(a)-parse_expr(b)),X,Y,extension=True)
def equivalent(a,b):
    pa,pb=polynomial(a),polynomial(b)
    # Compare complete equations modulo a NONZERO scalar, over all coefficients.
    da,db=pa.as_dict(),pb.as_dict()
    if set(da)!=set(db):return False
    scale=sp.simplify(next(iter(da.values()))/next(iter(db.values())))
    return scale!=0 and all(sp.simplify(da[m]-scale*db[m])==0 for m in da)

def recipe_values(p,bank):
    h,k,r=p['h'],p['k'],p['r']
    lookup={'h':h,'k':k,'-h':-h,'-k':-k,'zero':sp.Integer(0),'r':r,'r2':r*r,'sqrt_r':sp.sqrt(r)}
    return [tuple(lookup[c] for c in row) for row in BANKS[bank]]
def validate_bank(p,bank):
    objects=recipe_values(p,bank);values=[equation(*obj) for obj in objects]
    if any(equivalent(a,b) for i,a in enumerate(values) for b in values[i+1:]):raise ValueError('Complete bank collision; reject whole instance.')
    correct=equation(p['h'],p['k'],p['r']**2)
    hits=[i for i,v in enumerate(values) if equivalent(v,correct)]
    if len(hits)!=1:raise ValueError('Ambiguous or missing correct equation.')
    return values,hits[0]

def domain(level,p,observed):
    if level!='easy':raise ValueError('Only source-justified easy difficulty is supported.')
    if set(p)!={'h','k','r','orientation'}:raise ValueError('Parameters require h,k,r,orientation only.')
    if p['orientation'] not in ('horizontal','vertical'):raise ValueError('Unknown radius orientation.')
    if not all(p[t].is_Integer and abs(p[t])<=10 for t in ('h','k')) or not p['r'].is_Integer or not 2<=p['r']<=10:
        raise ValueError('Source-profile investigation: integer centers <=10, integer radius 2..10.')

def sample(level,rng,bank):
    if level!='easy':raise ValueError('Only easy supported.')
    p={'h':rng.choice([i for i in range(-8,9) if i]),'k':rng.choice([i for i in range(-8,9) if i]),'r':rng.randint(2,9),'orientation':rng.choice(('horizontal','vertical'))}
    if bank=='q-117081':p['k']=0
    return {k:exact(v) if k!='orientation' else v for k,v in p.items()}

def render_plots(p,source_id=None,output_dir=None):
    geom={k:str(v) for k,v in p.items()}
    if source_id and p=={k:(exact(v) if k!='orientation' else v) for k,v in ORIGINAL[source_id].items()}:
        images=re.findall(r'!\[\]\(([^)]+)\)',QUESTIONS[source_id][':question/problem'])
        if images:
            return images[0],{'renderer':'unchanged-source','geometry':geom}
    output_dir=output_dir or os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
    if not output_dir:raise ValueError('Set COURSE_ACADEMY_GENERATOR_OUTPUT_DIR for generated assets.')
    render_dir=Path(output_dir).resolve()
    # Never write runtime output beneath the relocated package itself.
    if render_dir==HERE or HERE in render_dir.parents:
        raise ValueError('Generated assets must be outside the runtime package.')
    key=digest({'parameters':geom,'render_version':'circle-plot-3'})
    output=render_dir/('circle-'+key+'.png')
    from render import render_circle
    side=output.with_suffix('.json')
    if not output.exists() or not side.exists():render_circle(geom,output)
    return str(output),json.loads(side.read_text())

GENERAL='The general equation of a circle with radius $r$ centered at the point $(a,b)$ is \n\n$$\n(x-a)^{2}+(y-b)^{2}={r}^{2}.\n$$'
def solution(p,blank=False):
    h,k,r=p['h'],p['k'],p['r'];eq=equation(h,k,r*r)
    if blank:
        opening='The equation of a circle with radius $r$  centered at the point $(a,b)$ in rectangular coordinates in standard form is\n\n$$\n(x-a)^{2}+(y-b)^{2}={r}^{2}.\n$$'
        intro=f'In our case, the circle is centered at $({tex(h)},{tex(k)})$ and the radius of the circle is $r={tex(r)}$, so'
    else:
        opening=GENERAL
        intro=f'From the picture, we see that our circle is centered at $C({tex(h)},{tex(k)})$ and the radius of the circle is $r={tex(r)}.$ Therefore, the equation of the circle is'
    out=opening+'\n\n'+intro+'\n\n$$\n'+r'\begin{aligned}(x-a)^{2}+(y-b)^{2} & ={r}^{2} '+r'\\ '+substitute(h,k)+' & ='+squared_radius(r)+' '+r'\\ '+eq.replace('=',' & =')+r'.\end{aligned}'+'\n$$'
    if blank:out+='\n\nFinally, the equation of the circle in rectangular coordinates is \n\n$$\n'+eq+'.\n$$'
    return out

def replay_solution(source_id,p):
    """Complete component masks retain every source sentence and ordered stage."""
    original=QUESTIONS[source_id].get(':question/worked-solution')
    if original is None:return None
    if p=={k:(exact(v) if k!='orientation' else v) for k,v in ORIGINAL[source_id].items()}:return original
    if source_id=='q-167948':return solution(p,True)
    old=ORIGINAL[source_id];h,k,r=map(exact,(old['h'],old['k'],old['r']))
    # Equation/substitution masks precede prose masks; never replace bare numbers.
    final=equation(h,k,r*r);subs=substitute(h,k)
    if source_id=='q-117081':subs='{'+subterm('x',h).removesuffix('^{2}')+'}^{2}+'+subterm('y',k)
    masks=[(final.replace('=',' & ='),'@FINALALIGNED@'),(final,'@FINAL@'),(subs,'@SUB@'),(f'({tex(h)},{tex(k)})','@CENTER@'),(f'r={tex(r)}','@RADIUS@'),(squared_radius(r),'@RSQUARE@')]
    result=original
    for old_component,marker in masks:result=result.replace(old_component,marker)
    replacements={'@FINALALIGNED@':equation(p['h'],p['k'],p['r']**2).replace('=',' & ='),'@FINAL@':equation(p['h'],p['k'],p['r']**2),'@SUB@':('{'+subterm('x',p['h']).removesuffix('^{2}')+'}^{2}+'+subterm('y',p['k']) if source_id=='q-117081' else substitute(p['h'],p['k'])),'@CENTER@':f"({tex(p['h'])},{tex(p['k'])})",'@RADIUS@':'r='+tex(p['r']),'@RSQUARE@':squared_radius(p['r'])}
    for marker,value in replacements.items():result=result.replace(marker,value)
    return result

def source_notation(value,source_id):
    if source_id in ('q-54187','q-54210'):
        value=value.replace('+',' + ').replace('-',' - ').replace('=',' = ')
    return value

def generate_source(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    """Generate normal records or public raw source replay (profile='raw:q-ID')."""
    if level!='easy':raise ValueError('Only source-justified easy difficulty is supported.')
    rng=random.Random(seed)
    if field_type:field_type=field_type.removeprefix(':answer-field.type/')
    raw=bool(profile and profile.startswith('raw:'))
    sid=profile.split(':')[-1] if profile and (profile.startswith('raw:') or profile.startswith('completed:')) else None
    if sid and sid not in QUESTIONS:raise ValueError('Unknown source profile.')
    if profile in QUESTIONS:sid=profile
    if not sid:raise ValueError('Explicit source profile required; use generate() for normal delivery.')
    observed=True
    if observed and level!='easy':raise ValueError('Observed sources support easy workload only; raw unrated level remains omitted.')
    if sid:
        bank='blank' if sid in ('q-167932','q-167948') else sid
        expected_template='missing_input_blank' if sid in ('q-167932','q-167948') and raw else ('graph_blank' if sid in ('q-167932','q-167948') else 'graph_radio')
        if template and template!=expected_template:raise ValueError('Template/profile disagreement.')
        template=expected_template
    kind='blank' if template in ('graph_blank','missing_input_blank') else 'radio'
    if field_type and field_type.removeprefix(':answer-field.type/')!=kind:raise ValueError('Field type conflicts with template.')
    if (kind=='blank') != (bank=='blank'):raise ValueError('Profile/field mismatch.')
    if parameters is not None:
        p={k:exact(v) if k!='orientation' else v for k,v in parameters.items()};domain(level,p,observed)
        if sid in ('q-117081','q-167932') and p['k']!=0:raise ValueError('Observed axis template requires k=0.')
        if sid=='q-167948' and p['h']!=0:raise ValueError('Observed axis template requires h=0.')
        values,correct=validate_bank(p,bank)
    else:
        for _ in range(500):
            p=sample(level,rng,bank)
            if sid=='q-167932':p['k']=sp.Integer(0)
            if sid=='q-167948':p['h']=sp.Integer(0)
            try:domain(level,p,observed);values,correct=validate_bank(p,bank);break
            except ValueError:continue
        else:raise ValueError('No eligible full bank.')
    plot=None
    if raw and template=='missing_input_blank':prompt=QUESTIONS[sid][':question/problem']
    else:
        image,plot=render_plots(p,sid)
        if kind=='radio':prompt=f'![]({image})\n\nWhat is the equation of the circle given above?'
        else:prompt='Write the equation of this circle in the form $(x-a)^{2}+(y-b)^{2}={r}^{2}.$\n\n'+f'![]({image})\n\n'+ '{{field-1}}'
    if observed:values=[source_notation(v,sid) for v in values]
    if raw and sid=='q-167948' and p=={k:(exact(v) if k!='orientation' else v) for k,v in ORIGINAL[sid].items()}:
        values=[QUESTIONS[sid][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']]
    sol=replay_solution(sid,p) if raw else solution(p,kind=='blank')
    # Source q-117081 uses braces around a full shifted term. Its exact source
    # display notation is preserved by replay_solution, including all stages.
    rated=not(raw and ':question/difficulty' not in QUESTIONS[sid])
    correct_present=not(raw and ':answer-field/correct' not in QUESTIONS[sid][':question/answer-fields'][0])
    if not raw:
        prompt=normalize_prose(prompt);sol=normalize_prose(sol);values=[normalize_tex(v) for v in values]
    assessment={'h':str(p['h']),'k':str(p['k']),'r2':str(p['r']**2),'response':'full-circle-equation','information':'missing-source-diagram' if raw and sid in ('q-167932','q-167948') else 'labeled-center-and-radius'}
    fingerprint=digest(assessment)
    identity=digest({'version':VERSION,'prompt':prompt,'solution':sol,'bank':sorted(values),'kind':kind,'difficulty':level if rated else None,'correct':values[correct] if correct_present else None})
    question_id=uid('question:'+identity);field_id=uid(question_id+':field:'+kind)
    choices=[{':answer/id':uid(field_id+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    field={':answer-field/id':field_id,':answer-field/key':'field-1' if kind=='blank' else 'selection',':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':choices}
    if correct_present:field[':answer-field/correct']=[':answer/id',choices[correct][':answer/id']]
    if kind=='radio':rng.shuffle(choices)
    q={':question/id':question_id,':question/problem':prompt,':question/answer-fields':[field]}
    if rated:q[':question/difficulty']=':question.difficulty/'+level
    if sol is not None:q[':question/worked-solution']=sol
    meta={'version':VERSION,'seed':seed,'template':template,'bank_profile':profile or bank,'recipe_bank':BANKS[bank],'parameters':{k:str(v) for k,v in p.items()},'mathematical_fingerprint':fingerprint,'content_identity':identity,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'source_id':sid,'observed_level': 'easy' if sid and ':question/difficulty' in QUESTIONS[sid] else None,'authored_level':level if not sid else None,'domain':{'variables':'x,y real','radius':'positive','number_form':level if not sid else 'observed template','bounds':'See domain() and instructional-account.md'},'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'plot':plot,'raw_evidence_only':raw and (sid in ('q-54187','q-54210','q-167932','q-167948')),'eligible_for_learning':kind=='radio' and not(raw and sid in ('q-54187','q-54210','q-167932')),'evidence_only':kind=='blank' or not correct_present,'grading_compatibility':{'supported':kind=='radio' and correct_present,'reason':('Native symbolic grader does not parse complete equations (unconsumed mathematical notation); blank retained for source-field fidelity and mathematical review only.' if kind=='blank' else 'Raw source omits canonical correct ref.' if not correct_present else None)},'correct_inferred':bool(sid in ('q-54187','q-54210') and not raw),'presentation_repaired':bool(sid in ('q-167932','q-167948') and not raw)}
    record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':meta}
    if not raw:
        q[':question/problem']=normalize_prose(q[':question/problem'])
        q[':question/worked-solution']=normalize_prose(q[':question/worked-solution'])
        for answer in choices:answer[':answer/value']=normalize_tex(answer[':answer/value'])
    return record

def build_candidate_bank(shape, u, v, radii):
    if type(u)!=int or type(v)!=int or not (1<=abs(u)<=8 and 1<=abs(v)<=8 and abs(u)!=abs(v)):raise ValueError('Distinct nonzero absolute center magnitudes 1..8 required.')
    centers={
      'sign_swap':[(-u,v),(v,u),(u,v),(-u,-v),(-v,-u)],
      'axis':[(u,0),(-u,0),(0,u),(0,-u),(v,0)]
    }
    if shape not in centers or len(radii)!=5 or any(type(r)!=int or not 2<=r<=9 for r in radii):
        raise ValueError('Invalid bank shape or integer radii.')
    selected=centers[shape]
    if len(set(radii))==2:
        # Two centers occur with BOTH possible radii; a third occurs once.
        # This mapping uses the bank only and never inspects the correct role.
        big,small=sorted(set(radii),key=lambda r:radii.count(r),reverse=True)
        first=[i for i,r in enumerate(radii) if r==big]
        second=[i for i,r in enumerate(radii) if r==small]
        selected=[None]*5
        for c,i,j in zip(centers[shape][:2],first[:2],second):selected[i]=selected[j]=c
        selected[first[2]]=centers[shape][2]
    return [(h,k,r) for (h,k),r in zip(selected,radii)]

@checked_math_content
def generate_normal(level='easy',seed=0,template=None,field_type=None,parameters=None,profile=None,
             decision=None,shape=None,radius_profile=None,orientation=None):
    """One seed; decide true role first, build an independently eligible bank.

    Source profiles remain explicit replay only. All normal choices can be true
    with the bank unchanged, preventing a bank-only rule from identifying a key.
    """
    if level!='easy':raise ValueError('Only easy is supported; moderate and hard lack source evidence.')
    if profile:raise ValueError('Source profiles use generate_source().')
    if field_type not in (None,'radio',':answer-field.type/radio') or template not in (None,'graph_radio'):
        raise ValueError('Normal delivery supports graph_radio only; use explicit source replay for blanks.')
    rng=random.Random(seed)
    role=rng.randrange(5) if decision is None else decision
    if type(role)!=int or not 0<=role<5:raise ValueError('Correct role must be 0..4.')
    shape=shape or rng.choice(('sign_swap','axis'))
    radius_profile=radius_profile or rng.choice(('common_radius','two_radii'))
    if parameters is None:
        u,v=rng.sample(range(1,9),2);u*=rng.choice((-1,1));v*=rng.choice((-1,1));a,b=rng.sample(range(2,10),2)
        radii=[a]*5
        if radius_profile=='two_radii':
            for i in rng.sample(range(5),rng.choice((2,3))):radii[i]=b
    else:
        if set(parameters)!={'u','v','radii'}:raise ValueError('Normal bank parameters require u,v,radii.')
        u,v,radii=parameters['u'],parameters['v'],list(parameters['radii'])
    if radius_profile not in ('common_radius','two_radii'):raise ValueError('Unknown radius profile.')
    if len(set(radii))!=(1 if radius_profile=='common_radius' else 2):raise ValueError('Radius bank/profile mismatch.')
    if radius_profile=='two_radii' and sorted(radii.count(r) for r in set(radii))!=[2,3]:raise ValueError('Two radius groups must have sizes two and three.')
    bank=build_candidate_bank(shape,u,v,radii)
    h,k,r=bank[role]
    p={'h':exact(h),'k':exact(k),'r':exact(r),'orientation':orientation or rng.choice(('horizontal','vertical'))}
    if p['orientation'] not in ('horizontal','vertical'):raise ValueError('Unknown orientation.')
    values=[normalize_tex(equation(hh,kk,rr*rr)) for hh,kk,rr in bank]
    image,plot=render_plots(p)
    prompt=normalize_prose(f'![]({image})\n\nWhat is the equation of the circle given above?')
    sol=normalize_prose(solution(p))
    # No source-bank profile is inferred from a question's literal key position.
    identity=digest({'version':VERSION,'bank':values,'geometry':{k:str(v) for k,v in p.items()},'shape':shape})
    qid=uid('question:'+identity);fid=uid(qid+':selection')
    choices=[{':answer/id':uid(fid+':'+value),':answer/type':':answer.type/math',':answer/value':value} for value in values]
    correct=choices[role][':answer/id'];rng.shuffle(choices)
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},
      'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':sol,
      ':question/difficulty':':question.difficulty/easy',':question/answer-fields':[{
      ':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',
      ':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]},
      'generation':{'version':VERSION,'seed':seed,'template':'graph_radio','bank_profile':'authored_eligible_circles',
      'shape':shape,'radius_profile':radius_profile,'correct_role':role,'parameters':{k:str(v) for k,v in p.items()},
      'bank_parameters':{'u':u,'v':v,'radii':radii},'candidates':bank,'plot':plot,
      'semantic_circle':[h,k,r],'semantic_bank':bank,'rejections':0,
      'source_basis':SOURCE['basis'],'source_profiles':['q-70896','q-70898','q-117081'],
      'extension':'eligible correct-role reassignment and optional two-radius bank'}}

def generate(level='easy',seed=0,template=None,field_type=None,parameters=None,profile=None,**kwargs):
    if profile:
        if kwargs:raise ValueError('Normal bank controls cannot be used with source replay.')
        if profile not in QUESTIONS and not profile.startswith(('raw:','completed:')):
            raise ValueError('Use a source ID, raw:q-ID or completed:q-ID.')
        return generate_source(level,seed,template,field_type,parameters,profile)
    return generate_normal(level,seed,template,field_type,parameters,**kwargs)

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)

def markdown(record):
    q=record['question'];g=record['generation'];sid=g.get('source_id')
    original=bool(sid and g['bank_profile'].startswith('raw:') and g['parameters']=={k:str(v) for k,v in ORIGINAL[sid].items()})
    level=q.get(':question/difficulty','not rated').removeprefix(':question.difficulty/')
    out=('Original source replay' if original else 'Generated variant')+' / '+level+' / '+g['template']+'\n\n'
    if g.get('evidence_only'):out+='[Evidence only: '+g['grading_compatibility']['reason']+']\n\n'
    out+=q[':question/problem']+'\n\n'
    for f in q[':question/answer-fields']:
        for a in f[':answer-field/choices']:
            marked=' **CORRECT**' if f.get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else ''
            out+='- $'+a[':answer/value']+'$'+marked+'\n'
        if ':answer-field/correct' not in f:out+='[Original correct designation absent.]\n'
    return out+'\n'+q.get(':question/worked-solution','[Source worked solution absent.]')
def main():
    a=argparse.ArgumentParser();a.add_argument('--difficulty',choices=['easy','moderate','hard'],default='easy')
    a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1)
    a.add_argument('--format',choices=['markdown','json'],default='json');a.add_argument('--profile');args=a.parse_args()
    if args.count<1:a.error('--count must be positive')
    if args.difficulty!='easy':a.error('Only source-justified easy band is supported.')
    records=[generate(args.difficulty,args.seed+i,profile=args.profile) for i in range(args.count)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))

from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186087655-source-policy.json'))

if __name__=='__main__':main()
