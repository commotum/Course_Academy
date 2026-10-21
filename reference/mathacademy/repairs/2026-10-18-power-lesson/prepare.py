"""Normalize malformed equality chains throughout this power-rule lesson."""
import copy,importlib.util,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
spec=importlib.util.spec_from_file_location('power_lesson_formatter',ROOT/'scripts/question_capture/math_format.py');fmt=importlib.util.module_from_spec(spec);spec.loader.exec_module(fmt)
FIRST=r'''\begin{aligned}
\left(5^2\right)^3 &= 5^{2 \cdot 3} \\
&= 5^6.
\end{aligned}'''
SECOND=r'''\begin{aligned}
\left(5^2\right)^3 &= \underbrace{5^2\cdot 5^2\cdot 5^2}_{3\text{ times}} \\[5pt]
&= (5 \cdot 5) \cdot (5 \cdot 5) \cdot (5 \cdot 5) \\[5pt]
&= \underbrace{5\cdot5\cdot5\cdot5\cdot5\cdot5}_{6\text{ times}} \\[5pt]
&= 5^6
\end{aligned}'''

def chain(text):
 text=fmt._legacy_commands(text)
 changes=[]
 for match in fmt.ENV.finditer(text):
  if match[1]!='begin' or match[2]!='aligned':continue
  span=fmt.environment(text,match.start());assert span
  rows=fmt.cells(text[span[0]:span[1]])
  if not rows or len(rows)<2:continue
  # Only rewrite chains whose every nonfinal row has an empty RHS.
  if not all(len(row)==2 and row[1].strip()=='=' and row[0].strip() for row in rows[:-1]):continue
  last=rows[-1]
  if not (len(last)==1 or len(last)==2 and not last[1].strip()):continue
  exprs=[row[0].strip() for row in rows]
  assert all(exprs)
  newrows=[exprs[0]+' &= '+exprs[1]]+['&= '+e for e in exprs[2:]]
  new=r'\begin{aligned}'+'\n'+(' '+r'\\'+'\n').join(newrows)+'\n'+r'\end{aligned}'
  changes.append((match.start(),span[2],new))
 for start,end,new in sorted(changes,reverse=True):text=text[:start]+new+text[end:]
 return fmt.scalable_fraction_parentheses(text)

def normalized(value,prose=True):
 return fmt.MATH.sub(lambda m:chain(m[0]),value) if prose else chain(value)
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2,default=str)+'\n')
def run():
 questions=json.loads((HERE/'questions.json').read_text());after=copy.deepcopy(questions)
 activities=json.loads((HERE/'activities.json').read_text());tutorials=[s[':step/content'] for [a] in activities for s in a[':activity/steps'] if ':tutorial/content' in s[':step/content']];tutorials_after=copy.deepcopy(tutorials)
 changes=[]
 def change(entity,key,new):
  old=entity[key]
  if old!=new:changes.append({'entity':entity[':db/id'],'attribute':key,'before':old,'after':new});entity[key]=new
 def field(entity,key,prose=True):
  old=entity.get(key)
  if isinstance(old,str):change(entity,key,normalized(old,prose))
 for t in tutorials_after:
  if t[':db/id']==17592186065338:
   blocks=list(re.finditer(r'\$\$.*?\$\$',t[':tutorial/content'],re.S));assert len(blocks)==3
   new=t[':tutorial/content']
   for b,replacement in reversed(list(zip(blocks[1:],[FIRST,SECOND]))):new=new[:b.start()]+'$$\n'+replacement+'\n$$'+new[b.end():]
   assert re.sub(r'\$\$.*?\$\$','',new,flags=re.S)==re.sub(r'\$\$.*?\$\$','',t[':tutorial/content'],flags=re.S)
   assert new.count(r'\underbrace{')==2
   change(t,':tutorial/content',new)
  else:field(t,':tutorial/content')
 for [q] in after:
  field(q,':question/problem');field(q,':question/worked-solution')
  for f in q.get(':question/answer-fields',[]):
   for a in f.get(':answer-field/choices',[]):
    kind=a[':answer/type'][':db/ident']
    field(a,':answer/value',kind!=':answer.type/math');field(a,':answer/feedback')
   correct=f.get(':answer-field/correct',{})
   if correct:
    for a in f.get(':answer-field/choices',[]):
     if a[':db/id']==correct[':db/id']:correct.update(a)
 # The repair must retain exactly the same mathematical tokens, apart from
 # alignment markup, legacy wrappers, and scalable fraction parentheses.
 def signature(text):
  text=fmt._legacy_commands(text)
  text=re.sub(r'\\(?:begin|end)\{aligned\}|\\\\(?:\[[^]]*\])?|&|\\(?:left|right)','',text)
  text=re.sub(r'\s+','',text)
  return text
 for c in changes:
  if c['entity']!=17592186065338:assert signature(c['before'])==signature(c['after']),(c['entity'],c['attribute'])
 # TeX validators plus chain-layout checks run on every content field.
 errors=[];strings=0
 def audit(e,key,prose=True):
  nonlocal strings
  text=e.get(key)
  if not isinstance(text,str) or not text.strip():return
  strings+=1
  try:
   (fmt.validate_prose if prose else fmt.validate_tex)(text)
   assert r'\eqalign' not in text
   assert not re.search(r'&\s*=\s*\\\\',text),'Dangling equals before row break'
  except (ValueError,AssertionError) as ex:errors.append({'entity':e[':db/id'],'attribute':key,'error':str(ex)})
 for t in tutorials_after:audit(t,':tutorial/content')
 for [q] in after:
  audit(q,':question/problem');audit(q,':question/worked-solution')
  for f in q.get(':question/answer-fields',[]):
   for a in f.get(':answer-field/choices',[]):
    audit(a,':answer/value',a[':answer/type'][':db/ident']!=':answer.type/math');audit(a,':answer/feedback')
 save('changes.json',changes);save('questions-after.json',after);save('tutorials-before.json',tutorials);save('tutorials-after.json',tutorials_after);save('audit.json',{'passed':not errors,'questions':len(after),'tutorials':len(tutorials),'fields_checked':strings,'findings':errors})
 assert not errors,errors
 records=[];mapping=[]
 for t in tutorials_after:
  records.append({'question':{':question/problem':t[':tutorial/content'],':question/worked-solution':'',':question/answer-fields':[]}});mapping.append({'kind':'tutorial','entity':t[':db/id']})
 for [q] in after:
  render=copy.deepcopy(q);render.setdefault(':question/answer-fields',[])
  for f in render[':question/answer-fields']:
   # Missing source answer keys are outside this formatting repair. Choose a
   # preview-only placeholder solely to display all authored choice formulas.
   if ':answer-field/correct' not in f:f[':answer-field/correct']=f[':answer-field/choices'][0]
  records.append({'question':render});mapping.append({'kind':'question','entity':q[':db/id']})
 save('render-input.json',records);save('render-index.json',mapping)
 print(json.dumps({'questions_audited':len(after),'tutorials_audited':len(tutorials),'questions_changed':len({c['entity'] for c in changes if c['attribute'].startswith(':question/')}),'tutorials_changed':len({c['entity'] for c in changes if c['attribute'].startswith(':tutorial/')}),'fields_changed':len(changes),'field_audit_passed':not errors}))
if __name__=='__main__':run()
