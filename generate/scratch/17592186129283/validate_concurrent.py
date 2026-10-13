"""Read-only API concurrency regression for unique inputs and atomic plot assets."""
import concurrent.futures,importlib.util,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('orientation',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def run(i):
    return g.generate('moderate',i,template='q-160601',parameters={'h':4 if i<2 else -4,'k':-3 if i<2 else 3},profile='observed')
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:records=list(executor.map(run,range(3)))
assert records[0]['question'][':question/id']==records[1]['question'][':question/id']
assert records[0]['question'][':question/id']!=records[2]['question'][':question/id']
for r in records:
    for answer in r['question'][':question/answer-fields'][0][':answer-field/choices']:
        path=Path(answer[':answer/value']);assert path.is_file();json.loads(Path(str(path)+'.json').read_text())
report={'calls':3,'same_instance_concurrent_calls':2,'distinct_instances':2,'atomic_images_and_sidecars':True,'unique_inputs_cleaned':not list(HERE.glob('render-call-*')),'identity_preserved':True}
assert report['unique_inputs_cleaned']
(HERE/'concurrent-render-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print('Concurrent renderer: 3 calls, 2 instances,atomic assets and stable identity passed')
