#!/usr/bin/env python3
"""Seeded, relocatable sign-and-magnitude vector diagram practice.
Repairs the supplied draft: complete current source profiles, varying decision
cases, local declared renderer dependencies, and caller-owned output assets.
"""
from __future__ import annotations
import hashlib,re
import argparse, copy, hashlib, json, os, random, sys, uuid
from fractions import Fraction as F
from pathlib import Path
import sympy as sp
import math_format

HERE = Path(__file__).resolve().parent
KP_ID = 17592186096700
KP_UUID = 'dc5bab6c-1ce7-58b5-a59d-cff2ce35ecca'
TITLE = 'Identifying Parallel Vectors From a Diagram'
VERSION = 'parallel-diagram-5'
PROFILES = ('opposite_multiple', 'reciprocal_multiple', 'reciprocal_separated', 'shared_chain')
ROMAN = ('I', 'II', 'III')
RADIO_BANK = ('III only', 'II only', 'I only', 'II and III only', 'I and III only')
SOURCE_DATA = json.loads((HERE / 'source-data.json').read_text())

def canonical(x): return json.dumps(x, sort_keys=True, separators=(',', ':'))
def digest(x): return hashlib.sha256(canonical(x).encode()).hexdigest()
def owned(parent, value): return str(uuid.uuid5(uuid.UUID(parent), canonical(value)))
def scale(v, k): return [int(F(x) * F(k)) if (F(x)*F(k)).denominator == 1 else str(F(x)*F(k)) for x in v]
def tex_factor(k):
    # Retained exact factor rendering from the supplied draft.
    k = sp.Rational(str(k))
    if k == 1: return ''
    if k == -1: return '-'
    if k.q == 1: return str(k)
    return ('-' if k < 0 else '') + r'\frac{' + str(abs(k.p)) + '}{' + str(k.q) + '}'
def statement_tex(a, k, b): return a + '=' + tex_factor(k) + b
def subset_text(mask):
    names = [ROMAN[i] for i, yes in enumerate(mask) if yes]
    return ' and '.join(names) + ' only' if names else 'None of the statements'
def truth_set(vectors, statements):
    return [all(F(vectors[a][j]) == F(k)*F(vectors[b][j]) for j in (0,1)) for a,k,b in statements]
def masks_for(profile):
    if profile in PROFILES[:2]:
        return [list(m) for m in __import__('itertools').product((False,True), repeat=3)
                if not (m[0] and m[2] if profile == PROFILES[0] else m[0] and m[1])]
    if profile == PROFILES[2]: return [[True,False,False],[False,True,False],[False,False,True],[False,True,True]]
    return [[False,False,True],[False,True,False],[True,False,False],[False,True,True],[True,False,True]]

def _relation(rng, claim, correct, alternatives):
    if correct: return F(claim)
    # A false equality may fail direction, magnitude, or both. Geometry carries
    # the evidence, never a field label or an unused arrow's fixed orientation.
    modes = [F(-claim)] + [F(x) for x in alternatives if F(x) != F(claim)]
    return rng.choice(modes)

