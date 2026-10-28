import json,re,sys,collections,difflib
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import MATH,validate_math_structure,validate_tex,normalize_matrix_answer_tables
fields=json.loads((H/'fields.json').read_text());sources=json.loads((H/'sources.json').read_text());src=collections.defaultdict(list)
for s in sources:src[s['identity'],s['attribute']].append(s)
def neutral(s):
 s=re.sub(r'\\color\{[^{}]*\}|\\hspace\{[^{}]*\}','',s)
 s=re.sub(r'\\(?:mathbf|mathit|mathrm|textrm|text|operatorname|mathcal|mathbb)\s*(?=\{)','',s)
 s=re.sub(r'\\(?:left|right|displaystyle|textstyle|quad|qquad)\b|\\[,;!]','',s)
 s=s.replace(r'\{','').replace(r'\}','')
 s=re.sub(r'\\begin\{array\}\{[clr]+\}',lambda _:r'\begin{bmatrix}',s);s=s.replace(r'\end{array}',r'\end{bmatrix}')
 s=s.replace('[','').replace(']','')
 s=s.replace(r'\times',r'\cdot').replace(r'\dfrac',r'\frac').replace('⁡','').replace('−','-').replace('⋯',r'\cdots').replace('⋮',r'\vdots').replace('…',r'\ldots').replace('↔',r'\leftrightarrow').replace('⇒',r'\Rightarrow')
 return re.sub(r'\s|[{}]','',s).rstrip('.,?')
def source_tex(bef,after):
 # Retain whether terminal punctuation belongs inside or outside current math.
 old=bef.strip();new=after.strip()
 new=new.rstrip('.,?')+(old[-1]if old.endswith(('.',',','?'))else'')
 return new
props=[];proof=[]
for e,a,v,ident,bare in fields:
 if bare or a not in ['tutorial/content','question/problem','question/worked-solution']:continue
 matches=list(MATH.finditer(v));ms=[m[0][2:-2]if m[0].startswith('$$')else m[0][1:-1]for m in matches];edits=[]
 for i,old in enumerate(ms):
  options=[]
  for s in src[ident,a]:
   fs=s['formulas']
   if len(fs)!=len(ms)or not isinstance(fs[i],str):continue
   new=fs[i]
   if neutral(old)!=neutral(new):continue
   flags=[]
   if re.findall(r'\\color\{(?!black)[^}]+\}',new)and len(re.findall(r'\\color\{(?!black)[^}]+\}',new))>len(re.findall(r'\\color\{(?!black)[^}]+\}',old)):flags.append('source-teaching-highlights')
   if r'\{'in new and r'\{'not in old:flags.append('visible-set-braces')
   if r'\mathbb'in new and r'\mathbb'not in old:flags.append('real-number-domain-font')
   # Restore vector/basis role where import stripped fonts, but do not standardize a deliberate matrix/environment format alone.
   if r'\mathbf'in new and r'\mathbf'not in old:flags.append('source-vector-notation')
   if r'\mathcal'in new and r'\mathcal'not in old:flags.append('source-basis-notation')
   if flags and r'\bbox'not in old:options.append((source_tex(old,new),flags,s['path']))
  unique={o[0]:o for o in options}
  if len(unique)==1:
   new,flags,path=next(iter(unique.values()));edits.append((i,new,flags,path))
 if edits:
  after=v
  for i,new,flags,path in sorted(edits,reverse=True):
   m=matches[i];after=after[:m.start()]+('$$\n'+new+'\n$$'if m[0].startswith('$$')else'$'+new+'$')+after[m.end():]
  validate_math_structure(after);props.append({'entity':e,'attribute':a,'before':v,'after':after,'reason':','.join(sorted({f for i,n,fs,p in edits for f in fs})),'evidence':[{'math_index':i,'source_path':p,'before_math':ms[i],'after_math':n,'features':fs}for i,n,fs,p in edits],'confidence':'high'})
# Two individually checked tutorial derivations lost the augmentation separator and A/I vs I/A-inverse highlighting.
for e,index in [(17592186116501,6),(17592186116496,8)]:
 f=next(f for f in fields if f[0]==e);_,a,v,ident,bare=f;s=next(s for s in src[ident,a]if len(s['formulas'])==len(list(MATH.finditer(v))));new=s['formulas'][index];matches=list(MATH.finditer(v));m=matches[index]
 old=next((p['after']for p in props if p['entity']==e and p['attribute']==a),v);mm=list(MATH.finditer(old))[index];after=old[:mm.start()]+'$$\n'+new+'\n$$'+old[mm.end():]
 existing=next((p for p in props if p['entity']==e and p['attribute']==a),None)
 evidence={'math_index':index,'source_path':s['path'],'before_math':m[0],'after_math':new,'features':['augmentation-rule','coefficient-inverse-highlights']}
 if existing:existing['after']=after;existing['reason']+=',augmentation-rule';existing['evidence'].append(evidence)
 else:props.append({'entity':e,'attribute':a,'before':v,'after':after,'reason':'augmentation-rule-and-coefficient-inverse-highlights','evidence':[evidence],'confidence':'high'})
for issue in json.loads((H/'issues.json').read_text()):
 if issue['issue']!='matrix-answer-table':continue
 e=issue['entity'];f=next(f for f in fields if f[0]==e and f[1]=='question/problem');ident=f[3]
 # Source HTML retained explicitly identifies bracket cells/rowspans, and only blank grids are changed.
 paths=[s['path']for s in src[ident,'question/problem']if'table'in s['html']]
 existing=next((p for p in props if p['entity']==e and p['attribute']=='question/problem'),None)
 before=issue['value'];after=normalize_matrix_answer_tables(existing['after']if existing else before)
 p={'entity':e,'attribute':'question/problem','before':before,'after':after,'reason':'source-matrix-answer-grid','evidence':{'identity':ident,'source_paths':sorted(set(paths)),'field_order_unchanged':re.findall(r'\{\{[^{}]+\}\}',before)==re.findall(r'\{\{[^{}]+\}\}',after)},'confidence':'high'if paths else'medium'}
 if existing:existing['after']=after;existing['reason']+=',source-matrix-answer-grid';existing['evidence'].append(p['evidence'])
 else:props.append(p)
(H/'proposals.json').write_text(json.dumps(props,indent=2)+'\n');print(len(props),collections.Counter(p['reason']for p in props))
