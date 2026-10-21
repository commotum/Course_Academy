"""Exercise equivalent blanks and distractors with the current native engine."""
import sys,importlib.util,json,copy,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3]
spec=importlib.util.spec_from_file_location('integration_math_checks',H/'quality.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
records=json.loads((H/'grading-records.json').read_text());checks=[]
for r in records:
 r=copy.deepcopy(r);q=r['question'];f=q[':question/answer-fields'][0];kind=m.enum(f[':answer-field/type']);f[':answer-field/type']=kind;correct=m.answer_id(f[':answer-field/correct']);f[':answer-field/correct']=[':answer/id',correct]
 for a in f[':answer-field/choices']:a[':answer/type']=m.enum(a[':answer/type'])
 canonical=next(a[':answer/value']for a in f[':answer-field/choices']if str(a[':answer/id'])==correct)
 if kind.endswith('/blank'):
  parsed=m.expr(canonical);var=next(iter(parsed.free_symbols));alt=m.sp.latex(m.sp.expand(parsed));probes=[{'submitted':canonical,'expected':'accepted'},{'submitted':alt,'expected':'accepted'},{'submitted':'('+canonical+')+7','expected':'accepted'},{'submitted':'('+canonical+')+'+str(var),'expected':'rejected'}]
 else:probes=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==correct else'rejected'}for a in f[':answer-field/choices']]
 checks.append({'label':str(q[':question/id']),'record':r,'checks':probes})
out=H/'current-native';out.mkdir(exist_ok=True);(out/'input.json').write_text(json.dumps(checks)+'\n');deps=ROOT/'target/release/deps';cmd=['rustc','--edition=2024','-O',str(ROOT/'generate/runs/current/check-engine.rs')]
for name in ('course_academy_engine','serde_json'):
 lib=max(deps.glob('lib'+name+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns);cmd+=['--extern',name+'='+str(lib)]
cmd+=['-L','dependency='+str(deps),'-o',str(out/'grader')];subprocess.run(cmd,check=True);subprocess.run([str(out/'grader'),str(out/'input.json'),str(out/'results.json')],check=True)
