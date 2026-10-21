"""Check restored None-only source cases and explicitly supplied parameters."""
import importlib.util,sys
from read import *
from scripts.generator_policy import checkbox_selection

def load(path,name):
 sys.path.insert(0,str(path.parent));spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module);return module

def check(record):
 q=record['question'];fields=q[':question/answer-fields'];none=[f for f in fields if f[':answer-field/key']=='None of the above'];assert len(none)==1
 ordinary=checkbox_selection({':question/answer-fields':[f for f in fields if f is not none[0]]});selected=checkbox_selection({':question/answer-fields':none})[0];assert selected==(not any(ordinary));return selected

if __name__=='__main__':
 rows={r['kp']:r for r in json.loads((HERE/'patched.json').read_text())};all_records=[];reports=[]
 for kp in (17592186147456,17592186119848,17592186100888,17592186054815):
  row=rows[kp];g=load(Path(row['updated_script']),'special_none_'+str(kp));current=[]
  if kp==17592186147456:
   for template,(level,_)in g.CASES.items():
    for seed in range(3):current.append(g.generate(level,seed,template=template))
   zero=g.generate('moderate',template='q-108916',parameters={'left_scales':[1,1,1],'right_scales':[1,1,1]});assert check(zero)is True;current.append(zero)
  elif kp==17592186119848:
   current=g.catalog()
   for sid in g.CASES:
    if g.kind(sid)=='three-matrix-checkbox':
     zero=g.generate('easy',profile=sid,parameters={'matches':[]});assert check(zero)is True;current.append(zero)
  elif kp==17592186100888:
   for template,level in g.LEVELS.items():
    for case in g.CASES:
     r=g.generate(level,17,template=template,decision_case=case);assert check(r)==(case==(False,False));current.append(r)
  else:
   import random
   for target in g.TARGETS:
    _,values,_=g.sample(random.Random(37),target=target,mask=0)
    r=g.generate(target,values);assert check(r)is True;current.append(r)
  for r in current:
   if checkbox_selection(r):check(r)
  all_records.extend(current);reports.append({'kp':kp,'records':len(current),'none_correct':sum(check(r)for r in current if checkbox_selection(r)),'passed':True});print(json.dumps(reports[-1]),flush=True)
 save('special-records.json',all_records);save('special-verification.json',reports)
