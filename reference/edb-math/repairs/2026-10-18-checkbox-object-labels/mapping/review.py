import collections,copy,importlib.util,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent;RUN=HERE.parent;ROOT=RUN.parents[3]
spec=importlib.util.spec_from_file_location('presentation_lint',ROOT/'skills/radio2checkbox/scripts/lint_presentation.py');lint=importlib.util.module_from_spec(spec);spec.loader.exec_module(lint)
qs={q[':db/id']:q for q in json.loads((RUN/'questions.json').read_text())};cases=json.loads((HERE/'cases.json').read_text())
findings=[];inputs=[]
for c in cases:
 q=copy.deepcopy(qs[c['question_eid']]);q[':question/problem']=c['problem_after'];q[':question/worked-solution']=c['solution_after']
 for f in q[':question/answer-fields']:
  if f[':db/id']in {o['field_id']for o in c['objects']}:f[':answer-field/key']=next(o['content']for o in c['objects']if o['field_id']==f[':db/id'])
 errors=lint.lint_question(q,c['objects']);inputs.append({'question':q,'objects':c['objects']})
 if errors:findings.append({'question_eid':c['question_eid'],'findings':errors,'objects':c['objects'],'problem_after':c['problem_after']})
(HERE/'lint-findings.json').write_text(json.dumps(findings,ensure_ascii=False,indent=2)+'\n')
(HERE/'presentation-input.json').write_text(json.dumps({'cases':inputs},ensure_ascii=False)+'\n')
print(json.dumps({'cases':len(cases),'finding_questions':len(findings),'findings':dict(collections.Counter(f['code']for c in findings for f in c['findings']))},indent=2))
