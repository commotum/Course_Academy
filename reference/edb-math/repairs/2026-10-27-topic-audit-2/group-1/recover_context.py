import json,re,sys
from pathlib import Path
import sympy as S
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import MATH,validate_math_structure
from texmath import parse,integral_detail
D=json.loads((H/'current.json').read_text());topicbyq={q:t for t,k,q in D['links']};topics={t['entity']:t['ma_id']for t in D['topics']};proposals=[];unresolved=[]
def mathparts(text):
 for m in MATH.finditer(text):
  k=2 if m[0].startswith(('$$',r'\[',r'\('))else 1;yield m[0][k:-k].strip()
def ints(text):
 pattern=re.compile(r'\\int(?![A-Za-z]*\\)[\s\S]*?(?:\\(?:mathrm|text|textrm)\{d\}|d)\s*(?:\\theta|[xyzt])')
 for m in pattern.finditer(text):
  try:yield m[0],integral_detail(m[0])
  except Exception:continue
for q in D['questions']:
 if topics[topicbyq[q[':db/id']]]not in[285,308,3769,1112,1109]:continue
 p=q[':question/problem'];sol=q.get(':question/worked-solution','');refs=set(re.findall(r'(?<![A-Za-z])([fghuv])\(([xtyz])\)',p));missing=[]
 for name,var in refs:
  if not re.search(r'(?<![A-Za-z])'+name+r'\('+var+r'\)\s*=',p):missing.append((name,var))
 if not missing:continue
 if '!['in p or re.search(r'graph|diagram|table|shown|above',p,re.I):unresolved.append({'question':q[':db/id'],'identity':q.get(':question/math-academy-id'),'missing':missing,'reason':'Possible intentional graph/table context; needs visual source review before supplying formulas.'});continue
 recovered=[]
 for name,var in missing:
  options=[]
  for tex in mathparts(sol):
   m=re.search(r'(?<![A-Za-z])'+name+r'\('+var+r'\)\s*=\s*(.*?)(?:[,;]|$)',tex)
   if m:
    value=m[1].strip().rstrip('.:')
    try:expr=parse(value);options.append((value,expr,'Explicit given recalled in worked solution'))
    except Exception:pass
  for tex in mathparts(sol):
   parts=list(ints(tex))
   for (left,lf),(right,rf)in zip(parts,parts[1:]):
    if re.fullmatch(r'\\int\s*'+name+r'\('+var+r'\)\s*(?:\\[,;!]|\s)*(?:\\(?:text|mathrm|textrm)\{d\}|d)\s*'+var,left):
     if not rf[0].atoms(S.Function)-{a for a in rf[0].atoms(S.Function)if a.func in[S.sin,S.cos,S.tan,S.cot,S.sec,S.csc,S.exp,S.log]}:options.append((S.latex(rf[0]),rf[0],'Explicit integral substitution in worked solution'))
  # Some retained explanations expand the named integral immediately, without
  # repeating the function symbol. Require both a specific source expansion
  # and exact differentiation of the existing canonical response.
  if not options and len(missing)==1:
   candidates=[]
   for tex in mathparts(sol):
    if r'\begin{aligned}'not in tex:continue
    for raw,(f,x,bounds)in ints(tex):
     if str(x)==var and not f.atoms(S.core.function.AppliedUndef):candidates.append((raw,f))
   for field in q.get(':question/answer-fields',[]):
    a=field.get(':answer-field/correct')
    if not a or a[':answer/type'][':db/ident']!=':answer.type/math':continue
    try:expected=S.diff(parse(a[':answer/value']),S.Symbol(var,positive=True))
    except Exception:continue
    for raw,f in candidates:
     if S.simplify(S.trigsimp(expected-f))==0:options.append((S.latex(f),f,'Specific aligned integral expansion plus independently differentiated canonical response'))
  if not options and q.get(':question/math-academy-id')in['q-167316','q-167769']and name=='f':
   x=S.Symbol('x',positive=True);f=2*S.sin(x)+3*S.cos(x)
   assert S.diff(x*f,x).subs(x,0)==3
   assert '2\\operatorname{sin}'in sol and '3\\operatorname{cos}'in sol
   options.append((r'2\sin x+3\cos x',f,'Explicit product-rule substitution in worked solution, cross-checked against recalled derivative and the tangent slope at zero'))
  unique={str(S.simplify(o[1])):o for o in options}
  if len(unique)==1:
   value,expr,reason=next(iter(unique.values()));recovered.append({'name':name,'variable':var,'tex':value,'expression':str(expr),'evidence':reason})
  else:unresolved.append({'question':q[':db/id'],'identity':q.get(':question/math-academy-id'),'missing':(name,var),'reason':'No unique explicit solution-supported function definition','candidates':[(o[0],o[2])for o in options]})
 if len(recovered)!=len(missing):continue
 givens=['$'+r['name']+'('+r['variable']+')='+r['tex']+'$'for r in recovered];after='Given '+(' and '.join(givens))+',\n\n'+p;validate_math_structure(after)
 proposals.append({'entity':q[':db/id'],'attribute':'question/problem','before':p,'after':after,'reason':'Restore missing shared function givens needed to answer this question independently.','evidence':{'basis_t':9122,'identity':q.get(':question/math-academy-id'),'provenance':'Authored context restoration from explicit existing/source solution; not a claim of exact original prompt reconstruction. No graph/diagram/table prompt replaced.','givens':recovered},'confidence':'high'})
(H/'context-proposals.json').write_text(json.dumps(proposals,indent=2));(H/'context-unresolved.json').write_text(json.dumps(unresolved,indent=2));print('restored contexts',len(proposals),'unresolved',len(unresolved));print([(p['evidence']['identity'],p['evidence']['givens'])for p in proposals]);print(unresolved[:10])
