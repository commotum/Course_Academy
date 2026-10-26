import collections,hashlib,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import dumps,kw
from question_capture.math_format import MATH,normalize_limit_operators,validate_tex
qs=json.loads((H/'questions.json').read_text());fields=[];blockchanges=[]
for q in qs:
 for a in ['question/problem','question/worked-solution']:
  if ':'+a not in q:continue
  before=q[':'+a]
  def replace(m):
   old=m[0];display=old.startswith(('$$',r'\['));edge=2 if old.startswith(('$$',r'\[',r'\('))else 1;body=old[edge:-edge];newbody=normalize_limit_operators(body);haslimit=(chr(92)+'lim')in newbody;promote=a=='question/problem'and haslimit and not display
   if newbody==body and not promote:return old
   new=('\n\n$$\n'+newbody.strip()+'\n$$\n\n')if promote else old[:edge]+newbody+old[-edge:];blockchanges.append({'entity':q[':db/id'],'attribute':a,'before':old,'after':new,'promoted_display':promote});return new
  after=MATH.sub(replace,before)
  if before==after:continue
  assert re.findall(r'\{\{[^{}]+\}\}',before)==re.findall(r'\{\{[^{}]+\}\}',after)
  for m in MATH.finditer(after):
   edge=2 if m[0].startswith(('$$',r'\[',r'\('))else 1;validate_tex(m[0][edge:-edge])
  fields.append({'entity':q[':db/id'],'attribute':a,'before':before,'after':after,'before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':hashlib.sha256(after.encode()).hexdigest()});q[':'+a]=after
(H/'fields.json').write_text(json.dumps(fields,indent=2)+'\n');(H/'block-changes.json').write_text(json.dumps(blockchanges,indent=2)+'\n');(H/'repaired-questions.json').write_text(json.dumps(qs,indent=2)+'\n');(H/'transaction.edn').write_text(dumps([[kw('db/cas'),f['entity'],kw(f['attribute']),f['before'],f['after']]for f in fields])+'\n');report={'fields':len(fields),'entities':len({f['entity']for f in fields}),'formula_blocks':len(blockchanges),'promoted_display_blocks':sum(c['promoted_display']for c in blockchanges),'attributes':dict(collections.Counter(f['attribute']for f in fields))};(H/'preparation.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
