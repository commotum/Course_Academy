"""Self-contained generator counterexample. Optional argv[1]: package directory.
Exit 1 means the reported shortcut still answers the generated minimal case.
"""
import sys,pathlib,json,importlib.util
sys.dont_write_bytecode=True
from bank_shortcut import choose,power_sign_shortest
R=pathlib.Path(__file__).resolve().parent
P=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else R.parent/'workspace'
s=importlib.util.spec_from_file_location('reviewed_minimal',P/'17592186068842.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
r=m.generate_easy(17,'simple_quotient',parameters={'n':1});f=r['question'][':question/answer-fields'][0];cs=f[':answer-field/choices'];key=f[':answer-field/correct'][1]
(R/'minimal-reproduction-records.json').write_text(json.dumps([r],indent=2,ensure_ascii=False))
res={}
for label,method in [('modal',choose),('shortest_among_repeated_left',power_sign_shortest)]:
 idx=method(cs);res[label]={'chosen_index':idx,'chosen_value':cs[idx][':answer/value'] if idx is not None else None,'correct':idx is not None and cs[idx][':answer/id']==key}
(R/'minimal-reproduction-results.json').write_text(json.dumps({'command':[sys.executable,str(R/'minimal_repro.py'),str(P)],'generation':r['generation'],'independent_expected_equation':'y*dy/dx=x on y!=0','probes':res},indent=2))
print(json.dumps(res))
if any(v['correct'] for v in res.values()):raise SystemExit('FAIL: prompt-blind answer-bank signature identifies y*dy/dx=x')
