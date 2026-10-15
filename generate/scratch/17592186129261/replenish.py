"""KP-scoped additive replenishment using the application's EDB integration."""
import copy, fcntl, hashlib, importlib.util, json, os, re, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
from capture.scripts.database.images import ImageLibrary
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from serve_graph_explorer import database_environment, image_path
from inventory_jobs import save
from database import Database, QUESTION_PULL
from edn import dumps, loads, kw
spec=importlib.util.spec_from_file_location('validation',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g;S=v.S
KP=g.KP; LEVELS=('easy','moderate','hard'); LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.SOURCE['lineage'];SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT));OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'87abf9f9f7a693632e560ff848e9f2610b57fb4411d05f2f44b8fd79dc72a9e9'
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']));DB.env=database_environment('math');MATH=Path(DB.env['EDB_MATH_ROOT'])
NATIVE=max((p for p in (ROOT/'.local/graph-explorer').glob('learning-*') if p.is_file() and os.access(p,os.X_OK) and 'tests' not in p.name),key=lambda p:p.stat().st_mtime)
QUERY=(OUT/'current-source-query.edn').read_text()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inventory(p):
 r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,capture_output=True,text=True,check=True,timeout=55)
 x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(p,x['data']);return x['data']
def read(p,b):return DB.query(QUERY,[KP],p,'kp',b)[0][0]
def canonical(obj):
 if isinstance(obj,dict):return {str(k):canonical(z) for k,z in obj.items() if k!=':db/id' and '/_' not in k}
 if isinstance(obj,(list,tuple,set)):return sorted((canonical(z) for z in obj),key=lambda z:json.dumps(z,sort_keys=True))
 return str(obj) if isinstance(obj,uuid.UUID) else obj

def normalize(q):
 return {':question/id':str(q[':question/id']),':question/problem':q[':question/problem'],':question/worked-solution':q[':question/worked-solution'],':question/difficulty':str(q[':question/difficulty'][':db/ident']),':question/answer-fields':sorted([{':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':sorted([{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],key=lambda a:a[':answer/id'])} for f in q[':question/answer-fields']],key=lambda f:f[':answer-field/key'])}
def ordered(q):
 q=copy.deepcopy(q);q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
 for f in q[':question/answer-fields']:f[':answer-field/choices'].sort(key=lambda a:a[':answer/id'])
 return q

def printed(q):
 q=copy.deepcopy(q)
 text=q[':question/problem'].replace(r'\dfrac',r'\frac')
 text=re.sub(r'\\frac(\{[^{}]*\}|[a-zA-Z0-9])(\{[^{}]*\}|[a-zA-Z0-9])',lambda m:r'\frac'+''.join(z if z.startswith('{') else '{'+z+'}' for z in m.groups()),text)
 q[':question/problem']=text
 blocks=re.findall(r'\$\$(.*?)\$\$',q[':question/problem'].replace(r'\dfrac',r'\frac'),re.S)
 if not blocks:blocks=re.findall(r'\$(.*?)\$',q[':question/problem'],re.S)
 defs=blocks[0].strip().rstrip(',').replace(r'\qquad','').replace(r'\,','')
 m=re.fullmatch(r'\s*u\s*=\s*(.*?),\s*v\s*=\s*(.*?)\s*',defs,re.S);assert m
 U,V=map(v.parse,m.groups());boundary=blocks[-1].strip().rstrip('.')
 equations=[]
 for part in re.split(r',\s*(?:\\qquad|\\,)?\s*',boundary):
  a,b=part.split('=');equations.append((v.parse(a),v.parse(b)))
 assert len(equations)==4
 return U,V,equations

def fingerprint(q):
 # Exact boundary loci; ignore bank, ordering, seed, layout, coordinate-map scaling.
 _,_,equations=printed(q);rows=[]
 for a,b in equations:
  poly=S.Poly(S.together(a-b).as_numer_denom()[0],g.x,g.y);coefs=poly.terms();lead=coefs[0][1]
  rows.append(str(S.expand(poly.as_expr()/lead)))
 return g.identity(sorted(rows))

def literal_area(q):
 U,V,eqs=printed(q);vals=[]
 for T,(a,b) in zip((U,U,V,V),eqs):
  symbol=g.x if a==g.x else g.y;assert a==symbol
  vals.append(S.simplify(T.subs(symbol,b)))
 assert all(z.is_number for z in vals)
 L,H=sorted(vals[:2]);j,k=sorted(vals[2:]);assert L<H and j<k
 jac=S.det(S.Matrix([[S.diff(U,g.x),S.diff(U,g.y)],[S.diff(V,g.x),S.diff(V,g.y)]]))
 inv=S.solve([g.u-U,g.v-V],(g.x,g.y)) if not jac.free_symbols else None
 if inv:
  area=(H-L)*(k-j)/abs(jac)
  if 'first quadrant' in q[':question/problem']:
   poly=[(L,j),(H,j),(H,k),(L,k)]
   for expr in (inv[g.x],inv[g.y]):
    nxt=[]
    for a,b in zip(poly,poly[1:]+poly[:1]):
     fa=expr.subs({g.u:a[0],g.v:a[1]});fb=expr.subs({g.u:b[0],g.v:b[1]})
     if fa>=0:nxt.append(a)
     if (fa<0<=fb) or (fb<0<=fa):
      t=fa/(fa-fb);nxt.append(tuple(S.simplify(a[i]+t*(b[i]-a[i])) for i in (0,1)))
    poly=nxt
   area=abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(poly,poly[1:]+poly[:1])))/2/abs(jac)
 else:
  blocks=re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S)
  J=v.parse(blocks[9].strip().rstrip('.').split('=')[-1]);assert v.equal(J.subs({g.u:U,g.v:V},simultaneous=True)*jac,1)
  # All observed nonlinear maps are monomials: invertible in positive quadrant
  # since the exponent matrix has nonzero determinant. Bounds are positive.
  assert min(L,j)>0
  exponent=S.Matrix([[S.simplify(g.x*S.diff(T,g.x)/T),S.simplify(g.y*S.diff(T,g.y)/T)] for T in (U,V)])
  assert exponent.det()!=0 and not any(z.free_symbols for z in exponent)
  area=S.integrate(S.integrate(abs(J),(g.v,j,k)),(g.u,L,H))
 return S.simplify(area)

