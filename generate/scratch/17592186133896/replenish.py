"""Green area setup replenishment: scoped additive exact requests under application lock."""
import copy,fcntl,hashlib,importlib.util,json,os,re,subprocess,sys,threading,uuid,urllib.request,urllib.parse
from pathlib import Path
from types import SimpleNamespace
import sympy as sp
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'scripts'));from serve_graph_explorer import database_environment
from inventory_jobs import save
sys.path.insert(0,str(ROOT));from capture.scripts.database.preview import preview_executable
sys.path.insert(0,str(ROOT/'scripts/question_capture'));from database import Database,QUESTION_PULL
from edn import dumps,loads,kw
spec=importlib.util.spec_from_file_location('green_validate',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
KP=g.KP_ID;LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.SOURCE['lineage'];SOURCE=':application/ca-engine'
LEVELS=('easy','moderate','hard');SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'103309cc68ea7eba6cc838b3214e91042ea51d6f90db545e5aa792bda5326d9d'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']));DB.env=database_environment('math')
QUERY='[:find (pull ?kp [* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example '+QUESTION_PULL+'} {[:knowledge-point/questions :limit nil] '+QUESTION_PULL+'}]) :in $ ?kp :where [?kp :knowledge-point/id _]]'
NATIVE=ROOT/'.local/graph-explorer/learning-ef48cfde3a25d91e';POOL=HERE/'reference/native/check-pool';ENGINE=HERE/'reference/native/check-engine'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def inventory(p):
 r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,capture_output=True,text=True,check=True,timeout=55)
 x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(p,x['data']);return x['data']

def read(p,b):return DB.query(QUERY,[KP],p,'kp',b)[0][0]

def normalize(q):
    return {':question/id':str(q[':question/id']),':question/problem':q[':question/problem'],':question/worked-solution':q[':question/worked-solution'],':question/difficulty':str(q[':question/difficulty'][':db/ident']),':question/answer-fields':sorted([{':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':sorted([{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],key=lambda a:a[':answer/id'])} for f in q[':question/answer-fields']],key=lambda f:f[':answer-field/key'])}

def ordered(q):
    q=copy.deepcopy(q);q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in q[':question/answer-fields']:f[':answer-field/choices'].sort(key=lambda a:a[':answer/id'])
    return q

def scoped(kp,b,seen):
    entities={};enums={}
    def enum(value):
        name=str(value[':db/ident']).lstrip(':')
        if name not in enums:
            e=len(enums)+1;enums[name]=e;entities[str(e)]={'db/ident':name}
        return enums[name]
    for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]:
        r={'question/id':str(q[':question/id']),'question/problem':q[':question/problem'],'question/answer-fields':[]};entities[str(q[':db/id'])]=r
        if ':question/difficulty' in q:r['question/difficulty']=enum(q[':question/difficulty'])
        for f in q.get(':question/answer-fields',[]):
            r['question/answer-fields'].append(f[':db/id']);field={'answer-field/key':f[':answer-field/key'],'answer-field/type':enum(f[':answer-field/type']),'answer-field/choices':[a[':db/id'] for a in f.get(':answer-field/choices',[])]};entities[str(f[':db/id'])]=field
            if ':answer-field/correct'in f:field['answer-field/correct']=f[':answer-field/correct'][':db/id']
            for a in f.get(':answer-field/choices',[]):entities[str(a[':db/id'])]={'answer/type':enum(a[':answer/type']),'answer/value':a[':answer/value']}
    entities[str(KP)]={'knowledge-point/id':str(kp[':knowledge-point/id']),'knowledge-point/title':kp[':knowledge-point/title'],'knowledge-point/questions':[q[':db/id'] for q in kp[':knowledge-point/questions']],'knowledge-point/canonical-example':kp[':knowledge-point/canonical-example'][':db/id']}
    return {'basis_t':b,'knowledge_point':KP,'entities':entities,'seen':sorted(seen)}