def sample_instance(profile, rng, mask=None):
    # Decision assignments precede numerical and presentational choices.
    mask = list(rng.choice(masks_for(profile))) if mask is None else list(mask)
    if mask not in masks_for(profile): raise ValueError('Mask incompatible with source bank/algebra')
    directions = [(1,2),(2,1),(1,-2),(2,-1),(-1,2),(-2,1),(-1,-2),(-2,-1),(1,1),(-1,1),(1,-1),(-1,-1),(0,1),(1,0)]
    u = rng.choice(directions)
    small = [(1,1),(1,-1),(-1,1),(-1,-1),(1,0),(-1,0),(0,1),(0,-1)]
    v = rng.choice(small if profile == 'shared_chain' else directions)
    while u[0]*v[1] == u[1]*v[0]: v = rng.choice(small if profile == 'shared_chain' else directions)
    if profile == 'opposite_multiple':
        ratio = -2 if mask[0] else 2 if mask[2] else rng.choice((-1,1))
        secondary = _relation(rng, -1, mask[1], (1,2,-2))
        target = rng.choice(('a','b'))
        other = 'a' if target == 'b' else 'b'
        vs = {target:scale(u,ratio), other:scale(u,rng.choice((-2,-1,1,2))), 'e':list(u), 'c':scale(v,secondary), 'd':list(v)}
        st = [(target,'-2','e'),('c','-1','d'),(target,'2','e')]
    elif profile in ('reciprocal_multiple','reciprocal_separated'):
        x,y,z = (mask[0],mask[1],mask[2]) if profile == 'reciprocal_multiple' else (mask[0],mask[2],mask[1])
        ratio = -1 if x else -2 if y else rng.choice((1,2,3,-3))
        secondary = _relation(rng, 1, z, (-1,2,-2))
        vs = dict(a=scale(u,ratio),c=list(u),b=scale(v,secondary),d=list(v),e=scale(u,1))
        # The fifth arrow is unused and belongs to either family, independently.
        vs['e'] = scale(rng.choice((u,v)),rng.choice((-1,1,2)))
        st = [('a','-1','c'),('c','-1/2','a'),('b','1','d')]
        if rng.choice((False,True)):
            vs['a'],vs['c']=vs['c'],vs['a']
            st=[('c','-1','a'),('a','-1/2','c'),('b','1','d')]
        if profile == 'reciprocal_separated': st = [st[0],st[2],st[1]]
    else:
        rq = _relation(rng,3,mask[0],(1,2,-1,-2))
        st_ratio = _relation(rng,2,mask[1],(1,3,-1,-3))
        ps = _relation(rng,-1,mask[2],(1,2,-2))
        vs = dict(q=list(u),r=scale(u,rq),t=list(v),s=scale(v,st_ratio))
        vs['p'] = scale(v,F(st_ratio)*ps)
        st = [('r','3','q'),('s','2','t'),('p','-1','s')]
    if max(abs(F(z)) for vec in vs.values() for z in vec)>6: raise AssertionError('Geometry workload bound')
    labels = list('pqrst' if profile=='shared_chain' else 'magzk' if profile=='reciprocal_separated' else 'abcde')
    rng.shuffle(labels); names = dict(zip(vs,labels))
    vectors = {names[a]:v for a,v in vs.items()}
    statements = [[names[a],k,names[b]] for a,k,b in st]
    cells = [(4,4),(13,4),(22,4),(7,13),(18,13)]; rng.shuffle(cells)
    geometry={}
    for (label,vec),center in zip(vectors.items(),cells):
        tail=[center[j]-int(F(vec[j])//2) for j in (0,1)]
        geometry[label]={'tail':tail,'tip':[tail[j]+int(vec[j]) for j in (0,1)]}
    result={'profile':profile,'vectors':vectors,'statements':statements,'geometry':geometry,'target_mask':mask}
    assert truth_set(vectors,statements)==mask
    return result

def task_key(instance):
    # Count assessed sign/scale relations, not labels, arrow translations,
    # reflections, unused vectors, seeds, or option permutations.
    vs=instance['vectors']; rows=[]
    for a,k,b in instance['statements']:
        axis=next(j for j in (0,1) if F(vs[b][j]))
        actual=F(vs[a][axis])/F(vs[b][axis])
        assert all(F(vs[a][j])==actual*F(vs[b][j]) for j in (0,1))
        rows.append([str(F(k)),str(actual)])
    return digest([instance['profile'],rows])

def plot_geometry(instance, output_dir):
    if output_dir is None: raise ValueError('Set COURSE_ACADEMY_GENERATOR_OUTPUT_DIR to an explicit asset directory')
    import render_plot
    root=Path(output_dir).resolve();root.mkdir(parents=True,exist_ok=True)
    if root==HERE or HERE in root.parents:
        # Local evidence is allowed but never runtime-file directories.
        if not any(part in ('evidence','test-output') for part in root.relative_to(HERE).parts):
            raise ValueError('Assets must not be written into the runtime package')
    config={'geometry':instance['geometry'],'renderer_sha256':hashlib.sha256((HERE/'render_plot.py').read_bytes()).hexdigest(),'version':VERSION}
    target=root/(digest(config)+'.png')
    if not target.exists(): render_plot.render({'config':config,'output':str(target)})
    return str(target)

def solution(instance):
    vs=instance['vectors']; st=instance['statements']; mask=truth_set(vs,st); lines=[]
    for i,(a,k,b) in enumerate(st):
        axis=next(j for j in (0,1) if F(vs[b][j]));ratio=F(vs[a][axis])/F(vs[b][axis])
        direction='the same direction' if ratio>0 else 'opposite directions'
        relation=statement_tex(a,k,b)
        outcome=relation if mask[i] else relation.replace('=',r'\ne ')
        lines.append(f'- Statement {ROMAN[i]} is {"true" if mask[i] else "false"}. The vectors ${a}$ and ${b}$ are parallel and have {direction}. The magnitude of ${a}$ is ${tex_factor(abs(ratio)) or "1"}$ times the magnitude of ${b}$. So, ${outcome}$.')
    true=[ROMAN[i] for i,yes in enumerate(mask) if yes]
    conclusion='none of the statements are true' if not true else ('only statement '+true[0]+' is true') if len(true)==1 else 'only statements '+' and '.join(true)+' are true'
    return '\n\n'.join(lines)+'\n\nTherefore, '+conclusion+'.'


def asset_identity(value):
    """Content identity omits caller-owned filesystem placement."""
    value=str(value)
    def one(path):
        p=Path(path)
        return 'asset-sha256:'+hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else path
    if value.endswith(('.png','.svg')) and Path(value).is_file():return one(value)
    return re.sub(r'!\[([^\]]*)\]\(([^)]+)\)',lambda m:'!['+m[1]+']('+one(m[2])+')',value)

def make_record(instance, seed=0, output_dir=None, replay=None, option_order=None):
    instance=copy.deepcopy(instance); profile=instance['profile'];mask=truth_set(instance['vectors'],instance['statements'])
    if instance.get('target_mask') is not None and mask!=instance['target_mask']:raise ValueError('Stale decision assignment')
    statements=[statement_tex(*row) for row in instance['statements']]
    radio=profile in PROFILES[2:]
    if replay:
        original=SOURCE_DATA['cases'][replay]['question']
        asset=original[':question/problem'].split('![](',1)[1].split(')',1)[0]
        prompt=original[':question/problem'];worked=original[':question/worked-solution']
        # Replay preserves raw source sentence layouts, but validates key truth
        # against the independent measured original arrow geometry.
    else:
        asset=plot_geometry(instance,output_dir)
        prompt='![]('+asset+')\n\nConsider the diagram that is shown above. Which of the following statements are true?'
        if radio: prompt+='\n\n'+'\n\n'.join(f'{ROMAN[i]}. ${s}$' for i,s in enumerate(statements))
        else: prompt+='\n\nSelect all that apply.'
        worked=solution(instance)
    prompt=math_format.normalize_prose(prompt);worked=math_format.normalize_prose(worked)
    content={'version':VERSION,'prompt':asset_identity(prompt),'worked':asset_identity(worked),'profile':profile,'truth':mask,'replay':replay}
    qid=owned(KP_UUID,content);fields=[]
    def field(key,kind,values,correct):
        fid=owned(qid,key)
        choices=[{':answer/id':owned(fid,x),':answer/type':':answer.type/text',':answer/value':x} for x in values]
        return {':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':choices,':answer-field/correct':[':answer/id',owned(fid,correct)]}
    if replay:
        for f in original[':question/answer-fields']:
            values=[a[':answer/value'] for a in f[':answer-field/choices']]
            kind=f[':answer-field/type'][':db/ident'].split('/')[-1]
            fields.append(field(f[':answer-field/key'],kind,values,f[':answer-field/correct'][':answer/value']))
    elif radio:
        correct=subset_text(mask)
        if correct not in RADIO_BANK:raise ValueError('Truth not represented by source bank')
        values=list(RADIO_BANK)
        if option_order is None:random.Random(seed^0xB411).shuffle(values)
        else:values=list(option_order)
        fields=[field('selection','radio',values,correct)]
    else:
        fields=[field('$'+s+'$','checkbox',['false','true'],'true' if mask[i] else 'false') for i,s in enumerate(statements)]
    q={':question/id':qid,':question/problem':prompt,':question/worked-solution':worked,':question/answer-fields':fields}
    if not replay:q[':question/difficulty']=':question.difficulty/moderate'
    elif ':question/difficulty' in original:q[':question/difficulty']=original[':question/difficulty'][':db/ident']
    record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':profile,'bank_profile':profile,'source_ids':SOURCE_DATA['profiles'][profile], 'instance':instance,'mathematical_fingerprint':task_key(instance),'source_replay':replay,'asset':asset,'difficulty_status':'original source labels' if replay else 'source-justified moderate'}}
    return math_format.validate_generated_record(record)

def replay_source(source_id):
    data=SOURCE_DATA['cases'][source_id]
    return make_record(data['instance'],replay=source_id)

def generate_records(difficulty='moderate',count=1,seed=0,output_dir=None,profile=None):
    if difficulty!='moderate':raise ValueError('Only source-justified moderate difficulty is supported')
    if type(count) is not int or count<1:raise ValueError('count must be positive')
    if type(seed) is not int:raise ValueError('seed must be an integer')
    if profile is not None and profile not in PROFILES:raise ValueError('Unknown profile')
    rng=random.Random(seed);seen=set();records=[];attempts=0
    while len(records)<count and attempts<max(500,count*100):
        attempts+=1;selected=profile or rng.choice(PROFILES)
        instance=sample_instance(selected,rng);key=task_key(instance)
        if key in seen:continue
        seen.add(key)
        record=make_record(instance,seed+attempts-1,output_dir)
        record['generation']['sampler_attempt']=attempts
        records.append(record)
    if len(records)!=count:raise ValueError('Requested count exceeds finite sign/scale family or bounded sampling capacity')
    return records

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty',default='moderate',choices=['easy','moderate','hard'])
    ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0)
    ap.add_argument('--format',choices=['json'],default='json');ap.add_argument('--profile',choices=PROFILES)
    ap.add_argument('--replay-source',choices=list(SOURCE_DATA['cases']))
    args=ap.parse_args()
    try:
        records=[replay_source(args.replay_source)] if args.replay_source else generate_records(args.difficulty,args.count,args.seed,os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR'),args.profile)
    except ValueError as exc:ap.error(str(exc))
    print(json.dumps(records,indent=2))

# Every learner-facing checkbox question has a nonempty correct selection.
from generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate_records']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__=='__main__':main()