def source_checks(q):
 A=literal_area(q);f=q[':question/answer-fields'][0];values=[v.parse(a[':answer/value']) for a in f[':answer-field/choices']]
 assert all(not v.equal(a,b) for i,a in enumerate(values) for b in values[:i])
 correct=[a for a,z in zip(f[':answer-field/choices'],values) if v.equal(z,A)]
 assert len(correct)==1 and str(correct[0][':answer/id'])==str(f[':answer-field/correct'][':answer/id']),('Source key differs from literal first-quadrant area',str(A))
 blocks=re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S)
 final=blocks[-1].split('=')[-1].replace(r'\end{aligned}','').strip().rstrip('.')
 assert v.equal(v.parse(final),A)
 return str(A)

def local(r):
 r=copy.deepcopy(r)
 for p in OUT.glob('basis-*/assets.json'):
  for source,a in json.loads(p.read_text()).items():
   assert sha(MATH/a['path'])==a['sha256']
   for k in (':question/problem',':question/worked-solution'):r['question'][k]=r['question'][k].replace(a['path'],source)
 return r

def validate(r):
 r=local(r);m=r['generation'];q=r['question'];level=q[':question/difficulty'].split('/')[-1]
 assert level in LEVELS and m['eligible_for_learning'] and not m['evidence_only']
 assert r['knowledge_point']=={'db_id':KP,'id':g.REC[':knowledge-point/id'],'title':g.REC[':knowledge-point/title']}
 replay=g.generate(level,seed=m['seed'],template=m['template'],parameters=m['parameters'],profile=m['profile'])
 assert ordered(replay['question'])==ordered(q) and replay['generation']==m
 v.check_record(r);v.check_plot(m['plot']['path'],m['plot']['spec']);return fingerprint(q)

def native(records,p):
 save(p/'input.json',[v.fixture(r,r['question'][':question/id']) for r in records])
 if not records:return
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(p/'input.json'),str(p/'report.json')],capture_output=True,text=True,check=True,timeout=55)
 report=json.loads((p/'report.json').read_text());assert report['documented_unresolved_checks']==0

