"""Strict canonical source-bank replay test; executes unmodified relocated generator."""
from review import *
import importlib.util,re
s=importlib.util.spec_from_file_location('gen',PK/(KP+'.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
source=json.loads((J/'source/source.json').read_text())['material']['kp'][':knowledge-point/canonical-example']
shutil.copyfile('/media/jake/SSD/EDB/math/images/3b/3bd19865d2a1bb6bbb40c57112f269b51a3740d01da2c80b81db4eb84c6766f1.png',E/'canonical-source-bank.png')
p={'a':1,'b':1,'c':0,'px':1,'py':1,'orientation':'y','single':'linear'}
r=g.generate('easy',seed=991,template='possible_linear',parameters=p)
try:g.generate('easy',seed=991,profile='e-8507');profile_error=None
except Exception as ex:profile_error=repr(ex)
dump('canonical-replay-case.json',{'source':source,'generated_record':r,'parameters':p,'profile_error':profile_error,'source_bank_panels':['I','II','III','IV'],'generated_choice_count':len(r['question'][':question/answer-fields'][0][':answer-field/choices']),'source_image':'canonical-source-bank.png','conclusion':'Canonical four-panel bank is present in source but has no replay profile. Authored x+y instance supplies five different fields x+y, x, y, -x, -y; it demonstrates the method but does not reproduce this original bank.'})
assert profile_error is None, 'Canonical e-8507 source-bank replay unavailable: '+str(profile_error)