def transaction(records,kp,gid):
    forms=[]
    for r in records:
        q=r['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
            forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
        forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
    gen=kp.get(':knowledge-point/question-generator')
    if gen:
        assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
    else:
        forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
    if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
    return forms

def check_report(report,p,source):
    attrs=dict(DB.attributes(p,report[':edb/db-before-t']));new=set(report[':edb/tempids'].values())
    allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s==source and added,'Unexpected attribution/retraction'
        name=str(attrs[a])
        if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name!=':db/txInstant':assert e in new and name in allowed,name

def fixtures(records):
 result=[]
 for rec in records:
  checks=[]
  for i,f in enumerate(rec['question'][':question/answer-fields']):
   correct=f[':answer-field/correct'][1]
   if f[':answer-field/type'].endswith('/radio'):
    checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'independently verified complete bank'} for a in f[':answer-field/choices'])
   else:
    value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==correct)
    checks.extend([{'field_index':i,'submitted':value,'expected':'accepted','purpose':'canonical exact answer'},{'field_index':i,'submitted':'('+value+')','expected':'accepted','purpose':'equivalent grouped exact expression through current learner grader'},{'field_index':i,'submitted':'('+value+')+1','expected':'rejected','purpose':'incorrect derivative'}])
  result.append({'label':rec['question'][':question/id'],'record':rec,'checks':checks})
 return result

def math(value):
 try:return g.parse_math(value)
 except (ValueError,TypeError):pass
 from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
 s=value.replace('⁡','').replace(r'\,','').replace(r'\cdot','*').replace(r'\left','').replace(r'\right','')
 s=re.sub(r'\\operatorname\{(sin|cos)\}',r'\\\1',s);s=re.sub(r'\{(sin|cos)\}',r'\\\1',s)
 s=re.sub(r'\\(sin|cos)(?:\^\{(\d+)\})?\s*([23]?)\s*t',lambda m:'('+m[1]+'('+ (m[3]+'*' if m[3] else '')+'t)'+('**'+m[2] if m[2] else '')+')',s)
 s=s.replace('{e}','e').replace('^','**').replace('{','(').replace('}',')')
 assert not re.search(r'[^0-9a-zA-Z+\-*/().\s]',s),s
 return parse_expr(s,local_dict={'t':g.t,'sin':sp.sin,'cos':sp.cos,'e':sp.E},transformations=standard_transformations+(implicit_multiplication_application,))

def task(q):
 prompt=q[':question/problem'].replace(r'\langle','⟨').replace(r'\rangle','⟩').replace(r'\:','').replace(r'\left','').replace(r'\right','');curve=re.search('⟨(.*?)⟩',prompt)[1].replace(r'\,','').split(',');x,y=map(math,curve)
 bounds=re.search(r'for \$t.*?\[(.*?)[\]\)]',prompt)[1];lo,hi=map(v.bound,bounds.split(','));domain=(lo,hi)
 area=g.integral_value(x*sp.diff(y,g.t),domain);sign=1 if float(sp.N(area))>0 else -1
 field='P' if '$P(x,y)=-y$' in prompt.replace(' ','') else 'Q';correct=sign*(-y*sp.diff(x,g.t) if field=='P' else x*sp.diff(y,g.t))
 fp=g.digest({'integrand':str(sp.expand_trig(sp.expand(correct))),'domain':[str(z) for z in domain]})
 return fp,correct,domain,x,y,sign,field

def native(records,p):
 p.mkdir(parents=True,exist_ok=True);save(p/'input.json',fixtures(records))
 r=subprocess.run([str(ENGINE),str(p/'input.json'),str(p/'report.json')],text=True,capture_output=True,timeout=55)
 (p/'run.log').write_text(r.stdout+r.stderr)
 if r.returncode:raise RuntimeError(r.stderr)
 return json.loads((p/'report.json').read_text())

def audit_source(q):
 fp,correct,domain,x,y,sign,field=task(q)
 assert sp.simplify(x.subs(g.t,domain[0])-x.subs(g.t,domain[1]))==0 and sp.simplify(y.subs(g.t,domain[0])-y.subs(g.t,domain[1]))==0
 solution=q.get(':question/worked-solution','');assert solution
 derivative=re.search('⟨(.*?)⟩',solution)[1].replace(r'\,','').split(',')
 assert all(sp.trigsimp(math(z)-sp.diff(c,g.t))==0 for z,c in zip(derivative,[x,y]))
 collisions=[];matched=0
 for f in q[':question/answer-fields']:
  assert ':answer-field/correct' in f,'missing correct link'
  vals=[math(a[':answer/value']) for a in f[':answer-field/choices']];matches=[a[':answer/id'] for a,z in zip(f[':answer-field/choices'],vals) if sp.trigsimp(z-correct)==0]
  assert len(matches)==1 and matches[0]==f[':answer-field/correct'][':answer/id'],'incorrect or ambiguous pointwise key'
  integrals=[g.integral_value(z,domain) for z in vals]
  collisions.extend([{'values':[f[':answer-field/choices'][i][':answer/value'],f[':answer-field/choices'][j][':answer/value']],'integral':str(integrals[i])} for i in range(len(vals)) for j in range(i) if g.equivalent_scalar(integrals[i],integrals[j])])
  matched+=len(vals)
 return {'source_id':q.get(':question/math-academy-id'),'fingerprint':fp,'orientation':sign,'field':field,'domain':[str(z) for z in domain],'matched_pointwise_bank_values':matched,'complete_integral_collisions':collisions,'gradable':not collisions}