def counts(kp,b,p):
 p.mkdir(parents=True,exist_ok=True)
 shown=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]',[KP,LEARNER],p,'shown',b,history=True)
 reserved=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]',[KP,LEARNER],p,'reserved',b)
 unavailable={z[0] for z in shown+reserved};levels={l:set() for l in LEVELS};records=[];excluded=[]
 known={r['question'][':question/id']:r for f in OUT.glob('basis-*/generated-published.json') for r in json.loads(f.read_text())}
 for q in kp[':knowledge-point/questions']:
  level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
  if q[':db/id'] in unavailable or q.get(':knowledge-point/_canonical-example') or level not in LEVELS or not q.get(':question/worked-solution') or any(not f.get(':answer-field/correct') for f in q[':question/answer-fields']):
   excluded.append({'db_id':q[':db/id'],'source_id':q.get(':question/math-academy-id'),'reason':'shown/reserved, canonical, unrated, or incomplete'});continue
  if ':question/math-academy-id' in q:
   try:A=source_checks(q)
   except AssertionError as e:
    excluded.append({'db_id':q[':db/id'],'source_id':q[':question/math-academy-id'],'reason':str(e)});continue
   r={'question':normalize(q)}
  else:
   r=known[str(q[':question/id'])];assert normalize(q)==ordered(r['question']);validate(r)
  levels[level].add(fingerprint(q));records.append(r)
 native(records,p/'actual-grading')
 result={'basis':b,'distinct_available':{l:len(xs) for l,xs in levels.items()},'excluded':excluded,'unavailable':sorted(unavailable),'validated_question_ids':[r['question'][':question/id'] for r in records],'deduplication':'Normalized exact boundary loci; seed, identity, bank, option order and coordinate-map scaling ignored'}
 save(p/'counts.json',result);return result

