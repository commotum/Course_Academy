"""Read the displayed substitution, coefficient, factor, and solved-z stages."""
import importlib.util,json,re,subprocess,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('v',H/'validate.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
def clean(t):return t.strip().rstrip('.,').replace(r'\end{aligned}','').rstrip('.,')
checks=[]
for t,source in v.g.SOURCES.items():
 for h in ([0] if t=='q-109029' else [0,*v.g.SHIFTS]):
  r=v.g.generate(source[':question/difficulty'][':db/ident'].split('/')[-1],template=t,parameters={'shift':h})
  text=r['question'][':question/worked-solution'];F,p,q,n=v.ode(r['question'])
  p=v.sp.simplify(p.subs(v.x,v.x-h));q=v.sp.simplify(q.subs(v.x,v.x-h))
  def read(s):
   try:return v.sp.simplify(v.parse(clean(s)).subs(v.x,v.x-h))
   except Exception as e:raise AssertionError((t,h,s)) from e
  m=re.search(r'p\(x\)=(.*?),\\,q\(x\)=(.*?),\\,n=(.*?)\.',text)
  assert m and v.sp.simplify(read(m[1])-p)==0 and v.sp.simplify(read(m[2])-q)==0 and read(m[3])==n,(t,h,'Bernoulli coefficients')
  m=re.search(r'P\(x\)=(.*?),\\,Q\(x\)=(.*?)\\,\.',text)
  assert m and v.sp.simplify(read(m[1])-(1-n)*p)==0 and v.sp.simplify(read(m[2])-(1-n)*q)==0,(t,h,'linear coefficients')
  block=text.split('We then compute an integrating factor:')[1].split('Multiplying both')[0]
  I=read(block.split('& =')[-1].split(r'\end{aligned}')[0])
  assert v.sp.simplify(v.sp.diff(I,v.x)/I-(1-n)*p)==0,(t,h,'integrating factor')
  block=text.split('Now, we integrate')[1].split('Finally,')[0]
  z=read(block.split('z & =')[-1].split(r'\end{aligned}')[0])
  assert v.sp.simplify(v.sp.diff(z,v.x)+(1-n)*p*z-(1-n)*q)==0,(t,h,'solved z')
  checks.append({'template':t,'shift':h,'coefficients':True,'integrating_factor':True,'solved_z':True})
cli=subprocess.run(['python3',str(H.with_suffix('.py')),'--difficulty','hard','--count','2','--seed','14123','--format','json'],capture_output=True,text=True,check=True)
rs=json.loads(cli.stdout);assert isinstance(rs,list) and len(rs)==2
for r in rs:v.independent(r)
assert len({v.g.fingerprint(r['question']) for r in rs})==2
(H/'stage-validation.json').write_text(json.dumps({'passed':True,'generator_sha256':hashlib.sha256(H.with_suffix('.py').read_bytes()).hexdigest(),'checks':checks,'normal_python_cli_protocol_passed':True,'cli_instances':rs},indent=2)+'\n')
print('Displayed stages validated for',len(checks),'instances; normal Python CLI passed.')
