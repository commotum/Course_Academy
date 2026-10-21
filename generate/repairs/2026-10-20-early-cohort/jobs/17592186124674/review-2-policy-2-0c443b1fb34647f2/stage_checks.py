from review_utils import *
from html.parser import HTMLParser
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.radios=[]
 def handle_starttag(self,t,attrs):
  d=dict(attrs)
  if t=='input' and d.get('type')=='radio':self.radios.append(d['value'])
def display_order(r,index,group):
 parser=Parser();parser.feed((E/group/f'question-{index+1:03}.html').read_text());assert len(parser.radios)==5
 return [next(c for c in opts(r) if c[':answer/id']==cid) for cid in parser.radios]
def row(r,options=None):
 xs=options or opts(r);prompt=q(r)[':question/problem'];symbol=re.search(r'\$([A-Z])\(t\)\$',prompt)[1];X=sp.Symbol(symbol);k=sp.Symbol('k');cap=int(re.search(r'maximum.+?is \$(\d+)\$',prompt)[1]);es=[rhs(c[':answer/value']) for c in xs]
 pos=next(i for i,c in enumerate(xs) if c[':answer/id']==key(r));lens=[len(clean(c[':answer/value'])) for c in xs];lin=[i for i,e in enumerate(es) if sp.degree(e,X)==1 and e.coeff(X)==-k and e.subs(X,0)/k>0];kind='mixed' if len(lin)==2 else 'capacities';caps={i:int(es[i].subs(X,0)/k) for i in lin};nums=[set(map(int,re.findall(r'\d+',c[':answer/value']))) for c in xs];matching=[i for i,n in enumerate(nums) if cap in n];shortmatch=[i for i in matching if lens[i]==min(lens[j] for j in matching)];freq={n:sum(n in ns for ns in nums) for n in caps.values()};most={n for n,v in freq.items() if v==max(freq.values())};least={n for n,v in freq.items() if v==min(freq.values())}
 scores={f'position_{i}':pos==i for i in range(5)}
 scores.update(unique_shortest=lens.count(min(lens))==1 and lens[pos]==min(lens),shortest_first=pos==lens.index(min(lens)),longest_first=pos==lens.index(max(lens)),numeral_unique=len(matching)==1 and matching[0]==pos,numeral_shortest_unique=len(shortmatch)==1 and shortmatch[0]==pos,numeral_shortest_first=shortmatch[0]==pos,most_frequent_first=next(i for i,ns in enumerate(nums) if ns&most)==pos,least_frequent_first=next(i for i,ns in enumerate(nums) if ns&least)==pos,min_positive_linear=pos==min(lin,key=caps.get),max_positive_linear=pos==max(lin,key=caps.get))
 extra='none';extra_cap=None
 if kind=='mixed':
  rem=[e for e in es if not any(sp.expand(e-sign*k*(n-X))==0 for n in caps.values() for sign in (-1,1))];assert len(rem)==1;z=rem[0];deg=sp.degree(z,X);extra={1:'negative_sum',2:'population_factor',3:'quadratic_factor'}[deg];extra_cap=int(-z.subs(X,0)/k if deg==1 else z.coeff(X,deg-1)/k)
  scores['extra_capacity_linear']=caps[pos]==extra_cap;scores['other_capacity_linear']=caps[pos]!=extra_cap
 return {'id':q(r)[':question/id'],'seed':r['generation']['seed'],'parameters':r['generation']['parameters'],'template':r['generation']['template'],'kind':kind,'operation':extra,'extra_capacity':extra_cap,'capacity':cap,'position':pos,'rank':sorted(caps.values()).index(cap),'lengths':lens,'matching_count':len(matching),'shortest_matching_count':len(shortmatch),'scores':scores}
