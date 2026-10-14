#!/usr/bin/env python3
"""Identify 2D vector fields; frozen math basis 1356. No database operations.

Eight observed easy recipes and complete five-choice banks. Moderate/hard are
explicitly authored labels for the same categorical method, not recovered levels.
Only signatures, output dimensions and nonempty restricted domains matter;
coefficient changes and variable/function aliases do not increase task counts.
Source profiles preserve literal source prose, including documented name errors.
Normal records use the same prose stages with minimal name/set-notation repairs.
"""
from __future__ import annotations
import argparse, copy, hashlib, itertools, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186172085
KP_UUID='019e5a17-1aab-565b-8881-447c86a9a7ec'
TITLE='Identifying Vector Fields on Two-Dimensions'
VERSION='vector-identification-1'
DIR=Path(__file__).with_suffix('')
CAPTURE=json.loads((DIR/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in CAPTURE['record'][':knowledge-point/questions']}
# Complete expression/domain slots; no replacement of isolated variable letters.
# Anchors are observed constants; each slot is evaluated for every ordinary call.
RECIPES={
 'q-122465': (r'\operatorname{ln}⁡y',lambda h:r'\operatorname{ln}⁡'+('y' if h==0 else '(y'+signed(-h)+')'),r'y>0',lambda h:'y>'+str(h)),
 'q-122643': (r'\frac{1}{{x}^{2}}',lambda h:r'\frac{1}{'+('{x}^{2}' if h==0 else '(x'+signed(-h)+')^{2}')+'}',r'x\ne 0',lambda h:r'x\ne '+str(h)),
 'q-122650': (r'\frac{1}{x+2}',lambda h:r'\frac{1}{x'+signed(h)+'}',r'x\ne -2,\,x-y\ge 0',lambda h:r'x\ne '+str(-h)+r',\,x-y\ge 0'),
 'q-122653': (r'\operatorname{ln}⁡(x+y)',lambda h:r'\operatorname{ln}⁡(x+y'+('' if h==0 else signed(-h))+')',r'x+y>0',lambda h:'x+y>'+str(h)),
 'q-122678': (r'\frac{{x}^{2}}{x-y}',lambda h:r'\frac{{x}^{2}}{x-y'+('' if h==0 else signed(-h))+'}',r'x\ne y',lambda h:r'x\ne y'+('' if h==0 else signed(h))),
 'q-122641': (r'{x}^{2}',lambda h:'{x}^{'+str(h)+'}',None,None),
 'q-122656': (r'\operatorname{cos}⁡y+1',lambda h:r'\operatorname{cos}⁡y'+signed(h),None,None),
 'q-122675': (r'\frac{1}{x+y}',lambda h:r'\frac{1}{x+y'+('' if h==0 else signed(-h))+'}',r'x+y\ne 0',lambda h:r'x+y\ne '+str(h)),
}
ANCHORS={s:0 for s in SOURCES};ANCHORS.update({'q-122650':2,'q-122641':2,'q-122656':1})
DIMENSIONS={
 'q-122465':[(2,2,'all'),(2,2,'log'),(3,3,'all')],
 'q-122643':[(2,2,'reciprocal'),(3,3,'all'),(1,2,'all')],
 'q-122650':[(2,2,'reciprocal+sqrt'),(2,2,'all'),(3,3,'all')],
 'q-122653':[(2,2,'log'),(3,3,'all'),(1,2,'all')],
 'q-122678':[(2,2,'reciprocal'),(3,3,'all'),(2,2,'all')],
 'q-122641':[(2,2,'all'),(1,2,'sqrt'),(3,3,'all')],
 'q-122656':[(2,3,'reciprocal'),(2,2,'all'),(1,2,'sqrt')],
 'q-122675':[(2,2,'reciprocal'),(2,2,'all'),(2,3,'all')],
}
LABELS={1:'I only',2:'II only',3:'I and II only',4:'III only',5:'I and III only',6:'II and III only',7:'I, II, and III'}
TEMPLATES={s:'easy' for s in SOURCES}|{'mixed_dimensions':'moderate','restricted_mixed_dimensions':'hard'}
BANK_PROFILES={s:{'template':s,'origin':'observed'} for s in SOURCES}|{s+'-normal':{'template':s,'origin':'presentation-repaired'} for s in SOURCES}|{'authored':{'origin':'authored'}}
def signed(n): return ('+' if n>=0 else '')+str(n)
def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy/'+s))
def subset(ds):return sum(1<<i for i,(inp,out,_) in enumerate(ds) if inp==out==2)
def prose():return SOURCES['q-122465'][':question/worked-solution'].split('\n\n- ')[0]
def normal_repairs(s,text):
 if s=='q-122678':text=text.replace('$K(x,y,z)$','$V(x,y,z)$').replace('$V(x,y)$','$W(x,y)$')
 if s=='q-122675':text=text.replace('$E(x,y,z)$','$E(x,y)$')
 return text.replace('S={','S=\\{').replace('}\n$$','\\}\n$$')
def authored(level,h,order,kind):
 # One qualifying map, two mismatches. Signatures include unused variables,
 # so dependence alone cannot replace reading the declared input dimension.
 log=r'\operatorname{ln}⁡(x+y'+('' if h==0 else signed(-h))+')'
 reciprocal=r'\frac{1}{x'+signed(h)+'}'
 sqrt=r'\sqrt{x-y}'
 if level=='moderate':
  f='A(x,y)=⟨'+{'log':log,'reciprocal':reciprocal,'sqrt':sqrt}[kind]+r',y^{2}⟩'
  restriction={'log':'x+y>'+str(h),'reciprocal':r'x\ne '+str(-h),'sqrt':r'x-y\ge 0'}[kind]
 else:
  components={'reciprocal+sqrt':(reciprocal,sqrt),'log+sqrt':(log,sqrt),'log+reciprocal':(log,reciprocal)}[kind]
  f='A(x,y)=⟨'+','.join(components)+'⟩'
  restriction={'reciprocal+sqrt':r'x\ne '+str(-h)+r',\,x-y\ge 0','log+sqrt':'x+y>'+str(h)+r',\,x-y\ge 0','log+reciprocal':'x+y>'+str(h)+r',\,x\ne '+str(-h)}[kind]
 formulas=[f,r'B(x,y,z)=⟨x+y,y^{2}⟩',r'C(x,y)=⟨x,y,x-y⟩']
 ds=[(2,2,kind),(3,2,'all'),(2,3,'all')]
 entries=["- The function $A(x,y)$ is a vector field on ${R}^{2}.$ It maps every point in the set $S,$ given by\n\n$$\nS=\\{(x,y)\\in {R}^{2}\\,|\\,"+restriction+"\\}\n$$\n\nto a vector in ${R}^{2}.$",
 '- The function $B(x,y,z)$ is *not* a vector field on ${R}^{2}.$ It assigns points in ${R}^{3}$ (not ${R}^{2}$) to vectors in ${R}^{2}.$',
 '- The function $C(x,y)$ is *not* a vector field on ${R}^{2}.$ It assigns points in ${R}^{2}$ to vectors in ${R}^{3}$ (not ${R}^{2}$).']
 ds=[ds[i] for i in order];correct=LABELS[subset(ds)]
 return 'Which of the following are vector fields on ${R}^{2}?$\n\n'+'\n'.join('- $'+formulas[i]+'$' for i in order),prose()+'\n\n'+'\n\n'.join(entries[i] for i in order)+'\n\nTherefore, the correct answer is "'+correct+'."',ds

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
 if field_type not in (None,'radio'):raise ValueError('only source radio shape supported')
 rng=random.Random(seed)
 if profile not in (None,'authored'):
  if profile not in BANK_PROFILES:raise ValueError('unknown profile')
  pt=BANK_PROFILES[profile]['template']
  if template is not None and template!=pt:raise ValueError('profile/template mismatch')
  template=pt
 if template is None:template=rng.choice(list(SOURCES)) if level=='easy' else ('mixed_dimensions' if level=='moderate' else 'restricted_mixed_dimensions')
 if TEMPLATES.get(template)!=level:raise ValueError('template/difficulty mismatch')
 if profile=='authored' and level=='easy':raise ValueError('easy uses complete observed banks')
 raw=profile in SOURCES
 kinds=['log','sqrt','reciprocal'] if level=='moderate' else ['reciprocal+sqrt','log+sqrt','log+reciprocal']
 if parameters is None:
  p={'h':rng.choice([1,2,3,4]) if template=='q-122641' else rng.randint(-4,4),'order':list(rng.choice(list(itertools.permutations(range(3)))))}
  if raw:p['order']=[0,1,2]
  elif level=='easy':
   bank={a[':answer/value'] for a in SOURCES[template][':question/answer-fields'][0][':answer-field/choices']}
   eligible=[list(o) for o in itertools.permutations(range(3)) if LABELS[subset([DIMENSIONS[template][i] for i in o])] in bank]
   p['order']=rng.choice(eligible)
  if level!='easy':p['kind']=rng.choice(kinds)
 else:p=copy.deepcopy(parameters)
 if level!='easy':
  p.setdefault('kind',kinds[0])
  if p['kind'] not in kinds:raise ValueError('invalid restriction kind for difficulty')
 if set(p)!=({'h','order'} if level=='easy' else {'h','order','kind'}) or type(p['h']) is not int or sorted(p['order'])!=[0,1,2]:raise ValueError('parameters require integer h and order permutation')
 if not -4<=p['h']<=4 or (template=='q-122641' and not 1<=p['h']<=4):raise ValueError('h outside comparable source workload')
 order=p['order'];h=p['h']
 if raw and order!=[0,1,2]:raise ValueError('raw source profile preserves source ordering')
 if level=='easy':
  s=SOURCES[template];anchor,calc,domain,dcalc=RECIPES[template]
  problem=s[':question/problem'].replace(anchor,calc(h));solution=s[':question/worked-solution']
  if domain:solution=solution.replace(domain,dcalc(h))
  ds=[DIMENSIONS[template][i] for i in order]
  correct=LABELS[subset(ds)]
  if not raw:
   formulas=problem.split('\n\n',1)[1].split('\n')
   problem=problem.split('\n\n',1)[0]+'\n\n'+'\n'.join(formulas[i] for i in order)
   intro,*bullets=solution.split('\n\n- ')
   ending=bullets[-1].split('\n\nTherefore,')[0];bullets[-1]=ending
   solution=intro+'\n\n'+'\n\n'.join('- '+bullets[i] for i in order)+'\n\nTherefore, the correct answer is "'+correct+'."'
   solution=normal_repairs(template,solution)
  values=[a[':answer/value'] for a in s[':question/answer-fields'][0][':answer-field/choices']]
  if correct not in values:raise ValueError('permutation not eligible for this complete source bank')
  selected=profile or template+'-normal'
 else:
  if profile not in (None,'authored'):raise ValueError('authored level profile mismatch')
  problem,solution,ds=authored(level,h,order,p['kind']);correct=LABELS[subset(ds)]
  values=[LABELS[m] for m in (1,2,3,4,5)] # all three singleton outcomes included
  selected='authored'
 if len(set(values))!=5 or values.count(correct)!=1:raise ValueError('complete bank ambiguity')
 canonical={'version':VERSION,'difficulty':level,'prompt':problem,'solution':solution,'bank':sorted(values)}
 ident=digest(canonical);qid=uid(ident);fid=uid(ident+'/selection')
 choices=[{':answer/id':uid(fid+'/'+v),':answer/type':':answer.type/text',':answer/value':v} for v in values];rng.shuffle(choices)
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',uid(fid+'/'+correct)]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':[field]},'generation':{'version':VERSION,'template':template,'seed':seed,'parameters':p,'bank_profile':selected,'source':{'database':'math','basis':1356,'lineage':CAPTURE['lineage']},'raw_evidence':raw,'eligible_for_learning':not(raw and template in ('q-122678','q-122675')),'origin':'observed' if level=='easy' else 'authored missing-level design','dimensions':ds,'mathematical_fingerprint':digest(ds),'content_fingerprint':ident,'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'plot_rating':'none'}}
# EASY: source signatures, component-count checks, and elementary restrictions.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: authored mixed mismatches; unused formal z requires signature reading.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: same mixed mismatch check plus two compatible component restrictions.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- '+a[':answer/value'] for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
def main():
 a=argparse.ArgumentParser(description=__doc__);a.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',choices=['markdown','json'],default='markdown');a.add_argument('--template');a.add_argument('--profile');a.add_argument('--field-type',choices=['radio']);v=a.parse_args()
 if v.count<1:a.error('count must be positive')
 levels=['easy','moderate','hard'] if v.difficulty=='all' else [v.difficulty]
 try:rs=[generate(l,v.seed+i,v.template,v.field_type,profile=v.profile) for l in levels for i in range(v.count)]
 except ValueError as e:a.error(str(e))
 print(json.dumps(rs,indent=2,ensure_ascii=False) if v.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in rs))
if __name__=='__main__':main()
