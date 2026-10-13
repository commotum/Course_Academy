#!/usr/bin/env python3
"""Interpreting Divergence; captured math basis 1356; steps 3–7 only.

Normal authored graph catalogs assess source/sink/solenoidal interpretation, never
partial differentiation. Every level has one fixed workload: easy constant or
radial visual patterns; moderate positive-quadrant same-coordinate growth versus
cross-coordinate shear with a constant transverse component; hard the same sign
interpretation in a signed plane with both components oblique and a nonzero
cross-coordinate shear. Hard is an authored extension anchored to q-131195/196.
Finite reduced matrices, drift directions, and domains define actual task counts;
positive magnitude, field letters, seeds, profiles and order are not new tasks.
Observed replay profiles are evidence_only, never default learner sampling. They
retain all original attribute presence, legacy fields, exact prose and banks.
Their recipes transform complete field/coordinate/plot components; no source
answer lookup or literal-question return is used. See private extraction evidence.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, random, re, subprocess, sys, uuid
from pathlib import Path

KP_ID=17592186133880
KP_UUID='4f47e201-105a-579a-8cde-fcb6bf8cfa2a'
TITLE='Interpreting Divergence'
VERSION='divergence-interpretation-v1'
HERE=Path(__file__).with_suffix('')
ROOT=Path(__file__).resolve().parents[2]
SNAPSHOT=json.loads((HERE/'source.json').read_text())
SOURCES=SNAPSHOT['record'][':knowledge-point/questions']
SOURCE_BY_ID={q[':question/math-academy-id']:q for q in SOURCES}
SOURCE_META={k:SNAPSHOT[k] for k in ('database','basis','lineage')}
ROMANS=('I','II','III','IV')


def choice_set(value):
    if value=='None of the statements are true.': return ()
    m=re.fullmatch(r'((?:I|II|III|IV)(?: and (?:I|II|III|IV))*) only',value)
    if not m: raise ValueError('Unsupported complete statement subset: '+value)
    return tuple(m.group(1).split(' and '))


def subset_value(subset):
    return ' and '.join(subset)+' only' if subset else 'None of the statements are true.'


# Whole observed banks; interpretations are literal statement subsets, not inferred errors.
BANKS={}
for source in SOURCES:
    for field in source.get(':question/answer-fields',[]):
        bank=tuple(sorted(choice_set(a[':answer/value']) for a in field[':answer-field/choices']))
        if bank not in BANKS.values(): BANKS['bank-'+str(len(BANKS)+1)]=bank


# Unlabelled source rasters admit normalized qualitative recipes, not exact scale recovery.
# M = [[dU/dx,dU/dy],[dV/dx,dV/dy]], drift, first-quadrant versus signed plane.
SOURCE_GEOMETRY={
 'q-105075':([[0,0],[0,-1]],[0,12],'quadrant'),
 'q-105571':([[0,0],[0,0]],[1,2],'quadrant'),
 'q-105046':([[0,0],[0,0]],[1,0],'plane'),
 'q-105573':([[0,0],[0,1]],[0,0],'quadrant'),
 'q-105575':([[0,-1],[0,0]],[0,0],'plane'),
 'q-105576':([[0,0],[0,0]],[-1,-1],'plane'),
 'q-105578':([[1,0],[0,1]],[0,0],'quadrant'),
 'q-123245':([[1,0],[0,1]],[0,0],'plane'),
 'q-131192':([[0,0],[0,1]],[1,0],'quadrant'),
 'q-131193':([[0,0],[0,0]],[1,-1],'plane'),
 'q-105577':([[0,0],[-1,0]],[0,0],'quadrant'),
 'q-105572':([[-1,0],[0,-1]],[0,0],'quadrant'),
 'q-131195':([[0,0],[0,1]],[1,0],'plane'),
 'q-131196':([[-1,0],[0,0]],[0,1],'plane'),
}


def truth(sign): return ('I','IV') if sign==0 else ('II',) if sign>0 else ('III',)
def signof(n): return (n>0)-(n<0)
def stable(value): return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def digest(value): return hashlib.sha256(stable(value).encode()).hexdigest()
def uid(value): return str(uuid.uuid5(uuid.NAMESPACE_URL,'divergence:'+stable(value)))


def rotate(M,b,k):
    # Exact quarter-turn coordinate rotations; makes independently enumerable orientations.
    for _ in range(k): M=[[M[1][1],-M[1][0]],[-M[0][1],M[0][0]]];b=[-b[1],b[0]]
    return M,b


def catalog(level):
    objects=[]
    if level=='easy':
        bases=[([[0,0],[0,0]],b,'constant') for b in ([1,0],[1,1])]
        bases += [([[s,0],[0,s]],[0,0],'radial') for s in (-1,1)]
        domain='plane'
    elif level=='moderate':
        bases=[([[0,0],[0,s]],[1,0],'own-coordinate') for s in (-1,1)]
        bases += [([[0,s],[0,0]],[0,1],'cross-coordinate') for s in (-1,1)]
        domain='quadrant'
    elif level=='hard':
        bases=[([[0,h],[0,s]],[1,0],'oblique') for s in (-1,1) for h in (-1,1)]
        # Cross-coordinate oblique shear; both components nonconstant but trace zero.
        bases += [([[0,h],[h,0]],[1,1],'oblique') for h in (-1,1)]
        domain='plane'
    else: raise ValueError('Unknown difficulty')
    for M,b,family in bases:
        for orientation in range(4):
            m,d=rotate(M,b,orientation)
            obj={'matrix':m,'drift':d,'domain':domain,'family':family}
            if obj not in objects: objects.append(obj)
    return objects
CATALOGS={l:catalog(l) for l in ('easy','moderate','hard')}


def render_plot(M,b,domain,scale=1):
    data={'matrix':M,'drift':b,'domain':domain,'scale':scale}
    key=digest(data); asset=HERE/'plots'/(key+'.png'); side=asset.with_suffix('.json')
    if not (asset.exists() and side.exists()):
        asset.parent.mkdir(exist_ok=True)
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w',suffix='.json',prefix='render-',dir=asset.parent,delete=False) as f:
            json.dump({'data':data,'output':str(asset)},f);path=Path(f.name)
        try: subprocess.run([sys.executable,str(HERE/'render.py'),str(path)],check=True,stdout=subprocess.DEVNULL)
        finally: path.unlink(missing_ok=True)
    return str(asset.resolve())


def replace_math_components(text,symbol='F',swap=False):
    # Replace complete mathematical symbols only inside inline/display math.
    def change(m):
        t=m.group(0);t=re.sub(r'(?<![A-Za-z])F(?![A-Za-z])',symbol,t)
        if swap:
            t=re.sub(r'(?<![A-Za-z])([xy])(?![A-Za-z])',lambda a:'y' if a[1]=='x' else 'x',t)
        return t
    return re.sub(r'\$\$[\s\S]*?\$\$|\$[^$]*?\$',change,text)


def normalize_enum(obj):
    if isinstance(obj,dict) and set(obj)=={':db/ident'}: return obj[':db/ident']
    if isinstance(obj,dict): return {k:normalize_enum(v) for k,v in obj.items()}
    if isinstance(obj,list): return [normalize_enum(v) for v in obj]
    return obj


def source_replay(level,source_id,parameters,seed):
    """Public raw replay: schema assembly + parameterized graph/prose/subset recipes.

    Original IDs and key presence are evidence; missing correct refs stay missing.
    Original unnumbered statement markup is retained. Therefore ineligible.
    """
    q=SOURCE_BY_ID[source_id]; actual=q[':question/difficulty'][':db/ident'].split('/')[-1]
    if level!=actual: raise ValueError('Source difficulty mismatch')
    p={'field_symbol':'F','swap_axes':False,'scale':1}
    if parameters:
        if set(parameters)-set(p): raise ValueError('Unknown replay parameter')
        p.update(parameters)
    if p['field_symbol'] not in ('F','G','H') or type(p['swap_axes']) is not bool or type(p['scale']) is not int or p['scale'] not in (1,2,3): raise ValueError('Invalid replay domain')
    problem=replace_math_components(q[':question/problem'],p['field_symbol'],p['swap_axes'])
    solution=replace_math_components(q[':question/worked-solution'],p['field_symbol'],p['swap_axes'])
    if p['swap_axes'] or p['scale']!=1:
        M,b,domain=SOURCE_GEOMETRY[source_id]
        if p['swap_axes']: M=[[M[1][1],M[1][0]],[M[0][1],M[0][0]]];b=[b[1],b[0]]
        newplot=render_plot(M,b,domain,p['scale'])
        problem=re.sub(r'!\[\]\([^)]+\)',lambda _:f'![]({newplot})',problem,count=1)
        if p['swap_axes']:
            # Complete directional prose clauses rather than blind single-letter replacement.
            for old,new in [('horizontally and vertically','vertically and horizontally'),('vertically and horizontally','horizontally and vertically'),('move horizontally','move vertically'),('move vertically','move horizontally')]:
                # Axis-specific source sentences have one of these; preserve fixed prose at originals.
                if old in q[':question/worked-solution']:solution=solution.replace(old,new);break
    result={k:normalize_enum(v) for k,v in q.items() if k not in (':question/problem',':question/worked-solution',':question/answer-fields')}
    result[':question/problem']=problem;result[':question/worked-solution']=solution
    fields=[]
    for f in q.get(':question/answer-fields',[]):
        out={k:normalize_enum(v) for k,v in f.items() if k not in (':answer-field/choices',':answer-field/correct')}
        out[':answer-field/choices']=[]
        for a in f[':answer-field/choices']:
            aa={k:normalize_enum(v) for k,v in a.items() if k!=':answer/value'}
            aa[':answer/value']=subset_value(choice_set(a[':answer/value']));out[':answer-field/choices'].append(aa)
        if ':answer-field/correct' in f: out[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
        fields.append(out)
    if ':question/answer-fields' in q: result[':question/answer-fields']=fields
    M,b,domain=SOURCE_GEOMETRY[source_id]
    if p['swap_axes']: M=[[M[1][1],M[1][0]],[M[0][1],M[0][0]]];b=[b[1],b[0]]
    content=digest({'version':VERSION,'prompt':problem,'solution':solution,
                    'fields':[{'key':f[':answer-field/key'],'type':f[':answer-field/type'],
                     'values':sorted(a[':answer/value'] for a in f[':answer-field/choices']),
                     'correct':next((a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f.get(':answer-field/correct',[None,None])[1]),None)} for f in fields]})
    if p != {'field_symbol':'F','swap_axes':False,'scale':1}:
        result[':question/id']=uid([content,'question'])
        for i,f in enumerate(fields):
            old_correct=f.get(':answer-field/correct',[None,None])[1]
            f[':answer-field/id']=uid([content,'field',i])
            for a in f[':answer-field/choices']:
                old_id=a[':answer/id'];a[':answer/id']=uid([f[':answer-field/id'],a[':answer/value']])
                if old_id==old_correct:f[':answer-field/correct']=[':answer/id',a[':answer/id']]
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':result,
      'generation':{'version':VERSION,'source':SOURCE_META,'seed':seed,'template':'observed-'+source_id,
      'bank_profile':'raw-'+source_id,'parameters':p,'evidence_only':True,'eligible':False,'eligible_for_learning':False,
      'mathematical_fingerprint':digest({'matrix':M,'drift':b,'domain':domain}),
      'content_identity':content,'source_id':source_id}}


OPENING=r'''Recall that $\text{div}\,F=∇\cdot F$ denotes the divergence of the vector field $F.$

Intuitively, the divergence of $F$ at a point $P$ measures how much $F$ acts like a source or a sink at $P:$

- If $F$ acts like a source at $P,$ then $∇\cdot F>0$ at $P.$

- If $F$ acts like a sink at $P,$ then $∇\cdot F<0$ at $P.$

- If $F$ acts like neither a source nor a sink at $P,$ then $∇\cdot F=0$ at $P.$

If $∇\cdot F=0$ everywhere in the domain of $F,$ we say that $F$ is solenoidal.

With that in mind, let's examine each statement:'''


def normal_solution(obj,symbol):
    M=obj['matrix'];s=signof(M[0][0]+M[1][1]);family=obj['family']
    if family=='constant':reason='The vectors have the same direction and length everywhere. There is no local excess of outward or inward flow.'
    elif family=='radial':reason='The vectors point '+('away from' if s>0 else 'towards')+' the origin and their lengths grow with distance from it. Around every point, there is a local excess of '+('outward' if s>0 else 'inward')+' flow.'
    elif s==0:reason="Each component changes only in the other coordinate's direction. Across opposite sides of a small rectangle, the matching normal components balance. There is no local excess of outward or inward flow."
    else:
        axis='x' if M[0][0] else 'y';other='y' if axis=='x' else 'x'
        reason=f'The ${axis}$-component '+('increases' if s>0 else 'decreases')+f' as we move in the positive ${axis}$-direction. The ${other}$-component does not change as we move in the ${other}$-direction. Therefore, there is a local excess of '+('outward' if s>0 else 'inward')+' flow at every point.'
    result=truth(s);state='neither a source nor a sink' if s==0 else 'a source' if s>0 else 'a sink'
    statement='I' if s==0 else 'II' if s>0 else 'III'
    false='II and III' if s==0 else 'I and III' if s>0 else 'I and II'
    tail=f'\n\n- Statement {statement} is true, whereas statements {false} are false. {reason} Therefore, $F$ acts like {state}.\n\n'
    if s==0:tail+=r'- Statement IV is true. Since $∇\cdot F=0$ everywhere, the vector field $F$ is solenoidal.'
    else:tail+=r'- Statement IV is false. Since $∇\cdot F\ne 0,$ the vector field $F$ is not solenoidal.'
    tail+='\n\nTherefore, the correct answer is "'+subset_value(result)+'."'
    return replace_math_components(OPENING+tail,symbol)


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in CATALOGS:raise ValueError('Unknown difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only radio supported')
    if profile and profile.startswith('raw-'):
        source_id=profile[4:]
        if source_id not in SOURCE_BY_ID or template not in (None,'observed-'+source_id):raise ValueError('Invalid raw source profile/template')
        return source_replay(level,source_id,parameters,seed)
    if template not in (None,'visual-sign'):raise ValueError('Normal template is visual-sign; observed replay requires raw profile')
    rng=random.Random(seed)
    # Select one complete bank first; its response criterion constrains catalog eligibility.
    profile=profile or rng.choice(list(BANKS))
    if profile not in BANKS:raise ValueError('Unknown bank')
    bank=BANKS[profile]
    eligible=[o for o in CATALOGS[level] if truth(signof(o['matrix'][0][0]+o['matrix'][1][1])) in bank]
    if not eligible:raise ValueError('No eligible catalog objects for complete bank')
    if parameters is None:
        obj=copy.deepcopy(rng.choice(eligible));symbol=rng.choice(('F','G','H'));scale=rng.choice((1,2,3))
    else:
        if set(parameters)-{'object','field_symbol','scale'}:raise ValueError('Unknown parameter')
        if 'object' not in parameters:raise ValueError('Explicit parameters require complete catalog object')
        obj=copy.deepcopy(parameters['object']);symbol=parameters.get('field_symbol','F');scale=parameters.get('scale',1)
        if obj not in eligible:raise ValueError('Object fails level/workload/whole-bank eligibility guard')
    if symbol not in ('F','G','H') or type(scale) is not int or scale not in (1,2,3):raise ValueError('Invalid symbol or positive scale')
    M=obj['matrix'];b=obj['drift'];s=signof(M[0][0]+M[1][1]);correct=truth(s)
    values=[subset_value(subset) for subset in bank]
    if len(set(values))!=5 or len({choice_set(v) for v in values})!=5 or sum(choice_set(v)==correct for v in values)!=1:raise ValueError('Reject whole ambiguous/colliding bank')
    plot=render_plot(M,b,obj['domain'],1)
    domain='the whole plane' if obj['domain']=='plane' else 'the open first quadrant after the indicated coordinate rotation'
    # Rotated quadrant uses the exact displayed sample domain; statements apply to affine continuation.
    if obj['domain']=='quadrant':domain='the open square shown in the plot'
    problem=f'![]({plot})\n\nConsider the smooth vector field $F$ shown above. The displayed pattern continues throughout {domain}. All arrows use the same length scale; arrow lengths represent speed. Which of the following statements are true everywhere in that domain?\n\nI. $∇\\cdot F=0$\n\nII. $∇\\cdot F>0$\n\nIII. $∇\\cdot F<0$\n\nIV. $F$ is solenoidal'
    problem=replace_math_components(problem,symbol)
    solution=normal_solution(obj,symbol)
    # Identity comes from actual complete learner content, not unused parameters/profile aliases/order.
    identity=digest({'version':VERSION,'prompt':problem,'solution':solution,'values':sorted(values),'field_type':'radio'})
    field_id=uid([identity,'selection']);answers=[{':answer/id':uid([field_id,v]),':answer/type':':answer.type/text',':answer/value':v} for v in values]
    correct_id=next(a[':answer/id'] for a in answers if choice_set(a[':answer/value'])==correct)
    rng.shuffle(answers)
    q={':question/id':uid([identity,'question']),':question/difficulty':':question.difficulty/'+level,
       ':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':[
       {':answer-field/id':field_id,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',
        ':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}]}
    fp=digest({'matrix':M,'drift':b,'domain':obj['domain']})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,
            'generation':{'version':VERSION,'source':SOURCE_META,'seed':seed,'template':'visual-sign','bank_profile':profile,
            'parameters':{'object':obj,'field_symbol':symbol,'scale':scale},'evidence_only':False,'eligible':True,'eligible_for_learning':True,
            'authorship':'authored equal-workload catalog extension','mathematical_fingerprint':fp,'content_identity':identity,
            'domain':domain,'units':'No measurements declared; sign and source/sink interpretation only.',
            'catalog_size':len(CATALOGS[level]),'plot':plot}}


# Easy: direct constant or radial local source/sink recognition, no algebra.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# Moderate: separate same-coordinate component change from cross-coordinate shear.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# Hard: signed-plane oblique fields retain nonzero shear and both changing components.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)


def markdown(record,label='GENERATED'):
    q=record['question'];g=record['generation'];level=q.get(':question/difficulty','unrated').split('/')[-1]
    lines=[f'### {label} | difficulty: {level} | {g["template"]} | {g["bank_profile"]}',q[':question/problem']]
    for i,f in enumerate(q.get(':question/answer-fields',[])):
        lines.append(f'Field {i+1}: {f[":answer-field/type"]}, key {f[":answer-field/key"]}')
        ref=f.get(':answer-field/correct');cid=ref[1] if ref else None
        for a in f[':answer-field/choices']:lines.append('- '+a[':answer/value']+(' **CORRECT**' if a[':answer/id']==cid else ''))
        if cid is None:lines.append('**Original correct designation absent.**')
    if ':question/worked-solution' in q:lines += ['Worked solution:',q[':question/worked-solution']]
    return '\n\n'.join(lines)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown')
    parser.add_argument('--template');parser.add_argument('--profile');args=parser.parse_args()
    if args.count<1:parser.error('--count must be positive')
    levels=list(CATALOGS) if args.difficulty=='all' else [args.difficulty]
    records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in levels for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n'.join(markdown(r,'ORIGINAL RAW REPLAY' if r['generation']['evidence_only'] else 'GENERATED') for r in records))
if __name__=='__main__':main()
