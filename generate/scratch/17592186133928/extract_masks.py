"""One-time extraction of full observed source templates; frozen input only."""
import json,re
from pathlib import Path
ROOT=Path(__file__).parent
cap=json.loads((ROOT/'source.json').read_text());masks={};cases=[]
for q in cap['record'][':knowledge-point/questions']:
 sid=q[':question/math-academy-id'];slots={};attrs={}
 for key in [':question/problem',':question/worked-solution',':question/difficulty']:
  if key not in q:continue
  value=q[key]
  if isinstance(value,dict):attrs[key]=value[':db/ident'];continue
  if key==':question/problem':
   # Capture only the complete field definition; never replace x/i/k tokens.
   match=re.search(r'(F\(x,\s*y,\s*z\)\s*=)(.*?)(,?\$)',value)
   assert match,sid
   start,end=match.span(2);fragment=match[2]
   if fragment.endswith(','):fragment=fragment[:-1];end-=1
   slots['field']=fragment;value=value[:start]+'{{field}}'+value[end:]
  else:
   def block(m):
    content=m[0]
    if 'F(r(t)) &' in content:kind='field'
    elif 'F(r(t))\\cdot' in content and '&' in content and not ('{∬}' in content):kind='dot'
    elif '{∬}' in content and '&' in content:kind='integral'
    else:return content
    row_counter=[0]
    def rhs(mm):
     idx=row_counter[0];row_counter[0]+=1
     raw=mm[2]
     if kind=='integral' and idx<2:return mm[0]
     # Keep punctuation outside the complete mathematical component.
     ending=''
     if raw.endswith('.'):raw,ending=raw[:-1],'.'
     name=kind+'_'+str(idx);slots[name]=raw
     return mm[1]+'{{'+name+'}}'+ending
    return re.sub(r'(&\s*=)(.*?)(?=\s*\\\\|\\end\{aligned\})',rhs,content,flags=re.S)
   value=re.sub(r'\\begin\{aligned\}.*?\\end\{aligned\}',block,value,flags=re.S)
  attrs[key]=value
 banks=[]
 for f in q[':question/answer-fields']:
  b={'values':[a[':answer/value'] for a in f[':answer-field/choices']]}
  if ':answer-field/correct' in f:
   b['correct_index']=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][':answer/id'])
  banks.append(b)
 opening=q.get(':question/worked-solution','').split('\n\nAlong the curve')[0]
 masks[sid]={'attributes':attrs,'slots':slots,'banks':banks,'opening':opening}
 cases.append({'source_id':sid,'source_db_id':q[':db/id'],'template':sid,'parameters':{'c':1},'bank_profile':'raw','level':q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/hard').split('/')[-1],'authored_level_assignment':sid=='q-162377'})
(ROOT/'source-masks.json').write_text(json.dumps(masks,indent=2,ensure_ascii=False)+'\n')
(ROOT/'source-cases.json').write_text(json.dumps(cases,indent=2,ensure_ascii=False)+'\n')
