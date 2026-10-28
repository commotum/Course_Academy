import collections,json,re,sys
from pathlib import Path
sys.path.insert(0,'scripts');from question_capture.math_format import normalize_source_tex
H=Path(__file__).resolve().parent;D=json.loads((H/'snapshot.json').read_text());Q={q[':question/math-academy-id']:q for q in D['questions']if ':question/math-academy-id'in q};M=json.loads((H/'source-manifest.json').read_text());out=[]
def canon(v):
 v=normalize_source_tex(v);v=re.sub(r'\\(?:displaystyle|left|right)|\$|[{}\s]','',v);return v.replace(r'\cdot',r'\times').replace('−','-')
for sid,paths in M.items():
 q=Q[sid];checks=[]
 for p in paths:
  if not p.endswith('.json'):continue
  d=json.loads(Path(p).read_text());fs=d.get('fields',[])
  for sf in fs:
   if not sf.get('choices_complete')or not sf.get('choices'):continue
   targets=[f for f in q.get(':question/answer-fields',[])if f[':answer-field/key']==sf.get('key')]
   if not targets:checks.append({'path':p,'source_key':sf.get('key'),'status':'response representation changed; no same-key field'});continue
   want=sorted(canon(a[':answer/value'])for a in targets[0][':answer-field/choices']);got=sorted(canon(a['value'])for a in sf['choices']);checks.append({'path':p,'source_key':sf.get('key'),'status':'exact normalized bank match'if got==want else'bank formatting difference retained for review','source_values':got if got!=want else None,'stored_values':want if got!=want else None})
 if checks:out.append({'entity':q[':db/id'],'source_identity':sid,'comparisons':checks})
(H/'source-bank-validation.json').write_text(json.dumps(out,indent=2));print('question banks',len(out),'checks',sum(len(x['comparisons'])for x in out),'statuses',collections.Counter(c['status']for x in out for c in x['comparisons']))
