from review import *
import subprocess
r=json.load(open('grading-counterexample.json'))[0]
forms=['64*sqrt(17)*e^(-5/4)/1445',r'\frac{64\sqrt{17}e^{-5/4}}{1445}',r'\frac{64\sqrt{17}}{1445\exp(5/4)}']
results=[]
for i,form in enumerate(forms):
 path='extra-grade-input-'+str(i)+'.json';save(path,[{'label':'negative power equivalent','record':r,'checks':[{'submitted':form,'expected':'accepted','purpose':'reciprocal power exponential equivalence'}]}]);p=subprocess.run(['/home/jake/Developer/Course_Academy/generate/runs/current/check-engine',str(ROOT/path),str(ROOT/('extra-grade-result-'+str(i)+'.json'))],capture_output=True,text=True);results.append({'submitted':form,'returncode':p.returncode,'stderr':p.stderr,'stdout':p.stdout})
save('extra-grade-results.json',results);print(json.dumps(results,indent=2))
