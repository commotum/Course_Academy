"""Strict source replay regression: exits 1 for current package omissions/bank changes."""
import argparse,json,pathlib,re,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--package',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parent.parent);p.add_argument('--source',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parent.parent/'source_cases.json');p.add_argument('--output',type=pathlib.Path,default=pathlib.Path(__file__).resolve().with_name('source-acceptance-result.json'));a=p.parse_args()
run=subprocess.run([sys.executable,'-B',str(a.package/'generator.py'),'--replay-source'],text=True,capture_output=True)
if run.returncode:raise RuntimeError(run.stderr)
records=json.loads(run.stdout);by_source={sid:r for r in records for sid in r['generation']['source_question_ids']}
source=json.load(open(a.source)); questions=source.get('material',{}).get('kp',source)[':knowledge-point/questions']
failures=[];checked=0
norm=lambda t:re.sub(r'\s+','',t)
def bank(q):
 return sorted((norm(f[':answer-field/key']),f[':answer-field/type'].get(':db/ident') if isinstance(f[':answer-field/type'],dict) else f[':answer-field/type'],sorted(x[':answer/value'] for x in f[':answer-field/choices'])) for f in q[':question/answer-fields'])
for q in questions:
 sid=q[':question/id'];checked+=1
 if sid not in by_source:failures.append({'source_id':sid,'defect':'source replay omitted','captured_key_and_solution_complete':bool(q.get(':question/worked-solution')) and all(f.get(':answer-field/correct') for f in q[':question/answer-fields'])});continue
 replay=by_source[sid]['question']
 if bank(q)!=bank(replay):failures.append({'source_id':sid,'defect':'response bank changed','expected_fields':len(q[':question/answer-fields']),'actual_fields':len(replay[':question/answer-fields'])})
report={'command':' '.join(sys.argv),'checked_source_cases':checked,'failures':failures,'passed':not failures}
a.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'passed':report['passed'],'checked':checked,'failures':len(failures)}));sys.exit(1 if failures else 0)
