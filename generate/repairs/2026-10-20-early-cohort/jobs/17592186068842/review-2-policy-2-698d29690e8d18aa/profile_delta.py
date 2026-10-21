import pathlib,json,sys,importlib.util
sys.dont_write_bytecode=True
R=pathlib.Path(__file__).resolve().parent;P=R.parent/'workspace'
s=importlib.util.spec_from_file_location('delta',P/'17592186068842.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def load(n):return json.loads((R/n).read_text())
def save(n,x):(R/n).write_text(json.dumps(x,indent=2,ensure_ascii=False))
rs=[];pairs=[];groups=load('same-bank-groups.json')
for t,b in [('simple_quotient',{}),('exp_quotient',{'base':2,'a':1}),('exp_quotient',{'base':5,'a':5})]:
 z=[m.generate_easy(6020,t,parameters={**b,'n':n}) for n in range(1,5)]
 assert all(r['generation']['bank_profile']=='quotient-power-ladder-exchange' for r in z)
 fs=[r['question'][':question/answer-fields'][0] for r in z];bs=[sorted(c[':answer/value'] for c in f[':answer-field/choices']) for f in fs];ks=[next(c[':answer/value'] for c in f[':answer-field/choices'] if c[':answer/id']==f[':answer-field/correct'][1]) for f in fs]
 assert all(b==bs[0] for b in bs) and len(set(ks))==4
 groups.append({'template':t,'seed':6020,'fixed':b,'powers':[1,2,3,4],'same_visible_bank':True,'keys':ks,'question_ids':[r['question'][':question/id'] for r in z]});rs+=z;pairs+=z[:2]
save('profile-delta-records.json',rs);save('same-bank-groups.json',groups)
for file in ['revision-records.json','independent-records.json','easy-records.json']:save(file,load(file)+rs)
old=load('revision-counterfactual-records.json');save('revision-counterfactual-records.json',old[:-2]+pairs+old[-2:]);save('independent-records.json',load('independent-records.json')+pairs)
save('render-records.json',load('batch.json')+load('revision-counterfactual-records.json'))
print('Added 12 exchange-profile cases and 3 relevant pairs, no author tests rerun.')
