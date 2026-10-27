"""Only explicit fenced alignment/matrix conversions, with exact CAS guards."""
import collections,hashlib,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/matrix-layout-2026-10-26';sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import dumps,kw
from question_capture.math_format import MATH,_matrix_layouts,cells,environment,ENV
meta=json.loads((W/'metadata.json').read_text());parents=json.loads((W/'parents.json').read_text());fields=[];uncovered=[];grid_checks=[]
for d in json.loads((H/'candidates.json').read_text()):
 before=d['v'];after=d['after'];math_answer=d['a']=='answer/value'and meta[str(d['e'])].get('answer/type')==17592186045498
 protected=_matrix_layouts(before)if math_answer else MATH.sub(lambda m:_matrix_layouts(m[0]),before)
 if protected!=after:uncovered.append(d);continue
 assert re.findall(r'\{\{[^{}]+\}\}',before)==re.findall(r'\{\{[^{}]+\}\}',after)
 assert re.findall(r'!\[[^\]]*\]\([^)]*\)|<img\b[^>]*>',before)==re.findall(r'!\[[^\]]*\]\([^)]*\)|<img\b[^>]*>',after)
 assert _matrix_layouts(after)==after
 fs=[p for p,a in parents.get(str(d['e']),[])if a in ('answer-field/choices','answer-field/correct')]
 f={'entity':d['e'],'attribute':d['a'],'before':before,'after':after,'before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':hashlib.sha256(after.encode()).hexdigest(),'math_answer':math_answer,'answer_fields':fs};fields.append(f)
for b in json.loads((H/'blocks.json').read_text()):
 new=b['new'];m=next(ENV.finditer(new));bounds=environment(new,m.start());g=cells(new[bounds[0]:bounds[1]]);old=b['rows']
 # This repair never changes an entry or its position. One old source table
 # contains an empty surplus trailing alignment column, not an extra entry.
 width=min(map(len,old));trimmed=[row[:width]for row in old]
 if len({len(row)for row in old})!=1:
  assert all(not c for row in old for c in row[width:])
 assert g==trimmed,(b,g,trimmed)
 grid_checks.append({'entity':b['e'],'attribute':b['a'],'source_span':b['span'],'rows':len(g),'columns':width,'ordered_cells_unchanged':True,'removed_empty_trailing_alignment_columns':old!=trimmed})
(H/'uncovered.json').write_text(json.dumps(uncovered,indent=2)+'\n');assert not uncovered,('Unprotected math requires review',len(uncovered))
(H/'fields.json').write_text(json.dumps(fields,indent=2)+'\n');(H/'grid-verification.json').write_text(json.dumps(grid_checks,indent=2)+'\n');(H/'transaction.edn').write_text(dumps([[kw('db/cas'),f['entity'],kw(f['attribute']),f['before'],f['after']]for f in fields])+'\n')
summary={'fields':len(fields),'entities':len({f['entity']for f in fields}),'attributes':dict(collections.Counter(f['attribute']for f in fields)),'matrix_layouts':len(grid_checks),'bare_math_answer_values':sum(f['math_answer']for f in fields),'affected_answer_fields':len({e for f in fields for e in f['answer_fields']}),'preserved_all_ordered_cells':True,'images_and_prompt_markers_unchanged':True,'only_protected_math_or_typed_math_answers_changed':True}
(H/'preparation.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
