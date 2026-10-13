"""Private extraction; outputs parameterized component masks, never generator answers."""
import json,re,shutil
from pathlib import Path
import sympy as sp
D=Path(__file__).resolve().parent
S=json.loads((D/'source.json').read_text()); templates={}; cases=[]
def rational(s):
 s=s.strip(); sign=-1 if s.startswith('-') else 1;s=s.lstrip('+-')
 m=re.fullmatch(r'\\frac\{(\d+)\}\{(\d+)\}',s)
 return sign*sp.Rational(*m.groups()) if m else sign*sp.Rational(s)
def tex(v,decimal=False):
 v=sp.Rational(v)
 if decimal and v.q in (1,2): return str(int(v)) if v.q==1 else str(float(v))
 return str(v) if v.q==1 else ('-' if v<0 else '')+r'\frac{'+str(abs(v.p))+'}{'+str(v.q)+'}'
def term(v,n,decimal=False,force=False):
 return ('-' if v==-1 else '' if v==1 else tex(v,decimal)) + n if abs(v)!=1 or not force else tex(v,decimal)+n
def total(v,w,n,m,decimal=False,force=False):
 return term(v,n,decimal,force)+('+' if w>0 else '')+term(w,m,decimal,force)
for q in S['record'][':knowledge-point/questions']:
 sid=q[':question/math-academy-id']; sol=q[':question/worked-solution']; prob=q[':question/problem']
 names=re.search(r'\$([a-z])=\\lambda ([a-z])\+\\mu ([a-z])\$',prob).groups();target,u,v=names
 vals=re.findall(r'\\lambda\s*=\s*(.*?)[,$]',sol),re.findall(r'\\mu\s*=\s*(.*?)[.$]',sol)
 # Scalar conclusion, rather than generic lambda expression.
 L=re.findall(r'\\lambda\s*=\s*(-?(?:\\frac\{\d+\}\{\d+\}|\d+(?:\.\d+)?))',sol)[-1]
 M=re.findall(r'\\mu\s*=\s*(-?(?:\\frac\{\d+\}\{\d+\}|\d+(?:\.\d+)?))',sol)[-1]
 a,b=rational(L),rational(M)
 lens=re.findall(r'([A-Z]{2})=(.*?)(?:\\cdot )?\|([a-z])\|',sol)
 first,mag1,n1=lens[0];second,mag2,n2=lens[1]
 c1=a if n1==u else b;c2=a if n2==u else b
 decimal='2.5' in sol
 t1=term(c1,n1,decimal);t2=term(c2,n2,decimal)
 tsum=total(c1,c2,n1,n2,decimal);ans=total(a,b,u,v,decimal)
 force=bool(re.search(r'Consequently.*?=[+-]?1[a-z]',sol));ansforce=total(a,b,u,v,decimal,force)
 replacements=[]
 # Complete component substitutions, from longest mathematical components first.
 def add(old,key):
  nonlocal_dummy=None
  replacements.append((old,'{{'+key+'}}'))
 add('\\lambda ='+L,'lambda_eq');add('\\mu ='+M,'mu_eq')
 # q327075 ends with a joint displayed scalar statement.
 add('\\lambda ='+L+r',\,\mu ='+M+'.','pair_eq')
 for seg,mag,n,c,key in ((first,mag1,n1,c1,'length1'),(second,mag2,n2,c2,'length2')):
  full=re.search(re.escape(seg)+r'=.*?\|'+n+r'\|',sol).group()
  add(full,key)
  add(r'\overset{\to }{'+seg+'}='+term(c,n,decimal)+'.','hence'+key[-1])
 # Only numerical combination expressions are replaced; protect basis labels/prose.
 add(tsum,'path_terms');add(ansforce,'answer_terms')
 # Prefer answer expression after Conseq; path expression elsewhere.
 before,after=sol.split('Consequently,',1)
 for old,new in sorted(replacements,key=lambda z:len(z[0]),reverse=True):
  before=before.replace(old,new)
  if new!='{{path_terms}}':after=after.replace(old,new)
 solmask=before+'Consequently,'+after
 # replacements can absorb parameterized numeric combination into inline general expression safely.
 # Source correct scalar values are exclusively rendered from a/b.
 images=re.findall(r'!\[\]\((.*?)\)',prob+sol)
 for role,ref in zip(('prompt_asset','solution_asset'),images):
  dst=D/ref;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(Path('/media/jake/SSD/EDB/math')/ref,dst)
  if role=='prompt_asset':prob=prob.replace(ref,'{{prompt_asset}}')
  else:solmask=solmask.replace(ref,'{{solution_asset}}')
 if sid=='q-275128':
  prob=prob.replace('$'+L+'$','{{field-1}}').replace('$'+M+'$','{{field-2}}')
 fields=[];bank=[]
 for f in q[':question/answer-fields']:
  fields.append({'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'].split('/')[-1]})
  if f[':answer-field/type'][':db/ident'].endswith('/radio'):
   for choice in f[':answer-field/choices']:
    x,y=re.findall(r'=(.*?)(?:\$)',choice[':answer/value']);x,y=rational(x),rational(y)
    # Explicit proportional observed patterns; no asserted student-intent inference.
    bank.append({'lambda_factor':str(x/a),'mu_factor':str(y/b),'correct':choice[':answer/id']==f[':answer-field/correct'][':answer/id']})
 templates[sid]={'level':q[':question/difficulty'][':db/ident'].split('/')[-1],'names':[target,u,v], 'segments':[first,second],'path_names':[n1,n2],'decimal':decimal,'length_dot':r'\cdot ' in lens[0][1] or r'\cdot ' in sol.split('Similarly:')[0],'force_one':force,'prompt':prob,'solution':solmask,'assets':images,'fields':fields,'bank_decimal':any('.' in c[':answer/value'] for f in q[':question/answer-fields'] for c in f[':answer-field/choices']),'bank':bank,'source_id':q[':question/id'],'original_parameters':{'lambda':str(a),'mu':str(b)}}
 cases.append({'source_id':q[':question/id'],'math_academy_id':sid,'template':sid,'level':templates[sid]['level'],'parameters':{'lambda':str(a),'mu':str(b)},'bank_profile':'observed-'+sid if bank else None})
(D/'templates.json').write_text(json.dumps(templates,indent=2)+'\n');(D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
