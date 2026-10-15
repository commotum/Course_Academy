import sys
sys.dont_write_bytecode=True
import importlib.util,json,hashlib,subprocess
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('v64208',P/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g;p=g.parser
cases=[]
for pars in [(2,1,1),(3,2,2),(5,3,3)]:
 z=g.canonical_reference(pars);raw=z['raw'];base=g.generate('hard',0,'q-49524',list(pars));assert p.integral_operands(raw[':question/problem'])==p.integral_operands(base['question'][':question/problem'])
 assert g.fmt.normalize_prose(raw[':question/worked-solution'])==base['question'][':question/worked-solution'];v.check(base);cases.append(z)
assert cases[0]['raw']==g.SOURCE[':knowledge-point/canonical-example']
(P/'canonical-sourcecases.json').write_text(json.dumps(cases,indent=2)+'\n')
# Confirm all changed-parameter source references represent meaningful task changes.
sourcecases=json.loads((P/'sourcecases.json').read_text())
for sid in {c['source_id'] for c in sourcecases}:
 records=[c['record'] for c in sourcecases if c['source_id']==sid];assert len({r['generation']['mathematical_fingerprint'] for r in records})==3,sid
# All ten original source/completion banks and their twenty variations get native tests.
native=[]
for i,c in enumerate(sourcecases):
 z=c['record'];field=z['question'][':question/answer-fields'][0];key=field[':answer-field/correct'][1]
 native.append({'label':'source-'+c['source_id']+'-'+str(c['variant']),'record':z,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key else 'rejected','purpose':'owned source/completion bank ID'} for a in field[':answer-field/choices']]})
reports=[]
for n,i in enumerate(range(0,len(native),6)):
 inp=P/f'native-source-batch-{n:02}.json';out=P/f'native-source-report-{n:02}.json';inp.write_text(json.dumps(native[i:i+6],indent=2)+'\n');subprocess.run(['generate/runs/current/check-engine',str(inp),str(out)],check=True,capture_output=True);reports.append(json.loads(out.read_text()))
summary=json.loads((P/'native-summary.json').read_text());summary['source_bank_checks']={k:sum(r[k] for r in reports) for k in ['accepted_checks','rejected_checks','documented_unresolved_checks']};summary['total_accepted']=summary['accepted_checks']+summary['source_bank_checks']['accepted_checks'];summary['total_rejected']=summary['rejected_checks']+summary['source_bank_checks']['rejected_checks'];summary['total_batches']=summary['batches']+len(reports);(P/'native-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
# Separate the observed MA inventory from non-MA entries; do not count the canonical.
questions=g.SOURCE[':knowledge-point/questions'];ma=[q for q in questions if q.get(':question/math-academy-id')];nonma=[q for q in questions if not q.get(':question/math-academy-id')]
(P/'non-ma-inventory.json').write_text(json.dumps({'source_basis':2275,'ma_practice_count':len(ma),'ma_correct_key_count':9,'ma_complete_solution_count':9,'non_ma_standard_questions':nonma,'non_ma_record_count':len(nonma),'canonical_count':1,'canonical_counted_as_practice':False},indent=2)+'\n')
# Check whole registered tree including file-set additions and cache writes.
baseline=json.loads((P/'registered-baseline.json').read_text());root=P.parent;registered=root/'17592186064208';paths=[root/'17592186064208.py']+sorted(a for a in registered.rglob('*') if a.is_file());actual={str(a.relative_to(Path.cwd())) if a.is_absolute() else str(a):hashlib.sha256(a.read_bytes()).hexdigest() for a in paths};assert actual==baseline
(P/'registered-integrity.json').write_text(json.dumps({'files':len(actual),'full_path_and_hash_equal':True,'added_paths':[],'removed_paths':[],'changed_paths':[],'imports_registered':False,'bytecode_disabled':True},indent=2)+'\n')
print(json.dumps({'canonical_cases':len(cases),'source_native_banks':len(native),'native_summary':summary,'immutable_registered_files':len(actual)}))
