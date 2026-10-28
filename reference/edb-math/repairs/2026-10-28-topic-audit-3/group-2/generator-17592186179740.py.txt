#!/usr/bin/env python3
"""Seeded diagram-based circulation practice; no database or repository imports."""
import argparse, copy, hashlib, itertools, json, math, os, random, uuid
from collections import Counter
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR', '/tmp/course-academy-circulation-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from math_format import normalize_prose, validate_generated_record

KP=17592186179740
NS=uuid.UUID('b226f076-4683-42a6-ad71-25d3b036e78a')
PROFILES=[('I only','II only','III only','I and III only','II and III only'),
          ('I only','II only','III only','I and II only','II and III only')]
ROMAN=['I','II','III']
CLAIMS=list(itertools.product((1,-1),(-1,0,1)))
GEOMETRIES=[(1,1,0),(1.6,1,0),(1,1.6,0),(1.6,1,30),(1.6,1,60)]
FAMILIES=('ccw','cw','outward','inward')

def uid(text): return str(uuid.uuid5(NS,text))
def sign(family,orientation):
    return {'ccw':1,'cw':-1,'outward':0,'inward':0}[family]*orientation

def truth(claim,s): return claim[0]*s == claim[1]
def combination(bits): return ' and '.join(ROMAN[i] for i,v in enumerate(bits) if v)+' only'
def expression(claim):
    path='C' if claim[0]==1 else '-C'
    relation={-1:'<',0:'=',1:'>'}[claim[1]]
    return r'\oint_{'+path+r'}\mathbf F\cdot\mathrm d\mathbf r '+relation+' 0'

def claim_sets(s,shape,profile):
    # The same printed claim/bank must support a different answer under another
    # field sign. Thus bank logic alone cannot uniquely determine the answer.
    allowed=[]
    for claims in itertools.permutations(CLAIMS,3):
        if len({c[0] for c in claims})!=2: continue
        bits=tuple(truth(c,s) for c in claims)
        if sum(bits) not in (1,2): continue
        if shape=='radio':
            if combination(bits) not in PROFILES[profile]: continue
            alternatives={combination(tuple(truth(c,k) for c in claims)) for k in (-1,0,1)}
            if len(alternatives.intersection(PROFILES[profile]))<2: continue
            if s and any(combination(tuple(truth(c,k) for c in claims)) not in PROFILES[profile] for k in (-1,1)): continue
        allowed.append(claims)
    return allowed

def world(x,y,angle):
    c,s=math.cos(math.radians(angle)),math.sin(math.radians(angle))
    return c*x-s*y,s*x+c*y

def vector(x,y,a,b,angle,family):
    nx,ny=x/(a*a),y/(b*b)
    u,v={'ccw':(-ny,nx),'cw':(ny,-nx),'outward':(nx,ny),'inward':(-nx,-ny)}[family]
    return world(u,v,angle)

def diagram(instance,out,traversal=0):
    a,b,angle=instance['geometry'];family=instance['family']
    identity=json.dumps([a,b,angle,family,traversal],separators=(',',':'))
    name='circulation-'+hashlib.sha256(identity.encode()).hexdigest()[:20]+'.png'
    path=out/name
    if path.exists(): return name
    fig,ax=plt.subplots(figsize=(4.6,4.6),dpi=130)
    fig.subplots_adjust(left=.02,right=.98,bottom=.02,top=.98)
    limit=2.35
    ax.set(xlim=(-limit,limit),ylim=(-limit,limit),aspect='equal')
    ax.axis('off')
    # All arrows are actual field samples. Preserve their directions, normalize
    # only magnitude; no annotation reveals the relationship before feedback.
    samples=[]
    for ix in range(-6,7):
        for iy in range(-6,7):
            X,Y=ix*.34,iy*.34
            x,y=world(X,Y,-angle)
            radius=math.hypot(x/a,y/b)
            if radius<.16 or abs(radius-1)<.13:continue
            samples.append((x,y))
    samples += [(a*math.cos(i*math.pi/8),b*math.sin(i*math.pi/8)) for i in range(16)]
    xs=[];ys=[];us=[];vs=[];witness=[]
    for x,y in samples:
        X,Y=world(x,y,angle);u,v=vector(x,y,a,b,angle,family)
        norm=math.hypot(u,v);u*=.25/norm;v*=.25/norm
        xs.append(X);ys.append(Y);us.append(u);vs.append(v)
        witness.append([X,Y,u,v])
    ax.quiver(xs,ys,us,vs,color='#858b91',angles='xy',scale_units='xy',scale=1,width=.0034,headwidth=3.8,headlength=4.8,pivot='tail',zorder=2)
    ts=[i*2*math.pi/400 for i in range(401)]
    curve=[world(a*math.cos(t),b*math.sin(t),angle) for t in ts]
    ax.plot([p[0] for p in curve],[p[1] for p in curve],color='#196ba5',lw=2.0,zorder=3)
    for start,end,label in [((-2.18,0),(2.2,0),'x'),((0,-2.18),(0,2.2),'y')]:
        ax.annotate('',xy=end,xytext=start,arrowprops={'arrowstyle':'->','color':'#30363b','lw':.9})
        ax.text(end[0]+.03,end[1]+.03,label,fontsize=11,fontstyle='italic')
    if traversal:
        for t in (.25,1.8,3.4,5.0):
            p=world(a*math.cos(t-.065*traversal),b*math.sin(t-.065*traversal),angle)
            q=world(a*math.cos(t+.065*traversal),b*math.sin(t+.065*traversal),angle)
            ax.annotate('',xy=q,xytext=p,arrowprops={'arrowstyle':'->','color':'#196ba5','lw':2,'mutation_scale':15},zorder=4)
    fig.savefig(path,facecolor='white',metadata={'Software':'Course Academy circulation generator 1'})
    plt.close(fig)
    (out/(name+'.json')).write_text(json.dumps({'geometry':[a,b,angle],'family':family,'traversal':traversal,'arrows':witness,'curve':curve},separators=(',',':'))+'\n')
    return name

