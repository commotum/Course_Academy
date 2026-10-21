import sys,json,copy
from pathlib import Path
sys.dont_write_bytecode=True
import review as v
E=v.E;g=v.module(v.W/'17592186115299.py');results=[];valid=[]
def test(label,p,expected,**kw):
 try:r=g.generate('moderate',seed=82119,parameters=p,**kw);ok=True;valid.append(r);detail=v.check(r)
 except Exception as e:ok=False;detail={'type':type(e).__name__,'message':str(e)}
 results.append({'label':label,'parameters':p,'options':kw,'expected':expected,'observed':'accept' if ok else 'reject','passed':ok==(expected=='accept'),'detail':detail})
for n in g.TEMPLATES:
 dim=v.system(g.generate('moderate',82119,template=n)['question'][':question/problem']).cols-1
 test('affine signed boundary '+n,{'scales':[-2]*dim,'translations':[2]*dim},'accept',template=n)
base={'matrix':[[1,1,0],[-2,98,100]],'order':['dependent','independent','inconsistent']}
test('coefficient bound100',base,'accept',template='q-74638')
test('denominator bound6',{'matrix':[['1','1/6',0],[-2,'-1/3','1/6']],'order':base['order']},'accept',template='q-74638')
for label,p in [('coefficient101',dict(base,matrix=[[1,1,0],[-2,98,101]])),('denominator7',dict(base,matrix=[[1,'1/7',0],[-2,'-2/7','1/7']])),('missing y',dict(base,matrix=[[1,0,0],[-2,0,1]])),('non echelon',dict(base,matrix=[[1,1,0],[1,2,1]])),('duplicate order',dict(base,order=['dependent']*3)),('scale3',{'scales':[3,1],'translations':[0,0]}),('translation3',{'scales':[1,1],'translations':[3,0]})]:
 test(label,p,'reject',template='q-74638')
for label,kw in [('field drift',{'field_type':'free'}),('invalid bank',{'profile':'absent'}),('invalid template',{'template':'absent'})]:
 test(label,base,'reject',**({'template':'q-74638'}|kw))
# Force one rejected construction through the real sampler retry loop; then use real RNG.
orig=g.sample;calls=[]
def injected(level,name,rng):
 if not calls:p={'matrix':[[1,1,0],[1,2,1]],'order':base['order']}
 else:p=orig(level,name,rng)
 calls.append(p);return p
g.sample=injected
r=g.generate('moderate',seed=82119,template='q-74638');g.sample=orig
v.save('boundary-records.json',valid+[r]);v.save('boundary-report.json',{'tests':results,'failures':[r for r in results if not r['passed']],'forced_retry':{'first_rejected':calls[0],'calls':len(calls),'result':v.check(r)},'scope':'Affirmative extreme affine source cases plus explicit current sampler parameter guards. Forced rejection is a test injection, not observed normal-sampler failure.'})
print('tests',len(results),'failures',[r['label'] for r in results if not r['passed']],'retry calls',len(calls),'math errors',[v.check(r) for r in valid if v.check(r)['errors']])
