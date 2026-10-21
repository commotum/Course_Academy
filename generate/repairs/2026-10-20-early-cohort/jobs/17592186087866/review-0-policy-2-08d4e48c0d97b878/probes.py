import audit as a
from collections import Counter,defaultdict
E=a.E

def probe(r):
 f=r['question'][':question/answer-fields'][0];choices=f[':answer-field/choices'];parts=[c[':answer/value'].split('=',1) for c in choices];lc=Counter(p[0] for p in parts);rc=Counter(p[1] for p in parts)
 scores=[lc[l]+rc[r] for l,r in parts];top=max(scores);ix=[i for i,v in enumerate(scores) if v==top];chosen=choices[ix[0]] if len(ix)==1 else None
 return {'question_id':r['question'][':question/id'],'template':r['generation']['template'],'parameters':r['generation']['parameters'],'scores':scores,'unique_maximum':len(ix)==1,'correct':bool(chosen and chosen[':answer/id']==f[':answer-field/correct'][1]),'chosen_id':chosen[':answer/id'] if chosen else None,'keyed_id':f[':answer-field/correct'][1]}
sets={'independent':a.json.loads((E/'independent-easy.json').read_text()),'delivered':a.json.loads((E/'delivery-independent/accepted.json').read_text()),'runner':a.json.loads((E/'runner-batch.json').read_text()),'runner_delivered':a.json.loads((E/'delivery-batch/accepted.json').read_text())}
result={};summaries={}
for name,rs in sets.items():
 result[name]=[probe(r) for r in rs];groups=defaultdict(list)
 for v in result[name]:groups[v['template']].append(v)
 summaries[name]={t:{'correct':sum(v['correct'] for v in vs),'total':len(vs),'unique_max':sum(v['unique_maximum'] for v in vs)} for t,vs in groups.items()}
a.save('shortcut-results.json',{'command':str(a.PY)+' '+str(E/'probes.py'),'strategy':'Split each option at =; score it by number of identical left sides plus number of identical right sides. Select a unique maximum. Uses no prompt, coefficient parsing, or algebra. Abstention counts as failure.','baseline':0.2,'records':result,'summaries':summaries})
# Read-only faithful reproduction of selection's within-band hash draw.
import hashlib,math
rs=sets['delivered'];byid={r['question'][':question/id']:r for r in rs};ordered=sorted(byid);draws=[]
for i in range(500):
 seed='review-fresh-easy-'+str(i);digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53);qid=ordered[int(u*len(ordered))];r=byid[qid];draws.append({'seed':seed,'question_id':qid,'template':r['generation']['template'],'shortcut_success':probe(r)['correct']})
a.save('selection-results.json',{'basis':5230,'source':'engine/rust/question_selection.rs select(): sorted unique candidates; positive easy band, within-band uniform SHA256 draw offset 8','candidate_order':'stable UUID lexical order assigned increasing synthetic entity IDs; counts for actual assigned database IDs are conditional, since publication has not occurred','history':'fresh learner, no excluded questions; excluding previously seen questions removes candidates without changing their option-bank defect','weights':'conditional on selecting easy with positive weight; no configured live policy/learner history supplied','draws':draws,'template_counts':dict(Counter(v['template'] for v in draws)),'shortcut_success':sum(v['shortcut_success'] for v in draws),'total':len(draws)})
print(a.json.dumps(summaries,indent=2));print('selection shortcut',sum(v['shortcut_success'] for v in draws),len(draws))
