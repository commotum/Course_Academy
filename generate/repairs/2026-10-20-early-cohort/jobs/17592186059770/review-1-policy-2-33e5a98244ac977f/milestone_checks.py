import sys
sys.dont_write_bytecode=True
from audit import *
g=module(W/'17592186059770.py')
records=[];checks=[]
# All supported moderate target roles, with latent bank fixed and actual equation evidence changed.
for t,p in g.SOURCE_PARAMETERS.items():
 names=['correct','keep_rhs_sign','appearance_order_and_keep_rhs_sign'] if t=='coefficient' else ['correct','reverse_second_constant']
 family=[g.generate('moderate',8271,t,parameters=p,target_recipe=name) for name in names]
 bank=lambda r:sorted(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])
 assert all(bank(r)==bank(family[0]) for r in family)
 assert len({r['question'][':question/problem'] for r in family})==len(family)
 for r in family:qcheck(r)
 checks.append({'template':t,'targets':names,'bank_preserved':True,'prompts_keys_solutions_recomputed':True});records+=family
# Test six entry dependencies one at a time with explicit easy source-style target.
p=dict(zip('abcdef',[2,3,5,7,8,9]));base=g.generate('easy',8271,parameters=p,profile='q-71733');records.append(base)
for slot in p:
 pp={**p,slot:-p[slot]};r=g.generate('easy',8271,parameters=pp,profile='q-71733');qcheck(r)
 a=visible(base['question']);b=visible(r['question']);assert sum(x!=y for row1,row2 in zip(a,b) for x,y in zip(row1,row2))==1
 checks.append({'slot':slot,'one_visible_entry_changed':True});records.append(r)
# The organized intermediate equation system must agree entrywise too.
for r in load(E/'moderate.json')+records[:5]:
 solution=r['question'][':question/worked-solution'];body=re.search(r'\\begin\{aligned\}.*?\\end\{aligned\}',solution,re.S)[0]
 fake={':question/problem':r['question'][':question/problem'].split('\n')[0]+'\n'+body};assert visible(fake)==visible(r['question'])
# Observe a duplicate-bank rejection followed by successful resampling.
orig=g.easy_banks;calls=[]
def watched(*args,**kwargs):calls.append(1);return orig(*args,**kwargs)
g.easy_banks=watched
witness=None
for seed in range(2000):
 calls.clear();r=g.generate('easy',seed,profile='q-71733')
 if len(calls)>3:witness={'seed':seed,'calls':len(calls),'profile':'q-71733','final':qcheck(r)};records.append(r);break
assert witness
try:g.generate('easy',1,profile='q-71733',parameters=dict(zip('abcdef',[1]*6)))
except ValueError as ex:checks.append({'duplicate_parameter_rejection':str(ex)})
else:raise AssertionError('duplicate bank accepted')
save('extra-controlled.json',records);save('construction.json',{'checks':checks,'resampling':witness})
# One native invocation for all extra cases, both valid and plausible wrong selections.
native=[]
for n,r in enumerate(records):
 f=r['question'][':question/answer-fields'][0];expected=visible(r['question']);native.append({'label':f'extra-controlled-{n}','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if mat(a[':answer/value'])==expected else 'rejected','purpose':'independent exact matrix under controlled entry/target change'} for a in f[':answer-field/choices']]})
save('extra-native-input.json',native);run=command([R/'generate/runs/current/check-engine',E/'extra-native-input.json',E/'extra-native-report.json']);save('extra-native-run.json',run);assert run['exit']==0
save('extra-render-records.json',records[:5]);print(json.dumps({'records':len(records),'resampling':witness,'native_exit':run['exit']},default=str))
