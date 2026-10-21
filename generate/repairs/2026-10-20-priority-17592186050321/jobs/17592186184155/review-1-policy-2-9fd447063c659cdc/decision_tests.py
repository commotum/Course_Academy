from audit import *
records=json.loads((E/'sampled.json').read_text());batch=json.loads((E/'runner-batch.json').read_text())
# Search for a generated sign-reversal pair with an unchanged mathematical bank.
pair=None
for r in records:
 m=r['generation'];_,_,key=qparts(r)
 for i,row in enumerate(m['candidate_states']):
  js=[j for j,v in enumerate(row) if v]
  if len(js)!=1:continue
  j=js[0];k=row[j]
  if m['error_recipes'][j][k-1]!='reverse_sign':continue
  terms=[list(t) for t in m['parameters']];terms[j][0]=str(-F(terms[j][0]))
  newstates=[]
  for ix,rr in enumerate(m['candidate_states']):
   if ix==i:continue
   ss=list(rr);ss[j]=k if rr[j]==0 else 0;newstates.append(ss)
  rr=g.generate(m['seed'],parameters=terms,design={'profile':m['template'],'order':m['order'],'states':newstates})
  if {tuple(sorted(a.items())) for a in visible(r)[1]}=={tuple(sorted(a.items())) for a in visible(rr)[1]}:pair=(r,rr,j);break
 if pair:break
assert pair
before,after,role=pair
m=before['generation'];irrelevant=g.generate(m['seed'],parameters=m['parameters'],design={'profile':m['template'],'order':list(reversed(m['order'])),'states':m['design_states']})
# Parameter dependencies, within declared bounds, in every role.
parameter_pairs=[]
for j in range(3):
 t=[list(x) for x in m['parameters']];t[j][0]=str(-F(t[j][0]));parameter_pairs.append((f'coefficient-role-{j}',before,g.generate(m['seed'],parameters=t,design={'profile':m['template'],'order':m['order'],'states':m['design_states']})))
 t=[list(x) for x in m['parameters']]
 if j==0:t[j][1]='-4/3' if m['template']=='negative_fractional' and F(t[j][1])!=F(-4,3) else '-6/5' if m['template']=='negative_fractional' else '1/3' if F(t[j][1])!=F(1,3) else '2/3'
 else:t[j][1]=str(F(t[j][1])+1 if j==1 and F(t[j][1])<7 or j==2 and F(t[j][1])<-2 else F(t[j][1])-1)
 parameter_pairs.append((f'exponent-role-{j}',before,g.generate(m['seed'],parameters=t,design={'profile':m['template'],'order':m['order'],'states':m['design_states']})))
cf=[before,after,irrelevant]+[r for _,_,r in parameter_pairs];save('counterfactual-records.json',cf)
cfresults=[]
for name,a,b in [('fixed-bank-sign-rekey',before,after),('irrelevant-term-order',before,irrelevant)]+parameter_pairs:
 ia,ba,ka=visible(a);ib,bb,kb=visible(b)
 assert (ba[ka]==bb[kb])==(name=='irrelevant-term-order')
 assert (ia==ib)==(name=='irrelevant-term-order')
 check(a);check(b)
 cfresults.append({'case':name,'before_record':0,'after_record':cf.index(b),'integrand_preserved':ia==ib,'answer_preserved':ba[ka]==bb[kb],'bank_preserved':{tuple(sorted(x.items())) for x in ba}=={tuple(sorted(x.items())) for x in bb},'prompt_changed':a['question'][':question/problem']!=b['question'][':question/problem'],'solution_changed':a['question'][':question/worked-solution']!=b['question'][':question/worked-solution']})
save('counterfactual-results.json',{'command':f'{PY} decision_tests.py','cases':cfresults,'role_rekeyed':role})
# Native grader: test all five options for every source, boundary, counterfactual, batch,
# plus distinct mathematical/profile sampled cases. Expectations independently derived.
rs=json.loads((E/'source-replays.json').read_text())+json.loads((E/'boundaries.json').read_text())+cf+batch+records[:24]
cases=[]
for i,r in enumerate(rs):
 integ,bank,k=visible(r);q,cs,_=qparts(r)
 cases.append({'label':f'visible-math-{i}','record':r,'checks':[{'field_index':0,'submitted_answer_id':c[':answer/id'],'expected':'accepted' if derivative(bank[j])==integ else 'rejected','purpose':'Independently differentiate the visible option; includes old-correct now-wrong in unchanged bank.'} for j,c in enumerate(cs)]})
