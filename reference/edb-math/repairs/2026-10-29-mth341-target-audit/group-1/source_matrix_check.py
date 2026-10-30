import json,re,collections,importlib.util,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];spec=importlib.util.spec_from_file_location('group1_math',H/'math_verify.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);D=m.D;P=m.P;src=json.loads((H/'sources.json').read_text());out=[];flags=[]
def matrices(formulas):
 return [str(mat)for v in formulas for start,end,mat in m.mats(v)]
for q in D['questions']:
 sid=q.get(':question/math-academy-id');problem=m.pm.get((q[':db/id'],'question/problem'),q[':question/problem']);formulas=[problem]+[m.pm.get((f[':db/id'],'answer-field/key'),f[':answer-field/key'])for f in q.get(':question/answer-fields',[])if f[':answer-field/type'][':db/ident'].endswith('checkbox')];actual=matrices(formulas);candidates=[]
 for s in src:
  if s['identity']!=sid or s['attribute']!='question/problem':continue
  fs=[x for x in s['formulas']if isinstance(x,str)];expected=matrices(fs)
  if expected:candidates.append({'source_path':s['path'],'matrices':expected,'matches':collections.Counter(expected)==collections.Counter(actual)})
 matches=[r for r in candidates if r['matches']]
 r={'entity':q[':db/id'],'identity':sid,'current_matrix_count':len(actual),'current_matrices':actual,'source_candidates':len(candidates),'matched':bool(matches),'matching_sources':sorted({s['source_path']for s in matches})};out.append(r)
 if candidates and not matches:flags.append(r)
(H/'source-matrix-verification.json').write_text(json.dumps({'checks':out,'flags':flags,'matched_questions':sum(r['matched']for r in out)},indent=2)+'\n');print('SOURCE MATRIX FLAGS',len(flags));print(json.dumps(flags,indent=2))
