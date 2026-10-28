import json
from pathlib import Path
H=Path(__file__).resolve().parent;names=['source-reviewed-proposals.json','answer-format-proposals.json','completion-solution-proposals.json','integral-display-proposals.json','answer-leak-proposals.json','arrow-notation-proposals.json'];out=[];counts={}
for name in names:
 ps=json.loads((H/name).read_text());counts[name]=len(ps);out.extend(ps)
assert len({(p['entity'],p['attribute'])for p in out})==len(out)
(H/'proposals.json').write_text(json.dumps(out,indent=2)+'\n');(H/'content-operation-counts.json').write_text(json.dumps({'basis_t':9837,'scalar_main':len(out),'by_file':counts,'existing_owned_missing_keys':len(json.loads((H/'missing-key-proposals.json').read_text())),'stable_new_owned_answers':len(json.loads((H/'new-answer-proposals.json').read_text())),'question_field_membership_detaches':len(json.loads((H/'membership-proposals.json').read_text())),'overlap':'All scalar main operations have distinct entity+attribute. Key completions target existing fields; new-answer allocation targets one separate empty field; memberships target only question/answer-fields. Old archived field keys are independently completed while all old banks/entities/history remain.'},indent=2)+'\n');print(counts,'main',len(out))
