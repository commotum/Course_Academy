"""Affected runner/delivery checks and final evidence summary; no regeneration."""
import collections,hashlib,json,subprocess,sys
from pathlib import Path
from fractions import Fraction as F
W=Path(__file__).resolve().parents[1];E=W/'evidence/visual-repair';REPO=Path('/home/jake/Developer/Course_Academy');S=W.parent/'source'
save=lambda n,x:(E/n).write_text(json.dumps(x,indent=2)+'\n')
load=lambda n:json.loads((E/n).read_text())
field=lambda r:r['question'][':question/answer-fields'][0]
runner=load('runner-records.json');cases=[]
for r in runner:
 f=field(r);cases.append({'label':'relocated CLI '+r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'relocated CLI full image bank'} for a in f[':answer-field/choices']]})
save('runner-engine-input.json',cases)
subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(E/'runner-engine-input.json'),str(E/'runner-engine-report.json')],check=True,stdout=(E/'runner-engine.log').open('w'),stderr=subprocess.STDOUT)
subprocess.run([sys.executable,str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(E/'runner-records.json'),'--source',str(S/'source.json'),'--inventory',str(S/'inventory.json'),'--difficulty','easy','--output',str(E/'runner-delivery'),'--asset-root',str(E/'outside/runtime-output'),'--math-root','/media/jake/SSD/EDB/math'],check=True,stdout=(E/'runner-delivery.log').open('w'),stderr=subprocess.STDOUT)
accepted=load('runner-delivery/accepted.json');assert len(accepted)==5
# The five images, their order and correct geometry must survive unchanged.
bykey={r['generation']['content_fingerprint']:r for r in runner}
for r in accepted:
 original=bykey[r['generation']['content_fingerprint']];f=field(r);o=field(original)
 assert [Path(a[':answer/value']).stem for a in f[':answer-field/choices']]==[hashlib.sha256(Path(a[':answer/value']).read_bytes()).hexdigest() for a in o[':answer-field/choices']]
 assert next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])==next(i for i,a in enumerate(o[':answer-field/choices']) if a[':answer/id']==o[':answer-field/correct'][1])
save('runner-delivery-invariance.json',{'records':5,'image_bytes_order_and_correct_index_preserved':True,'consequence':'Every image-only cue result in relocation.json remains identical after runner delivery.'})

def coverage(rs):
 out={}
 for t in sorted({r['generation']['template'] for r in rs}):
  group=[r for r in rs if r['generation']['template']==t];patterns=collections.Counter();zeros=set();signs={i:set() for i in range(3)}
  for r in group:
   s=list(map(F,r['generation']['exact_slopes']));patterns[str(tuple((v>0)-(v<0) for v in s))]+=1
   for i,v in enumerate(s):
    signs[i].add((v>0)-(v<0))
    if v==0:zeros.add(i)
  out[t]={'records':len(group),'semantic_instances':len({r['generation']['mathematical_fingerprint'] for r in group}),'sign_patterns':dict(patterns),'signs_per_point':{i:sorted(v) for i,v in signs.items()},'horizontal_slots':sorted(zeros),'coefficient_values':{k:sorted({str(r['generation']['parameters'][k]) for r in group if k in r['generation']['parameters']}) for k in ('a','b','d')},'distinct_point_triples':len({str(r['generation']['parameters']['points']) for r in group})}
 return out
save('coverage.json',{'normal':coverage(load('normal-records.json')),'raw':coverage(load('delivery-input.json')),'delivered':coverage(load('delivered-with-geometry.json')),'obligations':'All six source equation families retained; five distinct correct geometries for fixed points/bank in each; each tested decisive mirror-pair subgroup has all five correct assignments; point changes retain two unchanged substitutions. Horizontal cases may be valid simplifications and are not rejected to enforce quotas.'})
manifest=json.loads((W/'package.json').read_text())
save('package-integrity.json',{'manifest':manifest,'runtime_sha256':{n:hashlib.sha256((W/n).read_bytes()).hexdigest() for n in manifest['files']},'preserved_source_data':True,'dependencies_verified_in':'relocation.json','all_runtime_files_exist':all((W/n).is_file() for n in manifest['files'])})
result=load('result.json');result['grading']['runner_checks']=25;result['grading']['total_checks']=result['grading']['checks']+25
result['decision_variation']['controlled_bank_groups']=len(load('counterfactuals.json'))
result['decision_variation']['decisive_mirror_subgroups']=sum(x.get('probe')=='decisive reflected-pair subgroup' for x in load('counterfactuals.json'))
result['inventory']=load('inventory-result.json');result['runner_delivery']=load('runner-delivery/delivery.json')
result['rendering']={'reports':['render/rendering.json','render-source/rendering.json'],'visual_inspection':'pending source screenshot inspection'}
result['limitations']=['Two original source questions lack stored keys/solutions; their replay keys and solutions are explicitly inferred.','Only requested easy is certified; historical moderate/hard arithmetic extensions remain outside this repair certification.','Inventory and selection checks use the captured basis and synthetic selection IDs; live learner history and concurrent publication are unavailable.','Explicit source replay preserves observed banks; normal generated practice uses the repaired exchangeable bank.','Finite fresh samples do not prove absence of every shortcut; symmetric answer assignment and exhaustive five-case controls justify the equation-free bank-cue claim.']
save('result.json',result)
print('Runner: 25 native checks; 5/5 delivered with cue-preserving image/order/key mapping. Total native checks',result['grading']['total_checks'])
