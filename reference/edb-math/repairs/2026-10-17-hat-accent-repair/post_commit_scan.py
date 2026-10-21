"""Exhaustively recheck all string attributes at the exact committed basis."""
import json, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).resolve().parent))
from scripts.generator_publish import Publisher
from capture.scripts.database.edn import loads
from repair import structured_occurrences,FLATTENED
HERE=Path(__file__).resolve().parent
OUT=HERE/'post-commit-census'
OUT.mkdir(exist_ok=True)
receipt=loads((HERE/'receipt.edn').read_text())
assert receipt[':edb/committed'] is True
basis=receipt[':edb/db-after-t']
publisher=Publisher.from_environment(source=':agent/codex')
result=subprocess.run([str(HERE/'native/census'),str(OUT),str(basis)],env=publisher.client.environment,capture_output=True,text=True,check=True)
(OUT/'census.stdout').write_text(result.stdout)
(OUT/'census.stderr').write_text(result.stderr)
stats=[json.loads(path.read_text())for path in OUT.glob('current-*-stats.json')]
assert len(stats)==29 and all(v['completed_to_end']and v['as_of_basis']==basis for v in stats)
remaining=[]
for path in OUT.glob('current-*.edn'):
    for e,a,v,tx,source,added in loads(path.read_text()):
        assert added
        n=len(structured_occurrences(v))+len(FLATTENED.findall(v))
        if n:remaining.append({'entity':e,'attribute_id':a,'value':v,'malformed_hat_occurrences':n})
(OUT/'remaining-defects.json').write_text(json.dumps(remaining,ensure_ascii=False,indent=2)+'\n')
summary={'database':'math','basis':basis,'attributes_scanned':len(stats),'text_values_scanned':sum(v['current_datoms']for v in stats),
         'broad_candidate_values':sum(v['matching_rows']for v in stats),'remaining_malformed_hat_fields':len(remaining),
         'remaining_malformed_hat_occurrences':sum(v['malformed_hat_occurrences']for v in remaining),'completed_to_end':True,
         'note':'Broad candidates include valid hats and non-hat oversets; only the independently classified malformed patterns count as defects.'}
(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
assert not remaining, 'New or remaining malformed hats require investigation'