def source_refresh(kp,p,b):
 old=g.QUESTIONS;now={q[':question/math-academy-id']:q for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q};findings=[]
 assert set(old)<=set(now),'Captured source removed; requires reconciliation'
 for mid,q in now.items():
  item={'source_id':mid,'difficulty':str(q.get(':question/difficulty',{}).get(':db/ident')),'fields':len(q.get(':question/answer-fields',[])),'new_evidence':mid not in old}
  if mid in old:
   before=old[mid]
   if mid!='q-42221':
    assert q[':question/problem']==before[':question/problem'] and q.get(':question/worked-solution')==before.get(':question/worked-solution'),(mid,'source changed')
    for f,sf in zip(q[':question/answer-fields'],before[':question/answer-fields']):assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
   else:item['refresh']='Previously unrated incomplete exponential is now repaired and moderate. Frozen authored hard exp_ccw sampling is suspended.'
  try:item.update(audit_source(q))
  except (AssertionError,ValueError,KeyError) as e:item.update({'gradable':False,'exclusion':str(e)})
  findings.append(item)
 save(p/'source-refresh.json',{'basis':b,'frozen_basis':g.SOURCE['basis'],'source_count':len(now),'findings':findings,'normal_generator_subset':'All validated v4 families except exp_ccw. New source families are recorded but not claimed as generated templates.'})
 return findings

def local_record(r):
 r=copy.deepcopy(r)
 for a in r.get('publication',[]):
  assert sha(Path('/media/jake/SSD/EDB/math')/a['database_relative_path'])==a['sha256']
  r['question'][':question/problem']=r['question'][':question/problem'].replace(a['database_relative_path'],a['local_path'])
 return r

def validate(r):
 raw=local_record(r);meta=raw['generation'];q=raw['question'];l=q[':question/difficulty'].split('/')[-1]
 assert l in LEVELS and meta['learner_eligible'] and meta['profile']=='authored'
 assert meta['template']!='exp_ccw','Frozen inferred hard rating superseded by current moderate evidence'
 assert raw['knowledge_point']['db_id']==KP and raw['knowledge_point']['id']==g.KP_UUID
 replay=g.generate(l,seed=meta['seed'],template=meta['template'],parameters=meta['parameters'],profile=meta['profile'])
 assert ordered(replay['question'])==ordered(q) and replay['generation']==meta
 iv=v.verify(raw);fp=task(q)[0];assert fp==meta['mathematical_fingerprint']
 return {'id':q[':question/id'],'fingerprint':fp,'integral_values':iv,'template':meta['template'],'parameters':meta['parameters']}

def counts(kp,b,p):
 p.mkdir(parents=True,exist_ok=True)
 shown=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]',[KP,LEARNER],p,'ever-shown',b,history=True)
 reserved=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]',[KP,LEARNER],p,'reserved',b)
 seen={x[0] for x in shown+reserved};save(p/'scoped.json',scoped(kp,b,seen))
 subprocess.run([str(POOL),str(p/'scoped.json'),str(p/'native-pool.json')],capture_output=True,text=True,check=True,timeout=55)
 pool=json.loads((p/'native-pool.json').read_text());ids={q for xs in pool['available_ids_by_level'].values() for q in xs}
 levels={l:set() for l in LEVELS};validated=[];excluded=[];records=[]
 known={r['question'][':question/id']:r for f in OUT.glob('basis-*/generated-published.json') for r in json.loads(f.read_text())}
 for q in kp[':knowledge-point/questions']:
  if q[':db/id'] not in ids:excluded.append({'id':str(q[':question/id']),'reason':'native pool excludes incomplete, unrated, shown, reserved or canonical'});continue
  try:
   if ':question/math-academy-id' in q:
    a=audit_source(q);assert a['gradable'],'ambiguous complete-integral source bank'
    r={'question':normalize(q),'knowledge_point':{'db_id':KP,'id':g.KP_UUID,'title':g.TITLE}}
   else:
    r=known[str(q[':question/id'])];assert normalize(q)==ordered(r['question']);validate(r)
   fp=task(q)[0];l=str(q[':question/difficulty'][':db/ident']).split('/')[-1];levels[l].add(fp);validated.append(str(q[':question/id']));records.append(r)
  except (AssertionError,ValueError,KeyError) as e:excluded.append({'id':str(q[':question/id']),'reason':str(e)})
 native(records,p/'available-grading')
 result={'basis':b,'distinct_available':{l:len(x) for l,x in levels.items()},'validated_ids':validated,'excluded':excluded,'shown_or_reserved':sorted(seen),'native_pool':pool,'deduplication':'expanded pointwise integrand and parameter domain; ignores seed, choices, profile, geometry aliases and difficulty'}
 save(p/'counts.json',result);return result

