"""Reproduce the feedback; test exchangeability, source fidelity and real delivery/grading.
Run with the job Python from this workspace. All writes stay below evidence/visual-repair.
"""
import copy,collections,hashlib,importlib.util,importlib.metadata,json,math,os,random,shutil,subprocess,sys
from fractions import Fraction as F
from pathlib import Path
from verify_record import g,check
from probe_banks import probes
W=Path(__file__).resolve().parents[1]; E=W/'evidence/visual-repair'; E.mkdir(exist_ok=True)
REPO=Path('/home/jake/Developer/Course_Academy'); JOB=W.parent; S=JOB/'source'; AS=E/'assets'
os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']=str(AS)
sys.dont_write_bytecode=True

def save(name,x): (E/name).write_text(json.dumps(x,indent=2)+'\n')
def field(r):return r['question'][':question/answer-fields'][0]
def rows(r):return [[math.inf if x=='oo' else F(x) for x in r['generation']['choice_geometry'][a[':answer/value']]] for a in field(r)[':answer-field/choices']]
def ci(r):return next(i for i,a in enumerate(field(r)[':answer-field/choices']) if a[':answer/id']==field(r)[':answer-field/correct'][1])
def correct(r):return rows(r)[ci(r)]
def exact(t,p):
 a,b,d=F(p['a']),F(p.get('b',1)),F(p.get('d',1));out=[]
 for x,y in p['points']:
  x,y=F(x),F(y)
  out.append({'constant_product':lambda:a-b*x*y,'quadratic_linear':lambda:a*x*x-b*y,'rational_square':lambda:a*y*y/x,'two_quadratic':lambda:a*x*x-b*y*y,'affine_fraction':lambda:(a*x+b*y)/d,'affine':lambda:a*x+b*y}[t]())
 return out

def verify(r):
 check(r); m=r['generation'];assert correct(r)==exact(m['template'],m['parameters'])
 # Complete authored bank, including actual PNG sidecar endpoints checked by check().
 if m.get('bank_parameters'):
  assert {tuple(row) for row in rows(r)}=={tuple(exact(m['template'],p)) for p in m['bank_parameters']}
 return r

def mirror(r):
 rr=rows(r);pairs=[(i,j) for i in range(5) for j in range(i) if all(a==-b for a,b in zip(rr[i],rr[j]))]
 out={'question_id':r['question'][':question/id'],'template':r['generation']['template'],'pairs':pairs,'correct_index':ci(r)}
 if len(pairs)==1:
  pair=pairs[0];sg=lambda x:(x>0)-(x<0)
  scores={i:sum(sg(a)==sg(b) and a!=0 for j in range(5) if j not in pair for a,b in zip(rr[i],rr[j])) for i in pair}
  winners=[i for i in pair if scores[i]==max(scores.values())]
  if len(winners)==1:out.update(predicted=winners[0],success=winners[0]==ci(r))
 return out

def summarize(rs):
 out={'basic':probes(rs),'mirror':{}}
 for t in g.TEMPLATES:
  pp=[mirror(r) for r in rs if r['generation']['template']==t];active=[p for p in pp if 'predicted' in p]
  out['mirror'][t]={'total':len(pp),'decisive':len(active),'success':sum(p['success'] for p in active),'cases':pp}
 return out

# Preserve and reproduce the prior feedback before the repair.
sp=importlib.util.spec_from_file_location('old',W/'evidence/generator-before-visual-repair.py');old=importlib.util.module_from_spec(sp)
# Snapshot lives in evidence; the runtime data root remains the actual package data.
source=(W/'evidence/generator-before-visual-repair.py').read_text().replace("HERE=Path(__file__).resolve().with_suffix('')", "HERE=Path("+repr(str(W/'17592186172038'))+")")
exec(compile(source,str(W/'evidence/generator-before-visual-repair.py'),'exec'),old.__dict__)
before=old.generate('easy',73300,template='rational_square');assert mirror(before).get('success') is True
save('before-records.json',[before]);save('before-shortcut.json',mirror(before))

