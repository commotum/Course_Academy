import json,pathlib,collections,hashlib,sys,re
sys.dont_write_bytecode=True
from bank_shortcut import choose,power_sign_shortest
R=pathlib.Path(__file__).resolve().parent;J=R.parent
load=lambda p:json.load(open(p))
def save(n,v):(R/n).write_text(json.dumps(v,indent=2,ensure_ascii=False))
D=r'\frac{\text{d}y}{\text{d}x}'
def key(f):
 k=f[':answer-field/correct'];return k[':answer/id'] if isinstance(k,dict) else k[1]
def attacks(r):
 q=r.get('question',r);f=q[':question/answer-fields'][0];cs=f[':answer-field/choices'];vs=[c[':answer/value'].replace(D,'D') for c in cs]
 unique=lambda scores: scores.index(max(scores)) if scores.count(max(scores))==1 else None
 roots=collections.Counter(z for v in vs for z in re.findall(r'\\sqrt\{[1-5]\+\{y\}\^\{[24]\}\}',v))
 mode=roots.most_common(1)[0][0] if roots else None
 ri=[i for i,v in enumerate(vs) if mode and v.startswith('\\frac{1}{'+mode+'}\\cdot D=')]
 return {'first':0,'last':4,'shortest':unique([-len(v) for v in vs]),'longest':unique([len(v) for v in vs]),'unique_fractionless':unique([int('\\frac' not in v) for v in vs]) if sum('\\frac' not in v for v in vs)==1 else None,'modal_component':choose(cs),'three_lhs_shortest':power_sign_shortest(cs),'modal_root':ri[0] if len(ri)==1 else None}
def inspect(rs,pool):
 rows=[]
 for r in rs:
  q=r.get('question',r);f=q[':question/answer-fields'][0]
  rows.append({'pool':pool,'id':q[':question/id'],'template':r.get('generation',{}).get('template','inventory'),'profile':r.get('generation',{}).get('bank_profile','unknown'),'parameters':r.get('generation',{}).get('parameters'),'probes':{a:{'chosen':i,'success':i is not None and f[':answer-field/choices'][i][':answer/id']==key(f)} for a,i in attacks(r).items()}})
 return rows
def summary(rs):
 rows=inspect(rs,'summary');return {'count':len(rs),'templates':dict(collections.Counter(x['template'] for x in rows)),'profiles':dict(collections.Counter(x['profile'] for x in rows)),'powers':dict(collections.Counter(str(x['parameters'].get('n')) for x in rows)),'attack_hits':{a:sum(x['probes'][a]['success'] for x in rows) for a in rows[0]['probes']} if rows else {}}
pools={n:load(R/f) for n,f in [('control_before','easy-records.json'),('control_after','delivery-control/accepted.json'),('batch_before','batch.json'),('batch_after','delivery-batch/accepted.json')]}
rows=sum([inspect(rs,pool) for pool,rs in pools.items()],[]);save('stage-shortcut-results.json',rows)
i=load(J/'source/inventory.json');qs=i['questions'];save('inventory-tested-questions.json',qs)
inv=inspect(qs,'inventory');generated=[q for q in qs if ':question/math-academy-id' not in q]
save('inventory-probe.json',{'basis':i['basis'],'question_count':len(qs),'generated_count':len(generated),'rows':inv,'generated_prompts':[{'question_id':q[':question/id'],'entity_id':q[':db/id'],'prompt':q[':question/problem']} for q in generated],'conclusion':'All 16 captured complete banks examined. Six generated questions are exponent-sum or double-factor; none uses the repaired quotient or radical construction. No generated instance of retained family-specific defects is present. Chance attack successes outside these families are not attributed to the findings. Original source entries are not generated records.','limitations':['Generation metadata absent in captured inventory. No new affected generated instance demonstrated. Captured basis only; future inventory can change.']})
save('affected-inventory.json',{'affected_questions':[]})
def draw(pool,seed):
 pool=sorted(set(pool));d=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(d[8:16],'big')>>11)/(1<<53);return pool[int(u*len(pool))] if pool else None
existing=[q[':db/id'] for q in qs if q[':question/difficulty'][':db/ident']==':question.difficulty/easy'];first=max(q[':db/id'] for q in qs)+1
ba=pools['batch_after'];new={first+k:r['question'][':question/id'] for k,r in enumerate(ba)};pool=existing+list(new)
draws=collections.Counter(draw(pool,'review2-'+str(k)) for k in range(256))
selected=[{'entity_id':k,'question_id':v,'draws':draws[k]} for k,v in new.items()]
save('delivery-selection.json',{'stages':{k:summary(v) for k,v in pools.items()},'rejection_resampling':'No retry loop. Uniform eligible template, then uniform two-profile choice for quotients, independent bounded integer parameters; radical n independently 2 or 4. All sampled requests and valid boundaries returned. Invalid explicit inputs reject. Validation can raise but no valid tested branch was removed.','source':'question_selection.rs 109–202 inspected directly. Previous-task history and caller prefix exclusion; sorted/deduplicated eligible IDs; weighted rated band; uniform within positive-weight band. Unconfigured fallback chooses lowest ID. Unknown ratings used only absent positive rated pools.','captured_basis':i['basis'],'conditional_easy_simulation':{'existing_ids':existing,'future_surrogate_map':new,'draws':selected,'every_batch_member_selected':all(draws[k]>0 for k in new),'history_examples':[{'remaining':[k],'selected':draw([k],'review2-isolated')} for k in new]},'limitations':['No publication preparation exists. Actual shared publisher preparation reproduced read-only against captured inventory.','No live learner history, future entity IDs or weights supplied. Future IDs are surrogates; simulation conditions on positive easy weight. Zero easy weight excludes all easy records.','Selection never rewrites answer banks; history can remove any case. No guarantee of balance in a short personalized task.']})
print('Delivery coverage',json.dumps({k:summary(v) for k,v in pools.items()}));print('inventory generated',len(generated),'all batch members selectable',all(draws[k]>0 for k in new))
