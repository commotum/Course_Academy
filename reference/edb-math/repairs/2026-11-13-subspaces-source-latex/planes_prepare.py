"""Prepare source-backed math-only repairs for the plane KP; no database writes."""
import json,re,sys
from pathlib import Path
from collections import Counter,defaultdict
from bs4 import BeautifulSoup, NavigableString, Tag
ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
from import_historical_question_content import Renderer
MATH=re.compile(r'\$\$[\s\S]*?\$\$|\$(?:\\.|[^$])*?\$')
class Faithful(Renderer):
 def render(self,n,extract_fields=False):
  if getattr(n,"name",None)=="svg" and n.find("title"):
   tex="".join(str(c) if isinstance(c,NavigableString) else self.m(c.find("math")) if c.name=="mjx-container" else self.render(c,extract_fields) for c in n.find("title").children)
   delimiter="$$" if "mjpage__block" in n.parent.get("class",[]) else "$"
   return delimiter+tex+delimiter
  return super().render(n,extract_fields)
 def math_node(self,n):
  if getattr(n,'name',None)=='mspace':
   width=n.get('width','')
   if re.fullmatch(r'[+-]?\d+(?:\.\d+)?(?:em|ex|px|pt)',width):return r'\hspace{'+width+'}'
  return super().math_node(n)
def contents(p):
 if p.suffix=='.json':return json.loads(p.read_text())['html']
 return p.read_text()
def body(s):
 return s[2:-2].strip() if s.startswith('$$') else s[1:-1].strip()
def key(s):
 s=s.replace(r'\Pi','Π').replace(r'\checkmark','✓').replace(r'\not\in',r'\notin')
 s=re.sub(r'\\(?:mathbf|mathbb|mathrm|mathit|boldsymbol)(?=\{)','',s)
 s=re.sub(r'\\color\{[^{}]+\}','',s)
 s=re.sub(r'\\hspace\{[^{}]+\}|\\(?:quad|qquad)\b|\\[,;!:]','',s)
 s=s.replace(r'\left','').replace(r'\right','')
 s=re.sub(r'\\begin\{array\}\{[^{}]+\}|\\end\{array\}','',s)
 s=s.replace(r'\begin{bmatrix}','[').replace(r'\end{bmatrix}',']')
 s=s.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','')
 s=re.sub(r'[{}\s]','',s)
 return s

def sig(s):
 return Counter(re.findall(r'\\(?:mathbf|mathbb)\{[^{}]+\}|\\Pi\b|\\color\{[^{}]+\}|\\hspace\{[^{}]+\}',s))

x=json.loads((HERE/'snapshot.json').read_text());kp=next(k for k in x['topic'][':topic/knowledge-points'] if k[':db/id']==17592186119928)
qs=[kp[':knowledge-point/canonical-example']]+kp[':knowledge-point/questions']
paths=Path('/tmp/planes-source-paths.txt').read_text().splitlines()
proposals=[];audit=[]
for q in qs:
 ma=q[':question/math-academy-id'];num=ma[2:]
 if ma.startswith('e'):
  p=ROOT/'reference/mathacademy/capture/differential/14246322/observations/step-e10980-5c1f461373f62c788a41.html'
  soup=BeautifulSoup(contents(p),'html.parser');sections=[(p,soup.select_one('.exampleQuestion')),(p,soup.select_one('.exampleExplanation'))]
 elif num in ['156728','157468']:
  base=ROOT/'reference/mathacademy/question-capture-workers/linear/14044012'
  prompt=base/f'q-{num}-before.json';solution=base/f'history-q-{num}.json'
  sections=[(prompt,BeautifulSoup(contents(prompt),'html.parser').select_one('.questionWidget-text')),(solution,BeautifulSoup(contents(solution),'html.parser'))]
 else:
  candidates=sorted([ROOT/p for p in paths if f'history-solution-q-{num}-' in p],key=lambda p:('14246322' not in str(p),str(p)))
  solution=candidates[0];prompt=next(solution.parent.glob(f'history-q-{num}-*.html'))
  sections=[(prompt,BeautifulSoup(contents(prompt),'html.parser').select_one('.questionText')),(solution,BeautifulSoup(contents(solution),'html.parser'))]
 mapping=defaultdict(list);source_audit=[]
 for p,root in sections:
  assert root is not None,ma
  r=Faithful(1853);text=r.text(root).replace(r'\mathrm{Π}',r'\Pi').replace('✓',r'\checkmark ')
  assert not r.errors,(ma,r.errors)
  for match in MATH.finditer(text):
   tex=body(match.group());mapping[key(tex)].append((tex,str(p.relative_to(ROOT))))
  source_audit.append({'path':str(p.relative_to(ROOT)),'mathvariant_normal_pi':len(root.find_all('mi',attrs={'mathvariant':'normal'},string='Π')),'raw_math_formulas':len(root.find_all('math'))})
 values=[(q[':db/id'],':question/problem',q[':question/problem']),(q[':db/id'],':question/worked-solution',q[':question/worked-solution'])]
 seen=set()
 for f in q.get(':question/answer-fields',[]):
  values.append((f[':db/id'],':answer-field/key',f[':answer-field/key']))
  for a in f.get(':answer-field/choices',[])+([f[':answer-field/correct']] if f.get(':answer-field/correct') else []):
   if a[':db/id'] in seen:continue
   seen.add(a[':db/id']);values.append((a[':db/id'],':answer/value',a.get(':answer/value','')))
 unmatched=[];matched=0;changes=[]
 for eid,attr,before in values:
  field_changes=[]
  def repair(m):
   global matched
   old=m.group();oldtex=body(old);candidates=mapping.get(key(oldtex),[])
   if not candidates:
    unmatched.append({'entity':eid,'attribute':attr,'formula':old});return old
   matched+=1
   # All matching formulas must agree on source style to avoid context ambiguity.
   signatures={tuple(sorted(sig(t).items())) for t,p in candidates}
   if len(signatures)>1:
    unmatched.append({'entity':eid,'attribute':attr,'formula':old,'reason':'ambiguous source styles'});return old
   expected,source=candidates[0]
   missing=sig(expected)-sig(oldtex)
   if not missing:return old
   delimiter='$$' if old.startswith('$$') else '$'
   after=delimiter+ ('\n' if delimiter=='$$' else '')+expected+ ('\n' if delimiter=='$$' else '')+delimiter
   field_changes.append({'before':old,'after':after,'source':source,'missing':dict(missing)})
   return after
  after=MATH.sub(repair,before)
  if before!=after:
   proposals.append({'entity':eid,'attribute':attr,'before':before,'after':after,'reason':'Restore source MathML normal capital Pi, vector/zero boldface, real-number blackboard bold, colored verdict symbols and authored spacing; preserve surrounding prose and response structure.','source':sorted({c['source'] for c in field_changes}),'formula_changes':field_changes})
   changes.extend(field_changes)
 audit.append({'entity':q[':db/id'],'ma_id':ma,'sources':source_audit,'fields_checked':len(values),'math_formulas_matched':matched,'unmatched_formulas':unmatched,'formula_changes':len(changes)})
(HERE/'planes-proposals.json').write_text(json.dumps(proposals,indent=2)+'\n')
(HERE/'planes-audit.json').write_text(json.dumps({'basis':x['basis'],'knowledge_point':kp[':db/id'],'questions':audit},indent=2)+'\n')
print('proposals',len(proposals),'formula changes',sum(len(p['formula_changes']) for p in proposals))
for a in audit:print(a['ma_id'],'matches',a['math_formulas_matched'],'changes',a['formula_changes'],'unmatched',a['unmatched_formulas'])
