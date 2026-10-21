"""Independent source-byte and identity checks for proposed object moves; read only."""
import collections,hashlib,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent;RUN=HERE.parent
qs={q[':db/id']:q for q in json.loads((RUN/'questions.json').read_text())};cases=json.loads((HERE/'cases.json').read_text());pending=json.loads((HERE/'pending.json').read_text());descriptive=json.loads((HERE/'already-descriptive-ids.json').read_text())
assert len(cases)+len(pending)+len(descriptive)==len(qs)
assert {c['question_eid']for c in cases}.isdisjoint({c['id']for c in pending})
expected={qid for qid,q in qs.items()if all(re.fullmatch('[A-Z]+',f[':answer-field/key'].strip())for f in q[':question/answer-fields'])}
assert {c['question_eid']for c in cases}|{c['id']for c in pending}==expected
results=[]
for c in cases:
 q=qs[c['question_eid']];assert c['problem_before']==q[':question/problem']and c['solution_before']==q.get(':question/worked-solution','')
 fs={f[':db/id']:f for f in q[':question/answer-fields']};assert set(fs)=={o['field_id']for o in c['objects']}
 for o in c['objects']:
  assert fs[o['field_id']][':answer-field/key']==o['source_label']
  lo,hi=o['source_span'];assert c['problem_before'][lo:hi]==o['source_fragment']or c['extraction']=='named_matrix_assignments'
  content=o.get('source_content',o['content'])
  if o.get('layout_repair'):
   fix=o['layout_repair'];assert content==fix['after']
   tokens=lambda v:re.sub(r'\s+|\$|\\,','',v)
   assert tokens(fix['before'])==tokens(fix['after'])
   content=fix['before']
  repaired=o.get('format_repair',{}).get('after')
  if c['extraction']in ('explicit_label_list','historical_order_bullet_list'):
   fragment=o['source_fragment'];fragment=re.sub(r'^\s*(?:[-*+]\s+)?(?:\*\*)?'+re.escape(o['source_label'])+r'[.)](?:\*\*)?\s+','',fragment)if c['extraction']=='explicit_label_list'else re.sub(r'^\s*[-*+]\s+','',fragment)
   if repaired:
    assert fragment==o['format_repair']['before'];fragment=repaired
   assert content.strip()==fragment.strip()
  else:
   fragment=o['source_fragment'];expression=content[1:-1]
   assert expression in fragment or re.sub(r'\s+','',expression)in re.sub(r'\s+','',fragment)
 # Outside the source option spans, only whitespace folding, an empty layout
 # wrapper, and selection-pointer wording may change. No givens are removed.
 prompt=c['problem_before'];spans=set(tuple(o['source_span'])for o in c['objects'])
 for lo,hi in sorted(spans,reverse=True):prompt=prompt[:lo]+prompt[hi:]
 prompt=re.sub(r'<div class="matrix-operands matrix-operands-stacked">\s*</div>','',prompt)
 normalize=lambda s:re.sub(r'\s+',' ',s).strip()
 assert normalize(prompt)==normalize(c['problem_after']),(c['question_eid'],'shared setup differs')
 # Labels, fields, owned answer banks and all correctness/response references
 # are not part of the edit plan. Counts are documented for downstream checks.
 results.append({'question_eid':c['question_eid'],'fields':len(fs),'source_fragment_checks':True,'shared_setup_preserved':True,'field_identity_mapping_verified':True})
report={'passed':True,'snapshot_sha256':hashlib.sha256((RUN/'questions.json').read_bytes()).hexdigest(),'cases_sha256':hashlib.sha256((HERE/'cases.json').read_bytes()).hexdigest(),'questions':len(cases),'fields':sum(x['fields']for x in results),'pending':len(pending),'descriptive_elsewhere':len(descriptive),'checks':results}
(HERE/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='checks'},indent=2))
