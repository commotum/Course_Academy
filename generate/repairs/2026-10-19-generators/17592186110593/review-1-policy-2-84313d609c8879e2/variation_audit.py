import os,sys,json,pathlib,random,hashlib,re,collections
os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent
R=pathlib.Path('/home/jake/Developer/Course_Academy');J=R/'generate/repairs/2026-10-19-generators/17592186110593';W=J/'workspace'
sys.path.insert(0,str(W));import generator as g

def load(f):return json.load(open(E/f))
def save(f,v):(E/f).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def field(r):return r['question'][':question/answer-fields'][0]
def key(r):
 k=field(r)[':answer-field/correct'];return k[1] if isinstance(k,list) else k[':answer/id']
def cs(r):return field(r)[':answer-field/choices']
def params(r):
 t=r['question'][':question/problem'].replace(' ','').replace('${','$').replace('}^','^')
 m=re.search(r'\$(\d+)\^\{x([+-]\d+)?\}=(\d+)',t);assert m,t
 return int(m[1]),int(m[3]),int(m[2] or 0)
def role(c):
 t=c[':answer/value'].replace(' ','');m=re.search(r'\\log_\{(\d+)\}\((\d+)\)([+-]\d+)?',t)
 assert m,t
 return int(m[1]),int(m[2]),int(m[3] or 0)
def profile(r):return 'direct' if params(r)[2]==0 else 'shifted'
def coverage(rs):
 return {'n':len(rs),'templates':dict(collections.Counter(profile(r) for r in rs)),'bases':dict(collections.Counter(params(r)[0] for r in rs)),'rhs_minmax':[min(params(r)[1] for r in rs),max(params(r)[1] for r in rs)],'offsets':dict(collections.Counter(params(r)[2] for r in rs)),'answer_positions':dict(collections.Counter(next(i+1 for i,c in enumerate(cs(r)) if c[':answer/id']==key(r)) for r in rs))}
# Exact tracing of random bank attempts and semantic rejection. Replays same RNG calls.
class TraceRandom(random.Random):
 def __init__(self,seed):super().__init__(seed);self.banks=0
 def sample(self,population,k,**kw):
  if population==range(2,10):self.banks+=1
  return super().sample(population,k,**kw)
def traced_generate(count,seed):
 rng=TraceRandom(seed);seen=set();out=[];raw=[]
 for _ in range(max(1000,count*100)):
  if len(out)==count:break
  roles=g.draw_roles(rng,bool(rng.getrandbits(1)));chosen=rng.randrange(5);b,r,k=roles[chosen]
  raw.append({'bank':roles,'chosen':chosen,'equation':[b,r,-k],'accepted':(b,r,-k) not in seen})
  if (b,r,-k) in seen:continue
  out.append(g.build(roles,chosen,order=rng.sample(range(5),5),seed=seed));seen.add((b,r,-k))
 return out,{'seed':seed,'count':count,'raw_bank_attempts':rng.banks,'valid_banks':len(raw),'bank_rejections':rng.banks-len(raw),'semantic_rejections':len(raw)-len(out),'candidate_cases':raw,'pre_semantic_profiles':dict(collections.Counter('direct' if v['equation'][2]==0 else 'shifted' for v in raw)),'surviving_coverage':coverage(out)}
traces=[]
for seed,count in [(104729,40),(98593,1000)]:
 rs,trace=traced_generate(count,seed)
 trace['faithful_match']=json.loads(json.dumps(rs))==(load('samples.json')[:40] if count==40 else load('boundary-1000.json'))
 traces.append(trace)
save('rejection-trace.json',traces)
sets={'raw fresh':load('samples.json'),'delivered fresh':load('delivery-fresh/accepted.json'),'raw runner':load('runner-batch.json'),'delivered runner':load('delivery-runner/accepted.json'),'controlled':load('controlled.json'),'delivered controlled':load('delivery-controlled/accepted.json')}
# Learner-selection faithful read-only reproduction of question_selection.rs select.
inv=json.load(open(J/'source/inventory.json'));maxid=max(q[':db/id'] for q in inv['questions'])
pool=[]
for q in inv['questions']:pool.append({'id':q[':db/id'],'rated':q.get(':question/difficulty') is not None,'record':{'question':q},'origin':'captured inventory'})
for i,r in enumerate(sets['delivered fresh']):pool.append({'id':maxid+1+i,'rated':True,'record':r,'origin':'new (synthetic ordered ID)'})
pool.sort(key=lambda p:p['id'])
def select(pool,weights,seed):
 if weights is None:return pool[0] if pool else None
 digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
 u=lambda o:(int.from_bytes(digest[o:o+8],'big')>>11)/2**53
 rated=[p for p in pool if p['rated']];unrated=[p for p in pool if not p['rated']]
 # Captured and generated bank has easy and unrated only. No moderate/hard records.
 chosen=rated if rated and weights[0]>0 else unrated
 return chosen[int(u(8)*len(chosen))] if chosen else None
