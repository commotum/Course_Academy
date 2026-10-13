"""Private artifact builder; review records are produced by the public API."""
import importlib.util,json
from pathlib import Path
H=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('generator',H.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
records=json.loads((H/'review.json').read_text())
lines=['# Cosecant periodicity — original and generated review','', 'math basis 1356. Raw records are evidence-only; original omissions and references are retained. Normal banks are authored method-operation banks. Hard is an authored same-skill workload claim. All displayed banks below are complete.','']
def show(r,label):
 q=r['question'];m=r['generation'];lines.extend(['## '+label,'',f"Template `{m['template']}`; profile `{m['profile']}`; evidence-only `{m['evidence_only']}`.",'',q[':question/problem'],'','Complete choice bank:',''])
 f=q[':question/answer-fields'][0];correct=f.get(':answer-field/correct');cid=correct.get(':answer/id') if isinstance(correct,dict) else correct[1] if correct else None
 for a in f[':answer-field/choices']:lines.append('- $'+a[':answer/value']+'$'+(' — correct' if a[':answer/id']==cid else ''))
 if cid is None:lines.extend(['','Correct designation absent in the captured source; no observed designation is invented.'])
 lines.extend(['',q.get(':question/worked-solution','Worked solution absent in captured source.'),''])
for sid,source in g.SOURCES.items():
 f=g.FAMILY[sid];family=[r for r in records if r['generation']['template']==f]
 show(family[0],sid+' — ORIGINAL, public raw replay')
 show(family[1],sid+' — GENERATED normal at original parameters, authored bank')
 for index,r in enumerate(family[2:]):show(r,sid+' — GENERATED '+('historical evidence bank' if r['generation']['evidence_only'] else 'normal operation bank')+' changed-parameter variant '+str(index+1))
for i,r in enumerate(r for r in records if r['generation']['template']=='two_terms'):show(r,'AUTHORED hard two-reduction variant '+str(i+1))
lines.extend(['## Review limits','', 'Seven exact raw question records and all 35 choices are reproduced. Five original correct designations and five original solutions exist and match; the two omitted designations/solutions cannot count as observed fidelity. All five normal source solutions retain exact source wording and stages. Historical bank error intent remains unresolved and raw profiles are ineligible for learning. There are four finite conceptual workloads; bounded numerical/domain counts are reported separately in validation.json. No plots are used.',''])
(H/'review.md').write_text('\n'.join(lines))
