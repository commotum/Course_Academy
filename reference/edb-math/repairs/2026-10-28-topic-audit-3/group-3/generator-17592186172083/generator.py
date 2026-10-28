"""Seeded, relocatable vector-field practice. No services or database writes."""
from __future__ import annotations
import sys
sys.dont_write_bytecode=True
from audit_runtime import asset_payload,normalize_question
from math_format import normalize_prose,normalize_tex
import argparse, copy, hashlib, itertools, json, math, os, random, uuid
from pathlib import Path
import sympy as s
from math_format import normalize_prose, normalize_tex, validate_generated_record
KP_ID=17592186172083
KP_UUID='a5b00f0c-fc7f-5262-b1a3-cdd6c1560cd6'
TITLE='Sketching a Two-Dimensional Vector Field'
VERSION='vector-field-v2-audit9837'
HERE=Path(__file__).resolve().parent
X,Y=s.symbols('x y',real=True)
A,B=s.symbols('a b',real=True)

FAMILIES={
 'square_linear':(A*X**2,B*Y),
 'trig':(A*s.cos(s.pi*X),B*s.sin(s.pi*Y/2)),
 'trig_product':(A*s.sin(s.pi*X/2),B*X*Y),
 'linear_exp':(A*X,B**Y),
 'ratio_abs':(-A*X/Y,-B*s.Abs(X)),
 'rational_shift':(A*Y/(1-Y),B*X/(Y-1)),
 'rational_product':(A*Y/(X*Y+1),B*X/(X*Y+1)),
 'linear_shared':(Y-A*X,B*Y-A*B*X),
 'affine':(Y-A,X+B),
 'inward':(A*X,B*Y),
 'product_square':(A*X*Y,B*X**2)}
# Source geometries are extracted from inspected plots (units, NOT pixels).
# Geometry of the q-122745 small unlabelled arrow is approximate; raw reuse at
# original parameters guarantees its full fidelity, without exact-value claims.
OBSERVED={
 'q-122264':('square_linear',1,-2,[[-2,1],[0,-2],[2,3]],[
 [[4,-2],[0,4],[4,-6]],[[-2,-2],[0,4],[2,-6]],[[-2,'1/2'],[0,-1],[2,'3/2']],[[-4,-2],[0,4],[-4,-6]],[[4,-1],[0,2],[4,-3]]],0),
 'q-122756':('trig',2,2,[[-3,1],[-2,-1],[4,-4]],[
 [[0,2],[-2,-2],[0,2]],[[-2,2],[2,-2],[2,0]],[[0,2],[2,-2],[0,2]],[[-2,0],[2,2],[-2,0]],[[-2,0],[2,-2],[-2,0]]],1),
 'q-122742':('trig_product',3,1,[[-1,1],[1,2],[2,-1]],[
 [[0,-1],[0,2],[-3,-2]],[[-3,-1],[3,2],[0,-2]],[[3,1],[-3,2],[0,-1]],[[0,-1],[0,2],[3,-2]],[[-3,-1],[3,1],[0,2]]],1),
 'q-122744':('linear_exp',-2,2,[[-4,2],[-1,1],[2,0]],[
 [[4,5],[1,3],[-2,1]],[[8,2],[2,1],[-4,0]],[[-4,-1],[-1,-1],[2,-1]],[[0,3],[1,1],[4,-1]],[[8,4],[2,2],[-4,1]]],4),
 'q-122759':('ratio_abs',1,1,[[-3,1],[2,-1],[4,2]],[
 [[3,-2],[2,-2],[-2,-2]],[[3,-3],[2,-2],[-2,-4]],[[-3,-2],[-2,-2],[2,-2]],[[3,3],[2,2],[-2,4]],[[-3,-3],[-2,-2],[2,-4]]],1),
 'q-122764':('rational_shift',2,1,[[-2,3],[2,-1],[4,2]],[
 [[-1,-3],[-1,-1],[4,-4]],[[-1,1],[1,1],[-2,-4]],[[-3,1],[-1,1],[-4,-4]],[[-3,-1],[-1,-1],[-4,4]],[[1,3],[1,1],[-4,4]]],3),
 'q-122745':('rational_product',1,1,[[-2,0],[1,-2],[0,2]],[
 [[0,-2],[-1,-1],[2,0]],[[0,-4],[4,-2],['5/4',0]],[[0,2],[-1,'1/2'],[2,0]],[[0,2],[4,-2],[2,0]],[[0,-2],[2,-1],[2,0]]],4),
 'q-122752':('linear_shared',2,2,[[1,3],[-1,-1],[3,2]],[
 [[1,2],[1,2],[-4,-8]],[[-1,2],[-1,2],[4,-8]],[[-2,-4],[0,2],[1,-5]],[[5,-1],[-1,-1],[1,4]],[[2,1],[0,1],[-1,-4]]],0),
 'q-122754':('affine',2,2,[[-5,3],[0,0],[2,-3]],[
 [[4,-4],[1,1],[-2,3]],[[1,-3],[-2,2],[-5,4]],[[6,-2],[1,1],[-1,4]],[[2,-4],[-1,1],[-4,3]],[[7,-5],[2,-2],[0,1]]],1),
 'q-122758':('inward',-1,-1,[[1,4],[2,-2],[4,-2]],[
 [[-1,2],[-2,-1],[-4,-1]],[[4,1],[-2,2],[-2,4]],[[-4,1],[2,2],[2,4]],[[-1,-4],[-2,2],[-4,2]],[[1,4],[2,-2],[4,-2]]],3)}

