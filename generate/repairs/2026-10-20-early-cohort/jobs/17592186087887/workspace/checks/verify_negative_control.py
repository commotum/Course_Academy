#!/usr/bin/env python3
"""Demonstrate that the retained regression fails on the archived defective generator."""
import json,os,pathlib,shutil,subprocess,sys,tempfile
W=pathlib.Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='ode-repair-negative-') as d:
    p=pathlib.Path(d);(p/'checks').mkdir()
    shutil.copy2(W/'evidence/generator-before.py',p/'generator.py')
    shutil.copy2(W/'math_format.py',p/'math_format.py')
    for f in ('check_shortcuts.py','reproduce_shortcut_original.py'):shutil.copy2(W/'checks'/f,p/'checks'/f)
    cmd=[sys.executable,str(p/'checks/check_shortcuts.py')]
    result=subprocess.run(cmd,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},cwd=p)
    assert result.returncode!=0 and 'assert all(predict(field(r))[1] is None for r in exact)' in result.stderr,result.stderr
    report={'passed':True,'negative_control_exit':result.returncode,'command':'python checks/check_shortcuts.py, in an isolated copy using evidence/generator-before.py as generator.py','stderr':result.stderr,'reason':'The current executable regression rejects the actual legacy minimal counterexample before reaching new bank controls.'}
    (W/'evidence/negative-control.json').write_text(json.dumps(report,indent=2)+'\n')
print('Negative control passed: retained regression exits nonzero on archived defective generator.')
