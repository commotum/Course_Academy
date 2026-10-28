#!/usr/bin/env python3
"""Portable seeded image-radio generator for Creating Parallel Vectors.

Geometry, shared viewports, and solution stages adapted from the supplied draft.
See instructional-account.md for source observations and conservative extensions.
"""
from __future__ import annotations
import argparse
import copy
import itertools
import json
import os
import random
from pathlib import Path
import sympy as sp
from draft_helpers import digest, uid, tex, scalar, exact_vec, plot_spec, solution
from math_format import checked_math_content, normalize_prose
from render_vectors import render_one

VERSION = 'parallel-vectors-3'
HERE = Path(__file__).resolve().parent
SOURCE = json.loads((HERE / 'source_cases.json').read_text())
ANGLES = (0, 45, 90, 135, 180, 225, 270, 315)
SINGLE = ('-3', '-2', '-3/2', '-1', '-1/2', '1/2', '3/2', '2', '3')
PAIR = tuple(itertools.product(('-4', '-3', '-2', '2', '3', '4'), ('-3/2', '-3/4', '-1/2', '1/2', '3/4', '3/2')))
SOURCE_INFO = {
 'q-11324': {'angle':30, 'length':'1', 'scales':['3','-1'], 'correct_index':3,
   'bank':[['1','-2'],['1','-1'],['1','horizontal:-2'],['3','-1'],['3','horizontal:1']]},
 'q-12140': {'angle':60, 'length':'2', 'scales':['-1/2'], 'correct_index':2,
   'bank':[['horizontal:-1/2'],['1'],['-1/2'],['-1'],['horizontal:1/2']]},
 'q-69960': {'angle':120, 'length':'1', 'scales':['-3/4','2'], 'correct_index':4,
   'bank':[['-2','2'],['-3/4','-2'],['3/4','2'],['3/4','-2'],['-3/4','2']]},
 'q-119064': {'angle':225, 'length':'1', 'scales':['3/2'], 'correct_index':2,
   'bank':[['horizontal:3/2'],['-3/2'],['3/2'],['-1/2'],['1/2']]},
}

def output_dir():
 value = os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
 if not value:
  raise ValueError('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR must name an explicit generated-asset directory')
 out = Path(value).expanduser().resolve()
 if out == HERE or HERE in out.parents:
  # Generated assets may live in a workspace evidence folder during author testing,
  # but never beside runtime files inside a deployed package.
  if 'evidence' not in out.relative_to(HERE).parts:
   raise ValueError('Use a generated-asset directory outside the runtime package')
 out.mkdir(parents=True, exist_ok=True)
 return out

def render(vectors, labels, allvectors, reverse_lanes=False):
 spec = plot_spec(vectors, labels, allvectors)
 spec['renderer_version'] = VERSION
 if reverse_lanes and len(vectors) == 2:
  # Swap translations, keeping each vector and its label together.
  t0,t1 = [v['tail'][:] for v in spec['vectors']]
  v0,v1 = spec['vectors']
  mids = [[t[i]+v['vector'][i]/2 for i in range(2)] for t,v in zip((t0,t1),(v0,v1))]
  for v,mid in zip(spec['vectors'],mids[::-1]):
   v['tail'] = [mid[i]-v['vector'][i]/2 for i in range(2)]
 key = digest(spec)
 path = output_dir() / (key+'.png')
 if not path.exists():
  render_one(dict(spec,output=str(path)))
 return str(path)

def catalog(difficulty, order=0):
 if difficulty == 'easy': return [(k,) for k in SINGLE]
 if difficulty == 'moderate': return [tuple(reversed(p)) if order else p for p in PAIR]
 raise ValueError('Unsupported difficulty: '+difficulty)

def sample(difficulty, seed):
 rng=random.Random(seed)
 order = rng.randrange(2) if difficulty == 'moderate' else 0
 bank = rng.sample(catalog(difficulty,order),5)
 # Assign the answer-bearing target before sampling incidental geometry.
 target = rng.randrange(5)
 return {'bank':[list(b) for b in bank], 'target_index':target,
         'angle':rng.choice(ANGLES), 'length':str(rng.choice((1,2))),
         'reverse_lanes':bool(rng.randrange(2))}

def validate(difficulty,p):
 if difficulty not in ('easy','moderate'): raise ValueError('Unsupported difficulty: '+difficulty)
 if p['angle'] not in ANGLES or sp.Rational(p['length']) not in (1,2):raise ValueError('geometry bounds')
 bank=[tuple(str(sp.Rational(k)) for k in b) for b in p['bank']]
 if len(bank)!=5 or len(set(bank))!=5:raise ValueError('Bank must have five unique diagrams')
 allowed=[set(catalog(difficulty,order)) for order in (0,1)]
 if not any(set(bank)<=c for c in allowed):raise ValueError('Bank outside one supported order catalog')
 if type(p['target_index']) is not int or not 0<=p['target_index']<5:raise ValueError('target index')
 return dict(p,bank=[list(b) for b in bank],length=str(sp.Rational(p['length'])))

