import sys,json,subprocess,pathlib,collections,shutil,hashlib
sys.dont_write_bytecode=True
from audit import R,B,P,ROOT,g,save,expr,eq,promptdata,x,hashpackage,s
py=str(ROOT/'.venv/bin/python');commandlog=[]
samples=json.load(open(R/'independent-samples.json'))
for label,rows in [('independent',[r for r in samples if r['question'][':question/difficulty'].endswith('/easy')]),('batch',json.load(open(R/'runner-batch.json')))]:
 save(label+'-delivery-input.json',rows)
 cmd=[py,str(ROOT/'generate/pipeline/check_delivery.py'),'--input',str(R/(label+'-delivery-input.json')),'--source',str(B/'source/source.json'),'--inventory',str(B/'source/inventory.json'),'--difficulty','easy','--output',str(R/('delivery-'+label)),'--asset-root',str(R),'--math-root','/media/jake/SSD/EDB/math']
 out=subprocess.run(cmd,capture_output=True,text=True);commandlog.append({'command':cmd,'exit_code':out.returncode,'stdout':out.stdout,'stderr':out.stderr})
save('delivery-commands.json',commandlog)
# Correct mathematical multiset comparison: expand/factor forms do not change source fidelity.
source=json.load(open(B/'source/source.json'))['material']['kp'][':knowledge-point/questions'];replays=json.load(open(R/'source-replays.json'));results=[]
for r in replays:
 q=next(v for v in source if v[':question/math-academy-id']==r['generation']['template']);banks=[]
 for f in q[':question/answer-fields']:
  rf=next(v for v in r['question'][':question/answer-fields'] if v[':answer-field/key']==f[':answer-field/key']);remaining=[expr(a[':answer/value']) for a in rf[':answer-field/choices']];matched=True
  for a in f[':answer-field/choices']:
   v=expr(a[':answer/value']);i=next((i for i,b in enumerate(remaining) if eq(v,b)),None)
   if i is None:matched=False;break
   remaining.pop(i)
  banks.append({'key':f[':answer-field/key'],'count':len(f[':answer-field/choices']),'mathematical_multiset_match':matched and not remaining})
 norm=lambda z:z.replace(r'\left','').replace(r'\right','')
 solution=q.get(':question/worked-solution');rs=r['question'][':question/worked-solution']
 results.append({'source_id':q[':question/id'],'template':r['generation']['template'],'prompt_presentation_normalized':norm(q[':question/problem'])==norm(r['question'][':question/problem']),'banks':banks,'solution_exact':solution==rs if solution else None,'solution_stage_sequence':[z for z in ['standard form','integrating factor','Multiplying','integrate','initial condition','Therefore'] if z in rs],'source_missing_solution':not bool(solution)})
save('source-replay-results.json',results)
# Finite easy domain: boundaries, valid bank exclusions, and pre/post rejection support.
domain=[];valid=[]
for b in range(1,7):
 for h in range(-6,7):
  try:
   r=g.generate('easy',seed=9100,parameters={'a':1,'b':b,'h':h});valid.append(r);domain.append({'b':b,'h':h,'accepted':True,'id':r['question'][':question/id']})
  except Exception as e:domain.append({'b':b,'h':h,'accepted':False,'reason':str(e)})
