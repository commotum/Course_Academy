"""One-time structural extraction from immutable captured sources; no registered imports."""
import sys
sys.dont_write_bytecode=True
import json,re,shutil,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent; ROOT=D.parents[2]
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
import math_format as mf
R=D/'reference'; F=ROOT/'generate/runs/current/refresh-2026-10-14'
for name,src in [('topic.json',F/'topics/17592186050825.json'),('lesson.json',F/'lessons/17592186050825.json'),('supplemental-current-source.json',ROOT/'generate/runs/current/sources/17592186100868.json'),('ma-original-1195.json',Path('/home/jake/Developer/MA/DATA/Lessons/1195/Source/1195.json'))]:
 if src.exists():shutil.copyfile(src,R/name)
for p in [ROOT/'generate/principles.md',ROOT/'generate/runs/current/worker-instructions.md',ROOT/'docs/math-content.md',*sorted((ROOT/'generate/docs').glob('[3-7]-*.md'))]:shutil.copyfile(p,R/p.name)
wrapper=json.loads((R/'source-wrapper.json').read_text());src=wrapper['record'];(D/'source.json').write_text(json.dumps(src,indent=2)+'\n')
shutil.copyfile(ROOT/'scripts/question_capture/math_format.py',D/'math_format.py')
def spans(text):
 out=[];end=0
 for m in re.finditer(r'\\begin\{bmatrix\}',text):
  if m.start()<end:continue
  e=mf.environment(text,m.start());out.append((m.start(),e[2],text[e[0]:e[1]]));end=e[2]
 return out
def rows(body):
 if body.startswith(r'\begin{aligned}'):
  e=mf.environment(body,0);return [[''.join(r)] for r in mf.cells(body[e[0]:e[1]])]
 return mf.cells(body)
def masked(text):
 nodes=spans(text)
 for i,(a,b,_) in list(enumerate(nodes))[::-1]:text=text[:a]+'@@M'+str(i)+'@@'+text[b:]
 return text,[rows(x[2]) for x in nodes]
levels={};templates={};cases=[];inventory=[]
for q in src[':knowledge-point/questions']:
 sid=q[':question/math-academy-id'];level=q.get(':question/difficulty',{}).get(':db/ident','easy').split('/')[-1]
 prompt,mat=masked(q[':question/problem']); assert len(mat)==2
 sol=q.get(':question/worked-solution');solmask,stages=masked(sol) if sol else ('',[])
 variables=sorted(set(re.findall('[a-z]', ''.join(c for m in mat for row in m for c in row))))
 fields=[]
 for f in q[':question/answer-fields']:
  fields.append({'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'].split('/')[-1],'choices':[a[':answer/value'].replace('\\\\','\\') if False else a[':answer/value'] for a in f[':answer-field/choices']], 'correct_index':next((i for i,a in enumerate(f[':answer-field/choices']) if a.get(':answer/id')==f.get(':answer-field/correct',{}).get(':answer/id')),None)})
 # Captured choices have an extra serialization layer; shared normalizer fixes them.
 for f in fields:f['choices']=[mf.normalize_tex(x) for x in f['choices']]
 templates[sid]={'source_id':sid,'level':level,'source_level':q.get(':question/difficulty'), 'prompt_mask':prompt,'inputs':mat,'solution_mask':solmask,'solution_matrices':stages,'variables':variables,'fields':fields,'missing_solution':sol is None,'missing_correct':any(f['correct_index'] is None for f in fields)}
 cases.append({'source_id':sid,'template':sid,'level':level,'parameters':{'scales':{v:1 for v in variables},'names':{v:v for v in variables}},'profile':'observed'})
 if sid=='q-13554':cases[-1]['parameters']['vector']=[1,2]
 if sid=='q-318595':cases[-1]['parameters']['matrix_coefficients']=[6,-4,-5,2]
 inventory.append({'source_id':sid,'source_uuid':q[':question/id'],'source_level':q.get(':question/difficulty'),'field_count':len(fields),'choice_count':sum(len(f['choices']) for f in fields),'worked_solution_present':sol is not None})
(D/'templates.json').write_text(json.dumps(templates,indent=2)+'\n');(D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(D/'independent-inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')
print('Extracted',len(templates),'source templates')