save('grader-input.json',cases)
# Fixed option bank: locate previous correct mathematical value in the changed bank.
old=visible(before)[1][visible(before)[2]];newbank=visible(after)[1];oldidx=newbank.index(old);assert oldidx!=visible(after)[2]
# Probe visible cue strategies with stable first-match tie breaking.
def probes(rs,label):
 out=[]
 groups={'overall':rs}
 for r in rs:
  m=r['generation']; groups.setdefault('template:'+m['template'],[]).append(r)
  groups.setdefault('profile-order:'+m['template']+':'+str(m['order']),[]).append(r)
  groups.setdefault('profile-degree:'+m['template']+':'+str(F(m['parameters'][0][1]).denominator),[]).append(r)
 for subgroup,xs in groups.items():
  strategies=collections.defaultdict(lambda:[0,0])
  for r in xs:
   p,bank,key=visible(r);q,cs,_=qparts(r)
   # Position/length/sign cues use no integration. Agreement uses only candidate matching.
   scores=[]
   for a in bank:scores.append(sum(sum(a.get(p)==b.get(p) for p in set(a)|set(b)) for b in bank))
   choices={'choose-first':0,'choose-last':4,'shortest-TeX':min(range(5),key=lambda i:len(cs[i][':answer/value'])),'longest-TeX':max(range(5),key=lambda i:len(cs[i][':answer/value'])),'maximum-pairwise-agreement':max(range(5),key=lambda i:scores[i]),'minimum-pairwise-agreement':min(range(5),key=lambda i:scores[i]),'fewest-minus-signs':min(range(5),key=lambda i:cs[i][':answer/value'].count('-')),'most-minus-signs':max(range(5),key=lambda i:cs[i][':answer/value'].count('-'))}
   for name,pred in choices.items():strategies[name][0]+=pred==key;strategies[name][1]+=1
  for name,(correct,total) in strategies.items():out.append({'stage':label,'subgroup':subgroup,'strategy':name,'correct':correct,'total':total,'baseline':0.2,'rate':correct/total})
 return out
survived=json.loads((E/'delivery-sampled/accepted.json').read_text());delbatch=json.loads((E/'delivery-batch/accepted.json').read_text())
pr=probes(records,'raw')+probes(survived,'accepted')+probes(batch,'runner-raw')+probes(delbatch,'runner-accepted')
save('shortcut-results.json',{'command':f'{PY} decision_tests.py','tie_break':'First displayed candidate; no random tie resolution','baseline':'Uniform independent guess among five options (0.2). Small runner and fine subgroups have limited power.','results':pr})
coverage={}
for label,rs in [('raw',records),('accepted',survived),('runner-raw',batch),('runner-accepted',delbatch)]:
 c={}
 for r in rs:
  m=r['generation'];f=qparts(r)[2]
  for k,v in [('profile',m['template']),('order',str(m['order'])),('correct_position',f),('root_degree',F(m['parameters'][0][1]).denominator),('fractional_exponent',m['parameters'][0][1]),('integer_exponent',m['parameters'][1][1]),('reciprocal_exponent',m['parameters'][2][1])]:c.setdefault(k,collections.Counter())[str(v)]+=1
  for j,(a,p) in enumerate(m['parameters']):c.setdefault('coefficient-role-'+str(j),collections.Counter())[a]+=1
  for j in range(3):
   for state in set(row[j] for row in m['candidate_states'])-{0}:c.setdefault('actual-error-recipe-role-'+str(j),collections.Counter())[m['error_recipes'][j][state-1]]+=1
 c['assignment_attempts']={'minimum':min(r['generation']['assignment_attempts'] for r in rs),'maximum':max(r['generation']['assignment_attempts'] for r in rs)}
 coverage[label]=c
save('coverage.json',coverage)
print(json.dumps({'counterfactual_cases':len(cfresults),'grader_records':len(cases),'grader_checks':sum(len(c['checks']) for c in cases),'fixed_bank_old_correct_index':oldidx,'source_seed':m.get('seed'),'overall_probes':[x for x in pr if x['subgroup']=='overall'],'perfect_subgroups':[x for x in pr if x['correct']==x['total']]}))
(E/'session-state.md').write_text('Source analysis complete before author inspection. Independent audit.py checked 255 visible prompts, complete banks and all worked equalities, no failures. decision_tests.py saved 8 controlled pairs, 48 grader records, coverage and shortcut probes. Shared delivery accepted all 240 fresh plus 5 runner records at captured inventory basis 5277. Native grading, rendering, packaging and selection checks remain. Package untouched.\n')
