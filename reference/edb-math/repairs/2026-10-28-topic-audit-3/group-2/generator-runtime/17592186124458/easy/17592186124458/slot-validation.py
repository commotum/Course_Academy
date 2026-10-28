"""Validate declared numerical/direction slots and independently catch stale targets."""
import copy,importlib.util,json
from pathlib import Path
P=Path(__file__).parent
sp=importlib.util.spec_from_file_location('slot_validator',P/'validate.py');v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v);g=v.g
p={'a':2,'b':3,'c':1,'d':1,'x0':1,'y0':2,'dx':1,'dy':2}
a=g.generate('easy',template='linear_y2',parameters=p)
b=g.generate('easy',template='linear_y2',parameters={**p,'dx':2,'dy':-1})
assert v.check_normal(a)!=v.check_normal(b)
assert a['question'][':question/id']!=b['question'][':question/id']
for stale in ('solution','key'):
 bad=copy.deepcopy(b)
 if stale=='solution':bad['question'][':question/worked-solution']=a['question'][':question/worked-solution']
 else:
  oldf=a['question'][':question/answer-fields'][0];old=next(z for z in oldf[':answer-field/choices'] if z[':answer/id']==oldf[':answer-field/correct'][1]);newf=bad['question'][':question/answer-fields'][0];next(z for z in newf[':answer-field/choices'] if z[':answer/id']==newf[':answer-field/correct'][1])[':answer/value']=old[':answer/value']
 try:v.check_normal(bad)
 except AssertionError:pass
 else:raise AssertionError('stale '+stale+' accepted')
inputs=json.loads((P/'engine-input.json').read_text())
coverage={}
active={'linear_y2':['a','b'],'chain_square':['a','b'],'supplied_gradient':['a','b'],'xy':['a'],'log':['a'],'quadratic':['a','b','c'],'exp':['a','b'],'x2_linear':['a','b']}
for f,l in g.FAMILIES.items():
 records=[z['record'] for z in inputs if z['label'].startswith('normal-') and z['record']['generation']['template']==f]
 slots=active[f]+([] if f=='supplied_gradient' else ['x0','y0'])+['dx','dy']
 values={key:sorted({str(z['generation']['parameters'][key]) for z in records}) for key in slots}
 fixed={'y0':'0; retains e^0 evaluation'} if f=='exp' else {}
 for key,vals in values.items():assert len(vals)>1 or key in fixed,(f,key,vals)
 coverage[f]={'level':l,'slot_values':values,'intentional_fixed_slots':fixed,'profiles':sorted({z['generation']['profile'] for z in records}),'inactive_slots_excluded_from_task_identity':['c','d'] if f!='quadratic' else ['d']}
report={'passed':True,'coverage':coverage,'changed_direction_same_function_point':{'first':a,'second':b},'stale_solution_detected':True,'stale_key_detected':True,'unsupported_hard_checked_in_main_validation':True}
(P/'slot-validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print('Slot coverage and stale-target checks passed.')