raw=json.loads((S/'source.json').read_text())['material']['kp'][':knowledge-point/questions'];raw={q[':question/math-academy-id']:q for q in raw}
raster=json.loads((W/'17592186172038/source-raster.json').read_text());sources=[];fidelity=[]
for sid,(t,p,_) in g.PROFILES.items():
 rec=verify(g.generate('easy',seed=73071,profile=sid,parameters=p));sources.append(rec)
 assert rec['question'][':question/problem']==raw[sid][':question/problem']
 _,bank=g.banks(t,p,sid);obs=[v for v in raster if v['source_id']==sid]
 assert {x['asset'] for x in obs}=={a[':answer/value'] for a in raw[sid][':question/answer-fields'][0][':answer-field/choices']}
 for row,v in zip(bank,obs):
  for value,approx in zip(row,v['raster_slopes']):assert approx=='inf' if value==g.sp.oo else abs(math.atan(float(value))-math.atan(approx))<.06
 key=raw[sid][':question/answer-fields'][0].get(':answer-field/correct')
 if key:assert key[':answer/value']==obs[bank.index(g.banks(t,p,sid)[0])]['asset']
 if raw[sid].get(':question/worked-solution'):
  import re
  norm=lambda s:re.sub(r'!\[\]\([^)]*\)','<IMAGE>',re.sub(r'\\begin\{aligned\}.*?\\end\{aligned\}','<ROWS>',s,flags=re.S))
  assert norm(raw[sid][':question/worked-solution'])==norm(rec['question'][':question/worked-solution'])
 fidelity.append({'source':sid,'complete_options':5,'stored_key_matched':bool(key),'inferred_key':not bool(key)})
save('source-replays.json',sources);save('source-fidelity.json',fidelity)
print('source replay: 7 banks / 35 options',flush=True)

records=[];controls=[];normal=[];groups=[];invalid=[]
for ti,t in enumerate(g.TEMPLATES):
 for j in range(6):normal.append(verify(g.generate('easy',73100+100*ti+j,template=t)))
 base=normal[-6];bm=base['generation'];bank=bm['bank_parameters'];fixed=[]
 for j,p in enumerate(bank):
  rr=verify(g.generate('easy',1000+ti,template=t,parameters=p,bank_parameters=bank));fixed.append(rr)
 assert len({tuple(correct(r)) for r in fixed})==5
 assert len({tuple(sorted(tuple(x) for x in rows(r))) for r in fixed})==1
 assert len({r['question'][':question/problem'] for r in fixed})==5
 # Same image-only strategy has exactly one success across all five possible keys.
 stats=summarize(fixed)
 for v in stats['basic'][t]['strategies'].values():assert abs(v['successes']-1)<.002
 decisive=[mirror(r) for r in fixed if 'predicted' in mirror(r)]
 assert not decisive or sum(x['success'] for x in decisive)==1
 controls+=fixed
 # A single changed point: keep equation and four coefficient alternatives fixed.
 found=None
 for pt in [[x,y] for x in range(-4,5) for y in range(-4,5) if t!='rational_square' or x!=0]:
  pp=copy.deepcopy(bm['parameters']);pp['points'][ti%3]=pt
  alt=[{**p,'points':pp['points']} for p in bank]
  try:
   rr=g.generate('easy',1000+ti,template=t,parameters=pp,bank_parameters=alt)
   if correct(rr)[ti%3]==correct(base)[ti%3]:continue
   found=verify(rr);break
  except ValueError:pass
 assert found
 assert all(correct(base)[i]==correct(found)[i] for i in range(3) if i!=ti%3)
 controls.append(found)
 irr=verify(g.generate('easy',2000+ti,template=t,parameters=bm['parameters'],bank_parameters=bank))
 same=verify(g.generate('easy',3000+ti,template=t,parameters=bm['parameters'],bank_parameters=bank))
 assert irr['question'][':question/id']==same['question'][':question/id'] and correct(irr)==correct(same)
 controls += [irr,same]
 groups.append({'template':t,'fixed_bank_ids':[r['question'][':question/id'] for r in fixed],'five_distinct_correct_geometries':True,'point_base':base['question'][':question/id'],'point_changed':found['question'][':question/id'],'changed_index':ti%3,'irrelevant_reordering_same_id':True,'conditional_cue_scores':stats})
 print('validated',t,'fresh 6; fixed bank 5 keys; point/reordering',flush=True)
