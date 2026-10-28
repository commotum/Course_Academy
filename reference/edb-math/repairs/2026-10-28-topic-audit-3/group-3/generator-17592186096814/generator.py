#!/usr/bin/env python3
"""Portable repair of the existing diagram unit-vector generator, source basis 2765.
Easy: canonical integer legs. Moderate: half-grid single vector. Hard: two
slanted head-to-tail vectors and fractional resultant, as q119805/q19276.
Observed bank profiles are evidence only; defaults are complete authored banks.
See private evidence directory for limitations and source metadata repairs.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode=True
from audit_runtime import asset_payload,normalize_question
from math_format import normalize_prose,normalize_tex
import argparse,hashlib,json,random,uuid,os,sys
from importlib.metadata import version as dependency_version
sys.dont_write_bytecode=True
from math_format import normalize_prose, normalize_tex, checked_math_content
from pathlib import Path
import sympy as S
ID=17592186096814
HERE=Path(__file__).resolve().parent
RAW=json.loads((HERE/'source.json').read_text());REC=RAW['material']['kp'];SOURCES={x[':question/math-academy-id']:x for x in REC[':knowledge-point/questions']}
VERSION='unit-diagram-2-portable-audit9837'
def digest(x):return hashlib.sha256(json.dumps(asset_payload(x),sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.NAMESPACE_URL,'kp'+str(ID)+':'+x))
def tex(x):return S.latex(S.simplify(x))
def rat(x):return S.Rational(str(x))
def number(x):return str(int(x)) if x.q==1 else str(float(x))
def frac(k,v):return r'\frac{'+tex(k)+r'}{'+v+'}'
def norm(v):return S.sqrt(sum(x*x for x in v))
def vec(v):return [rat(x) for x in v]
def add(a,b):return [x+y for x,y in zip(a,b)]
def bank_data(template,p,profile):
    a=vec(p['a']);b=vec(p.get('b',[0,0]));v=add(a,b);L=norm(v);name=p['names'][0] if template=='single' else '+'.join(p['names']);V=name if template=='single' else '('+name+')'
    if profile=='observed_c':
        s=rat(p['scale']);Q=65*s*s;W=55*s*s
        vals=[r'\frac{1}{\sqrt{'+tex(Q)+r'}}c',r'\frac{1}{\sqrt{'+tex(W)+r'}}c',r'\frac{\sqrt{'+tex(Q)+r'}}{4}c',r'\frac{2}{\sqrt{'+tex(W)+r'}}c',r'\frac{2}{\sqrt{'+tex(Q)+r'}}c']
        co=[1/S.sqrt(Q),1/S.sqrt(W),S.sqrt(Q)/4,2/S.sqrt(W),2/S.sqrt(Q)];objects=[[k*x for x in v] for k in co];correct=4
    elif profile=='observed_qr':
        s=rat(p['scale']);q,r=p['names'];Q=13*s*s;R=29*s*s;T=73*s*s
        vals=[r'\frac{r}{\sqrt{'+tex(R)+'}}',r'\frac{q + r}{'+tex(5*s)+'}',r'\frac{2q}{\sqrt{'+tex(Q)+r'}} + \frac{r}{\sqrt{'+tex(R)+'}}','(2(q + r))/(\\sqrt{'+tex(T)+'})',r'\frac{q + r}{\sqrt{'+tex(Q)+'}}']
        objects=[[x/S.sqrt(R) for x in b],[x/(5*s) for x in v],[2*x/S.sqrt(Q)+y/S.sqrt(R) for x,y in zip(a,b)],[2*x/S.sqrt(T) for x in v],[x/S.sqrt(Q) for x in v]];correct=3
    elif profile=='observed_hard':
        h=abs(v[0]);co=[1/h,1/(h*S.sqrt(2)),h,1/L,1/(2*L)]
        vals=[tex(k)+V for k in co];objects=[[k*x for x in v] for k in co];correct=3
    else:
        co=[1/L,1/L**2,L,1/abs(v[0]),2/L];vals=[tex(k)+V for k in co];objects=[[k*x for x in v] for k in co];correct=0
    # Criterion uses the full actual vector, including opposite parallel unit vectors.
    valid=[S.simplify(sum(x*x for x in z)-1)==0 and S.simplify(z[0]*v[1]-z[1]*v[0])==0 for z in objects]
    if valid!=[i==correct for i in range(5)]:raise ValueError('ambiguous complete bank')
    if len({tuple(S.simplify(x) for x in z) for z in objects})!=5:raise ValueError('equivalent options')
    return vals,objects,correct,v,L,name

def output_dir():
    value=os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
    if not value: raise ValueError('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR must name an asset directory outside the package')
    out=Path(value).resolve()
    if out.is_relative_to(HERE):
        raise ValueError('Generated assets must not be written into the package root or its descendants')
    out.mkdir(parents=True,exist_ok=True)
    return out

def render_plots(geometry):
    key=digest({'geometry':geometry,'renderer_sha256':hashlib.sha256((HERE/'render.py').read_bytes()).hexdigest()})
    out=output_dir()/key
    paths={role:str(out.with_name(out.name+'-'+role+'.png')) for role in ('prompt','solution')}
    if not all(Path(p).exists() for p in paths.values()) or not out.with_suffix('.json').exists():
        from render import render
        render(geometry,out)
    return paths

def validate_parameters(level,template,p,profile):
    if set(p)-{'a','b','names','scale'}:raise ValueError('unknown parameter')
    a=vec(p['a']);b=vec(p.get('b',[0,0]));v=add(a,b)
    if len(a)!=2 or len(b)!=2 or len(p['names'])!=(1 if template=='single' else 2):raise ValueError('shape')
    if template=='single' and any(b):raise ValueError('single vector cannot have a hidden second vector')
    if any(not n.isalpha() or len(n)!=1 for n in p['names']) or len(set(p['names']))!=len(p['names']):raise ValueError('names')
    if any(x==0 for x in a) or any(x==0 for x in v):raise ValueError('two legs required')
    if profile in ('observed_c','observed_qr'):
        s=rat(p['scale']);expected=([2*s,-S.Rational(7,2)*s],[0,0]) if profile=='observed_c' else ([S.Rational(5,2)*s,-S.Rational(3,2)*s],[S.Rational(3,2)*s,3*s])
        if s not in (1,2) or a!=expected[0] or b!=expected[1]:raise ValueError('evidence-only similarity domain')
        if p['names']!=(['c'] if profile=='observed_c' else ['q','r']):raise ValueError('observed names')
    elif level=='easy':
        if template!='single' or any(x.q!=1 or not 1<=abs(x)<=5 for x in a):raise ValueError('easy integer legs 1..5')
    elif level=='moderate':
        if template!='single' or any((2*x).q!=1 or not S.Rational(1,2)<=abs(x)<=4 for x in a) or all(x.q==1 for x in a):raise ValueError('moderate half-grid legs')
    else:
        if template!='sum' or any(x==0 or (2*x).q!=1 or abs(x)>4 for x in a+b) or all(x.q==1 for x in v) or not any(x*y<0 for x,y in zip(a,b)):raise ValueError('hard fractional slanted sum with cancellation')
    bank_data(template,p,profile)

# Easy: canonical diagram and the unchanged Pythagorean/normalization operation.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: authored half-grid single vectors, anchored in unrated q20407.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: observed head-to-tail sums, fractional resultant and same normalization.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def _generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if profile in ('raw_c','raw_qr','raw_hard'):
        source_id={'raw_c':'q-20407','raw_qr':'q-19276','raw_hard':'q-119805'}[profile]
        if parameters is not None and parameters!=SOURCE_PARAMS[source_id]:
            raise ValueError('Raw replay is only defined at original source parameters')
        return {'knowledge_point':{'db_id':ID,'id':REC[':knowledge-point/id'],'title':REC[':knowledge-point/title']},
                'question':json.loads(json.dumps(SOURCES[source_id])),
                'generation':{'version':VERSION,'source_id':source_id,'bank_profile':profile,
                              'evidence_only':True,'eligible_for_learning':False,'seed':seed}}
    if level not in ('easy','moderate','hard') or field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('level/field')
    template=template or ('sum' if level=='hard' else 'single');profile=profile or 'authored_method'
    if profile=='observed_c' and (level!='moderate' or template!='single'):raise ValueError('c replay level/template')
    if profile=='observed_qr' and (level!='hard' or template!='sum'):raise ValueError('qr replay level/template')
    if template not in ('single','sum') or profile not in ('authored_method','observed_c','observed_qr','observed_hard'):raise ValueError('template/profile')
    if profile=='observed_hard' and (level!='hard' or template!='sum'):raise ValueError('hard replay')
    rng=random.Random(seed)
    if parameters is not None:p=json.loads(json.dumps(parameters));validate_parameters(level,template,p,profile)
    else:
        if profile=='observed_c':p={'a':[2,-3.5],'names':['c'],'scale':1};validate_parameters(level,template,p,profile)
        elif profile=='observed_hard':p=json.loads(json.dumps(SOURCE_PARAMS['q-119805']));validate_parameters(level,template,p,profile)
        elif profile=='observed_qr':p={'a':[2.5,-1.5],'b':[1.5,3],'names':['q','r'],'scale':1};validate_parameters(level,template,p,profile)
        else:
            for _ in range(1000):
                if level=='easy':p={'a':[rng.choice([-1,1])*rng.randint(1,5),rng.choice([-1,1])*rng.randint(1,5)],'names':['a']}
                elif level=='moderate':p={'a':[rng.choice([-1,1])*rng.randint(1,8)/2,rng.choice([-1,1])*rng.randint(1,8)/2],'names':['c']}
                else:p={'a':[rng.choice([-1,1])*rng.randint(1,8)/2,rng.choice([-1,1])*rng.randint(1,8)/2],'b':[rng.choice([-1,1])*rng.randint(1,8)/2,rng.choice([-1,1])*rng.randint(1,8)/2],'names':['m','n']}
                try:validate_parameters(level,template,p,profile);break
                except ValueError:continue
            else:raise RuntimeError('sampling exhausted')
    vals,objects,correct,v,L,name=bank_data(template,p,profile)
    a=vec(p['a']);b=vec(p.get('b',[0,0]));A=[0,0];B=[float(x) for x in v];geometry={'A':A,'B':B,'names':p['names'],'grid_increment':.5}
    if template=='sum':geometry['P']=[float(x) for x in a]
    plots=render_plots(geometry)
    source_id={'observed_c':'q-20407','observed_qr':'q-19276','observed_hard':'q-119805'}.get(profile)
    original=source_id and p==SOURCE_PARAMS[source_id]
    if original:
        # Reuse inspected exact raster; mathematics/banks still derive through recipes.
        prompt_image=SOURCES[source_id][':question/problem'].split(')')[0][4:]
    else:prompt_image=plots['prompt']
    if original:
        vals=[normalize_tex(a[':answer/value']) for a in SOURCES[source_id][':question/answer-fields'][0][':answer-field/choices']]
        # Source banks have their own ordering; locate the computed correct value.
        ordering={'q-20407':[2,3,4,0,1],'q-19276':[1,2,3,4,0],'q-119805':[0,1,2,3,4]}[source_id]
        objects=[objects[i] for i in ordering]
        correct={'q-20407':2,'q-19276':2,'q-119805':3}[source_id]
    image='![]('+prompt_image+')'
    if profile=='observed_hard':opening='Consider the picture above. Which of the following is a unit vector that is parallel to $'+name+'?$'
    elif profile=='observed_qr':opening='Consider the picture above. Which of the following is a unit vector that is parallel to $q + r$?'
    else:opening='Consider the picture shown above. Find a unit vector that is parallel to $'+name+'$.'
    prompt=image+'\n\n'+opening
    if not source_id:prompt+=' Choose the unit vector in the same direction.'
    hx,hy=[abs(x) for x in v];mtex=tex(L);ktex=tex(1/L);V=name if template=='single' else '('+name+')'
    if profile=='observed_hard':
        if p['names']!=['m','n']:raise ValueError('observed hard vector names')
        ktex=frac(S.sqrt((L**2).q),tex(S.sqrt((L**2).p)))
        sol_image=(SOURCES[source_id][':question/worked-solution'].split('![](')[1].split(')')[0]) if original else plots['solution']
        solution=HARD_SOLUTION.format(image=sol_image,h=number(hx),hfrac=tex(hx),y=number(hy),ytex=tex(hy),h2=tex(hx**2),y2=tex(hy**2),mag=mtex,unit=ktex)
    else:
        prefix=('First, we have to find $'+name+'$. According to the triangle law of addition, the resultant $'+name+'$ goes from the tail of $'+p['names'][0]+'$ to the head of $'+p['names'][1]+'$:\n\n') if template=='sum' else ''
        solution=prefix+'![]('+plots['solution']+')\n\nIn $\\bigtriangleup AHB$ we have $\\angle AHB=90^\\circ$, $AH='+number(hx)+'$ and $BH='+number(hy)+'$. So, the Pythagorean theorem gives\n\n$$\n\\begin{aligned}\nAB &= \\sqrt{AH^2+BH^2} \\\\\n&= \\sqrt{('+tex(hx)+')^2+('+tex(hy)+')^2} \\\\\n&= \\sqrt{'+tex(hx**2)+'+'+tex(hy**2)+'} \\\\\n&= '+mtex+'\n\\end{aligned}\n$$\n\nHence, the magnitude of $'+name+'$ is $'+mtex+'$. Consequently, the unit vector is\n\n$$\n\\begin{aligned}\nu &= \\frac{1}{|'+name+'|}\\cdot '+V+' \\\\\n&= '+ktex+V+'\n\\end{aligned}\n$$'
    if original and source_id=='q-119805':solution=SOURCES[source_id][':question/worked-solution']
    prompt=normalize_prose(prompt);solution=normalize_prose(solution);vals=[normalize_tex(v) for v in vals]
    # Output location is transport metadata, never mathematical identity.
    stable_prompt=prompt;stable_solution=solution
    for path in plots.values():
        stable_prompt=stable_prompt.replace(path,Path(path).name)
        stable_solution=stable_solution.replace(path,Path(path).name)
    identity=digest({'version':VERSION,'prompt':stable_prompt,'solution':stable_solution,'bank':sorted(vals)});qid=uid(identity);fid=uid(identity+':selection');choices=[{':answer/id':uid(fid+value),':answer/type':':answer.type/math',':answer/value':value} for value in vals];correct_id=choices[correct][':answer/id'];rng.shuffle(choices)
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct_id]}
    task=digest({'a':[str(x) for x in a],'b':[str(x) for x in b],'increment':.5,'template':template})
    return {'knowledge_point':{'db_id':ID,'id':REC[':knowledge-point/id'],'title':REC[':knowledge-point/title']},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[field]},'generation':{'version':VERSION,'template':template,'bank_profile':profile,'parameters':p,'seed':seed,'source_id':source_id,'provenance':{k:RAW[k] for k in ('database','basis','lineage')},'evidence_only':profile in ('observed_c','observed_qr'),'eligible_for_learning':profile not in ('observed_c','observed_qr'),'mathematical_fingerprint':task,'content_fingerprint':identity,'geometry':geometry,'plots':plots,'answer_vectors':{value:[str(S.simplify(x)) for x in obj] for value,obj in zip(vals,objects)},'magnitude':str(L),'dependencies':{'sympy':S.__version__,'matplotlib':dependency_version('matplotlib')},'source_repairs':(['inferred correct designation','authored difficulty','authored worked solution'] if profile in ('observed_c','observed_qr') else [] if profile=='observed_hard' else [])}}

@checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if profile and profile.startswith('raw_'):
        raise ValueError('Use replay_source for raw evidence; incomplete captures are not learner questions')
    return _generate(level,seed,template,field_type,parameters,profile)

def replay_source(source_id):
    if source_id=='e-5181':
        return {'knowledge_point':{'db_id':ID,'id':REC[':knowledge-point/id'],'title':REC[':knowledge-point/title']},'question':json.loads(json.dumps(REC[':knowledge-point/canonical-example'])),'generation':{'version':VERSION,'source_id':source_id,'evidence_only':True,'eligible_for_learning':False}}
    return _generate('hard',profile={'q-20407':'raw_c','q-19276':'raw_qr','q-119805':'raw_hard'}[source_id])

SOURCE_PARAMS={'q-19276':{'a':[2.5,-1.5],'b':[1.5,3],'names':['q','r'],'scale':1},'q-20407':{'a':[2,-3.5],'names':['c'],'scale':1},'q-119805':{'a':[1,-.5],'b':[-1.5,2.5],'names':['m','n']}}
# Extracted formal solution template, with complete mathematical slots.
HARD_SOLUTION=SOURCES['q-119805'][':question/worked-solution']
HARD_SOLUTION=HARD_SOLUTION.replace('{','{{').replace('}','}}')
HARD_SOLUTION=HARD_SOLUTION.replace('images/87/87647211f77776c5f5f740c205fafb150eef1b9d3ebefb82df73a9fdcd953bdb.png','{image}').replace('AH=0.5=\\frac{{1}}{{2}}','AH={h}={hfrac}').replace('BH=2.','BH={y}.').replace('\\frac{{1}}{{2}}','{hfrac}').replace('+{{2}}^{{2}}','+{{{ytex}}}^{{2}}').replace('\\frac{{1}}{{4}}+4','{h2}+{y2}').replace('\\frac{{\\sqrt{{17}}}}{{2}}','{mag}').replace('\\frac{{2}}{{\\sqrt{{17}}}}','{unit}')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='easy');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args();
    if args.count<1:ap.error('--count must be positive')
    records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    if args.format=='json':print(json.dumps(records,indent=2))
    else:
        for r in records:
            q=r['question'];print(q[':question/problem']);print('\n'.join('$'+a[':answer/value']+'$' for a in q.get(':question/answer-fields',[{':answer-field/choices':[]}])[0][':answer-field/choices']));print('\n'+q.get(':question/worked-solution','')+'\n')
if __name__=='__main__':main()
