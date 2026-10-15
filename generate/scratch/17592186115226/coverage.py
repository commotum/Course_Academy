"""Exhaustive eligible target positions with supplied matrices held constant."""
import copy,json,subprocess
import validate as v
g=v.g;records=[];report={}
for profile,q in g.SOURCES.items():
 level=q.get(':question/difficulty',{}).get(':db/ident','').split('/')[-1]
 if level not in g.SUPPORTED_LEVELS or len(q[':question/answer-fields'])==1 or profile=='q-138783':continue
 M=g.source_data(profile);R=v.result(q);original=g.targets(q,R);coverage={};negative=0
 for key,pos in original.items():
  eligible=[(i,j) for i in range(3) for j in range(3) if g.category(R[i,j])==g.category(R[tuple(pos)])]
  checked=[]
  for target in eligible:
   assigned={key:list(target)};taken={target}
   for other,old in original.items():
    if other==key:continue
    choices=[(i,j) for i in range(3) for j in range(3) if (i,j) not in taken and g.category(R[i,j])==g.category(R[tuple(old)])]
    p=tuple(old) if tuple(old) in choices else choices[0];assigned[other]=list(p);taken.add(p)
   params={'matrices':[[[str(v) for v in row] for row in a.tolist()] for a in M],'targets':assigned}
   rec=g.generate(level,0,bank_profile=profile,parameters=params);v.independent(rec);records.append(rec);checked.append(target)
   if R[target]!=R[tuple(pos)]:
    bad=copy.deepcopy(rec);f=next(f for f in bad['question'][':question/answer-fields'] if f[':answer-field/key']==key)
    f[':answer-field/choices'][0][':answer/value']=g.s.latex(R[tuple(pos)])
    try:v.solution_check(bad['question'])
    except AssertionError:negative+=1
    else:raise AssertionError('Stale key passed')
  assert set(checked)==set(eligible)
  coverage[key]={'eligible':eligible,'checked':checked,'uncovered':[]}
 report[profile]={'fields':coverage,'stale_key_negative_controls':negative}
v.save('target-domain-grading-input.json',[{'label':str(i),'record':r,'checks':v.checks(r)} for i,r in enumerate(records)])
subprocess.run([str(v.ROOT/'generate/runs/current/check-engine'),str(v.HERE/'target-domain-grading-input.json'),str(v.HERE/'target-domain-grading-report.json')],check=True)
v.save('target-domain-coverage.json',report)
p=v.HERE/'validation.json';x=json.loads(p.read_text());x['complete_target_domain_validation']={'records':len(records),'report':'target-domain-coverage.json','actual_grading':'target-domain-grading-report.json','all_eligible_positions_checked':True};x['hashes']['generate/scratch/17592186115226/coverage.py']=v.sha(v.HERE/'coverage.py');v.save('validation.json',x)
print('All eligible blank positions checked:',len(records))
