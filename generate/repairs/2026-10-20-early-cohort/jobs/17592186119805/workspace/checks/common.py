"""Independent reading of visible question and solution content; no generator math reused."""
import importlib.util,json,re,sys
from fractions import Fraction
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/'evidence';E.mkdir(exist_ok=True)
def load_generator(path=None):
 s=importlib.util.spec_from_file_location('candidate',path or ROOT/'17592186119805.py')
 g=importlib.util.module_from_spec(s);s.loader.exec_module(g);return g
def save(name,obj):
 p=E/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def scalar(v):
 v=str(v).strip().replace('\\\\frac','\\frac').replace(' ','')
 m=re.fullmatch(r'(-?)\\frac\{(-?\d+)\}\{(\d+)\}',v)
 return (-1 if m[1] else 1)*Fraction(int(m[2]),int(m[3])) if m else Fraction(v)
def mats(text):
 return [[scalar(x) for x in re.split(r'\\\\',m)] for m in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)]
def choices(q):return q[':question/answer-fields'][0][':answer-field/choices']
def key(q):
 c=q[':question/answer-fields'][0][':answer-field/correct'];cid=c[':answer/id'] if isinstance(c,dict) else c[1]
 return next(a[':answer/value'] for a in choices(q) if a[':answer/id']==cid)
def value(v):return v if v=='No solution' else scalar(v)
def solve(q):
 text=q[':question/problem'];a,u,*bs=mats(text)
 m=re.search(r'if \$(\d+)',text);c=int(m[1]) if m else 1
 sign=-1 if re.search(r'\{a\}_\{1\}-[a-z]',text) else 1
 b=bs[0] if bs else [Fraction(0)]*len(a)
 residual=[sign*(x-c*y) for x,y in zip(b,a)]
 ratios={x/y for x,y in zip(residual,u) if y}
 answer=next(iter(ratios)) if len(ratios)==1 and all(y or x==0 for x,y in zip(residual,u)) else 'No solution'
 return answer,residual,(a,u,b,c,sign)
def verify(r):
 q=r['question'];answer,residual,(a,u,b,c,sign)=solve(q)
 assert value(key(q))==answer,(q[':question/id'],key(q),str(answer))
 bank=[value(x[':answer/value']) for x in choices(q)]
 assert len(bank)==5 and len(set(bank))==5 and bank.count(answer)==1
 assert len({x[':answer/id'] for x in choices(q)})==5
 f=q[':question/answer-fields'][0]
 assert f[':answer-field/type']==':answer-field.type/radio'
 sm=mats(q[':question/worked-solution'])
 expected=[a,u,b,u,a,b,u,residual] if sign==-1 else [a,u,b,u,b,a,u,residual]
 if answer=='No solution':
  pivot=next(i for i,x in enumerate(u) if x);t=residual[pivot]/u[pivot]
  expected += [u,[t*x for x in u],residual]
  assert 'Therefore, there is no $' in q[':question/worked-solution']
 else:
  letter=re.search(r'Find \$([a-z])',q[':question/problem'])[1]
  m=re.search(re.escape('$'+letter+'=')+r'(.*?)\.\$',q[':question/worked-solution'])
  assert m and scalar(m[1])==answer
 assert sm==expected,(q[':question/id'],'solution matrices inconsistent')
 return answer
# Retained reviewer strategy: only labels, zero target and the visible bank.
def old_shortcut(q):
 text=q[':question/problem'];letter=re.search(r'Find \$([a-z])',text)[1]
 nums=sorted(value(a[':answer/value']) for a in choices(q) if a[':answer/value']!='No solution')
 if '=0$' in text:return 'No solution'
 if letter=='l' and any(a[':answer/value']=='No solution' for a in choices(q)):
  return next((x for x in nums if x<0),None)
 if letter=='l':return nums[-2]
 if letter=='h':return nums[-1]
 if letter=='m':return nums[0]
 if letter=='k':return nums[1]
 if letter=='j':return next((x for x in nums if x>0),None)
 return None
