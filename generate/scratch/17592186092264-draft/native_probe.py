import sys
sys.dont_write_bytecode=True
import importlib.util,json,subprocess
from pathlib import Path
H=Path(__file__).parent;spec=importlib.util.spec_from_file_location('g',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
r=g.source_case('q-341676');f=r['question'][':question/answer-fields'][0];a=f[':answer-field/choices'][0][':answer/value'];den='3-5x^6'
checks=[{'submitted':a,'expected':'accepted','purpose':'canonical'}, {'submitted':r'\frac{-60x^5}{6-10x^6}','expected':'accepted','purpose':'genuine scaled-fraction equivalent'}, {'submitted':r'\frac{-30x^5}{3-5x^6}+1','expected':'rejected','purpose':'wrong plus one'}]
p=H/'native-probe-input.json';p.write_text(json.dumps([{'label':'probe','record':r,'checks':checks}]))
z=subprocess.run(['generate/runs/current/check-engine',str(p),str(H/'native-probe-report.json')],capture_output=True,text=True);print(z.returncode,z.stdout,z.stderr)