# Exercise every decisive fresh reflected-pair subgroup under all five possible
# equation assignments, rather than treating its sparse fresh hit rate as proof.
for base in normal:
 if 'predicted' not in mirror(base):continue
 t=base['generation']['template'];bank=base['generation']['bank_parameters']
 fixed=[verify(g.generate('easy',4000,template=t,parameters=p,bank_parameters=bank)) for p in bank]
 pp=[mirror(r) for r in fixed];assert len(pp)==5 and all('predicted' in v for v in pp)
 assert sum(v['success'] for v in pp)==1
 controls+=fixed
 groups.append({'template':t,'probe':'decisive reflected-pair subgroup','fixed_bank_ids':[r['question'][':question/id'] for r in fixed],'five_distinct_correct_geometries':True,'conditional_cue_scores':summarize(fixed)})
records=normal+controls
for t,p in [('rational_square',{'a':1,'points':[[0,1],[1,2],[2,3]]}),('affine',{'a':1,'b':2,'points':[[1,1],[1,1],[2,2]]}),('affine',{'a':1,'b':2,'points':[[5,1],[1,2],[2,3]]}),('rational_square',{'a':1,'points':[[-1,0],[1,0],[2,0]]})]:
 try:g.generate('easy',template=t,parameters=p)
 except ValueError as e:invalid.append({'template':t,'parameters':p,'rejected':str(e)})
 else:raise AssertionError('invalid accepted')
save('invalid.json',invalid);save('normal-records.json',normal);save('controlled-records.json',controls);save('counterfactuals.json',groups)
save('delivery-input.json',records);save('shortcut-before-delivery.json',summarize(normal));save('all-shortcuts.json',summarize(records))
subprocess.run([sys.executable,str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(E/'delivery-input.json'),'--source',str(S/'source.json'),'--inventory',str(S/'inventory.json'),'--difficulty','easy','--output',str(E/'delivery'),'--asset-root',str(AS),'--math-root','/media/jake/SSD/EDB/math'],check=True,stdout=(E/'delivery.log').open('w'),stderr=subprocess.STDOUT)
accepted=json.loads((E/'delivery/accepted.json').read_text())
# Bind the publisher's localized PNGs back to geometry by file bytes, not option IDs.
geom={hashlib.sha256(Path(path).read_bytes()).hexdigest():row for r in records for path,row in r['generation']['choice_geometry'].items()}
for rr in accepted:
 for a in field(rr)[':answer-field/choices']:
  path=a[':answer/value'];rr['generation']['choice_geometry'][path]=geom[Path(path).stem]
save('delivered-with-geometry.json',accepted);save('shortcut-after-delivery.json',summarize(accepted))
accepted_by={g.uid(r['generation']['content_fingerprint']):r for r in accepted}
for group in groups:
 subset=[accepted_by[qid] for qid in group['fixed_bank_ids']]
 assert len(subset)==5
 group['post_delivery_cue_scores']=summarize(subset)
 for name,v in probes(subset)[group['template']]['strategies'].items():
  # Dedup can retain the earlier normal record's independent option shuffle.
  # Geometry cues must remain exactly 1/5; report actual position counts separately.
  if not name.startswith('position_'):assert abs(v['successes']-1)<.002
 assert not (active:=[mirror(r) for r in subset if 'predicted' in mirror(r)]) or sum(v['success'] for v in active)==1
save('counterfactuals.json',groups)
# All answers and stale prior correct image under changed equation, batched once.
cases=[]
for r in sources+records+accepted:
 f=field(r);cases.append({'label':r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if i==ci(r) else 'rejected','purpose':'independent equation and PNG endpoint check; includes fixed-bank stale images'} for i,a in enumerate(f[':answer-field/choices'])]})