save('easy-domain-results.json',domain);save('easy-domain-records.json',valid)
# Strict accepting and rejecting role changes: forbidden a=2, and observed h dependence.
probes=[]
for tid,(lev,fam) in g.TEMPLATES.items():
 rows=[r for r in samples if r['generation']['template']==tid]
 if not rows:continue
 first=rows[0];f=first['question'][':question/answer-fields'][0];correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
 successes=sum(eq(expr(next(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'] if a[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1])),expr(correct)) for r in rows)
 probes.append({'template':tid,'strategy':'Always select '+correct,'correct':successes,'total':len(rows),'baseline':0.25,'disposition':'defect' if tid=='easy_constant' else 'bounded probe; not independently classified'})
save('shortcut-results.json',probes)
# Reproduce generated inventory records by displayed constant b,h; original source questions excluded by source IDs.
inv=json.load(open(B/'source/inventory.json'));sourceids={q[':question/id'] for q in source};reproduced=[];affected=[];invchecks=[]
for q in inv['questions']:
 if q[':question/id'] in sourceids:continue
 r0={'question':q}
 try:
  p,qq,t,h=promptdata(r0)
  if p!=1 or qq.free_symbols or t!=0:invchecks.append({'id':q[':question/id'],'tested':False,'reason':'outside easy constant weakness'});continue
  r=g.generate('easy',seed=0,parameters={'a':1,'b':int(qq),'h':int(h)})
  identity=q[':question/id']==r['question'][':question/id'];prompt=q[':question/problem']==r['question'][':question/problem'];sol=q[':question/worked-solution']==r['question'][':question/worked-solution'];banks=all({a[':answer/id'] for a in f[':answer-field/choices']}=={a[':answer/id'] for a in next(f2 for f2 in q[':question/answer-fields'] if f2[':answer-field/key']==f[':answer-field/key'])[':answer-field/choices']} for f in r['question'][':question/answer-fields'])
  invchecks.append({'id':q[':question/id'],'identity_match':identity,'prompt_match':prompt,'solution_match':sol,'answer_ids_match':banks,'generation_metadata_available_in_inventory':False,'reproduction_seed':0})
  if identity and prompt and sol and banks:
   reproduced.append(r);affected.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'finding':'easy_constant always keys e^x for field-1; choose e^x without inspecting the ODE','reproduction':"PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python delivery_and_inventory.py (generates easy seed=0, parameters="+str(r['generation']['parameters'])+")",'evidence_path':'generated-records.json'})
 except Exception as e:invchecks.append({'id':q[':question/id'],'tested':False,'error':str(e)})
save('generated-records.json',reproduced);save('affected-inventory.json',{'affected_questions':affected});save('inventory-results.json',{'basis':inv['basis'],'question_count':len(inv['questions']),'original_sources_excluded':len(sourceids),'checks':invchecks,'limitation':'Inventory has no generation metadata. Reproduced full generator records match stored question UUID, exact prompt, solution and answer UUID sets. Seed 0 is a deterministic reconstruction seed, not a recovered historical seed; parameters are inferred from the stored prompt.'})
# Learner selection: faithful selection of fixed known candidate pool within easy band.
accepted=json.load(open(R/'delivery-independent/accepted.json'));sels=[]
for seed in ['review-'+str(i) for i in range(16)]:
 pool=sorted(accepted,key=lambda r:r['question'][':question/id']);bits=int.from_bytes(hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()[8:16],'big')>>11
 if pool:
  r=pool[int((bits/(1<<53))*len(pool))];sels.append({'seed':seed,'question_id':r['question'][':question/id'],'integrating_factor':next(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'] if a[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1])})
save('selection-results.json',{'algorithm':'question_selection.rs select: SHA256 stable uniform within a chosen nonempty band; fresh candidate membership supplied by caller','scope':'Conditional easy-band selection from accepted records; UUID sorted surrogate entity IDs. Actual entity order/history/weights unavailable. Every candidate has identical IF so all subsets/orderings share the shortcut.','cases':sels})
# Relocate the whole package under evidence and import with a different cwd.
rel=R/'relocated-package';shutil.copytree(P,rel,dirs_exist_ok=True)
code='import importlib.util,json,sys;sys.dont_write_bytecode=True;s=importlib.util.spec_from_file_location("rel",'+repr(str(rel/'17592186087879.py'))+');g=importlib.util.module_from_spec(s);s.loader.exec_module(g);print(json.dumps(g.generate("easy",seed=70401),sort_keys=True))'
out=subprocess.run([py,'-c',code],cwd=R,capture_output=True,text=True);save('relocation-results.json',{'command':[py,'-c',code],'exit_code':out.returncode,'stderr':out.stderr,'same_record':json.loads(out.stdout)==samples[0] if out.returncode==0 else False,'external_output':'No images or external outputs generated; data loaded relative to __file__.'})
save('package-integrity.json',{'unchanged':hashpackage()==json.load(open(R/'package-before.json')),'files':len(hashpackage())})
print(json.dumps({'delivery':commandlog,'valid_easy_tasks':len(valid),'affected_inventory':len(affected),'source_replay_failures':[r for r in results if not r['prompt_presentation_normalized'] or not all(b['mathematical_multiset_match'] for b in r['banks'])],'package_unchanged':hashpackage()==json.load(open(R/'package-before.json'))},indent=2))
