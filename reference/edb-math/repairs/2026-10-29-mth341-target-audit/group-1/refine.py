import json,re,sys,collections
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import MATH,normalize_source_tex,validate_math_structure
D=json.loads((H/'current.json').read_text());P=json.loads((H/'proposals.json').read_text());F=json.loads((H/'fields.json').read_text());sources=json.loads((H/'sources.json').read_text());src=collections.defaultdict(list)
for s in sources:src[s['identity'],s['attribute']].append(s)
ns={"re":re};s=(H/'propose_format.py').read_text();exec(s[s.index('def neutral(s):'):s.index('props=[];proof=[]')],ns);neutral=ns['neutral'];source_tex=ns['source_tex']
def put(e,a,before,after,reason,evidence):
 if before==after:return
 p=next((p for p in P if p['entity']==e and p['attribute']==a),None)
 if p:p['after']=after;p['reason']+=','+reason;p.setdefault('additional_evidence',[]).append(evidence)
 else:P.append({'entity':e,'attribute':a,'before':before,'after':after,'reason':reason,'evidence':evidence})
def get(e,a,v):return next((p['after']for p in P if p['entity']==e and p['attribute']==a),v)
def same(a,b):
 # Equivalent environment layouts; explicit math fonts and visible set fences are presentation.
 def n(s):
  s=neutral(s);s=s.replace('beginarrayll','beginaligned').replace('endarray','endaligned');s=s.replace('beginaligned','').replace('endaligned','');return s.strip('.,?')
 return n(a)==n(b)
# Restore equivalent formula notation from the retained source, choosing archive evidence over duplicate captures.
for e,a,original,ident,bare in F:
 if bare or a not in ['tutorial/content','question/problem','question/worked-solution']:continue
 current=get(e,a,original);matches=list(MATH.finditer(current));oldmatches=list(MATH.finditer(original));edits=[]
 if len(matches)!=len(oldmatches):continue
 for i,m in enumerate(matches):
  old=m[0][2:-2]if m[0].startswith('$$')else m[0][1:-1];options=[]
  for ss in src[ident,a]:
   if len(ss['formulas'])!=len(matches)or not isinstance(ss['formulas'][i],str):continue
   new=ss['formulas'][i]
   if same(old,new)and any(x in new and x not in old for x in [r'\mathbf',r'\mathcal',r'\mathbb',r'\{',r'\color']):options.append((new,ss['path']))
  if options:
   new,path=sorted(options,key=lambda x:('/DATA/Lessons/'not in x[1],x[1]))[0];new=source_tex(old,new)
   if new!=old:edits.append((m,new,path))
 after=current
 for m,new,path in reversed(edits):after=after[:m.start()]+('$$\n'+new+'\n$$'if m[0].startswith('$$')else'$'+new+'$')+after[m.end():]
 put(e,a,original,after,'source-equivalent-notation',{'identity':ident,'formula_edits':[{'before':m[0],'after':new,'source_path':path}for m,new,path in edits]})
# Canonical visible set fences: escape only the outer set-group, never coefficient or environment groups.
def set_fences(t):
 t=t.replace(r'\text{{}',r'\left\{').replace(r'\text{}}',r'\right\}')
 starts=[]
 for m in re.finditer(r'(?<!\\)\{(?=\\begin\{bmatrix\}|0\}|\{[a-z]\}_|[a-z]_\{)',t):
  # A candidate must be the full RHS/value or a clear vector-list set, not a scalar coefficient group.
  prefix=t[:m.start()].rstrip();rest=t[m.start():]
  if prefix and not prefix.endswith(('=','+')) and not rest.startswith('{{'):continue
  i=m.start()+1;depth=1
  while i<len(t)and depth:
   if t[i]=='\\':i+=2;continue
   depth+=(t[i]=='{')-(t[i]=='}');i+=1
  if depth:continue
  body=t[m.start()+1:i-1]
  if (body=='0'and(not prefix or prefix.endswith('=')))or'\\begin{bmatrix}'in body or(re.search(r'[a-z]\}_\{\d+\}',body)and(','in body or prefix.endswith('='))):starts.append((m.start(),i-1))
 for start,end in reversed(starts):t=t[:end]+r'\right\}'+t[end+1:];t=t[:start]+r'\left\{'+t[start+1:]
 return t