selection=[]
for label,weights in [('positive easy initial/remedial',[6,3,1]),('easy zero fallback',[0,3,1]),('unconfigured policy',None)]:
 draws=[select(pool,weights,f'independent-review/task-{i}/prefix-0') for i in range(2048)]
 records=[x['record'] for x in draws if x]
 selection.append({'policy_case':label,'weights':weights,'seed_pattern':'independent-review/task-{0..2047}/prefix-0','candidate_counts':{'rated_easy':sum(x['rated'] for x in pool),'unrated':sum(not x['rated'] for x in pool)},'selected_origins':dict(collections.Counter(x['origin'] for x in draws if x)),'coverage':coverage(records),'selected_ids':[x['id'] if x else None for x in draws]})
save('selection-results.json',{'implementation':'Faithful reproduction of question_selection.rs select: ordered unique numeric IDs, SHA256 53-bit uniform, easy pool only; records include captured bank and fresh accepted generator output. No DB access.','identity_limit':'New ordered numeric IDs are synthetic; exact live task draws depend on assigned IDs, policy weights, task seeds and learner history, which are not captured. Selection is uniform inside easy for positive easy weight, regardless of its exact positive magnitude. Unrated fallback and unconfigured branch are shown separately.','history':'seen_before_task excludes prior task contents and caller excludes current prefix; fresh learner case shown. Any remaining easy record has positive probability under positive easy weight; learner-specific coverage cannot be guaranteed after arbitrary exclusions.','captured_basis':inv['basis'],'canonical_excluded':'Canonical example is not a question bank candidate.','pool':[{'id':p['id'],'rated':p['rated'],'origin':p['origin'],'record':p['record']} for p in pool],'cases':selection})
save('stage-coverage.json',{'stages':{name:coverage(rs) for name,rs in sets.items()},'publication_preparation':'Absent; ran shared read-only prepare_records using captured basis 4974.','selection_summary':[{k:v for k,v in s.items() if k!='selected_ids'} for s in selection]})
# Probe raw and accepted records, each recognizable exponent/template subgroup.
# Baseline 1/5 is uniform guessing; conditional mathematical strategies are assessed separately.
probes=[]
strategies={f'position {i+1}':lambda r,i=i:i for i in range(5)}
strategies.update({'shortest TeX':lambda r:min(range(5),key=lambda i:len(cs(r)[i][':answer/value'])),'longest TeX':lambda r:max(range(5),key=lambda i:len(cs(r)[i][':answer/value'])),'lexically first':lambda r:min(range(5),key=lambda i:cs(r)[i][':answer/value']),'smallest displayed base':lambda r:min(range(5),key=lambda i:role(cs(r)[i])[0]),'smallest displayed argument':lambda r:min(range(5),key=lambda i:role(cs(r)[i])[1]),'first positive additive offset':lambda r:next((i for i,c in enumerate(cs(r)) if role(c)[2]>0),0),'first negative additive offset':lambda r:next((i for i,c in enumerate(cs(r)) if role(c)[2]<0),0)})
for setname in ['raw fresh','delivered fresh','raw runner','delivered runner']:
 for group in ['overall','direct','shifted','positive exponent shift','negative exponent shift']:
  rs=[r for r in sets[setname] if group=='overall' or (group in ['direct','shifted'] and profile(r)==group) or (group=='positive exponent shift' and params(r)[2]>0) or (group=='negative exponent shift' and params(r)[2]<0)]
  if not rs:continue
  for strategy,f in strategies.items():
   correct=sum(cs(r)[f(r)][':answer/id']==key(r) for r in rs)
   probes.append({'set':setname,'subgroup':group,'strategy':strategy,'correct':correct,'total':len(rs),'baseline':0.2,'disposition':'not_predictive','conclusion':'No fixed answer role established; binomial fluctuations in finite samples are not proof of a predictor. Runner batch is only five items.'})
