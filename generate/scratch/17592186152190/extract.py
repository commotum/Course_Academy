"""One-time extraction of parameterized prose skeletons and complete geometric banks."""
import json,re,hashlib
from pathlib import Path
from fractions import Fraction
D=Path(__file__).resolve().parent
src=json.loads((D/'source.json').read_text()); qs=src['record'][':knowledge-point/questions']
def angle(s):
 s=s.replace(' ','');s=re.sub(r'\\frac\{(.*?)\}\{(.*?)\}',r'(\1)/(\2)',s);s=re.sub(r'(\d)\\pi',r'\1*1',s).replace(r'\pi','1');return Fraction(eval(s,{'__builtins__':{}},{})).limit_denominator()
def interval(s):
 text=s.split('[')[1];parts=text.rstrip('])').split(',');return [str(angle(x)) for x in parts]+[s.rstrip().endswith(']')]
def fmt(n):return ('+' if n>0 else '')+str(n) if n else ''
profiles={};templates={};cases=[];mapping=[]
for q in qs:
 sid=q[':question/math-academy-id']; level=q[':question/difficulty'][':db/ident'].split('/')[-1]
 equation=re.search(r'x=(\d+)\\operatorname\{cos\}⁡\\theta ([-+]\d+)?,\\,y=(\d+)\\operatorname\{sin\}⁡\\theta ([-+]\d+)?',q[':question/problem']);assert equation,sid
 a,h,b,k=int(equation[1]),int(equation[2]or 0),int(equation[3]),int(equation[4]or 0)
 fields=q[':question/answer-fields'];kind=fields[0][':answer-field/type'][':db/ident'].split('/')[-1]
 if kind=='radio':
  correct=interval(fields[0][':answer-field/correct'][':answer/value']);bank=[interval(x[':answer/value']) for x in fields[0][':answer-field/choices']]
  canonical=sorted(bank);pk='observed_'+hashlib.sha256(json.dumps(canonical).encode()).hexdigest()[:10]
  profiles.setdefault(pk,{'intervals':canonical,'sources':[]})['sources'].append(sid)
 else:
  correct=[str(angle(next(f for f in fields if f[':answer-field/key']==key)[':answer-field/correct'][':answer/value'])) for key in ('field-1','field-2')]+[True];pk=None;bank=[]
 p={'a':a,'b':b,'h':h,'k':k,'lo':correct[0],'hi':correct[1]}
 def skeleton(text,solution=False):
  text=re.sub(r'!\[.*?\]\(.*?\)',lambda m:'![](@@'+('solution' if solution else 'prompt')+'@@)',text)
  text=re.sub(r'(?:x|p)=\d+\\operatorname\{cos\}⁡\\theta (?:[-+]\d+)?',lambda m:r'x=@@a@@\operatorname{cos}⁡\theta @@h_sign@@',text)
  text=re.sub(r'(?:y|q)=\d+\\operatorname\{sin\}⁡\\theta (?:[-+]\d+)?',lambda m:r'y=@@b@@\operatorname{sin}⁡\theta @@k_sign@@',text)
  text=re.sub(r'a=\d+',lambda m:'a=@@a@@',text);text=re.sub(r'b=\d+',lambda m:'b=@@b@@',text)
  text=re.sub(r'centered at the point \$\([-+]?\d+,[-+]?\d+\),',lambda m:'centered at the point $(@@h@@,@@k@@),',text)
  if solution:
   # Ellipse eccentric angle, not geometric polar angle: one mathematical repair in every source.
   text=text.replace('central angle formed by a point $(x,y)$ on the elipse and the $x$-axis','parameter angle on the unit circle with coordinates $(x/a,y/b)$')
   text=text.replace('central angle formed by a point $(x,y)$ on the ellipse and the $x$-axis','parameter angle on the unit circle with coordinates $(x/a,y/b)$')
   text=text.replace('central angle formed by a point $(x,y)$ on the ellipse and the line parallel to the $x$-axis and crossing the center of the ellipse','parameter angle on the unit circle with coordinates $((x-h)/a,(y-k)/b)$')
   text=text.replace('central angle formed by a point $(x,y)$ on the ellipse and the horizontal line through its center','parameter angle on the unit circle with coordinates $((x-h)/a,(y-k)/b)$')
   text=text.replace('central angle measured from the horizontal line through the center $(h,k).$','parameter angle on the unit circle with coordinates $((x-h)/a,(y-k)/b).$')
   text=text.replace(r'+k\,\theta',r'+k,\,\theta')
  return text
 problem=skeleton(q[':question/problem']);solution=skeleton(q[':question/worked-solution'],True)
 layout=[{'key':f[':answer-field/key'],'type':kind} for f in fields]
 key={'level':level,'problem':problem,'solution':solution,'layout':layout,'arc':correct[:2]}
 tname=level+'_'+kind+'_'+hashlib.sha256(json.dumps(key,sort_keys=True).encode()).hexdigest()[:8]
 templates.setdefault(tname,{**key,'sources':[],'profiles':[],'prompt_context':sid=='q-328327'})['sources'].append(sid)
 if pk and pk not in templates[tname]['profiles']:templates[tname]['profiles'].append(pk)
 cases.append({'source_id':sid,'template':tname,'parameters':p,'bank_profile':pk})
 mapping.append({'source_id':sid,'template':tname,'profile':pk,'parameters':p,'choices':[{'field':f[':answer-field/key'],'value':z[':answer/value'],'correct':z[':answer/id']==f[':answer-field/correct'][':answer/id'],'recipe':interval(z[':answer/value']) if kind=='radio' else ['endpoint',f[':answer-field/key']]} for f in fields for z in f[':answer-field/choices']]})
(D/'templates.json').write_text(json.dumps({'templates':templates,'profiles':profiles},indent=2,ensure_ascii=False)+'\n');(D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(D/'choice-mapping.json').write_text(json.dumps(mapping,indent=2,ensure_ascii=False)+'\n')
print(len(templates),'templates',len(profiles),'complete radio banks')
