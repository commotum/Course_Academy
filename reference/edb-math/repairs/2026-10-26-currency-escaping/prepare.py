import collections,hashlib,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/currency-escaping-2026-10-26';sys.path[:0]=[str(H),str(R/'scripts')]
# Import only helper constants, not the scan's main body.
from question_capture.math_format import validate_prose
from migrate_learner_history import dumps,kw
TOKEN=re.compile(r'(?<!\\)\\\[[\s\S]*?\\\]|(?<!\\)\\\([\s\S]*?\\\)|(?P<bad>(?<!\\)\$\$(?:\\,\s*)*\d[^$\n]*?(?<!\\)\$(?!\$))|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\[\s\S]|[^$\\])*?(?<!\\)\$')
parents={int(k):v for k,v in json.loads((W/'parents.json').read_text()).items()};rows=json.loads((H/'candidates.json').read_text());variants=json.loads((H/'currency-variants-review.json').read_text());out=[];review=[]
for d in rows+variants:
 before=d['v'];kind='nested-currency-delimiter';spans=[]
 if d in rows:
  for m in TOKEN.finditer(before):
   if m['bad']is not None:spans.append((m.start()+1,m.start()+1,'\\'))
 elif re.fullmatch(r'\$-\s*\$\d+(?:\.\d+)?\$',before):
  i=before.index('$',1);spans=[(i,i,'\\')];kind='negative-currency-delimiter'
 elif re.fullmatch(r'\$\$\(-?[\d, \\]+\)\$',before):spans=[(1,1,'\\')];kind='parenthesized-currency-delimiter'
 elif '$V(4) = $'in before:
  i=before.index('$V(4) = $')+len('$V(4) = ');spans=[(i,i,'\\')];kind='currency-in-equation'
 else:raise ValueError(d)
 assert spans and d['a']=='answer/value';after=before
 for s,z,v in reversed(spans):assert before[s]=='$';after=after[:s]+v+after[z:]
 assert after.replace(r'\$','$')==before.replace(r'\$','$');assert re.findall(r'[-+]?\d+(?:\.\d+)?',before)==re.findall(r'[-+]?\d+(?:\.\d+)?',after);validate_prose(after)
 fs=[f for f,a in parents.get(d['e'],[])if a=='answer-field/choices'];out.append({'entity':d['e'],'attribute':d['a'],'before':before,'after':after,'before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':hashlib.sha256(after.encode()).hexdigest(),'answer_fields':fs});review.append({**d,'repair_kind':kind,'inserted_escape_positions':[s for s,z,v in spans],'after':after})
assert len({f['entity']for f in out})==len(out)
(H/'fields.json').write_text(json.dumps(out,indent=2)+'\n');(H/'reviewed-repairs.json').write_text(json.dumps(review,indent=2)+'\n');(H/'transaction.edn').write_text(dumps([[kw('db/cas'),f['entity'],kw(f['attribute']),f['before'],f['after']]for f in out])+'\n');topics={c['topic/math-academy-id']for d in review for c in d['context']if'topic/math-academy-id'in c};qids=sorted({c['entity']for d in review for c in d['context']if'question/id'in c});(H/'question-ids.json').write_text(json.dumps(qids)+'\n');report={'fields':len(out),'escape_insertions':sum(len(r['inserted_escape_positions'])for r in review),'repair_kinds':dict(collections.Counter(r['repair_kind']for r in review)),'question_entities':len(qids),'topics':len(topics),'detached_answer_entities':sum(not f['answer_fields']for f in out),'basis_t':8170,'changes_only_insert_literal_dollar_escapes':True,'numeric_values_signs_units_types_and_ids_preserved':True};(H/'preparation.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
excluded=[d for d in json.loads((H/'other-delimiter-candidates.json').read_text())if d['e']not in{r['e']for r in variants}];(H/'excluded-other-defects.json').write_text(json.dumps(excluded,indent=2)+'\n');print('Excluded unrelated/bare literal delimiter records',len(excluded))
