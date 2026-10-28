import json,re,sys,collections
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import MATH,validate_math_structure
D=json.loads((H/'current.json').read_text());by={x[':db/id']:x for x in D['questions']+D['contents']};pending=json.loads((H/'source-formula-review.json').read_text());props=json.loads((H/'source-formula-proposals.json').read_text());pby={(p['entity'],p['attribute']):p for p in props};review=[];new=[]
operators={'q-1408','q-19783','q-20051','q-41899'}
for row in pending:
 e,a=row['entity'],row['attribute'];ident=row['identity'];old=row['before_tex'];source=row['source_tex'];newtex=None;proof=''
 if ident=='tutorial:5782':proof='Both Bbb and mathbb preserve the same blackboard-bold R; no repair.'
 elif ident in operators:newtex=source;proof='Original source explicitly uses a cross product. Independently evaluated cross/curl gives the existing owned answer; see authored-completion-proofs.json.'
 elif ident=='q-162407' or (r'\phantom{'in source and r'\boxed{}'in old):
  newtex=source;proof='Static source box retains hidden glyph width. No inline input/select/free-response control in this source formula; existing radio response frame retained.'
 elif ident in {'q-126427','q-41883'}:
  newtex=source.rstrip('?');proof='Restore source vector font/upright operator. Source question-mark punctuation remains outside the existing math span.'
 elif ident=='tutorial:5141':
  newtex=re.sub(r'(?<![A-Za-z])([ijk])(?![A-Za-z])',lambda m:r'\mathbf{'+m[1]+'}',old);proof='Preserve current valid vmatrix determinant, restore only bold i,j,k basis vectors; entries and row/column order unchanged.'
 elif ident=='q-162410':newtex=source;proof='Source thousands separator 2 hspace 000 is the same number 2000 as existing 2 thinspace 000; all values and integration factors unchanged.'
 else:proof='Unresolved; no automatic rewrite.'
 review.append({**row,'resolution':proof,'after_tex':newtex})
 if newtex is None:continue
 # deduplicate source variants for same position
 k=(e,a);p=pby.get(k);before=by[e][':'+a]
 if p is None:
  p={'entity':e,'attribute':a,'before':before,'after':before,'reason':'Individually reviewed source notation/geometry restoration.','evidence':{'basis_t':9837,'identity':ident,'formula_changes':[]},'confidence':'high'};pby[k]=p;new.append(p)
 if any(c['index']==row['index']for c in p['evidence']['formula_changes']):continue
 p['evidence']['formula_changes'].append({'index':row['index'],'before_tex':old,'after_tex':newtex,'independent_check':proof})
# Rebuild every combined value from immutable before spans.
for p in list(props)+new:
 spans=list(MATH.finditer(p['before']));after=p['before']
 for c in sorted(p['evidence']['formula_changes'],key=lambda c:c['index'],reverse=True):
  m=spans[c['index']];display=m[0].startswith(('$$',r'\[',r'\('));tex=c['after_tex'];wrapped='$$\n'+tex+'\n$$'if display else'$'+tex+'$';after=after[:m.start()]+wrapped+after[m.end():]
 validate_math_structure(after);p['after']=after
(H/'source-reviewed-proposals.json').write_text(json.dumps(props+new,indent=2)+'\n');(H/'source-review-resolutions.json').write_text(json.dumps(review,indent=2)+'\n')
print('fields',len(props+new),'formula changes',sum(len(p['evidence']['formula_changes'])for p in props+new),'review rows',len(review))
