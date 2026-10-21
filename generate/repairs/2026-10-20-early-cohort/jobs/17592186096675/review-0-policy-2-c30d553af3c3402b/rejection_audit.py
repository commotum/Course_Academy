import audit as a
import json
seen={};attempts=[];collision=None
for seed in range(310917,311417):
 r=a.g.generate(seed=seed);p=r['generation']['parameters'];key=(r['generation']['template'],tuple(p['solution']))
 attempts.append(r)
 if key in seen:
  collision=(seen[key],len(attempts)-1);break
 seen[key]=len(attempts)-1
if collision is None:
 a.save('rejection-results.json',{'seeds':[310917,311416],'collision_observed':False,'limitation':'No duplicate occurred in bounded 500-attempt search.'})
else:
 i,j=collision;seed=attempts[i]['generation']['seed'];count=j-i+1
 actual=a.g.batch(seed=seed,count=count);raw=attempts[i:j+1]
 a.save('rejection-records.json',raw+actual)
 a.save('rejection-results.json',{'collision_observed':True,'duplicate_seeds':[attempts[i]['generation']['seed'],attempts[j]['generation']['seed']],'command':f'generator.batch(seed={seed},count={count})','raw_attempt_count_to_collision':count,'raw_unique_systems':len({(r['generation']['template'],tuple(r['generation']['parameters']['solution'])) for r in raw}),'actual_accepted':len(actual),'actual_unique_systems':len({(r['generation']['template'],tuple(r['generation']['parameters']['solution'])) for r in actual}),'resampling_used_next_seed':actual[-1]['generation']['seed']>attempts[j]['generation']['seed'],'duplicate_equations_equal':attempts[i]['question'][':question/problem']==attempts[j]['question'][':question/problem'],'records_layout':{'raw':[0,len(raw)],'accepted':[len(raw),len(raw)+len(actual)]},'rule':'Bounded augmented-system duplicate rejection is used rather than changing mathematical roles. This branch test is separate from the actual runner batch.'})
print(json.dumps(json.load(open(a.E/'rejection-results.json'))))