answer_proofs=[]
for e,a,original,ident,bare in F:
 current=get(e,a,original)
 if bare:
  after=set_fences(current)
  if after!=current:
   # Delimiter-only edits: all bytes apart from escaped/scalable set fences are identical.
   strip=lambda v:v.replace(r'\left\{','{').replace(r'\right\}','}').replace(r'\text{{}','{').replace(r'\text{}}','}')
   assert strip(after)==strip(current),(e,current,after)
   proof={'identity':ident,'source_paths':sorted({s['path']for s in src[ident,'answer/value']}),'mathematical_entries_and_order_unchanged':True,'proof':'Only outer set grouping braces become visible scalable set fences. No coefficient, matrix entry, free-variable condition, answer identity or key changes.'}
   put(e,a,original,after,'display-only-visible-set-delimiters',proof);answer_proofs.append({'entity':e,'before':original,'after':after,**proof})
 elif a in ['tutorial/content','question/problem','question/worked-solution']:
  after=current
  for m in reversed(list(MATH.finditer(current))):
   v=m[0][2:-2]if m[0].startswith('$$')else m[0][1:-1];v2=set_fences(v)
   if v!=v2:after=after[:m.start()]+('$$\n'+v2+'\n$$'if m[0].startswith('$$')else'$'+v2+'$')+after[m.end():]
  after=after.replace(r'\begin{aligned}[A',r'\begin{aligned}{}[A')
  if e==17592186153353:after=after.replace(r'\color{rblack}',r'\color{black}')
  put(e,a,original,after,'visible-set-fences-and-renderer-guards',{'identity':ident,'source_paths':sorted({s['path']for s in src[ident,a]}),'review':'Restore visible mathematical set delimiters; retain first aligned augmented-matrix label; rblack is an invalid CSS source typo corrected to black.'})
# Individually derived source mathematical corrections.
for q in D['questions']:
 sid=q.get(':question/math-academy-id');e=q[':db/id'];a='question/worked-solution';original=q.get(':'+a)
 if sid=='q-35558':
  current=get(e,a,original);after=current.replace('the zero polynomial has degree $0$, which is less than $5.$','the zero polynomial is not a polynomial of degree $5$ or greater. Its degree is undefined (or is assigned $-\\infty$ by convention).')
  assert current!=after;put(e,a,original,after,'authored-mathematical-correction-zero-polynomial-degree',{'identity':sid,'proof':'The zero polynomial has no finite degree. The conclusion 0∉W is correct, but degree 0 incorrectly classifies the zero polynomial as a nonzero constant.'})
 if sid=='q-83749':
  current=get(e,a,original);old=r'\begin{bmatrix}3 \\ 2 \\ 3 \\ 4\end{bmatrix}';new=r'\begin{bmatrix}2 \\ 1 \\ 2 \\ 3\end{bmatrix}'
  assert current.count(old)==1;after=current.replace(old,new);put(e,a,original,after,'authored-mathematical-correction-basis-vector',{'identity':sid,'proof':'Final basis must retain the given third vector (2,1,2,3), not (3,2,3,4). The added vector (−1,−5,−1,3) has zero dot product with all three actual givens; those four vectors are nonzero and orthogonal, hence a basis.'})
(H/'proposals.json').write_text(json.dumps(P,indent=2)+'\n');(H/'answer-display-proposals.json').write_text(json.dumps([p for p in P if p['attribute']=='answer/value'],indent=2)+'\n');(H/'answer-display-proofs.json').write_text(json.dumps(answer_proofs,indent=2)+'\n');print('Total',len(P),'answer display repairs',len(answer_proofs))
