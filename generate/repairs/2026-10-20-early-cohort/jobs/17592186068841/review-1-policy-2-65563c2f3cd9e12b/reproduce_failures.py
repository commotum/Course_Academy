"""Run only the concrete review counterexamples. No package or DB writes.
Use: PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python reproduce_failures.py
The reported defects make strict assertions fail; exit 1 is expected until repaired.
"""
import sys,json,re,subprocess
from pathlib import Path
sys.dont_write_bytecode=True
from review import module,save,ROOT,REPO
from coverage import leak
m=module();out=[];samples=[]
try:
 r=m.generate_moderate(730033,template='q-128198',parameters={'a':1},profile='observed');samples.append(r);out.append({'finding':'missing source family','passed':True})
except Exception as e:out.append({'finding':'missing source family','passed':False,'source_id':'8363d7a8-d552-504e-a21c-ebf886d548c2','error':repr(e)})
for name in ['q-79665','q-8304']:
 r=m.generate_moderate(730061,template=name,parameters={'a':1});samples.append(r);v=leak(r);out.append({'finding':'interval copies integrated answer','passed':not v['correct'],'case':v})
r=m.generate_moderate(730033,template='q-128191',parameters={'a':1},profile='observed');samples.append(r)
cases=[{'label':'source blank arbitrary-constant equivalence','record':r,'checks':[{'submitted':'x^2+5','expected':'accepted','purpose':'K+5 is an arbitrary constant whenever K is arbitrary'}]}];save('minimal-grader-input.json',cases)
cmd=[str(REPO/'generate/runs/current/check-engine'),str(ROOT/'minimal-grader-input.json'),str(ROOT/'minimal-grader-report.json')];p=subprocess.run(cmd,capture_output=True,text=True);out.append({'finding':'missing family-equivalence grading','passed':p.returncode==0,'command':cmd,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
# Raw default blank family reproduces the known actual-UI code-block problem.
r=m.generate_moderate(730033,template='q-128191',parameters={'a':1});samples.append(r)
render=[r];save('minimal-render-input.json',render)
# Use the shared real renderer, not TeX approximation. All writes stay below evidence.
cmd=[str(REPO/'.venv/bin/python'),str(REPO/'generate/pipeline/render_preview.py'),'--input',str(ROOT/'minimal-render-input.json'),'--output',str(ROOT/'minimal-render'),'--asset-root',str(ROOT)]
p=subprocess.run(cmd,capture_output=True,text=True);html=(ROOT/'minimal-render/question-001.html').read_text() if (ROOT/'minimal-render/question-001.html').exists() else '';blocks=re.findall(r'<pre.*?</pre>',html,re.S)
out.append({'finding':'blank scaffold is literal code','passed':p.returncode==0 and not any('$y=' in b or '$+K)' in b for b in blocks),'command':cmd,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'literal_code_blocks':blocks})
save('minimal-failure-records.json',samples);save('minimal-failures.json',out)
print(json.dumps([{'finding':x['finding'],'passed':x['passed']} for x in out]));sys.exit(0 if all(x['passed'] for x in out) else 1)