def build(instance,out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    family=instance['family'];orientation=instance['orientation'];s=sign(family,orientation)
    claims=instance['claims'];bits=[truth(c,s) for c in claims]
    pic=diagram(instance,out);forward=diagram(instance,out,orientation);reverse=diagram(instance,out,-orientation)
    direction='counterclockwise' if orientation==1 else 'clockwise'
    opposite='clockwise' if orientation==1 else 'counterclockwise'
    kind='circle' if instance['geometry'][0]==instance['geometry'][1] else 'ellipse'
    problem=f'![]({pic})\n\nConsider the {kind} and vector field $\\mathbf F$ shown above. Let $C$ traverse the curve once in the **{direction}** direction. Which of the following statements are true?'
    if instance['shape']=='radio':
        problem+='\n\n'+'\n\n'.join(ROMAN[i]+'. $'+expression(c)+'$' for i,c in enumerate(claims))
    else:problem+='\n\nSelect all that apply.'
    relation={-1:'<',0:'=',1:'>'}
    if s:
        comparison=('assists' if s==1 else 'opposes')+f' the motion all the way around $C$ in the **{direction}** direction.'
    else:comparison='is perpendicular to the tangent all the way around $C$, so it neither assists nor opposes the motion.'
    solution=r'The circulation $\Gamma=\oint_C\mathbf F\cdot\mathrm d\mathbf r$ measures the work done around a *closed* curve. Assistance gives positive work, opposition gives negative work, and perpendicular force gives zero work.'
    solution+='\n\nThe field '+comparison+f'\n\n![]({forward})\n\nThus, $'+expression((1,s))+'$.'
    solution+=r' Reversing traversal reverses the work: $\oint_{-C}\mathbf F\cdot\mathrm d\mathbf r=-\oint_C\mathbf F\cdot\mathrm d\mathbf r$.'
    solution+=f' The reversed path $-C$ is **{opposite}**.\n\n![]({reverse})\n\nTherefore, $'+expression((-1,-s))+'$.'
    if not s:solution+=' Reversing zero still gives zero.'
    solution+='\n\n'+'\n\n'.join((f'{ROMAN[i]}. ' if instance['shape']=='radio' else '- ')+'$'+expression(c)+'$ is **'+('true' if bits[i] else 'false')+'**.' for i,c in enumerate(claims))
    if instance['shape']=='radio':solution+='\n\nThe true statements are '+combination(bits)+'.'
    else:solution+='\n\nTherefore, select '+ ' and '.join('$'+expression(c)+'$' for c,b in zip(claims,bits) if b)+'.'
    # Normalize BEFORE identity calculation; all owned entities derive from
    # normalized public content and the full rendered choice bank.
    problem=normalize_prose(problem);solution=normalize_prose(solution)
    labels=list(PROFILES[instance['profile']]) if instance['shape']=='radio' else []
    if labels:
        random.Random(instance['order_seed']).shuffle(labels)
        if 'answer_position' in instance:
            correct_index=labels.index(combination(bits))
            target=instance['answer_position']
            labels[correct_index],labels[target]=labels[target],labels[correct_index]
    token=hashlib.sha256(json.dumps([problem,solution,claims,sorted(labels)],sort_keys=True).encode()).hexdigest()
    def answer(value,key):return {':answer/id':uid(token+key+value),':answer/type':':answer.type/text',':answer/value':value}
    fields=[]
    if labels:
        choices=[answer(v,'radio') for v in labels];correct=combination(bits)
        fields=[{':answer-field/id':uid(token+'field'),':answer-field/type':':answer-field.type/radio',':answer-field/key':'selection',':answer-field/choices':choices,':answer-field/correct':[':answer/id',next(a[':answer/id'] for a in choices if a[':answer/value']==correct)]}]
    else:
        for i,c in enumerate(claims):
            choices=[answer(v,str(i)) for v in ('false','true')]
            fields.append({':answer-field/id':uid(token+'field'+str(i)),':answer-field/type':':answer-field.type/checkbox',':answer-field/key':'$'+expression(c)+'$',':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[int(bits[i])][':answer/id']]})
    r={'knowledge_point':KP,'question':{':question/id':uid(token),':question/difficulty':':question.difficulty/'+instance['difficulty'],':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':fields},'generation':{'version':'1.0','instance':instance,'source_support':['q-125395','q-125637','q-125394','q-125645','q-125392','q-125668','q-125640','q-125666','q-125649','q-125667','q-125669','q-125643']}}
    return validate_generated_record(r)

def generate(difficulty,count,seed,out):
    rng=random.Random(seed);records=[];seen=set()
    # Balanced shuffled decks operate for every seed and count; no seed-specific
    # cases. Role blocks couple both response forms to every field relationship.
    families=list(FAMILIES if difficulty=='hard' else FAMILIES[:2])
    shape_offsets={f:rng.randrange(2) for f in families}
    orientation_offsets={f:rng.choice((-1,1)) for f in families}
    cycle=0
    profiles=[0,1];rng.shuffle(profiles);radio_index=0;attempts=0
    response_counts=Counter(); family_counts=Counter(); position_counts=Counter(); cardinality_counts=Counter()
    while len(records)<count:
        deck=families[:];rng.shuffle(deck)
        for family in deck:
            shape=('checkbox','radio')[(cycle+shape_offsets[family])%2]
            orientation=(orientation_offsets[family]*(-1 if (cycle//2)%2 else 1)) if difficulty=='hard' else (1 if difficulty=='easy' else -1)
            profile=profiles[radio_index%2] if shape=='radio' else 0
            if shape=='radio':radio_index+=1
            s=sign(family,orientation)
            # Balance answer-producing actions as well as field relationships. A
            # random claim draw alone can make every radio in a short batch
            # answerable by the same Roman label. Prefer unused responses
            # globally and within each recognizable field/response family.
            candidates=claim_sets(s,shape,profile)
            def response(c): return tuple(truth(x,s) for x in c)
            def score(c):
                bits=response(c)
                return (cardinality_counts[shape,sum(bits)],response_counts[shape,bits],family_counts[family,shape,bits])
            best=min(map(score,candidates))
            claims=rng.choice([c for c in candidates if score(c)==best])
            instance={'difficulty':difficulty,'family':family,'orientation':orientation,'shape':shape,'profile':profile,'claims':claims,'geometry':rng.choice(GEOMETRIES),'order_seed':rng.getrandbits(64)}
            if shape=='radio':
                best_position=min(position_counts[i] for i in range(5))
                instance['answer_position']=rng.choice([i for i in range(5) if position_counts[i]==best_position])
            record=build(instance,out)
            identity=json.dumps([family,orientation,shape,profile if shape=='radio' else None,instance['geometry'],sorted(claims) if shape=='checkbox' else claims],sort_keys=True)
            attempts+=1
            if identity not in seen:
                records.append(record);seen.add(identity)
                bits=response(claims)
                response_counts[shape,bits]+=1
                cardinality_counts[shape,sum(bits)]+=1
                family_counts[family,shape,bits]+=1
                if shape=='radio':position_counts[instance['answer_position']]+=1
            if len(records)==count:break
            if attempts>count*100+100:raise RuntimeError('Requested batch exceeds available instances')
        cycle+=1
    return records

def replay(source_id):
    records=json.loads(Path(__file__).with_name('source-cases.json').read_text())
    return [r for r in records if source_id=='all' or r['generation']['source_id']==source_id]

def main():
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard'],default='easy');p.add_argument('--count',type=int,default=5);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json'],default='json');p.add_argument('--replay-source')
    args=p.parse_args()
    if args.count<0:p.error('count must be nonnegative')
    if args.replay_source:records=replay(args.replay_source)
    else:
        directory=os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
        if not directory:p.error('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR is required')
        records=generate(args.difficulty,args.count,args.seed,directory)
    print(json.dumps(records,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
