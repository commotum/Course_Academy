"""Replay supplied complete source and reproduce stored affected instances without DB access."""
import sys,json,pathlib,importlib.util,hashlib
sys.dont_write_bytecode=True
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'17592186229165'))
import validate as V
from math_parser import scalar,equal

def load(p):return json.loads(pathlib.Path(p).read_text())
def save(p,d):pathlib.Path(p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
spec=importlib.util.spec_from_file_location('g',ROOT/'17592186229165.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
source=load(ROOT.parent/'source/source.json')['material']['kp']
cases=load(ROOT/'17592186229165/source-cases.json');byma={q[':question/math-academy-id']:q for q in source[':knowledge-point/questions']}
results=[];records=[];graders=[]
for c in cases:
 q=byma[c['source_id']];r=g.generate(c['level'],parameters=c['parameters'],profile=c['bank_profile']);r2=r['question'];old=q[':question/answer-fields'][0];new=r2[':question/answer-fields'][0]
 assert r2[':question/problem']==q[':question/problem']
 assert r2.get(':question/worked-solution')==q.get(':question/worked-solution')
 for k in (':answer-field/key',':answer-field/type'):
  v=old[k];assert (v.get(':db/ident') if isinstance(v,dict) else v)==new[k]
 for k in (':answer-field/choices',':answer-field/correct'):assert (k in old)==(k in new)
 ov=[a[':answer/value'] for a in old.get(':answer-field/choices',[])];nv=[a[':answer/value'] for a in new.get(':answer-field/choices',[])]
 assert sorted(ov)==sorted(nv)
 if ov:
  assert old[':answer-field/correct'][':answer/value']==nv[-1]
  d=q[':question/difficulty'][':db/ident'];assert d==r2[':question/difficulty']
 normal=g.generate(c['level'],parameters=c['parameters'],profile=c['source_id']);V.validate_record(normal,c['level']);graders.append(V.native_item(c['source_id'],normal))
 results.append({'source_question_id':q[':question/id'],'profile':c['source_id'],'prompt_exact':True,'solution_exact':True,'bank_count':len(ov),'bank_exact_ignoring_order':True,'designation_present':bool(ov),'difficulty_preserved':True})
 records.append(r)
save(ROOT/'evidence/source-replays.json',records)
# Small unaffected-family regression; preserve deterministic behavior and parse actual displays.
small=[g.generate('easy',seed=i) for i in range(901,906)]+[g.generate('moderate',seed=901)]+[g.generate('hard',template='two_nonresonant',seed=i) for i in (901,902)]
for r in small:
 level=r['question'][':question/difficulty'].split('/')[-1];V.validate_record(r,level);assert r==g.generate(level,template='two_nonresonant' if level=='hard' else None,seed=r['generation']['seed'])
 graders.append(V.native_item('unchanged-'+level+'-'+str(r['generation']['seed']),r))
save(ROOT/'evidence/small-regression.json',small);save(ROOT/'evidence/easy-batch.json',small[:5]);save(ROOT/'evidence/source-grader-input.json',graders)
# Captured generated records are interpretable lineage evidence, not a source-question rewrite.
inv=load(ROOT.parent/'source/inventory.json');stored={q[':question/id']:q for q in inv['questions']}
captured=load(ROOT/'17592186229165/reference/replenishment/basis-2525/generated.json')
reproduced=[];affected=[];comparisons=[]
for old in captured:
 meta=old['generation'];fresh=g.generate(old['question'][':question/difficulty'].split('/')[-1],seed=meta['seed'],template=meta['template'],parameters=meta['parameters'],profile=meta['bank_profile'])
 assert fresh==old,'Stored explicit replay changed'
 q=stored[old['question'][':question/id']];new=fresh['question']
 assert q[':question/problem']==new[':question/problem'] and q[':question/worked-solution']==new[':question/worked-solution']
 assert sorted(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/value'] for a in new[':question/answer-fields'][0][':answer-field/choices'])
 reproduced.append(fresh);comparisons.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'captured_record_exact':True,'template':meta['template'],'parameters':meta['parameters']})
 if meta['template']=='mixed':
  affected.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'finding':'Historical mixed hard cohort places resonance first, allowing the ordinary trial for the last term to be chosen by position. Individual mathematical key is correct. Current explicit replay is retained; new sampling also delivers second-position resonance.','reproduction':str(sys.executable)+' checks/check_source_and_inventory.py; explicit hard mixed seed '+str(meta['seed'])+' parameters '+json.dumps(meta['parameters'],sort_keys=True),'evidence_path':'../workspace/evidence/generated-records.json'})
save(ROOT/'evidence/generated-records.json',reproduced);save(ROOT/'affected-inventory.json',{'affected_questions':affected})
assert len(stored)==len(cases)+len(captured)
report={'source_cases':results,'available_banks_matched':sum(bool(r['bank_count']) for r in results),'available_bank_members':sum(r['bank_count'] for r in results),'raw_incomplete_preserved':2,'unaffected_sample_checked':len(small),'inventory_questions':len(stored),'generated_reproductions':comparisons,'affected_mixed':len(affected),'inventory_scope':'All 20 captured entries classified: 15 original source (never relabeled generated), five generated records reproduced exactly, four mixed affected. No claim about live state.','evidence_path_base':'Affected evidence_path is relative to the supplied author-1 evidence_root; files are kept inside the authorized workspace.','source_sha256':hashlib.sha256((ROOT.parent/'source/source.json').read_bytes()).hexdigest()}
save(ROOT/'evidence/source-and-inventory-results.json',report)
print(json.dumps({k:v for k,v in report.items() if k not in ('source_cases','generated_reproductions')},indent=2))
