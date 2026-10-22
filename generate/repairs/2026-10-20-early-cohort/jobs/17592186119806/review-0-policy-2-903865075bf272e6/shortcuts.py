import json,re,pathlib,hashlib,collections
from fractions import Fraction
E=pathlib.Path(__file__).resolve().parent
def read(n):return json.load(open(E/n))
def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
M=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
def options(r):
 f=r['question'][':question/answer-fields'][0];cid=f[':answer-field/correct'][1]
 return [(a[':answer/id'],tuple(Fraction(v.strip()) for v in M.fullmatch(a[':answer/value'])[1].split('\\\\')) if M.fullmatch(a[':answer/value']) else Fraction(a[':answer/value'])) for a in f[':answer-field/choices']],cid
def signature(r):
 p=r['question'][':question/problem'];m=re.search(r'\$(\d+)a([+-])(\d+)x=b\$',p);ch,cid=options(r)
 return m[0]+' '+('scalar' if not isinstance(ch[0][1],tuple) else 'vector')+' '+str(len(M.findall(p)[0].split('\\\\')))+'D'
def bank_strategy(r):
 # Rules chosen from independently inspected source and code, never read the key.
 p=r['question'][':question/problem'];ch,_=options(r)
 if '$6a-2x=b$' in p:return sorted(ch,key=lambda x:x[1])[1][0],'6a-2x: choose second-smallest scalar'
 if '$7a+4x=b$' in p:return min(ch,key=lambda x:x[1])[0],'7a+4x: choose smallest scalar'
 if '$5a-3x=b$' in p:return max(ch,key=lambda x:x[1][2])[0],'5a-3x: choose largest third coordinate'
 return None,'No predeclared rule'
def measure(records):
 details=[]
 for r in records:
  ch,cid=options(r);picked,rule=bank_strategy(r)
  details.append({'id':r['question'][':question/id'],'profile':r['generation']['source_id'],'signature':signature(r),'parameters':r['generation']['parameters'],'rank':sorted(ch,key=lambda x:x[1]).index(next(a for a in ch if a[0]==cid))+1,'selected_id':picked,'correct_id':cid,'strategy':rule,'success':picked==cid if picked else None,'bank':[(a,str(v)) for a,v in ch]})
 return {'count':len(records),'profiles':dict(collections.Counter(r['generation']['source_id'] for r in records)),'correct_position_counts':dict(collections.Counter(next(i for i,(aid,v) in enumerate(options(r)[0]) if aid==options(r)[1])+1 for r in records)),'details':details}
sets={n:measure(read(p)) for n,p in [('raw_domain','domain-records.json'),('delivered_domain','delivery-domain/accepted.json'),('raw_batch','batch-records.json'),('delivered_batch','delivery-batch/accepted.json'),('fresh','fresh-records.json')]}
save('shortcut-results.json',{'command':'/home/jake/Developer/Course_Academy/.venv/bin/python '+str(E/'shortcuts.py'),'baseline':'Uniformly choose one of five radio answers = 0.2. Each rule uses only visible equation signature and the answer bank, never supplied a/b components.','sets':sets,'proof':'For every scalar profile v = answer + positive_scale*(source_option-source_correct). Strict scalar order and the correct rank are invariant under every allowed retarget and scale. Vector positive dilation likewise preserves all coordinate ranks. These relationships have no mathematical necessity in solving p*a+q*x=b.'})
# Strict tests intended to fail current package and remain as repair acceptance tests.
reg=[]
for sid in ['q-34601','q-105161']:
 rows=[x for x in sets['delivered_domain']['details'] if x['profile']==sid]
 reg.append({'test':'correct scalar rank must vary within recognizable '+sid,'observed_ranks':sorted(set(x['rank'] for x in rows)),'attempts':len(rows),'passed':len(set(x['rank'] for x in rows))>1})
rows=sets['delivered_batch']['details'];reg.append({'test':'fixed bank-only rules must not answer every surviving batch record','correct':sum(x['success'] is True for x in rows),'total':len(rows),'passed':not all(x['success'] for x in rows)})
save('regression-results.json',{'passed':all(x['passed'] for x in reg),'tests':reg})
# Native confirmation on delivery-normalized IDs, rather than assuming stored identifiers survive.
cases=[]
for r in read('delivery-batch/accepted.json'):
 aid,rule=bank_strategy(r);f=r['question'][':question/answer-fields'][0]
 cases.append({'label':rule+':delivered:'+r['question'][':question/id'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':aid,'expected':'accepted','purpose':'Confirm answer-bank-only shortcut using actual native learner grader'}]})
save('shortcut-grader-input.json',cases)
# Faithful read-only selection reproduction for all-easy candidates, from Rust select().
# Generated records have no DB IDs before publication; use explicitly declared surrogate IDs.
# Their assignment affects deterministic order only; no claim about a particular live learner.
selection=[]
for name,path in [('domain','delivery-domain/accepted.json'),('batch','delivery-batch/accepted.json')]:
 records=read(path);pool={100000+i:r for i,r in enumerate(sorted(records,key=lambda r:r['question'][':question/id']))}
 for scenario in ['fresh','earlier_members_seen']:
  seen=set(list(pool)[:len(pool)//2]) if scenario!='fresh' else set()
  ids=sorted(set(pool)-seen);chosen=[]
  for trial in range(128):
   seed='independent-review-87591-'+str(trial);h=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
   u=(int.from_bytes(h[8:16],'big')>>11)/(1<<53);entity=ids[int(u*len(ids))];r=pool[entity];aid,rule=bank_strategy(r)
   chosen.append({'seed':seed,'surrogate_entity':entity,'question_id':r['question'][':question/id'],'profile':r['generation']['source_id'],'shortcut_success':aid==options(r)[1] if aid else None})
  selection.append({'pool':name,'scenario':scenario,'candidate_count':len(ids),'all_easy':True,'weights':'Any positive easy band weight; moderate/hard empty. Both initial/remedial weights reduce to uniform within easy. Explicit zero easy gives no eligible generated question; unknown policy fallback uses first sorted entity.','profile_counts':dict(collections.Counter(x['profile'] for x in chosen)),'shortcut_cases':sum(x['shortcut_success'] is not None for x in chosen),'shortcut_successes':sum(x['shortcut_success'] is True for x in chosen),'draws':chosen})
save('learner-selection.json',{'implementation':'engine/rust/question_selection.rs select, seen_before_task; engine/rust/learning.rs lines 595-622 candidate freshness and validate_practice_question filter','basis':5402,'surrogate_id_map':'Sorted accepted question UUIDs mapped to 100000+i; generated DB entities do not exist before publication.','method':'Read-only reproduction of SHA256 draw and freshness exclusion. No duplicate or difficulty changes from the actual shared delivery outputs. Native grader confirms gradability for every surviving batch record.','scenarios':selection,'limits':['Live policy and learner histories are not supplied; cannot claim particular learner frequencies.','Captured original questions may also be candidates; a learner who has seen them retains this generated pool.','No rank/shortcut-aware filter is present; reweighting and freshness cannot break an item-wise invariant.','No DB entity identity collision test or publication performed.']})
print(json.dumps({'regressions':reg,'stages':{n:{'count':v['count'],'q34601':sum(x['profile']=='q-34601' for x in v['details']),'bank_rules_correct':sum(x['success'] is True for x in v['details'])} for n,v in sets.items()}}))
