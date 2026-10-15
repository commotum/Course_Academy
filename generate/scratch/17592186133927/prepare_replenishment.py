"""Revalidate the frozen generator and prepare scoped, distinct candidates."""
import importlib.util,json,subprocess,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('replenish',D/'replenish.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r);g=r.g;v=r.v

def main():
 # Fresh captured inventory precedes all generation.
 inv=r.inventory(D/'reference/candidate-inventory.json');b=inv['basis'];kp=r.read_kp(D/'reference/candidate-read',b)
 assert r.canonical(kp)==r.canonical(r.loads((D/'reference/initial/snapshot.edn').read_text()))
 freeze=json.loads((D/'freeze.json').read_text());checked={}
 for name in (str(D.with_suffix('.py').relative_to(ROOT)),str((D/'validate.py').relative_to(ROOT)),str((D/'render.py').relative_to(ROOT)),str((D/'source.json').relative_to(ROOT))):
  assert r.sha(ROOT/name)==freeze['file_sha256'][name];checked[name]=r.sha(ROOT/name)
 # Build the existing generic grading fixture against today's engine library.
 src=D/'reference/check-engine.rs';src.write_bytes((ROOT/'generate/runs/current/check-engine.rs').read_bytes())
 deps=ROOT/'target/release/deps';libs={n:max(deps.glob('lib'+n+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns) for n in ('course_academy_engine','serde_json')}
 command=['rustc','--edition=2024','-O',str(src)]
 for name,path in libs.items():command+=['--extern',name+'='+str(path)]
 command+=['-L','dependency='+str(deps),'-L','dependency='+str(ROOT.parent/'EDB/target/release/deps'),'-o',str(D/'reference/check-engine')]
 subprocess.run(command,check=True);r.save(D/'reference/grading-build.json',{'command':command,'libraries':{str(p):r.sha(p) for p in libs.values()},'source_sha256':r.sha(src),'binary_sha256':r.sha(D/'reference/check-engine')})
 records=[]
 samples=[('horizontal',{'k':1,'a':3,'h':1}),('horizontal',{'k':1,'a':3,'h':2}),('horizontal',{'k':1,'a':3,'h':3}),('horizontal',{'k':1,'a':3,'h':4}),('horizontal',{'k':2,'a':1,'h':3}),('triangle',{'k':2,'a':2,'h':4}),('tilted_blank',{'k':2,'a':2,'h':3}),('xy_triangle',{'k':3,'a':2,'h':2}),('reciprocal',{'k':2,'a':2,'h':3}),('cone_triangle',{'k':2,'a':2,'h':2}),('shifted_paraboloid',{'k':2,'a':3,'h':2}),('odd_plane',{'k':2,'a':3,'h':2}),('negative_cone',{'k':2,'a':2,'h':2}),('tilted_disk',{'k':2,'a':3,'h':3}),('exponential',{'k':2,'a':2,'h':3})]
 seen=set()
 for i,(name,p) in enumerate(samples):
  level=g.FAMILIES[name][0];rec=g.generate(level,seed=1579805955+i,template=name,parameters=p);v.validate_record(rec)
  fp=r.model_task(name,p);assert fp not in seen;seen.add(fp)
  rr=g.generate(level,seed=1579806055+i,template=name,parameters=p);assert rr['question'][':question/id']==rec['question'][':question/id'];assert r.model_task(name,p)==fp
  records.append(rec);print('Validated',level,name,p,flush=True)
 r.save(D/'reference/candidates.json',records)
 # Full historical evidence replays remain distinct from eligible authored banks.
 # All unchanged original banks were previously matched 56/56. Refresh their
 # immutable captured attributes with complete current source inspection.
 source_audit={'basis':b,'lineage':r.LINEAGE,'sources':[],'current_practice_count':len(kp[':knowledge-point/questions']),'prior_source_count':len(g.Q),'vetted_source_ids':sorted(r.VETTED),'source_mutations':0}
 exclusions={'q-161927':'Extra legacy field lacks correct reference and has malformed powers.','q-168625':'Prompt omits supplied graph and curl context; generated version explicitly supplies both.','q-162361':'Two source distractor integrals have the same complete scalar value.','q-162373':'Angular and radial primitives are wrong; generated solutions are independently recomputed.','q-162374':'Extra closing parenthesis in source flux row; generated version balances notation.','q-161926':'Now rated hard with correct 0 and a solution, but displayed radial primitive of 2r^2 is r^2; exclude this faulty solution.','q-162363':'New saddle/rectangle setup family; correct integral of 2 and choice integral of 2+2xy both evaluate to 16 on the symmetric rectangle; excluded from production until a separately validated complete-bank correction.'}
 for q in kp[':knowledge-point/questions']:
  sid=q[':question/math-academy-id'];entry={'source':sid,'id':str(q[':question/id']),'difficulty':str(q[':question/difficulty'][':db/ident']),'field_types':[str(f[':answer-field/type'][':db/ident']) for f in q[':question/answer-fields']],'plot_rating':'light' if '![](' in q.get(':question/worked-solution','') else 'none','eligible':sid in r.VETTED,'evidence':exclusions.get(sid,'Original exact model, complete bank and designated answer independently verified in source-math-audit.json; unchanged against frozen source.')}
  if sid in r.VETTED:
   old=g.Q[sid]
   for key in (':question/problem',':question/worked-solution'):assert old[key]==q[key]
   assert r.canonical(old[':question/answer-fields'])==r.canonical(q[':question/answer-fields'])
  source_audit['sources'].append(entry)
 # Additional source: divergence=0, graph gradient=(2x,-2y), flux=2,
 # exact equal values establish ambiguity without guessing a distractor intent.
 x,y=g.X,g.Y
 assert g.s.integrate(g.s.integrate(2+2*x*y,(y,-2,2)),(x,-1,1))==16
 assert g.s.integrate(g.s.integrate(2,(y,-2,2)),(x,-1,1))==16
 source_audit['new_saddle_family']={'graph':'x^2-y^2','curl':['y','x','2'],'bounds':[-1,1,-2,2],'upward_flux':'2','correct_and_equivalent_distractor_value':16,'choices_replayed':5,'production_support':False,'inferred_recipes':False}
 r.save(D/'current-source-audit.json',source_audit)
 r.save(D/'reference/candidate-engine-input.json',[v.engine_item(q,q['question'][':question/id']) for q in records])
 subprocess.run([str(D/'reference/check-engine'),str(D/'reference/candidate-engine-input.json'),str(D/'reference/candidate-engine-report.json')],check=True)
 engine=json.loads((D/'reference/candidate-engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
 r.save(D/'reference/candidate-validation.json',{'status':'passed','basis_before_generation':b,'lineage':r.LINEAGE,'records_checked':len(records),'distinct_tasks':len(seen),'math_checks':'Displayed graph, curl divergence, slope derivatives, substitution, flux, ordered integrals, full banks, primitives, endpoints, answers and solution formatting independently validated by validate_record.','deterministic_identity_with_changed_seed':True,'field_owned_answers':True,'source_fidelity':'56/56 original choices, 12/12 fields, 11/11 historical questions at frozen source basis; current deltas documented separately. Authored corrected banks explicitly identified.','native':{k:v for k,v in engine.items() if k!='records'},'frozen_inputs_checked':checked})
 r.save(D/'capabilities.json',{'supported_levels':list(r.LEVELS),'finite_distinct_tasks':{'easy':32,'moderate':168,'hard':152},'scope':'Conservative frozen source-shaped models; authored complete method banks. Current newly captured saddle family remains evidence only.','exceptions':[{'type':'excluded-source-family','source':'q-162363','reason':exclusions['q-162363'],'requested_reserve_impact':0}],'unsupported_levels':[],'unobserved_easy_support':'Canonical horizontal disk with same supplied curl and constant plus odd term, no nonzero slope contributions; radius/height/whole-curl scale vary.','no_cosmetic_duplicates':True})
 counts=r.count(kp,D/'reference/candidate-read',b);print('Fresh validated counts',json.dumps(counts['levels']),flush=True)
 review=['# Replenishment review','Current source basis '+str(b)+'. Existing historical evidence remains unchanged.','All candidates are generated; source and mathematical task identities are checked separately.']
 for rec in records:review.append(g.markdown(rec))
 (D/'reference/candidate-review.md').write_text('\n\n'.join(review))
 names=[D.with_suffix('.py'),D/'validate.py',D/'render.py',D/'source.json',D/'replenish.py',Path(__file__),D/'reference/candidates.json',D/'reference/check-engine',D/'reference/candidate-validation.json',D/'current-source-audit.json',D/'capabilities.json']
 r.save(D/'replenishment-freeze.json',{'status':'passed','basis':b,'hashes':{str(p.relative_to(ROOT)):r.sha(p) for p in names}})
if __name__=='__main__':main()
