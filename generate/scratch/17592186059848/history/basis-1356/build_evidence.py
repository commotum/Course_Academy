"""One-time extraction of captured evidence; generator never loads raw questions."""
import json,re,shutil
from pathlib import Path
import sympy as s
D=Path(__file__).parent
capture=Path('generate/runs/current/sources/17592186059848.json')
shutil.copyfile(capture,D/'source.json')
source=json.load(open(capture))
def math(t):
 t=t.replace(r'\,','').replace(' ','')
 t=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'(\1)/(\2)',t)
 t=re.sub(r'\\sqrt\{([^{}]+)\}',r'sqrt(\1)',t)
 t=re.sub(r'(\d|\))(?=sqrt)',r'\1*',t)
 return s.simplify(s.sympify(t))
registry={};cases=[];profiles={}
for q in source['record'][':knowledge-point/questions']:
 sid=q[':question/math-academy-id'];text=q[':question/problem']
 name=re.search(r'matrix \$(\w)\$',text)[1]
 matrix=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',text,re.S)[0]
 values=[str(math(v))for row in matrix.split(r'\\')for v in row.split('&')]
 lines=[l for l in text.splitlines() if l.startswith('- ') or re.match(r'I{1,3}\.',l)]
 statements=[];claim=[]
 for l in lines:
  if 'det(' in l:
   val=math(re.search(r'=([^$]+)',l)[1]);statements.append('det');claim.append(str(val))
  else:statements.append('nonsingular' if '**not**' in l else 'singular');claim.append(None)
 solution=q[':question/worked-solution'];rows=re.findall(r'\\begin\{aligned\}det\(.*?\\end\{aligned\}\n\$\$',solution,re.S)[0]
 # Count only outer alignment rows by & =, not matrix row separators.
 n=len(re.findall(r'& =',rows))
 signature=(q[':question/difficulty'][':db/ident'].split('/')[-1],tuple(statements),'roman-spaced' if 'I.' in text and '\n\nII.' in text else 'roman' if 'I.' in text else 'bullets',n)
 template='_'.join([signature[0],signature[2],*statements,str(n)])
 registry[template]={'level':q[':question/difficulty'][':db/ident'].split('/')[-1],
 'statements':statements,'layout':'roman-spaced' if 'I.' in text and '\n\nII.' in text else 'roman' if 'I.' in text else 'bullets',
 'solution_rows':n,'use_ne':r'\ne 0' in solution,'intro_suffix':'  ' if 'as follows:  ' in solution else '',
 'blank_before_since':'\n\n \n\n' if '\n\n \n\nSince' in solution else '\n\n',
 'source_ids':[sid] if template not in registry else registry[template]['source_ids']+[sid],'matrix_features':'fraction/radical' if any('/' in v or 'sqrt' in v for v in values)else 'integer'}
 for i,f in enumerate(q[':question/answer-fields']):
  vals=sorted(c[':answer/value']for c in f[':answer-field/choices'])
  pname='bank_'+str(len(profiles)+1)
  existing=next((k for k,v in profiles.items()if v['values']==vals),None)
  if existing:pname=existing
  else:profiles[pname]={'values':vals,'origin':'observed','source_fields':[]}
  profiles[pname]['source_fields'].append([sid,i])
  cases.append({'source_id':sid,'source_field_index':i,'template':template,'level':registry[template]['level'],
   'parameters':{'matrix':values,'name':name,'claims':claim,'style':{'use_ne':r'\ne 0' in solution,'intro_suffix':'  ' if 'as follows:  ' in solution else '', 'blank_before_since':'\n\n \n\n' if '\n\n \n\nSince' in solution else '\n\n'}},'bank_profile':pname,
   'correct_original':f.get(':answer-field/correct',{}).get(':answer/value'),
   'source_field_id':f[':answer-field/id'],'source_question_id':q[':question/id']})
registry['dense_exact']={'level':'hard','statements':['singular','nonsingular','det'],'layout':'roman',
 'solution_rows':6,'use_ne':True,'intro_suffix':'','blank_before_since':'\n\n',
 'source_ids':[],'matrix_features':'dense rational and radical entries (authored)'}
json.dump({'templates':registry,'profiles':profiles},open(D/'recipes.json','w'),indent=2)
json.dump(cases,open(D/'source-cases.json','w'),indent=2)
item=next(i for i in json.load(open('/home/jake/Developer/MA/DATA/Lessons/153/Source/153.json'))['lesson']['items']if i.get('question_id')=='128490')
json.dump(item,open(D/'q-128490-authoritative-widget.json','w'),indent=2)
print(len(registry),len(profiles),len(cases))
