import json,subprocess,pathlib
p=pathlib.Path(__file__).resolve().parent
cases=json.load(open(p/'grader-input.json'))
for name,rows in [('grader-valid',cases[:-1]),('grader-boundary',cases[-1:])]:
 inp=p/(name+'-input.json');report=p/(name+'-report.json');inp.write_text(json.dumps(rows,indent=2)+'\n')
 cmd=['/home/jake/Developer/Course_Academy/generate/runs/current/check-engine',str(inp),str(report)]
 r=subprocess.run(cmd,capture_output=True,text=True);(p/(name+'-execution.json')).write_text(json.dumps({'command':cmd,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'report_written':report.exists()},indent=2)+'\n');print(name,r.returncode,(r.stdout+r.stderr).strip()[:400])
