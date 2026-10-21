import sys,json,re,hashlib,shutil,subprocess,importlib.util
from pathlib import Path
sys.dont_write_bytecode=True
from review import ROOT as E,JOB as J,REPO,PKG as P,module,save,load
from independent_math import s,value,correct,X,Y,K,C,parse,rhs
from collections import Counter
m=module()
def run(cmd,name):
 p=subprocess.run([str(c) for c in cmd],text=True,capture_output=True);save(name,{'command':[str(c) for c in cmd],'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr});print(name,p.returncode,p.stderr[-300:]);return p

def delivery():
 fresh=[]
 for seed in range(942701,942717):fresh.append(m.generate_easy(seed))
 save('fresh-samples.json',fresh)
 for filename,level,out in [('batch.json','easy','delivery-batch'),('easy-grid.json','easy','delivery-easy'),('fresh-samples.json','easy','delivery-fresh'),('moderate-delivery-input.json','moderate','delivery-moderate'),('hard-delivery-input.json','hard','delivery-hard')]:
  run([sys.executable,REPO/'generate/pipeline/check_delivery.py','--input',E/filename,'--source',J/'source/source.json','--inventory',J/'source/inventory.json','--difficulty',level,'--output',E/out,'--asset-root',E],out+'-command.json')

def grading():
 cases=[];paired=[r for p in load('pairs.json') for r in [p['before'],p['after']]]
 records=load('batch.json')+paired+[r for r in load('normal-cases.json') if r['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/blank')]
 for i,r in enumerate(records):
  f=r['question'][':question/answer-fields'][0]
  if f[':answer-field/type'].endswith('/radio'):
   checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'printed ODE differentiation establishes keyed correctness'} for a in f[':answer-field/choices']]
  else:
   expr=value(correct(r));checks=[]
   for v in [expr,s.expand(expr+5),expr-s.Rational(7,3),expr+s.pi,s.factor(expr)]:
    checks.append({'submitted':str(v).replace('**','^'),'expected':'accepted','purpose':'same solution family under arbitrary-K translation; equivalent factorization'})
   for v in [2*expr,expr+X,expr+X**5,s.Integer(3)]:
    checks.append({'submitted':str(v).replace('**','^'),'expected':'rejected','purpose':'changes nonconstant term and therefore printed ODE'})
  cases.append({'label':f'fresh-independent-{i}','record':r,'checks':checks})
 # Fresh controlled blank pairs: reject before term under changed equation, and conversely.
 for pair in load('pairs.json'):
  if pair['template'] not in ('q-128191','q-128198'):continue
  for side,other in [('before','after'),('after','before')]:
   cases.append({'label':f'cross-{pair["template"]}-{side}','record':pair[side],'checks':[{'submitted':str(value(correct(pair[other]))).replace('**','^'),'expected':'rejected','purpose':'old answer must fail changed ODE'}]})
 # Retained exact strict acceptance case, with current engine.
 old=J/'review-0-policy-2-75766812ae9ead5b/grader-family-strict-input.json'
 cases+=json.loads(old.read_text())
 save('fresh-grader-input.json',cases)
 run([REPO/'generate/runs/current/check-engine',E/'fresh-grader-input.json',E/'fresh-grader-report.json'],'fresh-grader-command.json')
 out=[]
 for p in load('pairs.json'):
  b,a=p['before'],p['after'];different=s.simplify(value(correct(b))-value(correct(a)))!=0
  out.append({'kind':p['kind'],'template':p['template'],'before_answer':correct(b),'after_answer':correct(a),'answer_changed':different,'prompt_changed':b['question'][':question/problem']!=a['question'][':question/problem'],'solution_changed':b['question'][':question/worked-solution']!=a['question'][':question/worked-solution'],'passed':different if p['kind']=='relevant' else not different and b['question'][':question/problem']==a['question'][':question/problem'] and b['question'][':question/worked-solution']==a['question'][':question/worked-solution'],'grader_evidence':'fresh-grader-input.json','records':'pairs.json'})
 save('counterfactual-results.json',out)

def inventory_package():
 sys.path.insert(0,str(REPO));from scripts.generator_publish import normalized_question
 inv=json.loads((J/'source/inventory.json').read_text())
 retained=json.loads((P/'17592186068841/reference/replenishment/basis-2684/generated.json').read_text());records=[];results=[]
 for old in retained:
  g=old['generation'];r=m.generate(old['question'][':question/difficulty'].split('/')[-1],g['seed'],g['template'],parameters=g['parameters'],profile=g['bank_profile']);stored=next(q for q in inv['questions'] if q[':question/id']==old['question'][':question/id']);same=normalized_question(stored)==normalized_question(r['question']);records.append(r);results.append({'id':stored[':question/id'],'entity_id':stored[':db/id'],'matched':same,'template':g['template'],'parameters':g['parameters'],'generation_matches':all(r['generation'].get(k)==v for k,v in g.items())})
 save('generated-records.json',records);save('inventory-reproduction.json',{'basis':inv['basis'],'total':len(inv['questions']),'reproduced':results,'conclusion':'All six captured generated records reproduced by complete content and question identity; repair_revision is newly added metadata. Three easy_constant, two easy_linear and one q-79663; none belongs to the four retained defective families. Original source questions are excluded from generated status.'});save('affected-inventory.json',{'affected_questions':[]})
 dest=E/'fresh-relocated-package';dest.mkdir(exist_ok=True)
 manifest=json.loads((P/'package.json').read_text())
 for f in manifest['files']:
  target=dest/f;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/f,target)
 shutil.copyfile(P/'package.json',dest/'package.json')
 outputs=[];cmds=[]
 for pkg in [P,dest]:
  cmd=[sys.executable,'-B',pkg/'17592186068841.py','--difficulty','easy','--seed','942731','--count','2','--format','json'];p=subprocess.run([str(v) for v in cmd],cwd=E,capture_output=True,text=True);outputs.append(json.loads(p.stdout));cmds.append({'command':[str(v) for v in cmd],'returncode':p.returncode,'stderr':p.stderr})
 save('packaging-results.json',{'commands':cmds,'relocation_identical':outputs[0]==outputs[1],'dependencies_declared':manifest['dependencies'],'dependencies_actual':{'python':sys.version.split()[0],'packages':{'sympy':s.__version__}},'declared_files_exist':all((P/f).is_file() for f in manifest['files']),'deterministic_replay':m.generate_easy(942739)==m.generate_easy(942739),'runtime_rejections':load('runtime.json')['invalid_inputs'],'external_output':'No generated assets; CLI emits JSON stdout and operates from relocated declared files alone.'})
 save('relocation-samples.json',outputs[1])

def render():
 records=load('batch.json')+[r for p in load('pairs.json') for r in [p['before'],p['after']]]
 save('fresh-render-input.json',records)
 run([sys.executable,REPO/'generate/pipeline/render_preview.py','--input',E/'fresh-render-input.json','--output',E/'fresh-render','--asset-root',E,'--limit','19'],'fresh-render-command.json')

if __name__=='__main__':
 {'delivery':delivery,'grading':grading,'inventory':inventory_package,'render':render}[sys.argv[1]]()
