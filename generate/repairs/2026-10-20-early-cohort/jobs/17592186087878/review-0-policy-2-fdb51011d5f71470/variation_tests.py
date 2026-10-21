from audit import *
rs=json.load(open('independent-records.json'));batch=json.load(open('../samples.json'))
stages={'raw':rs,'accepted-easy':json.load(open('delivery-easy/accepted.json')),'accepted-moderate':json.load(open('delivery-moderate/accepted.json')),'accepted-hard':json.load(open('delivery-hard/accepted.json')),'runner-batch':batch,'runner-accepted':json.load(open('delivery-batch/accepted.json'))}
probes=[];coverage={}
for stage,records in stages.items():
 groups={'all':records}
 for r in records:groups.setdefault(r['generation']['template'],[]).append(r)
 coverage[stage]={}
 for template,subset in groups.items():
  coverage[stage][template]={'count':len(subset),'parameter_cases':[r['generation']['parameters'] for r in subset],'if_correct_positions':[],'solution_correct_positions':[],'role_cases':dict(collections.Counter(str(r['generation']['roles']['homogeneous_delta'])+','+str(r['generation']['roles']['coefficient_error']) for r in subset)),'rejection_count':sum(r['generation']['rejections'] for r in subset)}
  for field_key in ['field-1','field-2']:
   fs=[next(f for f in r['question'][':question/answer-fields'] if f[':answer-field/key']==field_key) for r in subset]
   positions=[next(i for i,c in enumerate(f[':answer-field/choices']) if c[':answer/id']==f[':answer-field/correct'][1]) for f in fs]
   coverage[stage][template]['if_correct_positions' if field_key=='field-1' else 'solution_correct_positions']=positions
   for strategy in ['first','shortest','longest']:
    n=0
    for f in fs:
     choices=f[':answer-field/choices'];chosen=choices[0] if strategy=='first' else (min if strategy=='shortest' else max)(choices,key=lambda c:len(c[':answer/value']))
     n+=chosen[':answer/id']==f[':answer-field/correct'][1]
    probes.append({'stage':stage,'template':template,'field':field_key,'cue':strategy+' displayed answer','scope':'overall' if template=='all' else 'within_template','correct':n,'total':len(fs),'baseline':sum(1/len(f[':answer-field/choices']) for f in fs)/len(fs),'positions':positions})
save('shortcut-results.json',probes);save('coverage-results.json',coverage)
print('perfect conditional probes',[(p['stage'],p['template'],p['field'],p['cue'],p['total']) for p in probes if p['correct']==p['total'] and p['total']>2])
print('raw position counts',{t:{k:dict(collections.Counter(v[k])) for k in ['if_correct_positions','solution_correct_positions']} for t,v in coverage['raw'].items()})
