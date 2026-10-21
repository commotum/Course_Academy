#!/usr/bin/env python3
"""Finite source-backed checkbox graph catalog. No cosmetic replenishment.
Easy only; v2 extensions archived. Unknown curve algebra fixes neighborhoods.
Seed chooses a catalog member; it never contributes to question identity.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, random, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186068697
KP_UUID='3f92e521-e7ab-56ba-8eac-0484b140b1a2'
TITLE='Determining the Behavior of a Function in the Neighborhood of a Point'
VERSION='neighborhood-checkbox-finite-3'
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'current-source.json').read_text())
SPECS=json.loads((ROOT/'specs.json').read_text())
SUPPORTED_LEVELS=('easy',)
GENERATOR_ID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
NS=uuid.UUID('28974b77-e87e-42cb-951b-9eeb8b63db1d')
CRITERIA={
 'q-48042':['left_finite','right_finite','discontinuous'],
 'q-48064':['defined','limit_exists','continuous'],
 'q-48063':['defined','left_exists','continuous'],
 'q-104049':['defined','limit_unequal_value','discontinuous'],
 'q-104051':['defined','limit_exists','discontinuous'],
 'q-104052':['not_defined','limit_exists','continuous'],
 'q-104124':['not_defined','limit_equals_value','continuous'],
 'q-48040':['defined','limit_exists','continuous'],
 'q-48062':['defined','limit_exists','continuous'],
 'q-48065':['defined','limit_equals_value','continuous'],
 'q-48067':['defined','limit_equals_value','continuous'],
 'q-48068':['left_finite','right_not_finite','secondary_continuous']}
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
TEMPLATES=tuple(k for k,q in QUESTIONS.items() if q.get(':question/difficulty',{}).get(':db/ident')==':question.difficulty/easy')
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def truth(template):
 z=SPECS[template];l=z['left'];r=z['right'];v=z['value'];finite=lambda x:not isinstance(x,str)
 exists=finite(l) and finite(r) and sp.Rational(l)==sp.Rational(r)
 equal=exists and v is not None and sp.Rational(l)==sp.Rational(v)
 p={'left_finite':finite(l),'right_finite':finite(r),'left_exists':finite(l),'right_not_finite':not finite(r),'defined':v is not None,'not_defined':v is None,'limit_exists':exists,'limit_equals_value':equal,'limit_unequal_value':exists and v is not None and sp.Rational(l)!=sp.Rational(v),'continuous':equal,'discontinuous':not equal,'secondary_continuous':z['b']!=z['a'] and any(x==z['b'] and filled for x,y,filled in z['markers']) and not any(x==z['b'] and not filled for x,y,filled in z['markers'])}
 return [bool(p[c]) for c in CRITERIA[template]]
def fingerprint(template):
 z=SPECS[template]
 return digest({'criteria':CRITERIA[template],'left_finite':not isinstance(z['left'],str),'right_finite':not isinstance(z['right'],str),'equal_limits':z['left']==z['right'],'defined':z['value'] is not None,'value_on_left':z['value'] is not None and z['value']==z['left'],'value_on_right':z['value'] is not None and z['value']==z['right']})
def normalize(q):
 result={k:str(q[k]) if k==':question/id' else q[k] for k in (':question/id',':question/problem',':question/worked-solution')}
 if ':question/difficulty' in q:result[':question/difficulty']=str(q[':question/difficulty'][':db/ident'])
 result[':question/answer-fields']=[]
 for f in sorted(q[':question/answer-fields'],key=lambda x:x[':answer-field/key']):
  result[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':sorted([{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],key=lambda a:a[':answer/value'])})
 return result
def replay_source(template):
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':normalize(QUESTIONS[template]),'generation':{'version':VERSION,'template':template,'seed':0,'parameters':{},'profile':'checkbox-true-false','mathematical_fingerprint':fingerprint(template),'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'source_question_id':QUESTIONS[template][':db/id'],'evidence_only':True,'eligible_for_learning':False,'dependencies':{'sympy':sp.__version__}}}
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('unsupported difficulty; see capabilities.json')
 if parameters not in (None,{}):raise ValueError('finite catalog has no parameter slots; coordinate shifts duplicate tasks')
 if field_type not in (None,'checkbox',':answer-field.type/checkbox'):raise ValueError('three checkbox fields required')
 if profile not in (None,'checkbox-true-false'):raise ValueError('unsupported profile')
 template=template or random.Random(seed).choice(TEMPLATES)
 if template not in TEMPLATES:raise ValueError('template is unrated or outside finite easy catalog')
 rec=copy.deepcopy(replay_source(template));q=rec['question'];fp=fingerprint(template);q[':question/id']=str(uuid.uuid5(NS,VERSION+digest({'task':fp,'problem':q[':question/problem'],'solution':q[':question/worked-solution']})))
 for f in q[':question/answer-fields']:
  correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);fid=str(uuid.uuid5(NS,q[':question/id']+f[':answer-field/key']));f[':answer-field/id']=fid
  for a in f[':answer-field/choices']:a[':answer/id']=str(uuid.uuid5(NS,fid+a[':answer/value']))
  f[':answer-field/correct']=[':answer/id',str(uuid.uuid5(NS,fid+correct))]
 rec['generation'].update(seed=seed,evidence_only=False,eligible_for_learning=True)
 return rec
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def batch(level,count,seed=0):
 if level not in SUPPORTED_LEVELS:raise ValueError('unsupported difficulty')
 if count<0:raise ValueError('nonnegative count required')
 order=list(TEMPLATES);random.Random(seed).shuffle(order);seen=set();out=[]
 for t in order:
  fp=fingerprint(t)
  if fp in seen:continue
  seen.add(fp)
  if len(out)<count:out.append(generate(level,seed,template=t))
 return out
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='json');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args();level='easy' if a.difficulty=='all' else a.difficulty
 out=[generate(level,a.seed,a.template,profile=a.profile)] if a.template else batch(level,a.count,a.seed)
 if a.format=='json':print(json.dumps(out,indent=2))
 else:
  for r in out:print(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'])

# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['batch', 'generate', 'generate_easy']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__=='__main__':main()
