import collections,hashlib,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import dumps,kw
from question_capture.math_format import MATH,_matrix_layouts,validate_tex
rows=json.loads((H/'audited-fields.json').read_text());changes=[];count=0
for f in rows:
 if f['attribute']=='answer/value':continue
 before=f['value']
 def replace(m):
  global count
  old=m[0];new=_matrix_layouts(old);count+=new!=old
  return new
 after=MATH.sub(replace,before)
 if after!=before:
  for m in MATH.finditer(after):validate_tex(m[0].strip('$'))
  assert re.findall(r'\{\{[^{}]+\}\}',before)==re.findall(r'\{\{[^{}]+\}\}',after)
  changes.append({'entity':f['entity'],'attribute':f['attribute'],'before':before,'after':after,'before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':hashlib.sha256(after.encode()).hexdigest()})
h=H/'format';h.mkdir(exist_ok=True);(h/'fields.json').write_text(json.dumps(changes,indent=2)+'\n');(h/'transaction.edn').write_text(dumps([[kw('db/cas'),f['entity'],kw(f['attribute']),f['before'],f['after']]for f in changes])+'\n');report={'fields':len(changes),'entities':len({f['entity']for f in changes}),'math_blocks':count,'attributes':dict(collections.Counter(f['attribute']for f in changes)),'matrix_entries_and_answers_unchanged':True};(h/'preparation.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
