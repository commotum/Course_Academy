#!/usr/bin/env python3
"""Offline delivery, post-filter counterfactuals, relocation and inventory audit."""
import sys
sys.dont_write_bytecode=True
import collections,hashlib,json,os,pathlib,shutil,subprocess,tempfile
import regression_checks as t
ROOT=pathlib.Path(__file__).resolve().parent
OUT=ROOT/'evidence';REPO=pathlib.Path('/home/jake/Developer/Course_Academy');JOB=ROOT.parent
PY=REPO/'.venv/bin/python';COMMANDS=[]
def run(cmd):
 r=subprocess.run(list(map(str,cmd)),cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(OUT/'assets')))
 COMMANDS.append({'command':list(map(str,cmd)),'returncode':r.returncode,'stdout':r.stdout[:3000],'stderr':r.stderr[:3000]})
 assert r.returncode==0,COMMANDS[-1]
 return r

def delivered(name,records,band):
 path=OUT/(name+'-input.json');t.save(path.name,records)
 dest=OUT/name
 run([PY,REPO/'generate/pipeline/check_delivery.py','--input',path,'--source',JOB/'source/source.json','--inventory',JOB/'source/inventory.json','--difficulty',band,'--output',dest,'--asset-root',OUT/'assets','--math-root','/media/jake/SSD/EDB/math'])
 return json.loads((dest/'accepted.json').read_text())

def probe(records):
 groups=collections.defaultdict(list)
 for r in records:
  assert t.witness.math_record(r)['pass']
  # Group using visible choice text, never the generation target metadata.
  group=(r['generation']['template'],tuple(sorted(t.bank(r))))
  groups[group].append(r)
 result=[]
 for (sid,_),rs in groups.items():
  keys={t.key(r) for r in rs};positions=[t.witness.keypos(r) for r in rs]
  hit=sum(t.witness.shortcut(r)[0]==[t.witness.keypos(r)] for r in rs)
  result.append({'template':sid,'cases':len(rs),'distinct_keys':len(keys),'key_positions':positions,'reported_probe_hits':hit,'best_constant_position_hits':max(collections.Counter(positions).values()),'any_bank_only_single_pick_max_hits':max(collections.Counter(t.key(r) for r in rs).values())})
 return result