FAMILIES['coupled']=(A*Y-B*X,B*X+A*Y)

def digest(obj):return hashlib.sha256(json.dumps(asset_payload(obj),sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(name):return str(uuid.uuid5(uuid.UUID(KP_UUID),str(asset_payload(name))))
def rat(v):
 z=s.Rational(str(v));return z

def field_components(template,p):
 family='product_square' if template.startswith('product_square_') else template
 return tuple(s.simplify(z.subs({A:rat(p['a']),B:rat(p['b'])})) for z in FAMILIES[family])
def evaluate(template,p):
 fs=field_components(template,p)
 return [[s.simplify(f.subs({X:rat(x),Y:rat(y)})) for f in fs] for x,y in p['points']]
def source_parameters(source_id):
 t,a,b,points,bank,k=OBSERVED[source_id]
 return {'a':a,'b':b,'points':points}
def exact_lists(v):return [[str(z) for z in row] for row in v]

def tex(z):return s.latex(s.sympify(z)).replace('\\log','\\ln')
def vector_tex(u,v):
 parts=[]
 for z,label in [(u,'i'),(v,'j')]:
  z=s.sympify(z)
  if z==0:continue
  sign='-' if not z.is_Add and z.could_extract_minus_sign() else '+'
  mag=-z if sign=='-' else z
  body=((r'\left('+tex(mag)+r'\right)' if mag.is_Add else tex(mag))+r'\,') if mag!=1 else ''
  if not parts and sign=='+':sign=''
  parts.append(sign+body+label)
 return ''.join(parts) or '0'
def point_tex(pt):return '('+','.join(tex(z) for z in pt)+')'
def substitution_tex(template,p,pt):
 # Unevaluated complete operation masks retain the two coordinate substitutions.
 x,y=map(tex,pt);a,b=tex(p['a']),tex(p['b']);px='('+x+')';py='('+y+')';pa='('+a+')';pb='('+b+')'
 family='product_square' if template.startswith('product_square_') else template
 masks={
 'coupled':(pa+py+'-'+pb+px,pb+px+'+'+pa+py),
 'square_linear':(pa+px+'^{2}',pb+py),
 'trig':(pa+r'\cos(\pi '+px+')',pb+r'\sin(\frac{\pi '+py+'}{2})'),
 'trig_product':(pa+r'\sin('+tex(s.pi*rat(pt[0])/2)+')',pb+px+py),
 'linear_exp':(pa+px,'{'+b+'}^{'+y+'}'),
 'ratio_abs':('-'+pa+r'\frac{'+x+'}{'+y+'}','-'+pb+'|'+x+'|'),
 'rational_shift':(r'\frac{'+pa+py+'}{1-'+py+'}',r'\frac{'+pb+px+'}{'+py+'-1}'),
 'rational_product':(r'\frac{'+pa+py+'}{'+px+py+'+1}',r'\frac{'+pb+px+'}{'+px+py+'+1}'),
 'linear_shared':(py+'-'+pa+px,pb+py+'-'+pa+pb+px),
 'affine':(py+'-'+pa,px+'+'+pb),
 'inward':(pa+px,pb+py),
 'product_square':(pa+px+py,pb+px+'^{2}')}
 u,v=masks[family];return r'\left('+u+r'\right)\,i+'+r'\left('+v+r'\right)\,j'


SOURCE_IDS={'q-122264': '19719bc2-a844-5b6e-926d-79b5bdfa6933', 'q-122756': '59a69c0f-c2af-5b88-9b38-1fbc42cfdc3f', 'q-122742': '2b3ac067-5818-5125-bedf-bd1f05f196a9', 'q-122744': 'f0ef3069-54df-58ef-8ea9-a7adc99649e7', 'q-122759': 'c5565e07-6be0-586e-b2a1-438c9383fcb4', 'q-122764': '30d646c9-1021-587c-bc37-6244d8e4d4a6', 'q-122745': '7e446a55-b0d3-59f4-abde-52af19baebe8', 'q-122752': '709ee56e-badf-53e5-8fe9-cd6e97119ca1', 'q-122754': '5b5b3650-421e-53e6-b6b4-9b4c7a243072', 'q-122758': 'd04f0b91-140d-549f-8f9d-31d1d9b6c7bc'}
def formula_components(template,p):
    """Ordered source forms, independent of the CAS's canonical rewrites."""
    a,b=rat(p['a']),rat(p['b'])
    def term(c,z=''):
        if not z:return tex(c)
        return ('-' if c==-1 else '' if c==1 else tex(c)) + z
    def signed(c,z=''):
        v=term(c,z);return v if v.startswith('-') else '+'+v
    return {
        'square_linear':(term(a,'x^{2}'),term(b,'y')),
        'trig':(term(a,r'\cos(\pi x)'),term(b,r'\sin(\frac{\pi y}{2})')),
        'trig_product':(term(a,r'\sin(\frac{\pi x}{2})'),term(b,'xy')),
        'linear_exp':(term(a,'x'),tex(b)+'^{y}'),
        'ratio_abs':(term(-a,r'\frac{x}{y}'),term(-b,'|x|')),
        'rational_shift':(r'\frac{'+term(a,'y')+'}{1-y}',r'\frac{'+term(b,'x')+'}{y-1}'),
        'rational_product':(r'\frac{'+term(a,'y')+'}{xy+1}',r'\frac{'+term(b,'x')+'}{xy+1}'),
        'linear_shared':('y'+signed(-a,'x'),term(b,'y')+signed(-a*b,'x')),
        'affine':('y'+signed(-a),'x'+signed(b)),
        'inward':(term(a,'x'),term(b,'y')),
        'coupled':(term(a,'y')+signed(-b,'x'),term(b,'x')+signed(a,'y')),
        'product_square':(term(a,'xy'),term(b,'x^{2}'))}[template]

EASY=list(dict.fromkeys(v[0] for v in OBSERVED.values()))
def sample(level,template,rng):
    if level=='easy':
        sid=next(k for k,v in OBSERVED.items() if v[0]==template)
        p=source_parameters(sid)
        p={'a':p['a'],'b':p['b'],'points':rng.sample(list(itertools.product(range(-3,4),repeat=2)),3)}
        # Preserve the full scalar form; vary signs where the domain permits it.
        p['a']=rng.choice([-1,1])*abs(p['a'])
        if template!='linear_exp':p['b']=rng.choice([-1,1])*abs(p['b'])
        return p
    pool=list(itertools.product([-2,-1,0,1,2],repeat=2))
    return {'a':rng.choice([-1,1] if level=='moderate' else [-2,-1,1,2]),
            'b':rng.choice([-1,1] if level=='moderate' else [-2,-1,1,2]),
            'points':rng.sample(pool,3)}

def valid(p,template):
    if set(p)!={'a','b','points'}:raise ValueError('Expected a,b,points')
    p={'a':str(rat(p['a'])),'b':str(rat(p['b'])),'points':exact_lists([[rat(z) for z in row] for row in p['points']])}
    pts=p['points']
    if not rat(p['a']) or not rat(p['b']):raise ValueError('Nonzero coefficients')
    if len(pts)!=3 or len(set(map(tuple,pts)))!=3 or any(len(row)!=2 for row in pts):raise ValueError('Three distinct tails')
    if any(rat(z).q!=1 or abs(rat(z))>5 for row in pts for z in row):raise ValueError('Small integer coordinates')
    vs=evaluate(template,p)
    if any(z.is_Rational is not True or abs(z)>8 for row in vs for z in row):raise ValueError('Domain or vector bound')
    # A whole zero field on these three tails would eliminate the task.
    if all(not z for row in vs for z in row):raise ValueError('All vectors zero')
    return p

def bank(correct,points,level,rng):
    if level=='easy':
        # Complete signed-permutation profiles, chosen before presentation.
        candidates=[]
        for swap,sx,sy in itertools.product([False,True],[-1,1],[-1,1]):
            z=[([sx*v,sy*u] if swap else [sx*u,sy*v]) for u,v in correct]
            if z!=correct and z not in candidates:candidates.append(z)
        if len(candidates)<4:raise ValueError('Degenerate signed-permutation bank')
        return [correct]+rng.sample(candidates,4),{'kind':'signed-permutation'}
    pools=[];names=[];unused=[]
    for (u,v),(x,y) in zip(correct,points):
        x,y=rat(x),rat(y)
        recipes=[('reverse-horizontal',[-u,v]),('reverse-vertical',[u,-v]),
                 ('swap-components',[v,u]),('double-horizontal',[2*u,v]),
                 ('halve-horizontal',[u/2,v]),('double-vertical',[u,2*v]),
                 ('halve-vertical',[u,v/2]),('head-as-displacement',[u-x,v-y])]
        unique=[]
        for name,z in recipes:
            if z!=[u,v] and max(map(abs,z))<=8 and all(z!=prev for _,prev in unique):unique.append((name,z))
        rng.shuffle(unique)
        # At the origin, every sign/scale error may coincide with a true zero.
        # Keep that legitimate vector and build alternatives at the other tails.
        chosen=unique[:1];unused.append(unique[1:])
        pools.append([[u,v]]+[z for _,z in chosen]);names.append(['correct']+[name for name,_ in chosen])
    # A bank still needs five distinct complete diagrams. Expand available
    # error alternatives rather than rejecting a genuine zero/cancellation.
    while math.prod(map(len,pools))<5:
        eligible=[i for i,z in enumerate(unused) if z]
        if not eligible:raise ValueError('Insufficient distinct plausible error diagrams')
        i=rng.choice(eligible);name,z=unused[i].pop();pools[i].append(z);names[i].append(name)
    profiles=[code for code in itertools.product(*(range(len(pool)) for pool in pools)) if any(code)]
    chosen=rng.sample(profiles,4)
    out=[correct]+[[pools[i][c] for i,c in enumerate(code)] for code in chosen]
    assert len({json.dumps(exact_lists(z)) for z in out})==5
    return out,{'kind':'local-products','codes':chosen,'errors':names}

def make_field(kind,key,values,correct,atype,identity):
    fid=uid(identity+'/field/'+key)
    choices=[{':answer/id':uid(fid+'/'+str(i)+'/'+str(v)),':answer/type':':answer.type/'+atype,':answer/value':v} for i,v in enumerate(values)]
    return {':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,
            ':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[correct][':answer/id']]}

def build(level,seed,template=None,parameters=None,output_dir=None):
    rng=random.Random(seed)
    template=template or rng.choice(EASY) if level=='easy' else template or ('coupled' if level=='moderate' else 'product_square')
    if template not in FAMILIES:raise ValueError('Unknown scalar family')
    for attempt in range(2000):
        try:
            p=valid(parameters if parameters is not None else sample(level,template,rng),template)
            correct=evaluate(template,p)
            banks,profile=bank(correct,p['points'],level,rng)
            break
        except ValueError:
            if parameters is not None:raise
    else:raise RuntimeError('Unable to build valid complete bank')
    # Normalization precedes identity. Only semantic geometry/profile enters IDs,
    # never the deployment-specific absolute output directory.
    fc=formula_components(template,p)
    formula=r'\left('+fc[0]+r'\right)\,i+\left('+fc[1]+r'\right)\,j'
    pts=[point_tex(row) for row in p['points']]
    prompt='Which diagram represents\n\n$$\n\\mathbf F(x,y)='+formula+'\n$$\n\nat '+', '.join('$'+label+'='+pt+'$' for label,pt in zip('ABC',pts))+'? All diagrams use one unit per grid interval.'
    if level=='easy':prompt+='\n\nEvaluate both components at each point, then place the tail of its vector at that point.'
    if level=='hard':
        prompt+='\n\nEnter the coordinates of each arrowhead when its tail is at the stated point, and choose the correct diagram below.'
        for label in 'ABC':prompt+='\n\nArrowhead from $'+label+'$: $(${{'+label+' x-coordinate}}$,\\,${{'+label+' y-coordinate}}$)$'
    substitutions=[];rows=[]
    for pt,xy,(u,v) in zip(pts,p['points'],correct):
        sub=substitution_tex(template,p,xy)
        su,sv=sub.removeprefix(r'\left(').removesuffix(r'\right)\,j').split(r'\right)\,i+\left(')
        su,sv=normalize_tex(su),normalize_tex(sv)
        substitutions.append([su,sv])
        rows.extend(['P'+pt+'&='+su+'='+tex(u),'Q'+pt+'&='+sv+'='+tex(v),r'\mathbf F'+pt+'&='+vector_tex(u,v)])
    solution=r'Write $\mathbf F=P\,i+Q\,j$. Substitute into each component, then combine the results:'+'\n\n$$\n'+r'\begin{aligned}'+'\n'+(' \\\\\n'.join(rows))+'\n'+r'\end{aligned}'+'\n$$\n\nThe first component gives the horizontal displacement and the second gives the vertical displacement. Place each tail at its labeled point. A zero component gives no displacement along that axis; a zero vector stays at its tail.'
    heads=[[rat(x)+u,rat(y)+v] for (x,y),(u,v) in zip(p['points'],correct)]
    if level=='hard':
        hr=[label+r'+\mathbf F('+label+')&=('+tex(x)+'+('+tex(u)+'),'+tex(y)+'+('+tex(v)+'))='+point_tex(head) for label,(x,y),(u,v),head in zip('ABC',p['points'],correct,heads)]
        solution+='\n\nAdd each displacement to its tail to find the arrowhead:\n\n$$\n'+r'\begin{aligned}'+'\n'+' \\\\\n'.join(hr)+'\n'+r'\end{aligned}'+'\n$$'
    prompt,solution=normalize_prose(prompt),normalize_prose(solution)
    identity=digest({'version':VERSION,'prompt':prompt,'solution':solution,'banks':[exact_lists(z) for z in banks],'level':level})
    from plotting import render_bank
    paths,bounds=render_bank(p['points'],banks,Path(output_dir or os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']))
    order=list(range(5));rng.shuffle(order)
    fields=[make_field('radio','selection',[paths[i] for i in order],order.index(0),'image',identity)]
    if level=='hard':
        for label,head in zip('ABC',heads):
            for axis,z in zip('xy',head):fields.append(make_field('blank',label+' '+axis+'-coordinate',[normalize_tex(tex(z))],0,'math',identity))
    solution=normalize_prose(solution+'\n\n![]('+paths[0]+')')
    rec={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},
         'question':{':question/id':uid(identity),':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':fields},
         'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':p,'profile':profile,'attempts':attempt+1,
                       'correct_vectors':exact_lists(correct),'heads':exact_lists(heads),'bounds':bounds,
                       'plot_banks':[{'path':path,'vectors':exact_lists(z)} for path,z in zip(paths,banks)],
                       'source_refs':[SOURCE_IDS[next(k for k,v in OBSERVED.items() if v[0]==template)]] if template in EASY else ['f0111439-4fd8-5add-b95f-5e783178fd63' if template=='product_square' else '36301cba-bb7d-56d6-bf60-1510c1ba0e9f'],
                       'solution_path':{'components':[normalize_tex(f) for f in fc],'substitutions':substitutions, 'conversions':[], 'final_vectors':exact_lists(correct),'endpoint_stage':level=='hard'},
                       'semantic_identity':identity}}
    return validate_generated_record(rec)

def replay_sources():
    records=[]
    def clean(o):
        if isinstance(o,list):return [clean(z) for z in o]
        if isinstance(o,dict):
            if set(o)=={':db/ident'}:return o[':db/ident']
            return {k:clean(v) for k,v in o.items() if k!=':db/id'}
        return o
    for raw in json.loads((HERE/'replay-data.json').read_text()):
        q=clean(raw);sid=q.pop(':question/math-academy-id');source_id=q[':question/id']
        for key in [':question/problem',':question/worked-solution']:q[key]=normalize_prose(q[key])
        for f in q[':question/answer-fields']:
            f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
        r={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'source_refs':[source_id], 'source_replay':sid,'parameters':source_parameters(sid),'template':OBSERVED[sid][0]}}
        records.append(validate_generated_record(r))
    return records

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all','unclassified'],default='easy');ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json'],default='json');ap.add_argument('--replay',action='store_true');args=ap.parse_args()
    if args.count<1:ap.error('count must be positive')
    if args.replay:records=replay_sources()
    else:
        levels=['easy','moderate','hard'] if args.difficulty=='all' else ['easy' if args.difficulty=='unclassified' else args.difficulty]
        records=[]
        for level in levels:
            rng=random.Random(str(args.seed)+'/'+level);seen=set()
            for _ in range(args.count):
                for attempt in range(2000):
                    r=build(level,rng.getrandbits(64))
                    task=digest({'family':r['generation']['template'],'a':r['generation']['parameters']['a'],'b':r['generation']['parameters']['b'],'tails':sorted(r['generation']['parameters']['points'])})
                    if task not in seen:break
                else:raise RuntimeError('Could not construct unique semantic batch')
                seen.add(task);records.append(r)
    print(json.dumps(records,indent=2))
if __name__=='__main__':main()
