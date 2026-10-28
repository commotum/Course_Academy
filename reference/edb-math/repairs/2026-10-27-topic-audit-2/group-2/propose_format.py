import json,re,sys,collections
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import MATH,normalize_prose,normalize_tex,validate_math_structure,validate_tex
F=json.loads((H/'fields.json').read_text());SOURCE=json.loads((H/'sources.json').read_text());index=collections.defaultdict(list)
for s in SOURCE:index[s['identity'],s['attribute']].append(s)
def neutral(v):
 v=re.sub(r'\\color\{[^{}]*\}|\\hspace\{[^{}]*\}','',v);v=re.sub(r'\\(?:mathbf|mathit|mathrm|textrm|text|operatorname|mathcal|mathbb)\s*(?=\{)','',v);v=re.sub(r'\\(?:left|right|displaystyle|textstyle|quad|qquad)\b|\\[,;!]','',v)
 v=v.replace(r'\{','').replace(r'\}','').replace('⁡','').replace('⁢','').replace('−','-').replace('′',"'").replace(r'\prime',"'")
 v=v.replace('π',r'\pi').replace('λ',r'\lambda').replace('∈',r'\in').replace('∉',r'\notin').replace('∞',r'\infty').replace('∂',r'\partial')
 v=re.sub(r'\\(sin|cos|tan|cot|sec|csc|ln|log|exp)\b',r'\1',v);v=v.replace(r'\dfrac',r'\frac').replace(r'\times',r'\cdot');return re.sub(r'\s|[{}]','',v).rstrip('.,?')
def punctuation(old,new):return new.strip().rstrip('.,?')+(old.strip()[-1]if old.strip().endswith(('.',',','?'))else'')
P=[]
for e,a,before,ident,bare in F:
 after=before;edits=[];matches=list(MATH.finditer(before))if not bare else[];ms=[before]if bare else[m[0][2:-2]if m[0].startswith('$$')else m[0][1:-1]for m in matches]
 for i,old in enumerate(ms):
  opts=[]
  for s in index[ident,'question/problem'if a=='answer-field/key'else a]:
   fs=s['formulas'];choices=fs if a in ['answer/value','answer-field/key']else[fs[i]]if len(fs)==len(ms)else[]
   for new in choices:
    if not isinstance(new,str)or neutral(old)!=neutral(new):continue
    flags=[]
    for command,label in [(r'\color','teaching-highlights'),(r'\mathbf','vector-notation'),(r'\mathcal','function-or-basis-notation'),(r'\mathbb','number-domain-notation')]:
     if new.count(command)>old.count(command):flags.append(label)
    if r'\{'in new and r'\{'not in old:flags.append('visible-set-braces')
    if flags and r'\bbox'not in old:opts.append((punctuation(old,new),flags,s['path']))
  unique={o[0]:o for o in opts}
  if len(unique)==1:edits.append((i,*next(iter(unique.values()))))
 for i,new,flags,path in sorted(edits,reverse=True):
  if bare:after=new
  else:
   m=matches[i];after=after[:m.start()]+('$$\n'+new+'\n$$'if m[0].startswith('$$')else'$'+new+'$')+after[m.end():]
 evidence=[{'math_index':i,'source_path':path,'features':flags,'before_math':ms[i],'after_math':new}for i,new,flags,path in edits];reasons=sorted({flag for i,new,flags,path in edits for flag in flags})
 # A literal brace plus equation rows is an actual system; make that brace scale and preserve equation alignment.
 if re.search(r'\\\{\s*\\begin\{aligned\}',after)and not re.search(r'\\left\\\{\s*\\begin\{aligned\}',after):
  normalized=normalize_tex(after)if bare else normalize_prose(after)
  if normalized!=after:evidence.append({'feature':'source equation-system brace','source_identity':ident});after=normalized;reasons.append('scalable-system-brace')
 # Requested standalone integration calculations use display math; references in prose remain inline.
 if a=='question/problem':
  for m in list(MATH.finditer(after))[::-1]:
   if not m[0].startswith('$$')and r'\int'in m[0]and re.search(r'\b(?:Calculate|Evaluate|Compute)\b',after[:m.start()],re.I):
    old=m[0];after=after[:m.start()].rstrip()+'\n\n$$\n'+old[1:-1].strip()+'\n$$'+after[m.end():];evidence.append({'feature':'requested integral calculation display','math':old});reasons.append('standalone-integral-display')
 if after!=before:
  (validate_tex if bare else validate_math_structure)(after);assert re.findall(r'\{\{[^{}]+\}\}',before)==re.findall(r'\{\{[^{}]+\}\}',after);P.append({'entity':e,'attribute':a,'before':before,'after':after,'reason':','.join(reasons),'evidence':evidence,'confidence':'high'})
(H/'proposals.json').write_text(json.dumps(P,indent=2)+'\n');print('proposals',len(P),collections.Counter(p['attribute']for p in P))