save('engine-input.json',cases)
subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(E/'engine-input.json'),str(E/'engine-report.json')],check=True,stdout=(E/'engine.log').open('w'),stderr=subprocess.STDOUT)
# Captured policy: uniform within a rated band. Enumerate all candidates; no live history.
selection=[]
for i in range(len(accepted)):
 seed='visual-repair/'+str(i);bits=int.from_bytes(hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()[8:16],'big')>>11
 index=min(int((bits/(1<<53))*len(accepted)),len(accepted)-1)
 selection.append({'seed':seed,'fixture_entity':index+1,'question_id':accepted[index]['question'][':question/id']})
save('selection.json',{'fixtures':selection,'all_accepted_candidates_eligible':len(accepted),'no_policy_first_entity':1,'limits':'Read-only reproduction of question_selection.rs uniform easy-band index on synthetic sorted entity IDs. Live learner history, freshness and future database IDs are unavailable; unconfigured policy selects smallest entity. No database writes.'})
# One copy, two deterministic relocated CLI runs, actual runner asset binding.
manifest=json.loads((W/'package.json').read_text());assert manifest['dependencies']=={'python':sys.version.split()[0],'packages':{p:importlib.metadata.version(p) for p in ('sympy','matplotlib')}}
root=E/'runtime';root.mkdir(exist_ok=True);output=E/'outside/runtime-output'
for name in manifest['files']:
 dst=root/name;dst.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(W/name,dst)
cmd=[sys.executable,'-E','-s','-B',str(root/manifest['entrypoint']),'--difficulty','easy','--count','5','--seed','49412305','--format','json']
runs=[]
for _ in range(2):runs.append(json.loads(subprocess.check_output(cmd,cwd=root,env={**os.environ,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(output)})))
assert runs[0]==runs[1]
sys.path.insert(0,str(REPO/'scripts'));from generator_pipeline import asset_hashes
assets=asset_hashes(runs[0],root,Path('/media/jake/SSD/EDB/math'));assert len(assets)==25
for r in runs[0]:verify(r)
assert {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}==set(manifest['files'])
save('runner-records.json',runs[0]);save('relocation.json',{'command':cmd,'deterministic_runs':2,'bound_assets':len(assets),'runtime_files_unchanged':all((root/n).read_bytes()==(W/n).read_bytes() for n in manifest['files']),'shortcut':summarize(runs[0])})
render=[next(r for r in normal if r['generation']['template']==t) for t in g.TEMPLATES]+[sources[3]]
save('render-records.json',render)
save('source-render-records.json',[sources[3]])
save('result.json',{'passed':True,'fidelity':{'banks':7,'choices':35,'observed_keys':5,'inferred_keys':2},'correctness':{'source_and_fresh_controlled_records':len(sources+records),'oracle':'Fractions arithmetic, visible TeX and actual image-sidecar endpoints','invalid_rejected':len(invalid)},'grading':{'checks':sum(len(c['checks']) for c in cases),'native_report':'engine-report.json'},'decision_variation':{'families':6,'fixed_bank_correct_assignments_per_family':5,'identical_bank_image_only_strategy_rate':.2,'normal_semantic_instances':len({r['generation']['mathematical_fingerprint'] for r in normal}),'raw':len(records),'delivered':len(accepted),'generator_attempts':{t:[r['generation']['sampling_attempts'] for r in normal if r['generation']['template']==t] for t in g.TEMPLATES},'proof':'Answer assignment is uniform AFTER all symmetric bank rejection tests. No correctness-dependent resampling follows it. Five-way controlled cases survive actual delivery in every family.','limits':'No claim that finite fresh samples exclude every shortcut. Conditional symmetry addresses every equation-free bank cue for normal generation. Explicit source replay banks retain observed arrangements.'},'rendering':'pending shared preview and visual inspection','inventory':'pending exact captured record reproduction'})
print('PASS:',len(records),'records;',len(accepted),'delivered;',len(cases)*5,'native checks',flush=True)