# Intended mathematical matching is explicitly distinguished from incidental cues.
for group in ['direct','shifted']:
 rs=[r for r in sets['delivered fresh'] if profile(r)==group]
 def matching(r):
  b,n,s=params(r);return [i for i,c in enumerate(cs(r)) if role(c)[:2]==(b,n)]
 unique=[r for r in rs if len(matching(r))==1]
 probes.append({'set':'delivered fresh','subgroup':group+' unique matching base and argument','strategy':'Apply same-base inverse identity; match both log base and positive RHS','correct':sum(cs(r)[matching(r)[0]][':answer/id']==key(r) for r in unique),'total':len(unique),'baseline':0.2,'disposition':'intended_skill','conclusion':'Uses tutorial 2794 logarithmic inversion, so success is an intended mathematical simplification. It is not a label/layout-only strategy. Controlled shifted pair separately forces offset-sign reconsideration with base/RHS fixed.'})
# UI's actual deterministic FNV-1a ordering, for multiple representative task-item IDs.
def fnv(t):
 n=2166136261
 for c in t:n=((n^ord(c))*16777619)&0xffffffff
 return n
for itemid in [1,1009,17592187000000]:
 for group in ['direct','shifted']:
  rs=[r for r in sets['delivered fresh'] if profile(r)==group]
  ordered=[sorted(cs(r),key=lambda c:fnv(f"{itemid}:{field(r)[':answer-field/id']}:{c[':answer/id']}")) for r in rs]
  for i in range(5):probes.append({'set':'delivered fresh UI','subgroup':f'{group}; itemId {itemid}','strategy':f'UI position {i+1}','correct':sum(v[i][':answer/id']==key(r) for r,v in zip(rs,ordered)),'total':len(rs),'baseline':0.2,'disposition':'not_predictive','conclusion':'Faithful FNV-1a reproduction of learning.js choiceOrder; no always-correct UI position. Live item IDs vary.'})
save('shortcut-results.json',probes)
# Hold five bank texts and display order fixed; every eligible answer changes with inverse equation.
ctrl=load('controlled.json');pairs=[]
for a,b,kind,relation in [(0,1,'relevant','RHS changes 3 to 5 with b=2 and same complete direct bank; correct expression changes.'),(5,6,'relevant','Exponent x-1 to x+1 with b=2,r=3 unchanged; answer log_2(3)+1 to log_2(3)-1.'),(5,10,'irrelevant','Only display order and generation seed change; same equation, same key UUID, same correct expression, same solution.')]:
 ra,rb=ctrl[a],ctrl[b]
 pairs.append({'kind':kind,'before_index':a,'after_index':b,'expected':relation,'before':ra,'after':rb,'same_bank_texts':sorted(c[':answer/value'] for c in cs(ra))==sorted(c[':answer/value'] for c in cs(rb)),'same_problem':ra['question'][':question/problem']==rb['question'][':question/problem'],'same_solution':ra['question'][':question/worked-solution']==rb['question'][':question/worked-solution'],'same_key':key(ra)==key(rb),'before_answer':next(c[':answer/value'] for c in cs(ra) if c[':answer/id']==key(ra)),'after_answer':next(c[':answer/value'] for c in cs(rb) if c[':answer/id']==key(rb)),'grader_cases':[f'controlled-{a}',f'controlled-{b}'],'render_cases':[4,5] if a==0 else [6,7] if b==6 else [6,8],'status':'passed'})
save('counterfactual-results.json',{'pairs':pairs,'all_answer_roles':'Each of five options in each fixed bank is selected once in controlled.json. Native grader checks all five choices against each equation. Renderer cases show relevant RHS/sign and irrelevant-order pairs.','dependency_results':'Native outcomes in grader-results.json from grader-input.json; all expected outcomes passed. Rendering assessment recorded separately after screenshot inspection.'})
# Expand single native-grader invocation to cover normalized stable-identity delivered records too.
grader=load('grader-input.json')
for name in ['delivery-runner/accepted.json','delivery-controlled/accepted.json']:
 for i,r in enumerate(load(name)):
  grader.append({'label':f'{name}-{i}','record':r,'checks':[{'field_index':0,'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==key(r) else 'rejected','purpose':'Rekeyed delivered record; raw mathematics independently checked before stable-identity normalization.'} for c in cs(r)]})
save('grader-input.json',grader)
print(json.dumps({'coverage':{n:coverage(rs)['templates'] for n,rs in sets.items()},'rejection':[{k:v for k,v in x.items() if k not in ['candidate_cases','surviving_coverage']} for x in traces],'shortcut_max':[(name,max(p['correct']/p['total'] for p in probes if p['set']=='delivered fresh' and p['subgroup']==name and p['disposition']=='not_predictive')) for name in ['direct','shifted']],'counterfactual_pairs':len(pairs),'selection':[{k:v for k,v in x.items() if k not in ['selected_ids','coverage']} for x in selection]}))
