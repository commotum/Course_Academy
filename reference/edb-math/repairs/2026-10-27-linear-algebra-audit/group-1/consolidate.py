import copy,hashlib,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import validate_math_structure,validate_math_boundaries
D=json.loads((H/'current.json').read_text());merged={}
for p in json.loads((H/'source-formula-proposals.json').read_text())+json.loads((H/'completion-proposals.json').read_text())+json.loads((H/'answer-format-proposals.json').read_text()):
 
 if p['attribute']=='answer/value':p['evidence']['parent_review']='Parent explicitly reviewed source-backed presentation-only radio-bank repairs; preserve answer IDs, field links, correct links, numeric/mathematical values and learner history.';p.pop('requires_parent_history_review',None)
 key=p['entity'],p['attribute'];assert key not in merged;merged[key]=copy.deepcopy(p)
for p in json.loads((H/'independent-proposals.json').read_text()):
 key=p['entity'],p['attribute']
 if key not in merged:merged[key]=copy.deepcopy(p);continue
 base=merged[key];assert base['before']==p['before'];after=base['after']
 for detail in p['evidence']['derivations']:
  old,new,count=detail['before_fragment'],detail['after_fragment'],detail['occurrences'];assert after.count(old)==count,(key,old,after.count(old));after=after.replace(old,new)
 base['after']=after;base['reason']+=' '+p['reason'];base['evidence']['independent_correction']=p['evidence']
props=list(merged.values());P=copy.deepcopy(D);objects={o[':db/id']:o for o in P['questions']+P['contents']}
for p in props:
 validate_math_structure(p['after'],bare_math=p['attribute']=='answer/value');
 if p['attribute']!='answer/value':validate_math_boundaries(p['after'],strict=True)
 if p['attribute']=='answer/value':
  for q in P['questions']:
   for f in q.get(':question/answer-fields',[]):
    for a in f.get(':answer-field/choices',[])+([f[':answer-field/correct']]if ':answer-field/correct'in f else[]):
     if a[':db/id']==p['entity']:assert a[':answer/value']==p['before'];a[':answer/value']=p['after']
 else:
  assert objects[p['entity']].get(':'+p['attribute'])==p['before'];objects[p['entity']][':'+p['attribute']]=p['after']
 p['before_sha256']=hashlib.sha256((p['before']or'').encode()).hexdigest();p['after_sha256']=hashlib.sha256(p['after'].encode()).hexdigest()
for l in json.loads((H/'missing-key-proposals.json').read_text()):
 q=objects[l['question']];f=next(f for f in q[':question/answer-fields']if f[':db/id']==l['field']);assert ':answer-field/correct'not in f;f[':answer-field/correct']=copy.deepcopy(next(a for a in f[':answer-field/choices']if a[':db/id']==l['answer']))
(H/'proposals.json').write_text(json.dumps(props,indent=2));(H/'proposed.json').write_text(json.dumps(P,indent=2))
items=[];checkboxes=[]
for q in D['questions']:
 for f in q.get(':question/answer-fields',[]):
  if f[':answer-field/type'][':db/ident']==':answer-field.type/checkbox':checkboxes.append([f[':db/id'],'answer-field/key',f[':answer-field/key'],False])
for e,a,v,bare in checkboxes:validate_math_structure(v);validate_math_boundaries(v,strict=True)
items+=checkboxes
for p in props:items.append([p['entity'],p['attribute'],p['after'],p['attribute']=='answer/value'])
for q in json.loads((H/'generator-samples.json').read_text()):
 q=q['question'];e=q[':question/id']
 for a in ['question/problem','question/worked-solution']:items.append([e,a,q[':'+a],False])
 for f in q.get(':question/answer-fields',[]):
  if(f[':answer-field/type'].get(':db/ident')if isinstance(f[':answer-field/type'],dict)else f[':answer-field/type'])==':answer-field.type/checkbox':items.append([f[':answer-field/id'],'answer-field/key',f[':answer-field/key'],False])
  for a in f.get(':answer-field/choices',[]):
   items.append([a[':answer/id'],'answer/value',a[':answer/value'],(a[':answer/type'].get(':db/ident')if isinstance(a[':answer/type'],dict)else a[':answer/type'])==':answer.type/math'])
   if a.get(':answer/feedback'):items.append([a[':answer/id'],'answer/feedback',a[':answer/feedback'],False])
(H/'additional-render-items.json').write_text(json.dumps(items,indent=2));(H/'checkbox-items.json').write_text(json.dumps(checkboxes,indent=2));print('default proposals',len(props),'checkboxes',len(checkboxes),'additional rendered values',len(items))
