import sys
sys.dont_write_bytecode=True
import json,importlib.util
from pathlib import Path
D=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('inverse_draft',D.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
components=[]
for sid,t in g.TEMPLATES.items():
 p=g.original_parameters(sid);mats=[g.sp.Matrix(m) for m in p['matrices']];values=g.truth(mats,t)
 components.append({'source_id':sid,'labels':t['labels'],'supplied_matrices':p['matrices'],'pair_roles':g.relations(t),'statement_truths':values,'displayed_ordered_product_stages':[{'pair':b['pair'],'product':g.serial_matrix(mats[b['pair'][0]]*mats[b['pair'][1]]),'witness':b['witness'],'complete_identity':b['identity']} for b in t['blocks']],'every_original_choice':[{'field':f['key'],'type':f['type'],'options':[{'value':a['value'],'role':'correct' if f['correct']==a['value'] else ('designation absent; mathematically correct' if f['type'].endswith('/radio') and a['value']==g.selected_words(values) else 'incorrect complete response predicate'),'recipe':'Boolean truth/complement from displayed relation' if f['type'].endswith('/checkbox') else 'complete stated subset of I/II/III; historical error intention unresolved'} for a in f['choices']],'original_correct':f['correct']} for f in t['fields']]})
(D/'source-components.json').write_text(json.dumps(components,indent=2)+'\n')
records=json.loads((D/'review.json').read_text());lines=['# Original source and generated variants','', 'All original records are preserved separately in source-cases/canonical JSON. Below, original supplied-parameter completed presentations are identified explicitly; q-7908’s placement/key/explanation and the canonical prompt repair are authored, not observed source content. Every changed instance uses the normal parameterized generator, retaining complete source banks and source-specific stage masks. Moderate/hard are authored uncalibrated placements.','']
for item in records:
 rec=item['record'];q=rec['question'];lines+=['## '+item['label'],'',q[':question/problem'],'','Field banks: '+('; '.join(f[':answer-field/key']+': '+', '.join(a[':answer/value'] for a in f[':answer-field/choices']) for f in q.get(':question/answer-fields',[])) or '[Canonical has no captured fields]'),'',q.get(':question/worked-solution','[Absent in raw capture]'),'']
(D/'review.md').write_text('\n'.join(lines))
(D/'replay-cases.json').write_text(json.dumps([{'source_id':sid,'template':sid,'difficulty':'easy','profile':'raw-source','parameters':g.original_parameters(sid),'evidence_only':True,'eligible_for_learning':False} for sid in g.TEMPLATES],indent=2)+'\n')
print('Built source component accounting and',len(records),'review records')
