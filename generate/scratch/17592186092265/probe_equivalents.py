"""Domain-aware unreduced radical and logarithm-power native probes.
Keeps mathematical expectation separate from the frozen engine's actual result.
"""
import sys
sys.dont_write_bytecode=True
import importlib.util,json,hashlib,re,subprocess,copy
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
g=load(H.with_suffix('.py'),'equiv92265g');p=load(H/'private_readback.py','equiv92265p')
def dump(name,z):(H/name).write_text(json.dumps(z,indent=2)+'\n')
checker=ROOT/'generate/runs/current/check-engine';assert hashlib.sha256(checker.read_bytes()).hexdigest()=='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
items=[]
r=g.generate('hard',template='q-341694',parameters=g.original('q-341694'));items.append(('radical-unreduced-chain',r,r'\frac{7}{2\sqrt{7x}\sqrt{7x}\ln(4)}','Original radicand7x and both chain-rule radical factors, domain x>0'))
for t in ('q-341694','q-341686','q-310149'):
 for base,root,exponent in ((4,2,2),(8,2,3),(9,3,2)):
  params=dict(g.original(t),b=base);r=g.generate(g.SPECS[t][1],template=t,parameters=params);inner,innerprime,der,answer,domain,point=g.math_data(t,params)
  alias=r'\frac{'+g.tex(innerprime)+'}{('+g.tex(inner)+')'+str(exponent)+r'\ln('+str(root)+')}'
  items.append((t+'-base'+str(base)+'-power-log',r,alias,'ln('+str(base)+')='+str(exponent)+' ln('+str(root)+') with actual inner derivative and operand'))
for base,root,exponent in ((4,2,2),(8,2,3),(9,3,2)):
 params=dict(g.original('q-341694'),b=base);r=g.generate('hard',template='q-341694',parameters=params);alias=r'\frac{1}{'+str(2*exponent)+r'x\ln('+str(root)+')}'
 items.append(('radical-simplified-base'+str(base)+'-power-log',r,alias,'Isolated logarithm identity on already simplified radical derivative'))
report=[];allinput=[]
for label,record,alias,purpose in items:
 field=record['question'][':question/answer-fields'][0];canonical=field[':answer-field/choices'][0][':answer/value'];assert p.eq(p.scalar(alias),p.scalar(canonical)),(label,alias,canonical)
 item={'label':label,'record':record,'checks':[{'submitted':canonical,'expected':'accepted','purpose':'canonical key'},{'submitted':alias,'expected':'accepted','purpose':purpose}]}
 dump('equivalent-probe-batch-input.json',[item]);out=H/'equivalent-probe-batch-output.json';res=subprocess.run([str(checker),str(H/'equivalent-probe-batch-input.json'),str(out)],capture_output=True,text=True);failure=None
 if res.returncode:
  failure=res.stderr.strip();match=re.search(r'expected (\w+), got (\w+)',failure);assert match,failure
  # Probe canonical alone to ensure any failure is specifically this equivalent.
  one=copy.deepcopy(item);one['checks']=one['checks'][:1];dump('equivalent-probe-batch-input.json',[one]);subprocess.run([str(checker),str(H/'equivalent-probe-batch-input.json'),str(out)],capture_output=True,text=True,check=True)
  item['checks'][1]['mathematical_expectation']='accepted';item['checks'][1]['expected']=match[2]
  dump('equivalent-probe-batch-input.json',[item]);subprocess.run([str(checker),str(H/'equivalent-probe-batch-input.json'),str(out)],capture_output=True,text=True,check=True)
 engine=json.loads(out.read_text());actual=engine['records'][0]['checks'][1]['outcome'];report.append({'label':label,'domain':record['generation']['domain'],'submitted':alias,'canonical':canonical,'symbolically_equal_under_stated_domain':True,'mathematical_expectation':'accepted','native_outcome':actual,'limitation':failure,'native':engine});allinput.append(item)
dump('equivalent-probe-input.json',allinput)
dump('equivalent-probe-validation.json',{'records':len(report),'native_equivalent_acceptances':sum(z['native_outcome']=='accepted' for z in report),'valid_equivalent_engine_gaps':[z for z in report if z['native_outcome']!='accepted'],'probes':report,'native_engine_sha256':hashlib.sha256(checker.read_bytes()).hexdigest(),'generator_and_parameters_unchanged':True,'database_writes':0})
print(json.dumps({'records':len(report),'accepted':sum(z['native_outcome']=='accepted' for z in report),'gaps':[{'label':z['label'],'outcome':z['native_outcome'],'reason':z['limitation']} for z in report if z['native_outcome']!='accepted']},indent=2))
