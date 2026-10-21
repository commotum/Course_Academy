import sys,json,re,hashlib,subprocess
from pathlib import Path
sys.dont_write_bytecode=True
import review as v
E=v.E;W=v.W
source=v.load(v.JOB/'source/source.json')['material']['kp'];replays=v.load(E/'source-replays.json')
def prose(s):return re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$|\$[^$]*\$','[MATH]',s,flags=re.S)).strip()
fidelity=[]
for q,r in zip(source[':knowledge-point/questions'],replays):
 s=q[':question/worked-solution'];t=r['question'][':question/worked-solution']
 if q[':question/math-academy-id']=='q-74638':s=s.replace('reduced row echelon form','row echelon form')
 a=v.matrices(s);b=v.matrices(t)
 diffs=[{'stage':i,'source':str(x),'generated':str(y)} for i,(x,y) in enumerate(zip(a,b)) if x!=y]
 fidelity.append({'source_id':q[':question/id'],'template':q[':question/math-academy-id'],'prose_matches_modulo_math_and_documented_correction':prose(s)==prose(t),'source_matrix_count':len(a),'generated_matrix_count':len(b),'matrix_differences':diffs,'difference_justification':'q-32242 source silently negates R1 without annotating it; generated final R1 retains prior R1 while keeping correctly executed R3 operation.' if diffs and q[':question/math-academy-id']=='q-32242' else ''})
v.save('solution-fidelity.json',fidelity)
g=v.module(W/'17592186115299.py');canonical=source[':knowledge-point/canonical-example'];m=v.system(canonical[':question/problem'])
r=g.generate('moderate',seed=82221,template='q-74638',parameters={'matrix':[[str(x) for x in row] for row in m.tolist()],'order':['dependent','inconsistent','independent']});v.save('canonical-math-record.json',[r]);v.save('canonical-report.json',{'source_id':canonical[':question/id'],'check':v.check(r),'matches_canonical_matrix':v.system(r['question'][':question/problem'])==m,'expected':'consistent dependent; first displayed category qualifies','limitation':'Canonical capture has no answer-field/bank data. Generated bank is a supported practice bank, not a claimed replay of absent canonical fields.'})
# Independently verify native pair outcomes match desired semantic actions.
native=v.load(E/'native-report.json');cf=v.load(E/'counterfactual-records.json');pair=[]
for r in cf:
 rr=next(n for n in native['records'] if n['label']==r['question'][':question/id'])
 pair.append({'id':r['question'][':question/id'],'selected':v.value(r['question'][':question/answer-fields'][0]),'accepted':sum(c['outcome']=='accepted' for c in rr['checks']),'rejected':sum(c['outcome']=='rejected' for c in rr['checks'])})
v.save('counterfactual-native-summary.json',pair)
# Actual historical bootstrap negative uses a virtual external __file__; exact unmodified lines extracted from original.
cmd=[v.PYTHON,str(E/'legacy-negative-control.py')];p=subprocess.run(cmd,cwd=E,text=True,capture_output=True)
v.save('legacy-negative.json',{'command':cmd,'exit':p.returncode,'stderr':p.stderr,'virtual_external_file':'/isolated/course-academy-package/17592186115299.py','method':'Exact historical bootstrap lines from existing_entrypoint with external __file__ simulation; source code has no dependency on the rest of the generator here. A physical copy under evidence_root remains inside repo ancestors, so it is not a valid external relocation negative.','reproduced_historical_failure':p.returncode!=0 and 'StopIteration' in p.stderr})
# Correct earlier provisional report now the exact negative has been executed.
pkg=v.load(E/'packaging-report.json');pkg['retained_check_inspection']='Current author relocation regression passes in evidence-owned copy; independent relocation/dependency checks pass. Historical bootstrap negative is executed in legacy-negative-control.py, reproducing StopIteration for a virtual external path. Provisional incomplete-closure test is a secondary control.';v.save('packaging-report.json',pkg)
after=v.package_hashes();before=v.load(E/'package-before.json');v.save('package-integrity.json',{'unchanged':after==before,'file_count':len(after),'changed':[k for k in set(after)|set(before) if after.get(k)!=before.get(k)],'before':'package-before.json','after_sha256':after})
inspection={'screenshots_inspected':['render/question-001.png','render/question-003.png','render/question-006.png','render-source/question-001.png']+['render-counterfactual/question-%03d.png'%i for i in range(1,5)],'result':'Readable equations, augmented separators, fractions, radio/checkbox controls and complete solutions. Normal radio Roman statements flow as a paragraph but labels remain clear. No clipping, missing glyphs or broken math observed. Counterfactual RHS/key/solution transitions verified visually.','actual_renderer_reports':['render/rendering.json','render-source/rendering.json','render-counterfactual/rendering.json']};v.save('visual-inspection.json',inspection)
refs=set()
ped=v.load(E/'pedagogical-variation.json')
for section in ['coverage','counterfactuals','shortcut_probes']:
 for x in ped[section]:refs.update(x['sample_refs'])
refs.update(ped['delivery']['sample_refs'])
missing=[r for r in refs if not (E/r).is_file() or not (E/r).stat().st_size]
v.save('evidence-contract.json',{'pedagogical_sample_refs_checked':len(refs),'missing_or_empty':missing,'package_unchanged':after==before,'schema_validation':'python3 jsonschema.validate against repo generate/pipeline/pedagogical-variation.schema.json passed','inventory_scope':'All27 independently math checked; no demonstrated weakness, so affected_questions empty.10 non-source records lack generation metadata; no universal absence of shortcuts is claimed.'})
print('solution fidelity mismatches',[(r['template'],r['prose_matches_modulo_math_and_documented_correction'],r['matrix_differences']) for r in fidelity if not r['prose_matches_modulo_math_and_documented_correction'] or r['matrix_differences']]);print('integrity',after==before,'evidence missing',missing)
(E/'session-state.md').write_text('Completed all eight review checks. Source replay17/17 and canonical math supported;170 fresh samples and5 exact batch math pass;134? see native-report.json for exact counts (614 accepted,725 rejected); delivery170/170 and5/5; actual UI11 records rendered,8 representative screenshots inspected;29 boundary tests pass; dependency versions exact; current relocation passes; historical bootstrap negative reproduces StopIteration. No demonstrated generator defect. Captured inventory math27/27; metadata limitations explicit. Package unchanged. Preparing final accepted report with evidence paths.\n')