sets={'fresh':load(E/'fresh-records.json'),'batch':load(E/'runner-batch.json'),'delivered_fresh':load(E/'delivery-fresh/accepted.json'),'delivered_batch':load(E/'delivery-batch/accepted.json'),'controlled':load(E/'author-check-rerun/regression-records.json')[3:71]}
refs={'fresh':'fresh-records.json','batch':'runner-batch.json','delivered_fresh':'delivery-fresh/accepted.json','delivered_batch':'delivery-batch/accepted.json','controlled':'author-check-rerun/regression-records.json'}
results={}; probes=[]
for stage,rs in sets.items():
 rows=[row(r,display_order(r,i,'render-delivered') if stage=='delivered_batch' else None) for i,r in enumerate(rs)];groups=[('all','overall',rows)]
 for kind in sorted({r['kind'] for r in rows}):groups.append((kind,'other_recognizable_subgroup',[r for r in rows if r['kind']==kind]))
 for template in sorted({r['template'] for r in rows}):groups.append((template,'within_template',[r for r in rows if r['template']==template]))
 for op in sorted({r['operation'] for r in rows if r['operation']!='none'}):groups.append(('extra '+op,'other_recognizable_subgroup',[r for r in rows if r['operation']==op]))
 summaries=[]
 for name,scope,xs in groups:
  scores={s:sum(r['scores'].get(s,False) for r in xs) for s in xs[0]['scores'] if all(s in r['scores'] for r in xs)}
  summaries.append({'subgroup':name,'scope':scope,'n':len(xs),'positions':dict(collections.Counter(r['position'] for r in xs)),'ranks':dict(collections.Counter(r['rank'] for r in xs)),'successes':scores})
  for strategy,correct in scores.items():
   baseline=.5 if strategy.endswith('_linear') and all(r['kind']=='mixed' for r in xs) else .2
   intended=all(r['kind']=='capacities' for r in xs) and strategy in ['numeral_unique','numeral_shortest_unique','numeral_shortest_first']
   conclusion='Baseline is uniform choice among '+('two positive linear models (after mathematical form recognition).' if baseline==.5 else 'five displayed equations.')
   conclusion+=' Capacity matching in the all-capacity source family is the intended equilibrium-identification skill.' if intended else ' No fixed cue is established: controlled full-bank reassignment supplies both target roles in each mixed template and all five roles in each capacity template. Small conditional samples can coincide; they do not override the paired witnesses.'
   if stage=='delivered_batch':conclusion+=' Positions and tie-breaking use actual unmodified UI HTML order.'
   probes.append({'cue':strategy,'subgroup':stage+': '+name,'scope':scope,'strategy':strategy.replace('_',' '),'correct':correct,'total':len(xs),'baseline':baseline,'disposition':'intended_skill' if intended else 'not_predictive','conclusion':conclusion,'sample_refs':[refs[stage],'shortcut-stage-results.json']})
 results[stage]={'count':len(rows),'order':'actual UI' if stage=='delivered_batch' else 'generator raw (position claims limited to this stage)','kinds':dict(collections.Counter(r['kind'] for r in rows)),'rows':rows,'groups':summaries}
save('shortcut-stage-results.json',results);save('shortcut-probes.json',probes)
# Independently verify every fixed-bank controlled template admits all eligible roles.
cs=sets['controlled'];banks=collections.defaultdict(list)
for r in cs:banks[(r['generation']['template'],tuple(sorted(c[':answer/value'] for c in opts(r))))].append(r)
coverage=[]
for (template,bank),rs in banks.items():
 rr=[row(r) for r in rs];want=2 if rr[0]['kind']=='mixed' else 5;assert len({r['capacity'] for r in rr})==want
 coverage.append({'template':template,'operation':rr[0]['operation'],'eligible':want,'observed':len({r['capacity'] for r in rr}),'seeds':sorted({r['seed'] for r in rr}),'bank':list(bank),'targets':sorted({r['capacity'] for r in rr})})
