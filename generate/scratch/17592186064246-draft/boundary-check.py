"""Exercise actual rendered-operand boundary slots and public explicit guards."""
import copy,hashlib,importlib.util,json,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('kp64246_validation',D/'validate.py');v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v);g=v.g
rows=[];req=[];rejected=[]
for name,t in g.TEMPLATES.items():
 for sign in [-1,1]:
  p=dict(a=10,b=0,k=1,h=0)
  if name in ['cos_frequency','cos_frequency_expanded','sin_frequency','affine_cos','affine_sin','phase_cos','phase_sin']:p['k']=5
  if name.startswith('affine'):p['a']=8;p['b']=sign*8
  if name.startswith('phase') or t[0]=='hard':p['h']=sign*8
  r=g.generate(t[0],template=name,parameters=p);v.validate_record(r);rows.append({'label':'Boundary '+name+'/'+str(sign),'record':r});req.append({'label':'boundary/'+name+'/'+str(sign),'record':r,'checks':v.checks(r)})
  invalid=copy.deepcopy(p)
  if name.startswith('affine'):invalid['b']=0
  elif name.startswith('phase'):invalid['h']=0
  elif t[0]=='hard':invalid['k']=2
  elif p['k']==5:invalid['k']=1
  else:invalid['h']=1
  try:g.generate(t[0],template=name,parameters=invalid)
  except ValueError:rejected.append({'template':name,'parameters':invalid})
  else:raise AssertionError(('workload removed',name,invalid))
  if name.startswith('affine'):
   invalid=dict(a=10,b=8,k=p['k'],h=0)
   try:g.generate(t[0],template=name,parameters=invalid)
   except ValueError:rejected.append({'template':name,'parameters':invalid,'guard':'coupled a*b'})
   else:raise AssertionError('coupled arithmetic guard bypassed')
for name,obj in [('boundary-records.json',rows),('boundary-engine-input.json',req)]:v.write(name,obj)
subprocess.run([str(D/'check-engine'),str(D/'boundary-engine-input.json'),str(D/'boundary-native-grading.json')],check=True)
v.write('boundary-validation.json',{'passed':True,'records_checked':len(rows),'rejected_invalid_explicit_calls':rejected,'source_shaped_max_products_and_denominators':True,'changed_signed_slots_consistent_in_actual_display':True,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'native':json.load(open(D/'boundary-native-grading.json'))})
print('Boundary PASS:',len(rows),'actual records;',len(rejected),'invalid public calls rejected.')
