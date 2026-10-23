"""Check formatting-only invariants and policy idempotency without opening EDB."""
import collections,json,re
from pathlib import Path
from prepare import transform,MARKER,audit
HERE=Path(__file__).resolve().parent

def main():
 fields=json.loads((HERE/'fields.json').read_text());failures=[]
 for f in fields:
  after,edits,_=transform({'e':f['entity'],'a':f['attribute'],'v':f['after']},{})
  if after!=f['after'] or edits:failures.append([f['entity'],f['attribute']])
  assert MARKER.findall(f['before'])==MARKER.findall(f['after'])
 retained=json.loads((HERE/'retained-inline.json').read_text());damaged=[{'entity':f['entity'],'attribute':f['attribute'],'occurrences':[o for o in f['occurrences'] if o['reason']=='preexisting-unbalanced-source-math']} for f in retained if any(o['reason']=='preexisting-unbalanced-source-math' for o in f['occurrences'])]
 report={'fields':len(fields),'all_repaired_fields_idempotent':not failures,'idempotency_failures':failures,'answer_markers_preserved':True,'deindented_captured_source_equations':sum(e.get('deindented_source_equation',False) for f in fields for e in f['edits']),'preexisting_malformed_occurrences_retained':sum(len(f['occurrences']) for f in damaged),'malformed_integral_occurrences':sum(bool(audit.INTEGRAL.search(o['math'])) for f in damaged for o in f['occurrences'])}
 (HERE/'content-verification.json').write_text(json.dumps(report,indent=2)+'\n');(HERE/'preexisting-source-exceptions.json').write_text(json.dumps(damaged,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report));assert not failures
if __name__=='__main__':main()
