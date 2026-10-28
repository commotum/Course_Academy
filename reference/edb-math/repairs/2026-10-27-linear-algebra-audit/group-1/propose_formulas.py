import collections,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import MATH,normalize_source_tex,validate_math_structure
D=json.loads((H/'current.json').read_text());S=json.loads((H/'sources.json').read_text());idx=collections.defaultdict(list)
for s in S:idx[s['identity'],s['attribute']].append(s)
def remove_group_cmd(v,cmd):
 while m:=re.search(r'\\'+cmd+r'\s*\{',v):
  i=m.end();depth=1
  while depth and i<len(v):
   if v[i]=='\\'and i+1<len(v)and v[i+1]in'{}':i+=2;continue
   depth+=(v[i]=='{')-(v[i]=='}');i+=1
  if depth:break
  v=v[:m.start()]+v[i:]
 return v
def canonical(v):
 v=normalize_source_tex(v);v=remove_group_cmd(v,'phantom');v=re.sub(r'\\hspace\{[^{}]*\}','',v);v=re.sub(r'\\color\{[^{}]+\}','',v);v=re.sub(r'\\(?:left|right|displaystyle|textstyle)|\\[,;!]','',v)
 v=re.sub(r'\[\s*\{?\s*\\begin\{array\}\{[clr|]+\}',lambda m:r'\begin{bmatrix}',v);v=re.sub(r'\\end\{array\}\s*\}?\s*\]',lambda m:r'\end{bmatrix}',v)
 v=re.sub(r'\\(?:mathbf|mathbb|mathrm|mathcal|mathit|textrm|text)\b','',v);v=v.replace(r'\{','{').replace(r'\}','}');v=re.sub(r'\\(?:Bigg|bigg|Big|big)\b','',v);v=v.rstrip('., ');v=v.replace('⁡','').replace('∼',r'\sim').replace('⟹',r'\Longrightarrow').replace('⟨',r'\langle').replace('⟩',r'\rangle').replace('∞',r'\infty').replace('∈',r'\in').replace('−','-').replace('×',r'\times').replace(r'\dfrac',r'\frac');return re.sub(r'\s+|[{}]','',v)
def nums(v):return re.findall(r'\d+(?:\.\d+)?',remove_group_cmd(re.sub(r'\\hspace\{[^{}]*\}','',v),'phantom'))
def role(v):return {'color':len(re.findall(r'\\color\{',v)),'vector_font':len(re.findall(r'\\(?:mathbf|mathbb)\b',v)),'set_delimiters':len(re.findall(r'\\[{}]',v)),'partition':len(re.findall(r'\\begin\{array\}\{[^{}]*\|[^{}]*\}',v))}
props=[];reject=[]
for r in json.loads((H/'comparison.json').read_text()):
 obj=next(o for o in(D['contents']if r['identity'].startswith('tutorial:')else D['questions'])if o[':db/id']==r['entity']);a=r['attribute'];before=obj[':'+a];matches=list(MATH.finditer(before));opts=[]
 for s in idx[r['identity'],a]:
  if len(matches)!=len(s['formulas']):continue
  changes=[]
  for i,(old,new)in enumerate(zip(r['current'],s['formulas'])):
   if old.rstrip() and old.rstrip()[-1]not in'.,'and new.rstrip().endswith(('.',',')):new=new.rstrip().rstrip('.,')
   ro,rn=role(old),role(new)
   if not any(rn[k]>ro[k]for k in ro):continue
   if canonical(old)==canonical(new)and nums(old)==nums(new):changes.append({'index':i,'before_tex':old,'after_tex':new,'roles_before':ro,'roles_after':rn})
   else:reject.append({'entity':r['entity'],'identity':r['identity'],'attribute':a,'index':i,'before_tex':old,'source_tex':new,'reason':'Not automatically proven equivalent by mathematical token sequence; requires individual review.'})
  if changes:opts.append((s,changes))
 if not opts:continue
 # Prefer the source variant with most uniquely checked retained annotations.
 s,changes=max(opts,key=lambda p:len(p[1]));after=before
 for c in reversed(changes):
  m=matches[c['index']];k=2 if m[0].startswith(('$$',r'\[',r'\('))else 1;wrapped='$$\n'+c['after_tex']+'\n$$'if k==2 else'$'+c['after_tex']+'$';after=after[:m.start()]+wrapped+after[m.end():]
 validate_math_structure(after);props.append({'entity':r['entity'],'attribute':a,'before':before,'after':after,'reason':'Restore source teaching annotations lost from complete formulas: selected rows/columns, coefficients, vector notation, visible set braces, and/or augmented-matrix partitions.','evidence':{'basis_t':9047,'identity':r['identity'],'source_path':s['path'],'formula_changes':changes,'independent_check':'Ordered mathematical tokens and numeric values unchanged after explicitly removing style/layout commands and mapping equivalent matrix wrappers.'},'confidence':'high'})
(H/'source-formula-proposals.json').write_text(json.dumps(props,indent=2));(H/'source-formula-review.json').write_text(json.dumps(reject,indent=2));print('proposals',len(props),'formulas',sum(len(p['evidence']['formula_changes'])for p in props),'unmatched candidates',len(reject))
