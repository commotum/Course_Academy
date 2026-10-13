from pathlib import Path
import json,re,shutil
HERE=Path(__file__).resolve().parent
GEN=HERE.parents[1]
source=json.loads((GEN/'runs/current/sources/17592186087693.json').read_text())
shutil.copyfile(GEN/'runs/current/sources/17592186087693.json',HERE/'source.json')
for kind,dbid in [('topics','17592186048896'),('lessons','17592186048896')]:
 shutil.copyfile(GEN/f'runs/current/{kind}/{dbid}.json',HERE/f'{kind}.json')
recipes={
'q-11454':['c,r','r,c','r,r','r+1,r+1','r,c-1'],
'q-7806':['r,c','c,r','c,c','r,c+1','r,r'],
'q-125527':['r-1,c-1','r,c','r-1,c','r-2,c-2','r,c-2'],
'q-125528':['r,c+1','r-1,c-1','r,c','r+1,c','r+1,c+1'],
'q-125529':['r,c-1','r-1,c-1','r+2,c+2','r+2,c','r,c'],
'q-69542':['r-1,c','c,r','r,c','r,c+1','r-1,c+2'],
}
specs={};cases=[];component_rows=[]
for q in source['record'][':knowledge-point/questions']:
 sid=q[':question/math-academy-id'];prompt=q[':question/problem']
 mat=re.search(r'\\begin\{(bmatrix|aligned)\}(.*?)\\end\{\1\}',prompt,re.S)
 entries=[[v.strip() for v in row.split('&')] for row in mat[2].split(r'\\')]
 name=re.search(r'\$([A-Z])',prompt)[1]
 f=q[':question/answer-fields'][0];kind=f[':answer-field/type'][':db/ident'].split('/')[-1]
 if kind=='blank': template='context-dual-blank' if sid=='q-139406' else 'let-dual-blank'
 else: template='bmatrix-radio' if mat[1]=='bmatrix' else 'aligned-radio-break' if sid=='q-69542' else 'aligned-radio-inline'
 mask=prompt[:mat.start(2)]+'@ARRAY@'+prompt[mat.end(2):]
 mask=mask.replace('$'+name,'$@NAME@').replace(name+'=','@NAME@=')
 profile='observed-'+sid
 formats=[]
 for ix,a in enumerate(f[':answer-field/choices']):
  if kind=='radio':
   m=re.fullmatch(r'(\d+)(.*?)(\d+)',a[':answer/value'])
   formats.append({'recipe':recipes[sid][ix],'separator':m[2]})
 specs[profile]={'template':template,'prompt_mask':mask,'environment':mat[1],'field_type':kind,'field_keys':[ff[':answer-field/key'] for ff in q[':question/answer-fields']], 'bank':formats,'solution_name':'R' if sid=='q-139406' else None,'source':sid,'missing_solution':':question/worked-solution' not in q,'missing_correct':':answer-field/correct' not in f}
 cases.append({'source_id':sid,'level':'easy','authored_level_assignment':':question/difficulty' not in q,'template':template,'bank_profile':profile,'parameters':{'entries':entries,'name':name}})
 component_rows.append({'source_id':sid,'rows':len(entries),'columns':len(entries[0]),'entry_forms':entries,'profile':profile,'bank':[{'original':a[':answer/value'],**formats[ix]} for ix,a in enumerate(f[':answer-field/choices'])] if kind=='radio' else {ff[':answer-field/key']:ff[':answer-field/choices'][0][':answer/value'] for ff in q[':question/answer-fields']}})
(HERE/'recipes.json').write_text(json.dumps(specs,indent=2)+'\n')
(HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
(HERE/'source-components.json').write_text(json.dumps(component_rows,indent=2)+'\n')
# Authoritative legacy widget evidence: layout/banks present, correct markers absent.
legacy=json.loads(Path('/home/jake/Developer/MA/DATA/Lessons/861/Source/861.json').read_text())
def find(x):
 if isinstance(x,dict):
  if x.get('question_id') in ('11454','7806'): yield x
  else:
   for v in x.values():yield from find(v)
 elif isinstance(x,list):
  for v in x:yield from find(v)
(HERE/'legacy-widget-evidence.json').write_text(json.dumps(list(find(legacy)),indent=2)+'\n')
