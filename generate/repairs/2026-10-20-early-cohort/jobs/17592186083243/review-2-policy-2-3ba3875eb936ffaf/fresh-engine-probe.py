from review import *
import subprocess
r=g.generate('hard',726041,'reciprocal_exp_root_blank',parameters=dict(a=1,b=1,c=1,u=2))
# Probe multiplicity normalization, positive/negative powers and cross-denominator cancellation.
terms=['exp(-1/6)^3','exp(-1/8)^4','exp(-1/4)*exp(-1/4)','exp(1/4)*exp(1/4)/exp(1)','exp(-1/3)*exp(-1/3)*exp(1/6)','(exp(-1/6)*exp(-1/6)*exp(-1/6))','1/(exp(1/6)^3)']
checks=[]; math=[]
for term in terms:
 v='8*('+term+')/(5*sqrt(5))'; delta=s.simplify(s.sympify(v.replace('^','**'))-8*s.exp(-s.Rational(1,2))/(5*s.sqrt(5))); assert delta==0
 math.append({'submitted':v,'difference_from_independent_derivative':str(delta)})
 checks += [{'submitted':v,'expected':'accepted'},{'submitted':'2*('+v+')','expected':'rejected'},{'submitted':'-('+v+')','expected':'rejected'}]
save('fresh-engine-input.json',[{'label':'multiplicity and cancellation boundary','record':r,'checks':checks}]);save('fresh-engine-math.json',{'record_check':mathcheck(r),'equivalence_checks':math})
p=subprocess.run(['/home/jake/Developer/Course_Academy/generate/runs/current/check-engine',str(ROOT/'fresh-engine-input.json'),str(ROOT/'fresh-engine-results.json')],text=True,capture_output=True)
save('fresh-engine-execution.json',{'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'command':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python fresh-engine-probe.py'});print(p.returncode,p.stderr)
