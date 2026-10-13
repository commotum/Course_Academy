"""One-time source slot compiler: complete vector components only."""
import json,re
from pathlib import Path
D=Path(__file__).parent
source=json.load(open(D/'source.json'))
out={};cases=[]
for q in source['record'][':knowledge-point/questions']:
 name=q[':question/math-academy-id'];level=q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/moderate').split('/')[-1]
 slots=[]
 def add(raw,kind,fi=None):
  d={'raw':raw,'kind':kind}
  if fi is not None:d['function_index']=fi
  slots.append(d);return '@@'+str(len(slots)-1)+'@@'
 def mask(s,basis=False):
  if basis:
   # Source basis layout uses outer aligned rows, no nested aligned vectors.
   pat=r'(?<=& =)(.*?)(?= \\\\|\\end\{aligned\})'
   fi=0
   def sub(m):
    nonlocal fi
    raw=m[0]
    if not any(x in raw for x in [r'\,i',r'\,j',r'\,k','ti','(j-']):return raw
    if r'\frac{\text{d}}{\text{d}t}' in raw:
     idx=fi;fi+=1;return add(raw,'basis-derivative',idx)
    return add(raw,'basis')
   return re.sub(pat,sub,s)
  return re.sub(r'⟨[^⟩]*⟩|\[\\begin\{aligned\}.*?\\end\{aligned\}\]',lambda m:add(m[0],'column' if m[0].startswith('[') else 'tuple'),s,flags=re.S)
 prompt=q[':question/problem'];sol=q.get(':question/worked-solution','');repairs=[]
 if name=='q-128452':
  prompt=prompt.replace(r'\operatorname{ln}⁡(2t)',r'\operatorname{ln}⁡(-2t)');sol=sol.replace(r'\operatorname{ln}⁡(2t)',r'\operatorname{ln}⁡(-2t)');repairs.append('real-domain repair ln(2t) -> ln(-2t) at t=-1; derivative unchanged')
 if name=='q-33143':
  prompt=prompt.replace('|=','=');repairs+=['unrated original receives authored moderate assignment','missing correct ref independently inferred as <12,3,-12>','missing worked solution authored','capture |= separators repaired from original widget']
 notation={'q-128137':('(f(0)-3g(0))^{′}',r'(f(t)-3g(t))^{′}\big|_{t=0}'),'q-128452':('(2f(-1)-g(-1))^{′}',r'(2f(t)-g(t))^{′}\big|_{t=-1}'),'q-128458':('(2f(1)+5g(1))^{′}',r'(2f(t)+5g(t))^{′}\big|_{t=1}'),'q-128144':('(f(1)-2g(1))^{′}',r'(f(t)-2g(t))^{′}\big|_{t=1}')}
 if name in notation:
  old,new=notation[name];assert old in sol;sol=sol.replace(old,new);repairs.append('derivative evaluation notation repaired: differentiate before substituting')
 basis=name=='q-33123'
 pm=mask(prompt,basis);sm=mask(sol,basis)
 out[name]={'level':level,'prompt':pm,'solution':sm,'slots':slots,'bank':[a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']],'repairs':repairs}
 cases.append({'source_id':name,'template':name,'level':level,'parameters':{'scales':[1,1,1]},'bank_profile':name,'original_correct_present':':answer-field/correct' in q[':question/answer-fields'][0]})
json.dump(out,open(D/'templates.json','w'),indent=2,ensure_ascii=False)
json.dump(cases,open(D/'source-cases.json','w'),indent=2)
