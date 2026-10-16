"""Inventory-wide structure checks. Findings are a review queue, not a quality certificate."""
import json,re,collections
from pathlib import Path
from scripts.question_capture.math_format import validate_prose,validate_tex
P=Path(__file__).resolve().parent
rows=json.loads((P/'content.json').read_text());questions={};tutorials={};owners=collections.defaultdict(list);canonical=set();findings=[];counts=collections.Counter()
def flag(entity,kind,detail,**more):findings.append(dict(entity=entity,kind=kind,detail=detail,**more))
def checktext(e,a,text):
 if not text.strip():flag(e,'empty-content',a);return
 try:validate_tex(text) if a=='answer/value:math' else validate_prose(text)
 except ValueError as ex:flag(e,'tex-structure',str(ex),attribute=a)
 if any(ord(c)<32 and c not in '\n\r\t' for c in text):flag(e,'control-byte',a)
 if re.search(r'\[MATH:|<mjx-container|<math\b|FORMULA',text):flag(e,'unconverted-source',a)
for t in rows:
 e=t[':db/id'];ks=t.get(':topic/knowledge-points',[])
 if not ks:flag(e,'no-kps',t[':topic/title'])
 for k in ks:
  example=k.get(':knowledge-point/canonical-example',{});qs=k.get(':knowledge-point/questions',[])
  if not example:flag(k[':db/id'],'no-canonical-example',k[':knowledge-point/title'])
  else:
   canonical.add(example[':db/id'])
   if not example.get(':question/worked-solution','').strip():flag(example[':db/id'],'no-example-solution',k[':knowledge-point/title'])
  if not qs:flag(k[':db/id'],'empty-pool',k[':knowledge-point/title'])
  for q in qs+[example]:
   if not q:continue
   questions[q[':db/id']]=q;owners[q[':db/id']].append({'topic':e,'kp':k[':db/id'],'role':'example' if q is example else 'practice'})
 for act in t.get(':activity/_scope',[]):
  if act.get(':activity/type',{}).get(':db/ident')!=':activity.type/lesson':continue
  steps={s[':db/id']:s for s in act.get(':activity/steps',[])};nextid=act.get(':activity/first-step',{}).get(':db/id');seen=set()
  while nextid:
   if nextid in seen:flag(act[':db/id'],'route-cycle',str(nextid));break
   if nextid not in steps:flag(act[':db/id'],'route-external-step',str(nextid));break
   seen.add(nextid);nextid=steps[nextid].get(':step/next',{}).get(':db/id')
  if len(seen)!=len(steps):flag(act[':db/id'],'unreachable-steps',str(set(steps)-seen))
  for s in steps.values():
   c=s.get(':step/content',{})
   if ':tutorial/id' in c:tutorials[c[':db/id']]=c
for e,q in questions.items():
 fs=q.get(':question/answer-fields',[]);keys=[f.get(':answer-field/key') for f in fs];prompt=q.get(':question/problem','')
 checktext(e,'question/problem',prompt)
 if q.get(':question/worked-solution'):checktext(e,'question/worked-solution',q[':question/worked-solution'])
 elif e not in canonical:flag(e,'no-practice-solution','No worked solution stored')
 if e in canonical and any(o['role']=='practice' for o in owners[e]):flag(e,'example-in-pool','Canonical example in practice pool')
 if e not in canonical and not fs:flag(e,'no-fields','Practice item is not gradable')
 if len(set(keys))!=len(keys):flag(e,'duplicate-field-keys',str(keys))
 placeholders=re.findall(r'\{\{([^{}]+)\}\}',prompt)
 for key in placeholders:
  if key not in keys:flag(e,'unbound-placeholder',key)
 for f in fs:
  fe=f[':db/id'];kind=f.get(':answer-field/type',{}).get(':db/ident');bank=f.get(':answer-field/choices',[]);correct=f.get(':answer-field/correct',{});counts[kind]+=1
  if kind!=':answer-field.type/free' and not correct:flag(e,'no-correct',str(fe))
  if correct and correct[':db/id'] not in [a[':db/id'] for a in bank]:flag(e,'correct-outside-bank',str(fe))
  if kind in [':answer-field.type/blank',':answer-field.type/select'] and f[':answer-field/key'] not in placeholders:flag(e,'unplaced-field',f[':answer-field/key'])
  if kind==':answer-field.type/checkbox' and {(a.get(':answer/type',{}).get(':db/ident'),a.get(':answer/value')) for a in bank}!={(':answer.type/text','true'),(':answer.type/text','false')}:flag(e,'checkbox-bank',str(fe))
  for a in bank:
   # Banks also hold verbatim learner entries; malformed noncanonical entries are history, not authored defects.
   if a[':db/id']==correct.get(':db/id') or kind in [':answer-field.type/radio',':answer-field.type/select',':answer-field.type/checkbox']:
    checktext(a[':db/id'],'answer/value:math' if a.get(':answer/type',{}).get(':db/ident')==':answer.type/math' else 'answer/value',a.get(':answer/value',''))
for e,t in tutorials.items():checktext(e,'tutorial/content',t.get(':tutorial/content',''))
summary={'basis':2855,'topics':len(rows),'knowledgePoints':sum(len(t.get(':topic/knowledge-points',[])) for t in rows),'questionsAndExamples':len(questions),'tutorials':len(tutorials),'fields':dict(counts),'findings':dict(collections.Counter(f['kind'] for f in findings))}
for name,obj in [('structure-summary',summary),('structure-findings',findings),('questions',list(questions.values())),('tutorials',list(tutorials.values())),('question-owners',owners)]: (P/(name+'.json')).write_text(json.dumps(obj,indent=2))
priority=[]
for t in rows:
 if t[':topic/math-academy-id'] not in [862,146,232]:continue
 priority.append('\n# '+t[':topic/title'])
 for a in t.get(':activity/_scope',[]):
  for s in a.get(':activity/steps',[]):
   c=s.get(':step/content',{})
   if ':tutorial/content' in c:priority.append(f"\n## Tutorial {c[':db/id']} {c[':tutorial/title']}\n{c[':tutorial/content']}")
 for k in t.get(':topic/knowledge-points',[]):
  priority.append('\n## '+k[':knowledge-point/title'])
  for q in [k[':knowledge-point/canonical-example']]+k[':knowledge-point/questions']:
   priority.append(f"\n### {q[':db/id']} {q.get(':question/math-academy-id','authored')}\n{q[':question/problem']}\n\nSolution: {q.get(':question/worked-solution','MISSING')}\n")
   for f in q.get(':question/answer-fields',[]):priority.append(f"{f[':answer-field/key']} {f[':answer-field/type']} => {f.get(':answer-field/correct')} ")
(P/'priority-content.md').write_text('\n'.join(priority))
print(json.dumps(summary,indent=2))
