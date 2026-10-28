import importlib.util,json,re,shutil,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];root=Path('/media/jake/SSD/EDB/math');D=json.loads((H/'current.json').read_text());qs={q[':question/id']:q for q in json.loads((H/'proposed-questions.json').read_text())};metadata=[]
for kp in D['knowledge_points']:
 g=kp[':knowledge-point/question-generator'];old=root/g[':question-generator/script'];manifest=json.loads((old.parent/'generator-package.json').read_text());dest=H/('generator-'+str(kp[':db/id']));dest.mkdir(exist_ok=True)
 for name in manifest['files']:p=dest/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(old.parent/name,p);p.chmod(0o644)
 shutil.copyfile(R/'scripts/question_capture/math_format.py',dest/'math_format.py')
 p=dest/'generator.py';s=p.read_text()
 if kp[':db/id']==17592186100875:
  s=s.replace('normalize_tex, validate_generated_record)','normalize_tex, normalize_matrix_answer_tables, validate_generated_record)');s=s.replace("VERSION = 'identity-2.0'","VERSION = 'identity-2.1-layout'");s=s.replace('prompt, solution = normalize_prose(prompt),','prompt, solution = normalize_prose(normalize_matrix_answer_tables(prompt)),')
  start=s.index('    if all(f[',s.index('def replay('));end=s.index('    specs = []',start)
  s=s[:start]+'''    if all(f[':answer-field/type'][':db/ident'].endswith('/blank') for f in fs):
        prompt = normalize_matrix_answer_tables(prompt)
        if 'matrix-answer-brackets' not in prompt:
            raise ValueError('Source replay requires a complete rectangular answer matrix')
'''+s[end:]

 else:
  s=s.replace('matrix_tex, validate_generated_record','matrix_tex, matrix_answer, normalize_matrix_answer_tables, validate_generated_record');s=s.replace("VERSION = 'identity-selection-3'","VERSION = 'identity-selection-4-layout'");s=s.replace('problem = normalize_prose(problem)','problem = normalize_prose(normalize_matrix_answer_tables(problem))')
  start=s.index('            if column:\n                problem +=');end=s.index('            return seal(',start)
  s=s[:start]+'''            keys = ['{{field-' + str(i+1) + '}}' for i in range(n)]
            grid = [[key] for key in keys] if column else [keys]
            problem += '\\nEnter the entries from ' + ('top to bottom.' if column else 'left to right.') + '\\n\\n' + matrix_answer('AB', grid)
'''+s[end:]
 p.write_text(s)
 source=dest/'source_cases.json';data=json.loads(source.read_text());changed=[]
 for q in (data if isinstance(data,list)else data.get('questions',[])):
  new=qs.get(q.get(':question/id'))
  if not new:continue
  for a in [':question/problem',':question/worked-solution']:
   if a in new and q.get(a)!=new[a]:q[a]=new[a];changed.append(new.get(':question/math-academy-id',new[':question/id']))
  for f in q.get(':question/answer-fields',[]):
   other=next((v for v in new.get(':question/answer-fields',[])if v[':answer-field/key']==f[':answer-field/key']),None)
   if other and ':answer-field/correct'not in f:f[':answer-field/correct']=other[':answer-field/correct'];changed.append(new.get(':question/math-academy-id',new[':question/id']))
 evidence={'audit_basis':9009,'source_questions':sorted(set(changed)),'kind':'Authored formatting and independently derived completions; original observed snapshot provenance retained'};(dest/'repair-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n');source.write_text(json.dumps(data,indent=2)+'\n')
 metadata.append({'kp':kp[':db/id'],'kp_uuid':kp[':knowledge-point/id'],'directory':str(dest),'old_reference':g[':question-generator/script'],'old_entity':g[':db/id'],'files':list(manifest['files'])+['repair-evidence.json'],'dependencies':manifest['dependencies']})
(H/'generator-candidates.json').write_text(json.dumps(metadata,indent=2)+'\n');print('Staged two new immutable-package candidates; original package bytes unchanged.')
