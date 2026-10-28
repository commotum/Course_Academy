"""Diameter-to-circle practice: role-first generation with complete source replay."""
from __future__ import annotations
import argparse
import json
import random
from pathlib import Path
import sys
import sympy as sp
import source_engine as source
from math_format import checked_math_content, normalize_prose, normalize_tex

VERSION = 'diameter-role-first-2'
SUPPORTED = ('moderate','hard')
PROFILES = ('reflect_x','reflect_y','reflect_both','swap')
ROLES = ((0,0),(0,1),(0,2),(1,0),(1,1))
HARD_VECTORS = {}
for u in range(1,6):
    for v in range(1,6):
        z=u*u+v*v
        if int(z**.5)**2 != z:
            HARD_VECTORS.setdefault(z,[]).append((u,v))


def center_partner(c, profile):
    h,k=c
    return {'reflect_x':(-h,k),'reflect_y':(h,-k),
            'reflect_both':(-h,-k),'swap':(k,h)}[profile]


def design(difficulty, seed=0, role=None, profile=None):
    """Select the correct role before compatible numerical and visual data."""
    if difficulty not in SUPPORTED:
        raise ValueError('Supported bands are moderate and hard; easy is unsupported')
    rng=random.Random(seed)
    role=rng.randrange(5) if role is None else role
    profile=rng.choice(PROFILES) if profile is None else profile
    if role not in range(5) or profile not in PROFILES:
        raise ValueError('Unknown role or center contrast profile')
    eligible=[(h,k) for h in range(-5,6) for k in range(-5,6)
              if center_partner((h,k),profile)!=(h,k)]
    c=rng.choice(eligible)
    centers=(c,center_partner(c,profile))
    radii_squared=rng.sample([r*r for r in range(1,7)] if difficulty=='moderate'
                             else sorted(HARD_VECTORS),3)
    # All candidate circles have compatible endpoints in the supported band.
    direction=rng.choice(('horizontal','vertical')) if difficulty=='moderate' else 'diagonal'
    signs=(rng.choice((-1,1)),rng.choice((-1,1)))
    vector_choices=[rng.choice(HARD_VECTORS[z]) if difficulty=='hard' else (int(z**.5),0)
                    for z in radii_squared]
    permutation=list(range(5)); rng.shuffle(permutation)
    return {'difficulty':difficulty,'seed':seed,'role':role,'profile':profile,
            'centers':[list(c) for c in centers],'radii_squared':radii_squared,
            'direction':direction,'signs':list(signs),'vectors':vector_choices,
            'permutation':permutation}


def endpoints(instance, role):
    ci,ri=ROLES[role]; h,k=instance['centers'][ci]
    u,v=instance['vectors'][ri]
    if instance['direction']=='vertical': u,v=v,u
    u*=instance['signs'][0]; v*=instance['signs'][1]
    return dict(zip(('x1','y1','x2','y2'),(h+u,k+v,h-u,k-v)))


@checked_math_content
def from_design(instance, role=None, reverse_endpoints=False):
    role=instance['role'] if role is None else role
    p=endpoints(instance,role)
    if reverse_endpoints:
        p=dict(zip(('x1','y1','x2','y2'),(p['x2'],p['y2'],p['x1'],p['y1'])))
    asset,plotmeta=source.render_plots(p)
    choices=[normalize_tex(source.eq(*instance['centers'][ci],instance['radii_squared'][ri]))
             for ci,ri in ROLES]
    prompt=(f'![]({asset})\n\nThe line segment $\\overline{{XY}}$ is a diameter of a circle. '
            f'Given that $X$ and $Y$ have coordinates $({p["x1"]},{p["y1"]})$ and '
            f'$({p["x2"]},{p["y2"]})$, respectively, what is the equation of the circle?')
    prompt=normalize_prose(prompt)
    solution=normalize_prose(source.normal_solution(p))
    # Content identity is independent of output-directory spelling.
    identity=source.digest([VERSION,instance['difficulty'],p,sorted(choices)])
    qid=source.uid(identity); fid=source.uid(qid+':selection')
    answers=[{':answer/id':source.uid(fid+':'+a),':answer/type':':answer.type/math',
              ':answer/value':a} for a in choices]
    field={':answer-field/id':fid,':answer-field/key':'selection',
           ':answer-field/type':':answer-field.type/radio',
           ':answer-field/choices':[answers[i] for i in instance['permutation']],
           ':answer-field/correct':[':answer/id',answers[role][':answer/id']]}
    q={':question/id':qid,':question/difficulty':':question.difficulty/'+instance['difficulty'],
       ':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[field]}
    return {'knowledge_point':{'db_id':source.KP_ID,'id':source.KP[':knowledge-point/id'],
                'title':source.KP[':knowledge-point/title']},'question':q,
            'generation':{'version':VERSION,'seed':instance['seed'],'template':'diameter_circle',
                'bank_profile':instance['profile'],'authored_bank':True,'design':instance,
                'selected_role':role,'parameters':p,'correct_value':choices[role],
                'source_ids':['q-117102','q-117103','q-70987'] if instance['difficulty']=='moderate'
                    else ['q-117105','q-117106','q-117107','q-70990'],
                'source_basis':source.CAPTURE['basis'],'dependencies':{'python':sys.version.split()[0],
                    'sympy':sp.__version__,'matplotlib':plotmeta['matplotlib']},
                'plots':[asset],'plot':plotmeta,'sampling_rejections':0,
                'semantic_circle':[sum((p['x1'],p['x2']))/2,sum((p['y1'],p['y2']))/2,
                    ((p['x1']-p['x2'])**2+(p['y1']-p['y2'])**2)//4]}}


@checked_math_content
def generate(difficulty='moderate',seed=0,**kwargs):
    return from_design(design(difficulty,seed,**kwargs))


def replay(source_id):
    p=dict(zip(('x1','y1','x2','y2'),source.PARAMS[source_id]))
    record=source.generate(source.LEVELS[source_id],seed=0,template=source_id,parameters=p)
    q=record['question']; q[':question/problem']=normalize_prose(q[':question/problem'])
    if ':question/worked-solution' in q:
        q[':question/worked-solution']=normalize_prose(q[':question/worked-solution'])
    # Two raw sources intentionally lack a solution; preserve that absence.
    if ':question/worked-solution' in q:
        from math_format import validate_generated_record
        validate_generated_record(record)
    return record


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=SUPPORTED,default='moderate')
    parser.add_argument('--count',type=int,default=5)
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=['json'],default='json')
    args=parser.parse_args()
    if args.count<0: parser.error('--count must be nonnegative')
    print(json.dumps([generate(args.difficulty,args.seed+i) for i in range(args.count)],indent=2))

if __name__=='__main__': main()
