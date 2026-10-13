#!/usr/bin/env python3
"""Given a labeled center and radius, construct the full standard circle equation.

Math database basis 1356. Source evidence and validation live in 17592186087655/.
Observed easy graph radio banks and blank template are parameterized faithfully.
Two unrated raw profiles retain absent difficulty, solution and correct refs.
Their completed profiles infer center/radius directly from inspected labeled plots.
The stripped blank diagram is raw evidence only; normal output restores information.
Moderate/hard are authored number-form extensions, never recovered source labels.
No center extraction, distance formula, midpoint, expansion or database writes.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, subprocess, sys, tempfile, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186087655
KP_UUID='82d6988b-3220-578f-ba1c-cd86b9e3dbf9'
TITLE='Finding the Equation of a Circle Given the Center and the Radius'
VERSION='circle-given-center-radius-2'
HERE=Path(__file__).resolve().with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
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
 'authored_sign_square':[('h','k','r2'),('-h','k','r2'),('h','-k','r2'),('-h','-k','r2'),('h','k','r')],
 'blank':[('h','k','r2')],
}
ORIGINAL={
 'q-54187':{'h':1,'k':3,'r':3,'orientation':'horizontal'},
 'q-54210':{'h':-2,'k':5,'r':7,'orientation':'vertical'},
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
    if set(p)!={'h','k','r','orientation'}:raise ValueError('Parameters require h,k,r,orientation only.')
    if p['orientation'] not in ('horizontal','vertical'):raise ValueError('Unknown radius orientation.')
    if p['r']<=0:raise ValueError('A circle needs positive radius.')
    if observed:
        # Preserve observed integer substitution workload. The complete bank
        # coefficient field still includes sqrt(r) in q-116929 distractors.
        if not all(p[t].is_Integer and abs(p[t])<=10 for t in ('h','k')) or not p['r'].is_Integer or not 2<=p['r']<=10:raise ValueError('Observed profiles: integer centers <=10, integer radius 2..10.')
        return
    if level=='easy':
        if not all(p[t].is_Integer and 1<=abs(p[t])<=8 for t in ('h','k')) or not p['r'].is_Integer or not 2<=p['r']<=9:raise ValueError('Easy: two nonzero integer shifts and integer radius 2..9.')
    elif level=='moderate':
        if not all(p[t].is_Integer and 1<=abs(p[t])<=6 for t in ('h','k')):raise ValueError('Moderate: two nonzero integer shifts <=6.')
        rational_radius(p['r'])
    elif level=='hard':
        if not all(p[t].is_Rational and not p[t].is_Integer and 1<=abs(p[t])<=6 and p[t].q in (2,3,4) for t in ('h','k')) or p['h']*p['k']>=0:raise ValueError('Hard: two proper noninteger rational shifts, denominators 2..4, opposite signs, magnitude 1..6.')
        rational_radius(p['r'])
    else:raise ValueError('Unknown difficulty.')
def rational_radius(r):
    if not r.is_Rational or r.is_Integer or not 1<r<5 or r.q not in (2,3,4) or r.p>19:raise ValueError('Authored rational radius: reduced denominator 2..4, numerator <=19, 1<r<5.')

def sample(level,rng,bank):
    radii=[sp.Rational(n,d) for d in (2,3,4) for n in range(3,20) if sp.Rational(n,d).q==d and 1<sp.Rational(n,d)<5]
    fractions=[sp.Rational(n,d) for d in (2,3,4) for n in range(3,25) if sp.Rational(n,d).q==d and 1<=sp.Rational(n,d)<=6]
    if level=='easy':p={'h':rng.choice([i for i in range(-8,9) if i]),'k':rng.choice([i for i in range(-8,9) if i]),'r':rng.randint(2,9)}
    elif level=='moderate':p={'h':rng.choice([i for i in range(-6,7) if i]),'k':rng.choice([i for i in range(-6,7) if i]),'r':rng.choice(radii)}
    elif level=='hard':
        sign=rng.choice((-1,1));p={'h':sign*rng.choice(fractions),'k':-sign*rng.choice(fractions),'r':rng.choice(radii)}
    else:raise ValueError('Unknown difficulty.')
    if bank=='q-117081':p['k']=0
    p['orientation']=rng.choice(('horizontal','vertical'))
    return {k:exact(v) if k!='orientation' else v for k,v in p.items()}

def render_plots(p,source_id=None,output_dir=None):
    if source_id and p=={k:(exact(v) if k!='orientation' else v) for k,v in ORIGINAL[source_id].items()}:
        q=QUESTIONS[source_id]
        images=re.findall(r'!\[\]\(([^)]+)\)',q[':question/problem'])
        if images:
            # Source path kept in learner markdown for raw fidelity; absolute
            # accessible path and hash carried separately in metadata.
            path=Path('/media/jake/SSD/EDB/math')/images[0]
            return images[0],{'renderer':'unchanged-source','absolute_path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'geometry':{k:str(v) for k,v in p.items()}}
    geom={k:str(v) for k,v in p.items()};key=digest({'parameters':geom,'render_version':'circle-plot-2'})
    render_dir=Path(output_dir) if output_dir is not None else HERE/'plots'
    output=render_dir/('circle-'+key+'.png');side=output.with_suffix('.json')
    output.parent.mkdir(parents=True,exist_ok=True)
    if not output.exists() or not side.exists():
        with tempfile.NamedTemporaryFile('w',suffix='.json',prefix='render-input-',dir=render_dir,delete=False) as f:
            json.dump({'parameters':geom,'output':str(output)},f);input_path=Path(f.name)
        try:subprocess.run([sys.executable,str(HERE/'render.py'),str(input_path)],check=True,capture_output=True,text=True)
        finally:input_path.unlink(missing_ok=True)
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

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    """Generate normal records or public raw source replay (profile='raw:q-ID')."""
    if level not in ('easy','moderate','hard'):raise ValueError('Difficulty must be easy, moderate or hard.')
    rng=random.Random(seed)
    if field_type:field_type=field_type.removeprefix(':answer-field.type/')
    raw=bool(profile and profile.startswith('raw:'))
    sid=profile.split(':')[-1] if profile and (profile.startswith('raw:') or profile.startswith('completed:')) else None
    if sid and sid not in QUESTIONS:raise ValueError('Unknown source profile.')
    if profile in QUESTIONS:sid=profile
    observed=bool(sid)
    if observed and level!='easy':raise ValueError('Observed sources support easy workload only; raw unrated level remains omitted.')
    if sid:
        bank='blank' if sid=='q-167932' else sid
        expected_template='missing_input_blank' if sid=='q-167932' and raw else ('graph_blank' if sid=='q-167932' else 'graph_radio')
        if template and template!=expected_template:raise ValueError('Template/profile disagreement.')
        template=expected_template
    else:
        template=template or ('graph_blank' if field_type=='blank' else 'graph_radio')
        if template not in ('graph_radio','graph_blank'):raise ValueError('Unknown template.')
        bank=profile or ('blank' if template=='graph_blank' else 'authored_sign_square')
        if bank not in BANKS or bank in QUESTIONS:raise ValueError('Select observed banks by source profile.')
    kind='blank' if template in ('graph_blank','missing_input_blank') else 'radio'
    if field_type and field_type.removeprefix(':answer-field.type/')!=kind:raise ValueError('Field type conflicts with template.')
    if (kind=='blank') != (bank=='blank'):raise ValueError('Profile/field mismatch.')
    if parameters is not None:
        p={k:exact(v) if k!='orientation' else v for k,v in parameters.items()};domain(level,p,observed)
        if sid in ('q-117081','q-167932') and p['k']!=0:raise ValueError('Observed axis template requires k=0.')
        values,correct=validate_bank(p,bank)
    else:
        for _ in range(500):
            p=sample(level,rng,bank)
            if sid=='q-167932':p['k']=sp.Integer(0)
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
    sol=replay_solution(sid,p) if raw else solution(p,kind=='blank')
    # Source q-117081 uses braces around a full shifted term. Its exact source
    # display notation is preserved by replay_solution, including all stages.
    rated=not(raw and ':question/difficulty' not in QUESTIONS[sid])
    correct_present=not(raw and ':answer-field/correct' not in QUESTIONS[sid][':question/answer-fields'][0])
    assessment={'h':str(p['h']),'k':str(p['k']),'r2':str(p['r']**2),'response':'full-circle-equation','information':'missing-source-diagram' if raw and sid=='q-167932' else 'labeled-center-and-radius'}
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
    meta={'version':VERSION,'seed':seed,'template':template,'bank_profile':profile or bank,'recipe_bank':BANKS[bank],'parameters':{k:str(v) for k,v in p.items()},'mathematical_fingerprint':fingerprint,'content_identity':identity,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'source_id':sid,'observed_level': 'easy' if sid and ':question/difficulty' in QUESTIONS[sid] else None,'authored_level':level if not sid else None,'domain':{'variables':'x,y real','radius':'positive','number_form':level if not sid else 'observed template','bounds':'See domain() and classification.md'},'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'plot':plot,'raw_evidence_only':raw and (sid in ('q-54187','q-54210','q-167932')),'eligible_for_learning':kind=='radio' and not(raw and sid in ('q-54187','q-54210','q-167932')),'evidence_only':kind=='blank' or not correct_present,'grading_compatibility':{'supported':kind=='radio' and correct_present,'reason':('Native symbolic grader does not parse complete equations (unconsumed mathematical notation); blank retained for source-field fidelity and mathematical review only.' if kind=='blank' else 'Raw source omits canonical correct ref.' if not correct_present else None)},'correct_inferred':bool(sid in ('q-54187','q-54210') and not raw),'presentation_repaired':bool(sid=='q-167932' and not raw)}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':meta}

# EASY: observed integer center/radius substitution; normal common bank uses two
# nonzero shifts. Source axis templates remain explicit source profiles.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# MODERATE (authored): two integer shifts, reduced noninteger rational radius;
# square numerator and denominator while retaining the same three solution rows.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# HARD (authored): two noninteger rational shifts of opposite signs plus rational
# radius. Exact fraction signs and square must all be retained; no new geometry.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

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
    a=argparse.ArgumentParser();a.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',choices=['markdown','json'],default='markdown');a.add_argument('--template');a.add_argument('--profile');args=a.parse_args()
    levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in levels for i in range(args.count)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
