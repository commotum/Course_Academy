from audit import *
roles={'if_rank':0,'homogeneous_delta':1,'coefficient_error':1,'factor_candidates':['-3','-2','2','3']}
pairs=[g.generate('easy',83017,template='exp_forcing',parameters=p,roles=roles) for p in [{'a':3,'b':6,'r':2},{'a':-3,'b':6,'r':2},{'a':3,'b':8,'r':2}]]
pairs.append(g.generate('easy',83018,template='exp_forcing',parameters={'a':3,'b':6,'r':2},roles=roles))
# Canonical cosine example, repaired duplicate-bank replay, and boundary samples.
extra=[g.generate('hard',83019,template='power_cos',parameters={'n':3,'r':1}),g.generate('hard',83020,profile='q-335409-repaired',parameters={'n':2,'r':1})]
for t,spec in g.TEMPLATES.items():
 keys=spec['base'];f=spec['family']
 pars=({'a':-6,'b':2,'r':5} if f=='exp' else {'a':6,'m':2} if f=='cancel' else {'n':6,'b':9} if f in ('power','powerlegacy') else {'k':6,'b':6} if f=='normalize' else {'n':6,'r':3})
 extra.append(g.generate(spec['level'],83021,template=t,parameters=pars))
save('counterfactual-records.json',pairs);save('boundary-records.json',extra)
checks=[mathcheck(r) for r in pairs+extra];save('boundary-math.json',checks)
def correct(r,key):
 f=next(f for f in r['question'][':question/answer-fields'] if f[':answer-field/key']==key)
 return parse(next(c[':answer/value'] for c in f[':answer-field/choices'] if c[':answer/id']==f[':answer-field/correct'][1]))
relationships=[{'kind':'relevant','before':0,'after':1,'I_changed':s.simplify(correct(pairs[0],'field-1')-correct(pairs[1],'field-1'))!=0,'Y_changed':s.simplify(correct(pairs[0],'field-2')-correct(pairs[1],'field-2'))!=0},{'kind':'irrelevant_to_IF','before':0,'after':2,'I_preserved':s.simplify(correct(pairs[0],'field-1')-correct(pairs[2],'field-1'))==0,'Y_changed':s.simplify(correct(pairs[0],'field-2')-correct(pairs[2],'field-2'))!=0},{'kind':'irrelevant_presentation','before':0,'after':3,'I_preserved':s.simplify(correct(pairs[0],'field-1')-correct(pairs[3],'field-1'))==0,'Y_preserved':s.simplify(correct(pairs[0],'field-2')-correct(pairs[3],'field-2'))==0}]
save('counterfactual-results.json',relationships)
rs=json.load(open('independent-records.json'))+pairs+extra+json.load(open('../samples.json'))
# Full banks and all IDs, testing independently determined ODE residuals.
cases=[]
for r in rs:
 q=r['question'];P,Q=equation(q);cs=[]
 for i,f in enumerate(q[':question/answer-fields']):
  for c in f[':answer-field/choices']:
   v=parse(c[':answer/value']);good=s.simplify(s.diff(v,x)-P*v if f[':answer-field/key']=='field-1' else s.diff(v,x)+P*v-Q)==0
   cs.append({'field_index':i,'submitted_answer_id':c[':answer/id'],'expected':'accepted' if good else 'rejected','purpose':'Independent differential-identity check for displayed choice'})
 cases.append({'label':str(r['generation']['seed'])+'/'+r['generation']['template']+'/'+str(r['generation']['parameters']),'record':r,'checks':cs})
save('grader-input.json',cases)
# Render every family, runner batch and all controlled pairs.
first={}
for r in json.load(open('independent-records.json')):first.setdefault(r['generation']['template'],r)
save('render-records.json',list(first.values())+pairs+json.load(open('../samples.json')))
print('controlled pairs',relationships,'boundary math failures',[c for c in checks if not c['passed']],'grader records',len(cases))