save('sampling-results.json',{'fresh_seeds':list(range(71631,71655)),'fresh_templates':dict(collections.Counter(r['generation']['template'] for r in sets['fresh'])),'bank_counts':results['fresh']['kinds'],'independent_visible_role_verification':coverage,'conclusion':'All fifteen normal templates represented in current fixed-bank controls; every eligible capacity reassigns with bank fixed. Extra operation and its capacity role vary independently. Fresh sample includes both source-supported decision families. Exact batch has five mixed banks; each requires capacity and gap-sign discrimination.','limitations':'Controlled records originate in rerun author check; independently parsed and verified against source-derived operation. Fresh seeds and source/mathematical analysis are reviewer chosen. Finite audit.'})
# Learner selection read-only reproduction: actual captured inventory plus hypothetical new batch IDs.
inv=load(J/'source/inventory.json');new=sets['delivered_batch'];items=[]
for x in inv['questions']:
 d=x.get(':question/difficulty');d=d.get(':db/ident') if isinstance(d,dict) else d;items.append((x[':db/id'],d.split('/')[-1] if d else None,x[':question/id'],None))
base=max(x[0] for x in items)+1
items.extend((base+i,'easy',q(r)[':question/id'],i) for i,r in enumerate(new))
def select(pool,distribution,seed):
 pool=sorted(pool);digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=lambda o:(int.from_bytes(digest[o:o+8],'big')>>11)/(1<<53)
 if distribution is None:return pool[0] if pool else None
 bands=[[x for x in pool if x[1]==band] for band in ('easy','moderate','hard')];total=sum(w for w,b in zip(distribution,bands) if b)
 if total:
  draw=u(0)*total
  for w,b in zip(distribution,bands):
   if not b or not w:continue
   chosen=b
   if draw<w:break
   draw-=w
 else:chosen=[x for x in pool if x[1] is None]
 return chosen[min(int(u(8)*len(chosen)),len(chosen)-1)] if chosen else None
traces=[]
for name,distribution in [('easy_only',[1,0,0]),('all_bands',[1,1,1]),('unconfigured',None)]:
 pool=items.copy();trace=[]
 for step in range(len(pool)):
  seed=f'reviewer-71631/{step}';sel=select(pool,distribution,seed)
  if sel is None:break
  trace.append({'seed':seed,'entity_id':sel[0],'question_id':sel[2],'difficulty':sel[1],'batch_index':sel[3],'available_before':len(pool)});pool.remove(sel)
 traces.append({'policy':name,'weights':distribution,'trace':trace,'batch_members_selected':[t['batch_index'] for t in trace if t['batch_index'] is not None]})
assert all(set(x['batch_members_selected'])==set(range(5)) for x in traces)
save('selection-results.json',{'basis':inv['basis'],'source':'engine/rust/question_selection.rs select and seen_before_task inspected; faithful SHA256 draw, sorted entities, difficulty renormalization, explicit prefix/previous-task exclusions.','synthetic_new_entity_ids':True,'inventory_count':len(inv['questions']),'added_batch':5,'traces':traces,'result':'All five batch members can survive learner selection; selection operates on difficulty/freshness, with no equation-shape or target-rank condition. Within-band weighted/unconfigured draws retain the varied answers; repeated-task exclusions remove members without rewriting their decisions.','limits':['Actual future entity IDs, live policy weights and real learner history are unavailable. Offline traces use synthetic appended IDs and explicit hypothetical weights.','Inventory conclusions apply only to captured basis5380. Zero easy weight would intentionally exclude every easy question; no unconditional all-band frequency claim.']})
ui=[]
for group,rs in [('render-delivered',sets['delivered_batch']),('render-batch',sets['batch']),('render-pairs',load(E/'counterfactual-records.json'))]:
 for i,r in enumerate(rs):ui.append({'html':f'{group}/question-{i+1:03}.html','choice_ids':[c[':answer/id'] for c in display_order(r,i,group)],'correct_position':row(r,display_order(r,i,group))['position']})
save('ui-order-results.json',{'cases':ui,'batch_positions':dict(collections.Counter(x['correct_position'] for x in ui[:5])),'conclusion':'UI hashes choice order; claims about learner-visible positions use rendered HTML. No position answers the entire batch.'})
print(json.dumps({stage:{'count':v['count'],'kinds':v['kinds'],'overall_scores':v['groups'][0]['successes']} for stage,v in results.items()}))