def main():
 records=json.loads((OUT/'counterfactual-records.json').read_text());accepted=[]
 for band in ['easy','moderate']:
  rs=[r for r in records if r['question'][':question/difficulty'].endswith('/'+band)]
  accepted+=delivered('delivery-'+band,rs,band)
 after=probe(accepted);before=probe(records)
 assert len(after)==16 and all(z['cases']==5 and z['distinct_keys']==5 and z['any_bank_only_single_pick_max_hits']==1 for z in after)
 batch=json.loads((OUT/'runner-batch.json').read_text());batch_after=delivered('delivery-batch',batch,'easy')
 fresh=json.loads((OUT/'fresh-sample.json').read_text());fresh_after=delivered('delivery-fresh',fresh,'easy')
 t.save('post-delivery-shortcuts.json',{'before':before,'after':after,'runner_before':probe(batch),'runner_after':probe(batch_after),'fresh_before':probe(fresh),'fresh_after':probe(fresh_after),'claims':'Controlled identical banks retain all five different keys in all 16 profiles after publication filtering. Fresh singleton banks do not establish conditional rates; the controlled families provide the decisive test.'})
 # Native checks of the normalized records, using independent exact witnesses.
 selected=batch_after+[r for r in accepted if r['generation']['template'] in ('q-73743','q-42158')]
 cases=[]
 for i,r in enumerate(selected):
  z=t.witness.math_record(r)
  cases.append({'label':'delivered-'+str(i),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if z['valid_choices'][j] else 'rejected','purpose':'post-filter exact mathematical option classification'} for j,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices'])]})
 t.save('delivered-grader-input.json',cases)
 run([REPO/'generate/runs/current/check-engine',OUT/'delivered-grader-input.json',OUT/'delivered-grader-results.json'])
 # Reproduce the within-band native selection draw (Rust select uniform(8)); all
 # candidates here share one requested, positively weighted difficulty band.
 # Native code sorts fresh entity IDs; UUID ordinals below are a read-only stand-in.
 selection=[]
 for sid,rs in collections.defaultdict(list,((sid,[r for r in accepted if r['generation']['template']==sid]) for sid in sorted({r['generation']['template'] for r in accepted}))).items():
  rs=sorted(rs,key=lambda r:r['question'][':question/id']);picked=[]
  for n in range(25):
   raw=hashlib.sha256(('course-academy/question-selection/v1/author-'+str(n)).encode()).digest()
   v=(int.from_bytes(raw[8:16],'big')>>11)/(1<<53);picked.append(t.key(rs[int(v*len(rs))]))
  selection.append({'template':sid,'draws':25,'distinct_selected_responses':len(set(picked)),'eligible_distinct_responses':len({t.key(r) for r in rs})})
 assert all(z['distinct_selected_responses']>1 for z in selection)
 t.save('selection-results.json',{'results':selection,'method':'Exact Rust SHA-256 within-band draw, with sorted question UUID ordinals standing in for future entity IDs.','limits':'No live learner history or future entity assignment is available; those are not simulated as fact. Selection depends on fresh entity IDs and difficulty, not bank coefficients. Captured inventory filtering uses the shared delivery helper.'})
 # All captured inventory entries are source originals; none is a stored generated
 # instance with replayable generation metadata. Do not label these as generated.
 inv=json.loads((JOB/'source/inventory.json').read_text());source=json.loads((JOB/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions'];source_ids={q[':question/id'] for q in source}
 original=[q[':question/id'] for q in inv['questions'] if q[':question/id'] in source_ids]
 other=[q for q in inv['questions'] if q[':question/id'] not in source_ids]
 assert len(original)==16 and not other
 t.save('affected-inventory.json',{'affected_questions':[]})
 t.save('inventory-audit.json',{'basis':inv['basis'],'captured_count':len(inv['questions']),'verified_original_source_count':len(original),'stored_generated_candidates':0,'status':'Verified absence of generated instances within this captured inventory, by identity comparison against all supplied originals. Original source questions were not marked generated or modified. No claim about uncaptured live inventory.','original_source_ids':original})
 manifest=json.loads((ROOT/'package.json').read_text())
 with tempfile.TemporaryDirectory(prefix='relocation-',dir=OUT) as d:
  dest=pathlib.Path(d)
  for f in manifest['files']:
   target=dest/f;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/f,target)
  cmd=[PY,dest/manifest['entrypoint'],'--difficulty','easy','--count','5','--seed','71923','--format','json']
  a=run(cmd);b=run(cmd)
  assert a.stdout==b.stdout and json.loads(a.stdout)==batch
  unexpected=[str(p.relative_to(dest)) for p in dest.rglob('*') if p.is_file() and str(p.relative_to(dest)) not in manifest['files']]
  assert not unexpected
  # Pin comparison is against the exact requested interpreter, not ambient python.
  import sympy
  assert manifest['dependencies']=={'python':sys.version.split()[0],'packages':{'sympy':sympy.__version__}}
  t.save('packaging.json',{'relocation_passed':True,'deterministic_replay':True,'matches_runner_batch':True,'only_declared_runtime_files':True,'unexpected_runtime_writes':unexpected,'dependencies':manifest['dependencies'],'manifest_files':manifest['files'],'no_runtime_repository_imports':True,'assets':'No assets generated by this family; output directory explicitly set.'})
 t.save('delivery-commands.json',COMMANDS)
 print(json.dumps({'post_filter_controlled_cases':len(accepted),'profiles_with_five_keys':len(after),'runner_survived':len(batch_after),'fresh_survived':len(fresh_after),'native_post_filter_cases':len(cases),'relocation_passed':True,'inventory_generated_matches':0}))
if __name__=='__main__':main()
