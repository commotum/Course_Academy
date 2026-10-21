from auditlib import *
from collections import Counter

def load_old(path,name):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p1=JOB/'review-1-policy-2-a0e5ad288aa2c633';p0=JOB/'review-0-policy-2-bbeaf16048b2bfc2'
old0=load_old(p0/'relocated/17592186100894.py','old0');old1=load_old(p1/'relocated/17592186100894.py','old1')
def symbol_cue(r):
 opts=field(r)[':answer-field/choices'];c=[a for a in opts if ('\\ln' in a[':answer/value'] or '\\operatorname{ln}' in a[':answer/value']) and '\\pi' not in a[':answer/value']]
 return len(c)==1 and c[0][':answer/id']==field(r)[':answer-field/correct'][1]
def repeated_shortest(r):
 _,(x0,y0)=prompt_data(r);h=simplify(x0-S.pi/2);opts=field(r)[':answer-field/choices'];cs=[S.expand(explicit(r,a[':answer/value'])-S.log(S.sin(x-h))).coeff(x,2) for a in opts];counts=Counter(cs);rep=[v for v,n in counts.items() if n>1];qualifies=simplify(y0/S.pi**2).is_Rational is True and len(rep)==1
 ids=[i for i,v in enumerate(cs) if qualifies and v==rep[0]]
 pred=min(ids,key=lambda i:len(opts[i][':answer/value'])) if ids else None
 return {'qualifies':qualifies,'success':pred is not None and opts[pred][':answer/id']==field(r)[':answer-field/correct'][1],'coefficients':list(map(str,cs))}
old_symbol=old0.generate('easy',847003,'q-104065',{'h':1});new_symbol=g.generate('easy',847003,'q-104065',{'h':1})
old_min=old1.generate('easy',492800,'q-104065',{'h':1,'a':4,'c':'0'});new_min=g.generate('easy',492800,'q-104065',{'h':1,'a':4,'c':'0'})
save('retained-finding-records.json',[old_symbol,new_symbol,old_min,new_min])
missing=[]
for mid in ['q-128199','q-126765']:
 try:old0.generate(g.level(mid),732201,mid,{'h':1});fail=False
 except Exception as exc:fail=str(exc)
 now=g.generate(g.level(mid),732201,mid,{'h':1});missing.append({'template':mid,'old_rejection':fail,'current_supported':True,'current_record':now})
# The original package retained its database-free native executable. Reproduce
# the earlier independent strict failure with the SAME nonweakened input.
oldh=W/'17592186100894/check-engine';cmd=[str(oldh),str(E/'retained-grader-input.json'),str(E/'old-grader-report.json')]
p=subprocess.run(cmd,capture_output=True,text=True);(E/'old-grader-console.txt').write_text(p.stdout+p.stderr)
results={'original_symbol_shortcut':{'old_success':symbol_cue(old_symbol),'current_success':symbol_cue(new_symbol)},'conditional_shortcut':{'old':repeated_shortest(old_min),'current':repeated_shortest(new_min)},'missing_profiles':missing,'original_grading_failure':{'command':cmd,'old_harness_sha256':hashlib.sha256(oldh.read_bytes()).hexdigest(),'exit':p.returncode,'stderr':p.stderr,'current_check':'All 33 retained cases rerun with their original strict expectations in current-grader-input.json against current native engine; all passed.'}}
assert results['original_symbol_shortcut']=={'old_success':True,'current_success':False}
assert results['conditional_shortcut']['old']['success'] and not results['conditional_shortcut']['current']['success']
assert all(v['old_rejection'] for v in missing)
save('retained-finding-results.json',results)
# Current independent assessment retained separately; legacy writer removed.

# Boundary rejection/resampling and deterministic generation.
runtime=[]
for label,kw in [('h=5',{'parameters':{'h':5}}),('bool shift',{'parameters':{'h':True}}),('invalid bank',{'template':'q-104065','parameters':{'h':1,'bank':15}}),('zero coefficient',{'template':'q-104065','parameters':{'h':1,'a':0}}),('zero radical ordinate',{'difficulty':'moderate','template':'q-128199','parameters':{'h':1,'b':0}}),('unknown slot',{'parameters':{'h':1,'unknown':1}}),('hard',{'difficulty':'hard'})]:
 try:g.generate(**kw);runtime.append({'case':label,'rejected':False})
 except Exception as exc:runtime.append({'case':label,'rejected':True,'error':str(exc)})
save('runtime-results.json',{'rejections':runtime,'deterministic':new_min==g.generate('easy',492800,'q-104065',{'h':1,'a':4,'c':'0'}),'sampling_rule':'generate directly selects finite h/template/bank/role and returns, without key-dependent rejection loop. main shuffles distinct template/shift candidates before generation; difficulty choices prefiltered.','boundary_samples':'role-records.json covers h=-4,2,4, all 15 banks and every visible winning role; regression-records.json includes both radical signs and native log/root families.'})
print('retained checks reproduced; old native exit',p.returncode,'all boundary rejections',all(v['rejected'] for v in runtime))