@checked_math_content
def generate(difficulty='moderate', seed=0, parameters=None):
 if type(seed) is not int:raise ValueError('seed must be an integer')
 p=validate(difficulty,sample(difficulty,seed) if parameters is None else copy.deepcopy(parameters))
 scales=p['bank'][p['target_index']]
 geom=dict(angle=p['angle'],length=p['length'],scales=scales)
 a=exact_vec(geom)
 bank=[[[sp.simplify(sp.Rational(k)*x) for x in a] for k in row] for row in p['bank']]
 allvectors=[[a]]+bank
 labels=[scalar(k) for k in scales]
 promptimage=render([a],['a'],allvectors)
 images=[render(row,labels,allvectors,p.get('reverse_lanes',False)) for row in bank]
 targetimage=images[p['target_index']]
 if difficulty=='easy':
  prompt='![]('+promptimage+')\n\nThe diagram above shows the vector $a$. Which of the following diagrams shows the vector $'+labels[0]+'$?'
 else:
  prompt='![]('+promptimage+')\n\nThe vector $a$ is depicted above. Which of the following diagrams shows the vectors $'+labels[0]+'$ and $'+labels[1]+'$?'
 # Preserve source's intermediate magnitude/sign illustration for a pair.
 sol=solution(geom,[targetimage])
 if difficulty=='moderate':
  first=render([bank[p['target_index']][0]],[labels[0]],allvectors)
  sol=sol.replace('\n\nNext,','\n\n![]('+first+')\n\nNext,',1)
 prompt,sol=normalize_prose(prompt),normalize_prose(sol)
 identity={'version':VERSION,'difficulty':difficulty,'prompt':prompt,'bank':sorted(images),'solution':sol}
 qid=uid(identity);fid=uid([qid,'selection'])
 choices=[{':answer/id':uid([fid,path]),':answer/type':':answer.type/image',':answer/value':path} for path in images]
 correct=choices[p['target_index']][':answer/id']
 random.Random(seed ^ 0xA53).shuffle(choices)
 q={':question/id':qid,':question/problem':prompt,':question/difficulty':':question.difficulty/'+difficulty,
    ':question/worked-solution':sol,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',
    ':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]}
 return {'knowledge_point':SOURCE['knowledge_point'],'question':q,'generation':{
  'version':VERSION,'seed':seed,'parameters':p,'scales':scales,
  'template':'single' if difficulty=='easy' else 'pair-'+('integer-first' if sp.Rational(scales[0]).q==1 else 'fraction-first'),
  'bank_profile':'authored_catalog','source_ids':['q-119064','q-12140'] if difficulty=='easy' else ['q-69960','q-11324'],
  'source_basis':SOURCE['basis'],'semantic_instance':[difficulty,scales],
  'choice_geometry':{c[':answer/id']:p['bank'][images.index(c[':answer/value'])] for c in choices},
  'plot_geometry':[[[str(x) for x in v] for v in row] for row in bank],
  'rejection_count':0}}

def source_replay(source_id, complete=False):
 """Exact capture replay, including original bank and omissions; completion is explicit."""
 q=copy.deepcopy(next(q for q in SOURCE['questions'] if q[':question/math-academy-id']==source_id))
 info=SOURCE_INFO[source_id];f=q[':question/answer-fields'][0]
 inferred=':answer-field/correct' not in f
 if complete and inferred:
  c=f[':answer-field/choices'][info['correct_index']]
  f[':answer-field/correct']=[':answer/id',c[':answer/id']]
  q[':question/worked-solution']=solution(info,[c[':answer/value']])
 return {'knowledge_point':SOURCE['knowledge_point'],'question':q,'generation':{'version':VERSION,
  'source_id':source_id,'source_replay':True,'inferred_completion':complete and inferred,
  'bank_profile':source_id,'parameters':info}}

def batch(difficulty,count,seed):
 if difficulty not in ('easy','moderate'):raise ValueError('Unsupported difficulty: '+difficulty)
 if count<0:raise ValueError('count must be nonnegative')
 return [generate(difficulty,seed+i) for i in range(count)]

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--difficulty',choices=['easy','moderate','hard'],default='moderate')
 ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0)
 ap.add_argument('--format',choices=['json'],default='json')
 args=ap.parse_args()
 try: records=batch(args.difficulty,args.count,args.seed)
 except ValueError as e:ap.error(str(e))
 print(json.dumps(records,indent=2))
