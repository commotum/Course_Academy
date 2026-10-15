"""Focused single/all-level JSON/Markdown CLI count, boundary and error regression."""
import collections, importlib.util, json, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('g',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
base=[str(ROOT/'.venv/bin/python'),str(D.with_suffix('.py'))];checks=[]
for selected in (*g.SUPPORTED_LEVELS,'all'):
    levels=g.SUPPORTED_LEVELS if selected=='all' else (selected,)
    boundary=min(g.CAPACITY[level]for level in levels)
    for count in (0,1,boundary):
        expected=[record for level in levels for record in g.batch(level,count,91)]
        for fmt in ('json','markdown'):
            args=base+['--difficulty',selected,'--count',str(count),'--seed','91','--format',fmt]
            result=subprocess.run(args,capture_output=True,text=True,check=True)
            assert '⏟'not in result.stdout
            if fmt=='json':
                parsed=json.loads(result.stdout);assert isinstance(parsed,list)and len(parsed)==len(expected)
                assert parsed==expected
                assert collections.Counter(r['question'][':question/difficulty'].split('/')[-1]for r in parsed)==collections.Counter({level:count for level in levels if count})
                assert len({r['question'][':question/id']for r in parsed})==len(parsed)
            else:
                assert result.stdout=='\n\n---\n\n'.join(g.markdown(r)for r in expected)+'\n'
                assert result.stdout.count('{{field-1}}')==count*len(levels)
            if count==1:assert subprocess.run(args,capture_output=True,text=True,check=True).stdout==result.stdout
            checks.append(dict(difficulty=selected,count=count,format=fmt,outcome='pass',flat_records=len(expected)))
    for count in (-1,boundary+1):
        for fmt in ('json','markdown'):
            result=subprocess.run(base+['--difficulty',selected,'--count',str(count),'--format',fmt],capture_output=True,text=True)
            assert result.returncode!=0 and result.stdout==''
            checks.append(dict(difficulty=selected,count=count,format=fmt,outcome='expected error; no partial output'))
for args in (['--difficulty','foreign'],['--difficulty','all','--count','1.2'],['--difficulty','all','--format','foreign']):
    result=subprocess.run(base+args,capture_output=True,text=True);assert result.returncode!=0 and result.stdout=='';checks.append(dict(arguments=args,outcome='expected error'))
(D/'cli-validation.json').write_text(json.dumps(dict(status='pass',checks=checks),indent=2)+'\n')
print(len(checks),'focused CLI regressions passed')
