"""Keep all supported native checks running when a canonical form is unsupported."""
import concurrent.futures,json,re,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent
records=json.loads((H/'grading-input.json').read_text());directory=H/'grading-batches';directory.mkdir(exist_ok=True)
def run(offset):
    batch=records[offset:offset+60];failures=[];attempts=[]
    while batch:
        source=directory/(str(offset)+'-input.json');target=directory/(str(offset)+'-report.json');source.write_text(json.dumps(batch))
        result=subprocess.run([str(H.parent/'check-engine'),str(source),str(target)],text=True,capture_output=True)
        attempts.append({'returncode':result.returncode,'stderr':result.stderr,'stdout':result.stdout})
        if result.returncode==0:return {'offset':offset,'attempts':attempts,'unsupported_or_failed_checks':failures,'report':json.loads(target.read_text())}
        match=re.search(r'"\\"([^"\\]+)\\" field (\d+):',result.stderr)
        if not match:raise RuntimeError(result.stderr)
        label,field=match[1],int(match[2]);case=next((r for r in batch if r['label']==label),None);assert case is not None
        failed=[c for c in case['checks']if c['field_index']==field]
        failures.append({'label':label,'field_index':field,'record':case['record'],'checks':failed,'native_error':result.stderr.strip()})
        case['checks']=[c for c in case['checks']if c['field_index']!=field];batch=[r for r in batch if r['checks']]
    return {'offset':offset,'attempts':attempts,'unsupported_or_failed_checks':failures,'report':None}
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
    reports=[]
    for report in pool.map(run,range(0,len(records),60)):
        reports.append(report);print('Checked batch',report['offset'],'unsupported fields',len(report['unsupported_or_failed_checks']),flush=True)
(H/'grading-bounded.json').write_text(json.dumps(reports,indent=2))
failures=[f for r in reports for f in r['unsupported_or_failed_checks']]
(H/'grading-unresolved.json').write_text(json.dumps(failures,indent=2));print('Native fields needing individual review',len(failures))
