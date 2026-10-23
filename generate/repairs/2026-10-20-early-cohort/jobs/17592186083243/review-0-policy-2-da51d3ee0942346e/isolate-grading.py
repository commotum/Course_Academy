from review import *
import subprocess
allcases=json.load(open('grader-input.json'))
r=allcases[59]['record'];save('grading-counterexample.json',[r])
print(r['generation']['parameters']);print(r['question'][':question/problem']);print('key',key(r))
forms=[key(r),'64*sqrt(17)*exp(-5/4)/1445','64*sqrt(17)/(1445*e^(5/4))',r'\frac{64\sqrt{17}}{1445e^{5/4}}',r'\frac{64}{85\sqrt{17}e^{5/4}}','0','1']
results=[]
for i,form in enumerate(forms):
 case={'label':'equivalent-'+str(i),'record':r,'checks':[{'submitted':form,'expected':'rejected' if form in ['0','1'] else 'accepted','purpose':'equivalent reciprocal/exponential forms of independently differentiated slope'}]}
 save('grade-isolate-input-'+str(i)+'.json',[case]);p=subprocess.run(['/home/jake/Developer/Course_Academy/generate/runs/current/check-engine',str(ROOT/('grade-isolate-input-'+str(i)+'.json')),str(ROOT/('grade-isolate-result-'+str(i)+'.json'))],capture_output=True,text=True)
 results.append({'submitted':form,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
save('grading-counterexample-results.json',results);print(json.dumps(results,indent=2))
# continue the complete batch while retaining failing expected-accepted test independently
allcases[59]['checks']=[v for v in allcases[59]['checks'] if 'exp(' not in v.get('submitted','')]
save('grader-followup-input.json',allcases)
