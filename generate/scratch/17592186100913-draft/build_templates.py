"""One-time read-only extraction; writes only this private evidence directory."""
import json,re,pathlib,hashlib,sys
sys.dont_write_bytecode=True
ROOT=pathlib.Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from math_format import normalize_prose,normalize_tex,cells
D=pathlib.Path(__file__).parent; source=json.load(open(D/'source.json'));r=source['record']
def clean(s):
 # Proven in decoded strings: answer choices have two slashes before begin/end,
 # four between rows. Collapse exactly this consistently doubled capture layer.
 if r'\\begin{bmatrix}' in s:s=s.replace('\\\\','\\')
 return s
pat=re.compile(r'\\begin\{bmatrix\}([\s\S]*?)\\end\{bmatrix\}')
def mats(s):return [cells(m[1])for m in pat.finditer(s)]
def exprmat(rows):return 'matrix('+repr(rows)+')'
def lit(x):return str(int(x))
def invec(rows):return [lit(c)for row in rows for c in row]
recipes={
'q-1031': ['undefined','"["+str(a[0]*b[0])+"]"','matrix([[p[0][0],p[0][1]],[p[2][0],p[2][1]],[p[2][0],p[2][1]]])','matrix([[p[0][0],p[0][1]],[a[0]+b[0],p[2][1]]])','matrix(p)'],
'q-13636':['undefined','matrix([[b[0],a[0]],[p[1][0],p[1][1]],[p[2][0],p[2][1]]])','"["+str(abs(b[1]*a[1]))+"]"','matrix([[p[0][0],p[0][1]],[p[1][0],p[1][1]],[-p[2][0],p[2][1]]])','matrix(p)'],
'q-1038':['matrix([[a[i]*b[min(i,len(b)-1)] for i in range(len(a))]])','matrix(p[:-1])','undefined','matrix(p)','matrix([[p[0][0],-p[0][1],-p[0][2]]]+p[1:])'],
'q-129961':['matrix([[p[0][0]],[a[0]]])','matrix(p)','matrix([[-p[0][0],-p[0][1]]]+p[1:])','matrix([[p[0][0],-p[1][0]]])','matrix([[a[0]],[p[1][0]]])'],
'q-130136':['matrix(p)','matrix([[p[0][0],a[2],p[0][2],a[3]],[p[0][1],p[1][1],p[2][1],p[3][1]],[p[1][0],-a[2],p[1][2],a[1]],[p[2][0],p[2][1],p[2][2],a[0]-a[2]]])','matrix([[p[0][0],a[2],p[0][2],a[3]],[p[1][0],-a[2],p[1][2],a[1]],[p[0][1],p[1][1],p[2][1],p[3][1]],[p[2][0],p[2][1],p[2][2],a[0]-a[2]]])','matrix([[p[0][0],a[2],p[0][2]],[p[1][0],-a[2],p[1][2]],[p[2][0],p[2][1],p[2][2]],[p[3][1],p[3][2],p[3][1]]])','undefined'],
'q-130230':['matrix([[sum(a[i]*b[i] for i in range(2))]])','matrix([[x*b[0],x*(b[1]-2)] for x in a])','undefined','matrix([[sum(a[:2])]])','matrix([[a[i]*b[0],a[i]*(b[1]-2)] for i in [0,2]])'],
'q-13635':['matrix(p)','matrix([[b[0],b[1]]]+p[1:])','matrix([[b[0],p[0][1]]]+p[1:])','undefined','matrix(p[:2]+[[-p[2][0],p[2][1]]])']}
profiles={};cases=[];inventory=[]
for q in r[':knowledge-point/questions']:
 sid=q.get(':question/math-academy-id'); assert sid
 prompt=q[':question/problem']; mm=mats(prompt);reverse=sid=='q-13636';undefined=sid in ['q-13636','q-130230'];a=invec(mm[1]if reverse else mm[0]);b=invec(mm[0]if reverse else mm[1]);params={'a':list(map(int,a)),'b':list(map(int,b))};n=len(a);k=len(b)
 # Complete matrix components become slots, never substring number replacement.
 def mask(text,solution=False):
  idx=0
  def sub(m):
   nonlocal idx
   rows=cells(m[1]);idx+=1
   if rows==mm[0]:return '@FIRST@'
   if rows==mm[1]:return '@SECOND@'
   if any(r'\cdot' in c for row in rows for c in row):return '@PRODUCTS@'
   # Source 2x2 element-by-element partial matrices retain row-major stars.
   if n==2 and k==2 and solution:
    count=sum(c!='∗' for row in rows for c in row)
    return '@PARTIAL'+str(count)+'@' if count<4 else '@RESULT@'
   return '@RESULT@'
  text=pat.sub(sub,text)
  if solution and n==2 and k==2:
   # Every completed-cell equation is a full role slot.
   matches=list(re.finditer(r'\\,(-?\d+)=[^\n]*?(?= \\\\|\\end\{aligned\})',text))
   assert len(matches)==4,(sid,matches)
   for i,m in reversed(list(enumerate(matches))):text=text[:m.start()]+'@CELL'+str(i)+'@'+text[m.end():]
  return text
 fields=[]
 for f in q.get(':question/answer-fields',[]):
  fs={':answer-field/key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'],'choices':[],'correct_present':':answer-field/correct'in f}
  for i,c in enumerate(f[':answer-field/choices']):
   recipe=recipes[sid][i]if sid in recipes else 'str(p['+str((int(f[':answer-field/key'].split('-')[1])-1)//k)+']['+str((int(f[':answer-field/key'].split('-')[1])-1)%k)+'])'
   fs['choices'].append({'recipe':recipe,'type':c[':answer/type'][':db/ident'],'raw':c[':answer/value'],'feedback':c.get(':answer/feedback'),'feedback_present':':answer/feedback'in c})
  if fs['correct_present']:fs['correct_index']=next(i for i,c in enumerate(f[':answer-field/choices'])if c[':answer/id']==f[':answer-field/correct'][':answer/id'])
  fields.append(fs)
 styles=[]
 for row in mats(q.get(':question/worked-solution','')):
  for rr in row:
   for c in rr:
    if r'\cdot' in c:styles.append([c.split(r'\cdot')[0].startswith('('),c.split(r'\cdot')[1].strip().startswith('(')])
 cellstyles=[]
 for m in re.finditer(r'\\,(-?\d+)=([^\n]*?)(?= \\\\|\\end\{aligned\})',q.get(':question/worked-solution','')):
  rhs=m[2];cellstyles.append([rhs.split(r'\cdot')[0].startswith('('),rhs.split(r'\cdot')[1].strip().startswith('(')])
 profiles[sid]={'product_styles':styles,'cell_styles':cellstyles,'prompt_mask':mask(prompt),'solution_mask':mask(q.get(':question/worked-solution',''),True),'difficulty':q.get(':question/difficulty',{}).get(':db/ident'),'solution_present':':question/worked-solution'in q,'fields_present':':question/answer-fields'in q,'fields':fields,'reverse':reverse,'undefined':undefined,'parameters':params,'template':('undefined-evidence'if undefined else 'outer-'+str(n)+'x'+str(k)),'opaque_bank':sid in ['q-1031','q-13636','q-129961','q-130136','q-130230'],'source_db_id':q[':db/id']}
 cases.append({'source_id':sid,'template':profiles[sid]['template'],'level':profiles[sid]['difficulty'].split('/')[-1]if profiles[sid]['difficulty']else 'easy','parameters':params,'bank_profile':sid,'unrated_assignment':'authored easy replay routing only'if not profiles[sid]['difficulty']else None})
(D/'templates.json').write_text(json.dumps(profiles,indent=2)+'\n');(D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(D/'independent-inventory.json').write_text(json.dumps({**{k:v for k,v in source.items()if k!='record'},'questions':[]},indent=2)+'\n')
print('extracted',len(profiles),'profiles')