def transaction(records, kp, gid):
    forms = []
    for rec in records:
        q = rec['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:
                forms.append({kw('db/id'):a[':answer/id'], kw('answer/id'):uuid.UUID(a[':answer/id']), kw('answer/type'):kw(a[':answer/type']), kw('answer/value'):a[':answer/value'], kw('db/ensure'):kw('answer/validate')})
            forms.append({kw('db/id'):f[':answer-field/id'], kw('answer-field/id'):uuid.UUID(f[':answer-field/id']), kw('answer-field/key'):f[':answer-field/key'], kw('answer-field/type'):kw(f[':answer-field/type']), kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']], kw('answer-field/correct'):f[':answer-field/correct'][1], kw('db/ensure'):kw('answer-field/validate')})
        forms.append({kw('db/id'):q[':question/id'], kw('question/id'):uuid.UUID(q[':question/id']), kw('question/problem'):q[':question/problem'], kw('question/worked-solution'):q[':question/worked-solution'], kw('question/difficulty'):kw(q[':question/difficulty']), kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']], kw('db/ensure'):kw('question/validate')})
    gen = kp.get(':knowledge-point/question-generator')
    if gen is None:
        forms.extend([{kw('db/id'):'generator', kw('question-generator/id'):uuid.UUID(gid), kw('question-generator/script'):SCRIPT}, [kw('db/add'), KP, kw('knowledge-point/question-generator'), 'generator']])
    else:
        assert str(gen[':question-generator/id']) == gid and gen[':question-generator/script'] == SCRIPT
    if records:
        forms.append({kw('db/id'):KP, kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms:
        forms.append([kw('db/ensure'), KP, kw('knowledge-point/validate')])
    return forms

def check_report(report, path, source):
    attrs = {e:str(a) for e,a in DB.attributes(path, report[':edb/db-before-t'])}
    new = set(report[':edb/tempids'].values())
    allowed = {':question/id', ':question/problem', ':question/worked-solution', ':question/difficulty', ':question/answer-fields', ':answer-field/id', ':answer-field/key', ':answer-field/type', ':answer-field/choices', ':answer-field/correct', ':answer/id', ':answer/type', ':answer/value', ':question-generator/id', ':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s == source and added, 'Unexpected attribution or retraction'
        name = attrs[a]
        if e == KP:
            assert name in (':knowledge-point/questions', ':knowledge-point/question-generator')
        elif name != ':db/txInstant':
            assert e in new and name in allowed, name

def select(kp,needed,p):
 supplied=JOB.with_suffix('.generated');data=json.loads(supplied.read_text()) if supplied.exists() else {};instances=data.get('instances',[]) if isinstance(data,dict) else data
 assert isinstance(instances,list)
 for r in instances:validate(r)
 save(p/'supplied-status.json',{'exists':supplied.exists(),'validated_instances':len(instances),'generator_error':data.get('generatorError') if isinstance(data,dict) else None})
 used={fingerprint(q) for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]};records=[];added={l:0 for l in LEVELS}
 for level in LEVELS:
  candidates=[r for r in instances if r['question'][':question/difficulty'].endswith('/'+level)]
  for n in range(100):
   if added[level]>=needed[level]:break
   r=candidates[n] if n<len(candidates) else g.generate(level,int(JOB.name[:8],16)+n)
   fp=fingerprint(r['question'])
   if fp in used:continue
   validate(r);records.append(r);used.add(fp);added[level]+=1
 save(p/'generated.json',records);native(records,p/'selected-grading')
 (p/'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in records)+'\n')
 published=copy.deepcopy(records);images=ImageLibrary(MATH,p)
 for r in published:
  for k in (':question/problem',':question/worked-solution'):r['question'][k]=images.text(r['question'][k])
 for source,a in images.saved.items():assert sha(MATH/a['path'])==a['sha256'] and image_path(a['path'],MATH)==(MATH/a['path']).resolve()
 save(p/'assets.json',images.saved);save(p/'generated-published.json',published)
 ids=[]
 for r in records:
  ids.append(uuid.UUID(r['question'][':question/id']))
  for f in r['question'][':question/answer-fields']:
   ids.append(uuid.UUID(f[':answer-field/id']));ids.extend(uuid.UUID(a[':answer/id']) for a in f[':answer-field/choices'])
 assert len(ids)==len(set(ids))
 if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],p,'identity-collisions',DB.basis())
 return published,added

def verify(p,intent,report):
 assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis'];check_report(report,p/'receipt-check',intent['source_eid'])
 b=report[':edb/db-after-t'];kp=read(p/'readback',b);before=loads((p/'before.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
 assert all(now[e]==q for e,q in old.items())
 excluded={':knowledge-point/questions',':knowledge-point/question-generator'}
 assert {k:v for k,v in before.items() if k not in excluded}=={k:v for k,v in kp.items() if k not in excluded}
 gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
 records=json.loads((p/'generated-published.json').read_text());assert len(now)==len(old)+len(records);byid={str(q[':question/id']):q for q in now.values()}
 for r in records:
  q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q and normalize(q)==ordered(r['question']);validate(r)
 assert not transaction([],kp,intent['generator_id'])
 after=counts(kp,b,p/'readback');prep=json.loads((p/'preparation.json').read_text())
 for l in LEVELS:assert after['distinct_available'][l]==prep['counts_before']['distinct_available'][l]+prep['new_by_level'][l]
 result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'all_previous_questions_preserved':len(old),'canonical_example_unchanged':True,'learner_history_unchanged':True,'only_scoped_additive_content_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'counts_after':after}
 save(p/'verification.json',result);return result

def finish(p,gid,verified,inv):
 prep=json.loads((p/'preparation.json').read_text());remaining={l:max(0,5-verified['counts_after']['distinct_available'][l]) for l in LEVELS};caps=json.loads((HERE/'capabilities.json').read_text())
 result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'generator_sha256':sha(HERE.with_suffix('.py')),'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'new_by_level':prep['new_by_level'],'supported_levels':list(LEVELS),'difficulty_basis':caps['difficulty_basis'],'available_counts_before':prep['counts_before']['distinct_available'],'available_counts_after':verified['counts_after']['distinct_available'],'shortage_remaining':remaining,'capability_exceptions':caps['exceptions'],'unsupported_levels_filled':False,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(x.relative_to(ROOT)) for x in (p/'verification.json',p/'commit-intent.json',p/'commit.edn',p/'preview.edn',p/'transaction.edn',p/'preparation.json',p/'inventory-after.json',p/'selected-grading/report.json',p/'readback/actual-grading/report.json',p/'generated-published.json',p/'assets.json',HERE/'validation.json',HERE/'capabilities.json',OUT/'current-classification.md') if x.exists()],'note':'Existing source questions and learner history preserved. Two source quadrant/key conflicts excluded from validated inventory; one incomplete unrated source remains explicit. Newer source-only families classified but not claimed as replayed by the frozen sampler.'}
 save(p/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','available_counts_after','remaining_jobs')}),flush=True)

def main():
 qa=json.loads((ROOT/'generate/runs/current/qa/17592186129261.json').read_text());validation=json.loads((HERE/'validation.json').read_text())
 assert qa['parent_review']=='passed' and qa['generator_sha256']==sha(HERE.with_suffix('.py')) and validation['status']=='pass'
 # Verify the frozen package evidence actually used, without rerunning unrelated work.
 for name in ('source.json','template-extraction.md','classification.md','plot-extraction.md','validate.py','validation.json'):
  assert sha(HERE/name)==qa['root_artifact_hashes'][name],name
 assert validation['engine_binary_sha256']==sha(ROOT/'generate/runs/current/check-engine')
 preview=preview_executable(SimpleNamespace(math_root=MATH,repo_root=ROOT,preview_bin=None),threading.Event())
 print('Validated frozen generator and native grader; acquiring application lock.',flush=True)
 with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  for p in sorted(OUT.glob('basis-*')):
   if (p/'commit-intent.json').exists():
    intent=json.loads((p/'commit-intent.json').read_text());assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['database']=='math'
    assert intent['transaction_sha256']==sha(p/'transaction.edn') and intent['exact_edn']==(p/'transaction.edn').read_text()
    assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
    report=DB._commit(intent,p/'transaction.edn',p);verified=verify(p,intent,report);finish(p,intent['generator_id'],verified,inventory(p/'inventory-after.json'));return
  inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b;p=OUT/('basis-'+str(b));p.mkdir(exist_ok=True);kp=read(p,b)
  assert str(kp[':knowledge-point/id'])==g.REC[':knowledge-point/id']
  initial=loads((OUT/'initial-before.edn').read_text());oldsource={q[':question/math-academy-id']:q for q in initial[':knowledge-point/questions'] if ':question/math-academy-id' in q};source={q[':question/math-academy-id']:q for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q}
  assert canonical(oldsource)==canonical(source),'New source evidence requires reclassification'
  assert canonical(initial[':knowledge-point/canonical-example'])==canonical(kp[':knowledge-point/canonical-example'])
  (p/'before.edn').write_text(dumps(kp)+'\n');contributor=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],p,'contributor',b);assert len(contributor)==1
  gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else g.uid('question-generator')
  before=counts(kp,b,p/'counts-before');needed={l:max(0,5-before['distinct_available'][l]) for l in LEVELS};print('Basis',b,'validated counts',before['distinct_available'],'needed',needed,flush=True)
  records,added=select(kp,needed,p);assert DB.basis()==b
  save(p/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'counts_before':before,'missing_by_level':needed,'new_by_level':added,'new_questions':len(records),'source_evidence_rechecked':True,'asset_hashes':json.loads((p/'assets.json').read_text()),'all_new_identities_absent':True,'finite_remaining':{l:max(0,needed[l]-added[l]) for l in LEVELS}})
  if '--prepare-only' in sys.argv:print('Prepared',len(records),'questions at basis',b,flush=True);return
  forms=transaction(records,kp,gid)
  if not forms:
   result={'passed':True,'basis_after':b,'new_questions':0,'counts_after':before,'no_changes':True};save(p/'verification.json',result);finish(p,gid,result,inv);return
  txpath=p/'transaction.edn';tx=dumps(forms)+'\n'
  with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
  r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,timeout=55)
  (p/'preview.stderr').write_text(r.stderr);assert r.returncode==0,r.stderr
  (p/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;check_report(pr,p/'preview-check',contributor[0][0]);assert DB.basis()==b
  intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'basis':b,'expected_basis':b,'request_key':'given-map-area-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
  save(p/'commit-intent.json',intent);print('Native preview passed; committing exact retained request at basis',b,flush=True)
  report=DB._commit(intent,txpath,p);verified=verify(p,intent,report);finish(p,gid,verified,inventory(p/'inventory-after.json'))
if __name__=='__main__':main()
