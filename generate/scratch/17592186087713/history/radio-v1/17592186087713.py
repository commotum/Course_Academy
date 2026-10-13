#!/usr/bin/env python3
"""Identify matrices by dimensions, math basis 1356; no database operations.

Observed: three labeled arrays, five text-radio subset choices. Entries may be
integers, decimals, or radicals but are not operated on. All source bank profiles
are positional subset recipes, not copied question payloads. Parameters supply
complete rectangular arrays and target dimensions; replay uses normal rendering.
Easy (authored): nonsquare targets <=3, one match, transpose and square foil.
Moderate (observed + authored peers): targets/arrays <=4, one or two matches.
Hard (authored): target sides 3..4, foils differ by one row/column within 2..4;
three visually similar arrays, one or two matches. These level labels are design
claims; the source provides no easy/hard labels. No arithmetic or index notation.
API generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None), plus individual level entrypoints. Invalid explicit inputs fail.
Content identity hashes actual prompt, solution, and complete unordered bank;
task fingerprint ignores entries, labels, option order and profiles because only
array dimensions are assessed. JSON is review data, never transaction EDN.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from itertools import combinations
import sympy as sp
KP_ID=17592186087713
KP_UUID='ed7286fe-b6e2-5544-8bc6-86afc6cdb813'
TITLE='Identifying a Matrix by Its Description'
VERSION='matrix-description-1'
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
TEMPLATES={'legacy_bmatrix':{'levels':['moderate'],'origin':'observed unrated'},'aligned_single':{'levels':['moderate'],'origin':'observed'},'aligned_multiple':{'levels':['moderate'],'origin':'observed'},'peer_single':{'levels':['easy','moderate','hard'],'origin':'authored'},'peer_multiple':{'levels':['moderate','hard'],'origin':'authored'}}
# Whole banks: 3 singletons and 2 pairs. Each index points to a displayed array.
PROFILES={
 'q-69514':((1,),(0,1),(1,2),(2,),(0,)),
 'q-69515':((1,2),(1,),(0,),(2,),(0,1)),
 'q-125550':((0,2),(2,),(1,2),(1,),(0,)),
 'q-125552':((0,),(1,),(1,2),(0,1),(2,)),
 'q-69518':((0,1),(2,),(1,2),(1,),(0,)),
 'q-69523':((2,),(0,1),(0,),(1,),(0,2)),
 'q-125549':((0,2),(2,),(1,),(0,),(0,1)),
 'q-69517':((1,2),(0,),(0,1),(2,),(1,)),
 'omit01':((0,),(1,),(2,),(0,2),(1,2)),
 'omit02':((0,),(1,),(2,),(0,1),(1,2)),
 'omit12':((0,),(1,),(2,),(0,1),(0,2)),
}
ENTRIES=('0','1','-1','2','-2','3','-3','4','5','7',r'\sqrt{2}',r'\sqrt{3}','-0.1','1.1')
def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def uid(s): return str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:'+s))
def dimensions(a): return [len(a),len(a[0])]
def entry_value(s):
 if not isinstance(s,str) or not re.fullmatch(r'-?\d+(?:\.\d+)?|\\sqrt\{[23]\}',s): raise ValueError('Entry must be a supported exact number token')
 return sp.sqrt(int(s[-2])) if s.startswith('\\sqrt') else sp.Rational(s)
def constraints(p,level,observed=False):
 if set(p)!={'target','labels','matrices'}: raise ValueError('Exact parameter keys: target, labels, matrices')
 if len(p['target'])!=2 or any(type(n)!=int or not 1<=n<=4 for n in p['target']): raise ValueError('Invalid target')
 if len(p['labels'])!=3 or len(set(p['labels']))!=3 or any(not re.fullmatch('[A-Z]',l) for l in p['labels']): raise ValueError('Three distinct uppercase labels required')
 if len(p['matrices'])!=3: raise ValueError('Three arrays required')
 for a in p['matrices']:
  if not isinstance(a,list) or not 1<=len(a)<=4 or not all(isinstance(row,list) and 1<=len(row)<=4 and len(row)==len(a[0]) for row in a): raise ValueError('Invalid rectangular array')
  for row in a:
   for s in row: entry_value(s)
 ds=[dimensions(a) for a in p['matrices']]; match=[i for i,d in enumerate(ds) if d==p['target']]
 if len(match) not in (1,2): raise ValueError('Exactly one or two matrices must match')
 if not observed and level=='easy':
  r,c=p['target']
  if max(r,c)>3 or r==c or len(match)!=1 or sorted(ds)!=sorted([[r,c],[c,r],[r,r]]) and sorted(ds)!=sorted([[r,c],[c,r],[c,c]]): raise ValueError('Easy requires target, transpose, square with sides <=3')
 if not observed and level=='hard':
  if min(p['target'])<3 or any(min(d)<2 or sum(abs(x-y) for x,y in zip(d,p['target']))!=1 for i,d in enumerate(ds) if i not in match): raise ValueError('Hard requires target sides 3..4 and adjacent foil dimensions 2..4')
 return match

def sample(level,rng,multiple):
 r,c=rng.choice([(r,c) for r in range(1,5) for c in range(1,5) if (level!='easy' or max(r,c)<=3 and r!=c) and (level!='hard' or min(r,c)>=3)])
 target=[r,c]; shapes=[target]*(2 if multiple else 1)
 if level=='easy':shapes += [[c,r],rng.choice([[r,r],[c,c]])]
 else:
  foils=[[a,b] for a in range(1,5) for b in range(1,5) if [a,b]!=target and (level!='hard' or min(a,b)>=2 and abs(a-r)+abs(b-c)==1)]
  shapes+=rng.sample(foils,3-len(shapes))
 rng.shuffle(shapes)
 labels=list(rng.choice(('ABC','EFG','LMN','PQR','BCD','FGH')))
 return {'target':target,'labels':labels,'matrices':[[[rng.choice(ENTRIES) for _ in range(c)] for _ in range(r)] for r,c in shapes]}

def render_array(a,legacy=False):
 inside=' \\\\ '.join(' & '.join(row) for row in a)
 return r'\begin{bmatrix}'+inside+r'\end{bmatrix}' if legacy else r'[\begin{aligned}'+inside+r'\end{aligned}]'
def choice_value(indices,labels):return ' and '.join('$'+labels[i]+'$' for i in indices)+' only'
def render(p,template):
 r,c=p['target'];legacy=template=='legacy_bmatrix'
 if legacy:
  problem=f'Which of the following is a ${r} \\cdot {c}$ matrix?\n\n$'+', '.join(l+' = '+render_array(a,True) for l,a in zip(p['labels'],p['matrices']))+'$'
 else:
  problem=f'Which of the following is a ${r}\\times {c}$ matrix?\n\n$$\n'+r',\,'.join(l+'='+render_array(a) for l,a in zip(p['labels'],p['matrices']))+'\n$$'
 match=[i for i,a in enumerate(p['matrices']) if dimensions(a)==p['target']]
 lines=[]
 for i,(l,a) in enumerate(zip(p['labels'],p['matrices'])):
  ar,ac=dimensions(a);mark=r'$\,✓$' if i in match else r'$\,\times $'
  lines.append(f'- The matrix ${l}$ has ${ar}$ '+('row' if ar==1 else 'rows')+f' and ${ac}$ '+('column' if ac==1 else 'columns')+f'. So, its dimensions are ${ar}\\times {ac}.$ '+mark)
 labels=' and '.join('$'+p['labels'][i]+'$' for i in match)
 solution='\n\n'.join(lines)+'\n\nTherefore, only '+labels+(' is a ' if len(match)==1 else ' are ')+f'${r}\\times {c}$ '+('matrix.' if len(match)==1 else 'matrices.')
 return problem,solution

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only original radio layout supported')
 if profile is not None and profile not in PROFILES:raise ValueError('Unknown profile')
 rng=random.Random(seed)
 if template is None:template='peer_single' if level=='easy' else rng.choice(('peer_single','peer_multiple'))
 if template not in TEMPLATES or level not in TEMPLATES[template]['levels']:raise ValueError('Unsupported template/level')
 observed=not template.startswith('peer_')
 if observed and parameters is None:raise ValueError('Observed template requires explicit array parameters')
 p=json.loads(json.dumps(parameters)) if parameters is not None else sample(level,rng,template.endswith('multiple'))
 matches=constraints(p,level,observed)
 if template.endswith('multiple') and len(matches)!=2 or (template.endswith('single') or template=='legacy_bmatrix') and len(matches)!=1:raise ValueError('Template requires its documented match count')
 if profile is None:profile=rng.choice([name for name in ('omit01','omit02','omit12') if tuple(matches) in PROFILES[name]])
 bank=PROFILES[profile]
 if tuple(matches) not in bank:raise ValueError('Whole bank omits correct subset')
 problem,solution=render(p,template)
 values=[choice_value(indices,p['labels']) for indices in bank]
 if len(values)!=5 or len(set(values))!=5:raise ValueError('Invalid whole bank')
 identity=digest({'version':VERSION,'prompt':problem,'solution':solution,'bank':sorted(values),'type':'radio'})
 qid=uid(identity);fid=uid(identity+':selection')
 answers=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/text',':answer/value':v} for v in values]
 correct=next(a[':answer/id'] for a in answers if a[':answer/value']==choice_value(matches,p['labels']))
 rng.shuffle(answers)
 task=digest({'criterion':'ordered-row-column-dimensions','target':p['target'],'candidate_dimensions':sorted(dimensions(a) for a in p['matrices'])})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'source':SOURCE,'seed':seed,'level':level,'template':template,'profile':profile,'origin':TEMPLATES[template]['origin'],'parameters':p,'parameter_fingerprint':task,'mathematical_task_fingerprint':task,'content_hash':identity,'recipes':[list(v) for v in bank],'dependencies':{'sympy':sp.__version__}}}
# EASY: authored nonsquare target, transpose, square; one match, <=3 entries/side.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# MODERATE: source workload, <=4 entries/side, one or two matching arrays.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# HARD: authored adjacent counts, target 3..4, foils 2..4; no new math operation.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(rec):
 q=rec['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- '+a[':answer/value'] for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=('easy','moderate','hard','all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('markdown','json'),default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 if args.count<1:ap.error('count must be positive')
 records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in (('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,)) for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
