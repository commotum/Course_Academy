import collections,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import MATH,normalize_source_tex,validate_math_structure
ns={'__file__':str(H/'propose_format.py')};exec((H/'propose_format.py').read_text().split('P=[]')[0],ns);base=ns['neutral'];F={(f[0],f[1]):f for f in json.loads((H/'fields.json').read_text())};C=json.loads((H/'semantic-candidates.json').read_text());out=[];res=[]
def neutral(v):
 v=v.replace('″',"''").replace('⇒',r'\Rightarrow').replace('⟹',r'\Longrightarrow').replace('≈',r'\approx').replace('θ',r'\theta').replace(r'\mid','|')
 v=re.sub(r'\\bbox\[[^\]]*\]','',v)
 v=v.replace('&','').replace(r'\begin{cases}',r'\{\begin{aligned}').replace(r'\end{cases}',r'\end{aligned}')
 v=v.replace(r'\mathrm{△}','△')
 return base(v)
for c in C:
 e,a=c['entity'],c['attribute'];before=F[e,a][2];matches=list(MATH.finditer(before));after=before;details=[];decisions=[]
 for d in reversed(c['differences']):
  old,new=d['current'],d['source'];flags=[];replacement=None
  if neutral(old)==neutral(new):
   if new.count(r'\mathbf')>old.count(r'\mathbf'):flags.append('source-vector-font')
   if new.count(r'\mathcal')>old.count(r'\mathcal'):flags.append('source-area-notation')
   if r'\bbox['in new and r'\bbox['not in old:flags.append('source-highlight')
   if r'\begin{cases}'in new and re.search(r'\\\{\s*\\begin\{aligned\}',old):flags.append('source-cases-brace')
   if flags:replacement=normalize_source_tex(new)
  # The radio source shows a box of a deliberate visible width, not an extra field.
  if r'\boxed{}'in old and re.search(r'\\enclose\{box\}\{\\phantom\{A+\}\}',new):
   width=re.search(r'\\phantom\{(A+)\}',new)[1];replacement=old.replace(r'\boxed{}',r'\boxed{\phantom{'+width+'}}')
   # Source's domain-set brace was also lost in these same equations.
   replacement=re.sub(r'D=\{(\([^$]*?)(\})\s*$',lambda m:r'D=\{'+m[1]+r'\}',replacement.strip())if'D={'in replacement else replacement
   flags=['source-visible-placeholder-width']
  # Source-proved vector/segment adornments, whose broken old exponent still
  # passes TeX syntax checks. Preserve both endpoint labels and direction.
  arrows=list(re.finditer(r'([A-Z]{2})\^\(([→―])\)',old))
  if arrows:
   replacement=old
   for ar in reversed(arrows):
    expected=r'\overset{'+(r'\to'if ar[2]=='→'else'―')+r'}{'+ar[1]+'}'
    if ar[1]in new and any(x in new for x in (r'\overset',r'\overrightarrow')):replacement=replacement[:ar.start()]+expected+replacement[ar.end():]
   if replacement!=old:flags=['source-vector-or-segment-adornment']
   else:replacement=None
  if replacement is not None and replacement!=old:
   m=matches[d['i']];n=2 if m[0].startswith('$$')else 1;after=after[:m.start()]+m[0][:n]+replacement+m[0][-n:]+after[m.end():];details.append({'math_index':d['i'],'source_path':c['path'],'before_math':old,'after_math':replacement,'features':flags});decisions.append({'index':d['i'],'decision':'repair','features':flags})
  else:decisions.append({'index':d['i'],'decision':'retain','reason':'Valid alternate grouping/alignment/operator spelling, source position or raw inherited source; no independently proved remaining semantic change from this pair.'})
 if after!=before:
  try:validate_math_structure(after)
  except Exception as ex:raise ValueError((c,str(ex)))
  out.append({'entity':e,'attribute':a,'before':before,'after':after,'reason':'Restore individually observed source notation/visual response geometry','evidence':details,'confidence':'high'})
 res.append({'entity':e,'attribute':a,'identity':c['identity'],'source_path':c['path'],'decisions':decisions})
(H/'source-extra-proposals.json').write_text(json.dumps(out,indent=2)+'\n');(H/'semantic-candidate-resolutions.json').write_text(json.dumps(res,indent=2)+'\n');print('extra proposals',len(out),collections.Counter(x['attribute']for x in out))
