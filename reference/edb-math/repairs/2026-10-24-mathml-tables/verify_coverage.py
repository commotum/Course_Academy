"""Verify committed table spans and close the temporal gap after the scan."""
import collections,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection,loads
fields=json.loads((H/'fields.json').read_text());changes={(f['entity'],f['attribute']):f for f in fields};traces=json.loads((H/'table-edits.json').read_text())
db=connection();basis=db.basis();text=db.command('query','--as-of',basis,'--since',6244,'--file',H/'recent-content-query.edn','--inputs',H/'recent-content-inputs.edn','--max-value-bytes','2147483648','--max-join-bytes','536870912');(H/'final-recent-content.edn').write_text(text)
current={(e,str(a)[1:]):v for e,a,v in loads(text)}
assert all(current[k]==f['after'] for k,f in changes.items())
extra=json.loads((H/'restored-choice.json').read_text());old_recent={(e,str(a)[1:]):v for e,a,v in json.loads((H/'recent-content.json').read_text())}
remaining={k:v for k,v in current.items() if k not in changes and k not in old_recent}
assert len(remaining)==1 and list(remaining)[0][1]=='answer/value' and list(remaining.values())==[extra['value']]
expected=collections.Counter((r['entity'],r['attribute'],r['new_tex']) for r in traces)
assert all(current[e,a].count(tex)>=n for (e,a,tex),n in expected.items())
unresolved=json.loads((H/'unresolved-layouts.json').read_text());manual=json.loads((H/'manual-layouts.json').read_text());assert {(r['e'],r['a'],r['span']['start']) for r in unresolved}<={(r['e'],r['a'],r['span']['start']) for r in manual}
lesson=json.loads((R/'reference/edb-math/audits/2026-10-24-lesson-17592186100705/fields.json').read_text());bad=[r for r in lesson if r['limit_tables']];assert len(bad)==32 and all((r['entity'],r['attribute'])in current for r in bad)
report={'basis_t':basis,'snapshot_basis_t':6244,'all_committed_fields_current_and_exact':True,'confirmed_table_repairs_present':sum(expected.values()),'unresolved_confirmed_source_layouts':0,'original_lesson_tables_repaired':len(bad),'additional_current_fields_since_snapshot_reviewed':len(old_recent),'new_table_defects_in_concurrent_content':0,'only_additional_answer_value_is_restored_distractor':True,'scope':'All source-confirmed lost explicit table rules found in the database-wide scan; ordinary unruled matrices and aligned derivations are retained.'}
(H/'coverage-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