# Reuse mathematical audits only for byte-identical records within this invocation.
_AUDITS={};_VALIDATIONS={};_audit_source=audit_source;_validate=validate
def audit_source(q):
 key=g.digest(json.loads(json.dumps(q,default=str)))
 if key not in _AUDITS:_AUDITS[key]=_audit_source(q)
 return copy.deepcopy(_AUDITS[key])
def validate(r):
 key=g.digest(r)
 if key not in _VALIDATIONS:_VALIDATIONS[key]=_validate(r)
 return copy.deepcopy(_VALIDATIONS[key])

if __name__=='__main__' and '--inspect' in sys.argv:
 inv=inventory(OUT/'inventory-before.json');b=inv['basis'];kp=read(OUT/'initial',b);source_refresh(kp,OUT/'initial',b);c=counts(kp,b,OUT/'initial');print(json.dumps({'basis':b,'counts':c['distinct_available'],'excluded':c['excluded'],'jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP]},indent=2))

def candidates(kp,needed,p):
 supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]) if isinstance(supplied,dict) else supplied;instances=[instances] if isinstance(instances,dict) else instances
 for r in instances:validate(r)
 save(p/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances)})
 used={task(q)[0] for q in kp[':knowledge-point/questions']}
 canonical=kp[':knowledge-point/canonical-example']
 used.add(task(canonical)[0]);records=[];results=[];new={l:0 for l in LEVELS}
 seed=int(JOB.name[:8],16)
 for level in LEVELS:
  templates=[t for t,(l,_,__) in g.TEMPLATES.items() if l==level and t!='exp_ccw']
  for i in range(250):
   if new[level]>=needed[level]:break
   if i<len(instances):r=instances[i]
   else:r=g.generate(level,seed+i,template=templates[i%len(templates)])
   if r['question'][':question/difficulty']!=':question.difficulty/'+level:continue
   fp=r['generation']['mathematical_fingerprint']
   if fp in used:continue
   results.append(validate(r));records.append(r);used.add(fp);new[level]+=1
  assert new[level]==needed[level],('bounded sampler exhausted',level,new[level],needed[level])
 save(p/'generated.json',records);save(p/'mathematics-validation.json',{'passed':True,'questions':results,'pointwise_and_complete_integral_banks_verified':True,'declared_subset':'v4 except exp_ccw','seed_or_order_duplicates':0})
 (p/'generated.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in records));native(records,p/'selected-grading')
 return records,new

def publish(records,p):
 published=copy.deepcopy(records);assets=[]
 for r in published:
  a=Path(r['generation']['plots']['prompt']);digest=sha(a);relative='images/'+digest[:2]+'/'+digest+'.png';dest=Path('/media/jake/SSD/EDB/math')/relative;dest.parent.mkdir(parents=True,exist_ok=True)
  if not dest.exists():
   tmp=dest.with_suffix('.tmp-'+str(os.getpid()));tmp.write_bytes(a.read_bytes());os.replace(tmp,dest)
  assert sha(dest)==digest
  body=urllib.request.urlopen('http://127.0.0.1:8765/api/asset?'+urllib.parse.urlencode({'path':relative}),timeout=10).read();assert hashlib.sha256(body).hexdigest()==digest
  item={'local_path':str(a),'database_relative_path':relative,'sha256':digest,'stored_bytes_verified':True,'http_availability_verified':True};assets.append(item);r['publication']=[item]
  r['question'][':question/problem']=r['question'][':question/problem'].replace(str(a),relative)
 save(p/'assets.json',assets);save(p/'generated-published.json',published);return published

def prepare():
 p=OUT/'prepared';p.mkdir(exist_ok=True);inv=inventory(p/'inventory-before.json');b=inv['basis'];kp=read(p,b);source_refresh(kp,p,b);c=counts(kp,b,p/'current-inventory');needed={l:max(0,5-c['distinct_available'][l]) for l in LEVELS}
 records,new=candidates(kp,needed,p);publish(records,p)
 save(p/'preparation.json',{'basis':b,'lineage':LINEAGE,'available':c['distinct_available'],'missing':needed,'new_by_level':new,'generator_sha256':sha(HERE.with_suffix('.py')),'native_build':json.loads((HERE/'reference/native/build.json').read_text())})
 from PIL import Image,ImageDraw
 canvas=Image.new('RGB',(1400,360*((len(records)+3)//4)),'white');draw=ImageDraw.Draw(canvas)
 for i,r in enumerate(records):
  im=Image.open(r['generation']['plots']['prompt']).convert('RGB');im.thumbnail((340,315));x=(i%4)*350;y=(i//4)*360;canvas.paste(im,(x,y+40));draw.text((x+10,y+8),r['question'][':question/difficulty'].split('/')[-1]+' '+r['generation']['template']+' '+str(r['generation']['parameters']),fill='black')
 canvas.save(p/'plot-review.png');print(json.dumps({'basis':b,'new_by_level':new,'candidate_count':len(records),'plot_review':str(p/'plot-review.png')}),flush=True)

if __name__=='__main__' and '--prepare' in sys.argv:prepare()

def verify(p,intent,report):
 assert report[':edb/committed'] and report[':edb/db-before-t']==intent['basis'];check_report(report,p/'receipt-check',intent['source_eid'])
 b=report[':edb/db-after-t'];kp=read(p/'readback',b);before=loads((p/'before.edn').read_text())
 old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']};assert all(now[e]==q for e,q in old.items())
 exclude={':knowledge-point/questions',':knowledge-point/question-generator'};assert {k:v for k,v in before.items() if k not in exclude}=={k:v for k,v in kp.items() if k not in exclude}
 gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
 records=json.loads((p/'generated-published.json').read_text());assert len(now)==len(old)+len(records);byid={str(q[':question/id']):q for q in now.values()}
 for r in records:
  q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q and normalize(q)==ordered(r['question']);validate(r)
 native([{'question':normalize(byid[r['question'][':question/id']]),'knowledge_point':r['knowledge_point']} for r in records],p/'readback-grading')
 assert not transaction([],kp,intent['generator_id'])
 after=counts(kp,b,p/'readback');result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'unchanged_source_questions':len(old),'canonical_example_unchanged':True,'learner_history_unchanged':True,'scoped_additive_datoms_only':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':after};save(p/'verification.json',result);return result

def finish(p,gid,verified,inv):
 c=verified['available_counts_after'];remaining={l:max(0,5-c['distinct_available'][l]) for l in LEVELS};prep=json.loads((p/'preparation.json').read_text())
 result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified.get('basis_after'),'new_questions':verified['new_questions'],'new_by_level':prep['new_by_level'],'supported_levels':list(LEVELS),'unsupported_levels':[],'unsupported_levels_filled':False,'shortage_remaining':remaining,'available_distinct':c['distinct_available'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'source_questions_and_learner_history_preserved':True,'application_contributor':SOURCE,'capability_exception':'The repaired positive exponential is rated moderate by current source evidence; its historic inferred hard generation is suspended. Additional positive mixed/power/third-harmonic and circle-bank profiles are observed evidence only. All three level reserves are supported through the validated remaining families.','legacy_source_exclusions':c['excluded'],'evidence':[str(f.relative_to(ROOT)) for f in [p/'verification.json',p/'commit-intent.json',p/'transaction.edn',p/'commit.edn',p/'preview.edn',p/'preparation.json',p/'source-refresh.json',p/'generated.json',p/'generated-published.json',p/'assets.json',p/'mathematics-validation.json',p/'selected-grading/report.json',p/'readback-grading/report.json',p/'inventory-after.json',HERE/'reference/current-classification.md',HERE/'reference/current-template-extraction.md',HERE/'reference/native/build.json',HERE/'validation.json',HERE/'reference/replenishment/prepared/visual-review.json'] if f.exists()]}
 save(p/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps({k:result[k] for k in ('outcome','new_questions','new_by_level','verified_commit_basis','available_distinct','shortage_remaining')}),flush=True)

def commit():
 full=json.loads((HERE/'validation.json').read_text());assert full['passed'] and full['version']==g.VERSION and full['generator_sha256']==sha(HERE.with_suffix('.py'))
 preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
 prepared=OUT/'prepared';prep=json.loads((prepared/'preparation.json').read_text());assert prep['generator_sha256']==sha(HERE.with_suffix('.py'));assert json.loads((prepared/'visual-review.json').read_text())['passed']
 with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
  print('Waiting for application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application api.lock acquired',flush=True)
  for p in sorted(OUT.glob('basis-*')):
   if not (p/'commit-intent.json').exists():continue
   intent=json.loads((p/'commit-intent.json').read_text());assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE and intent['sha256']==sha(p/'transaction.edn') and intent['exact_edn']==(p/'transaction.edn').read_text()
   assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
   inv=inventory(p/'recovery-inventory.json');assert inv['lineage']==intent['lineage']
   verified=verify(p,intent,DB._commit(intent,p/'transaction.edn',p));finish(p,intent['generator_id'],verified,inventory(p/'inventory-after.json'));return
  inv=inventory(OUT/'inventory-under-lock.json');b=inv['basis'];assert DB.basis()==b;p=OUT/('basis-'+str(b));p.mkdir(exist_ok=True);kp=read(p,b);source_refresh(kp,p,b);(p/'before.edn').write_text(dumps(kp)+'\n')
  print('Source recheck passed at basis '+str(b),flush=True)
  source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],p,'source',b);assert len(source)==1
  gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
  existing=DB.query('[:find (pull ?g [*]) :in $ ?id ?script :where (or-join [?g ?id ?script] [?g :question-generator/id ?id] [?g :question-generator/script ?script])]',[uuid.UUID(gid),SCRIPT],p,'generator-identity',b)
  if existing:assert len(existing)==1 and existing[0][0][':question-generator/script']==SCRIPT;gid=str(existing[0][0][':question-generator/id'])
  save(HERE/'registration.json',{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or existing)})
  c=counts(kp,b,p/'current-inventory');needed={l:max(0,5-c['distinct_available'][l]) for l in LEVELS};print(json.dumps({'basis':b,'available':c['distinct_available'],'missing':needed}),flush=True)
  allrecords=json.loads((prepared/'generated.json').read_text());used={task(q)[0] for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]};records=[];new={l:0 for l in LEVELS};results=[]
  for r in allrecords:
   l=r['question'][':question/difficulty'].split('/')[-1];a=validate(r)
   if new[l]>=needed[l] or a['fingerprint'] in used:continue
   records.append(r);results.append(a);used.add(a['fingerprint']);new[l]+=1
  assert new==needed,('Inventory changed beyond prepared capability; return to preparation',needed,new)
  ids=[uuid.UUID(uid) for r in records for uid in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
  if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],p,'generated-identities',b)
  save(p/'generated.json',records);save(p/'mathematics-validation.json',{'passed':True,'questions':results});published=publish(records,p);native(published,p/'selected-grading')
  save(p/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_version':g.VERSION,'generator_sha256':sha(HERE.with_suffix('.py')),'available_counts':c,'missing_by_level':needed,'new_by_level':new,'asset_hashes':[x['sha256'] for x in json.loads((p/'assets.json').read_text())],'mathematics_validated':True,'actual_grader_validated':True,'source_unchanged':True,'finite_shortages':{l:needed[l]-new[l] for l in LEVELS if needed[l]>new[l]}})
  forms=transaction(published,kp,gid)
  if not forms:
   verified={'passed':True,'basis_after':b,'new_questions':0,'available_counts_after':c};save(p/'verification.json',verified);finish(p,gid,verified,inv);return
  tx=dumps(forms)+'\n';txpath=p/'transaction.edn'
  with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
  assert DB.basis()==b,'Basis changed during preparation'
  r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,text=True,capture_output=True,timeout=55);(p/'preview.log').write_text(r.stderr)
  if r.returncode:raise RuntimeError(r.stderr)
  (p/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert not pr[':edb/committed'] and pr[':edb/db-before-t']==b;check_report(pr,p/'preview-check',source[0][0]);assert DB.basis()==b
  intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'green-area-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'question_uuids':[r['question'][':question/id'] for r in published],'lock':str(ROOT/'.local/learning/requests/math/api.lock')};save(p/'commit-intent.json',intent)
  print('Native preview passed; submitting exact saved request',flush=True)
  verified=verify(p,intent,DB._commit(intent,txpath,p));finish(p,gid,verified,inventory(p/'inventory-after.json'))

if __name__=='__main__' and '--commit' in sys.argv:commit()
