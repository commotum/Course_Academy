import pathlib,json,hashlib,shutil
E=pathlib.Path(__file__).resolve().parent
J=E.parent; OLD=J/'review-0-policy-2-3edbf008895863aa';P=J/'workspace'
def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
provenance=[]
for name in ['audit.py','delivery-analysis.py','packaging-check.py']:
 text=(OLD/name).read_text()
 if name=='audit.py':text=text.replace("PKG=JOB/'workspace';", "PKG=pathlib.Path(os.environ.get('AUDIT_PACKAGE_ROOT',str(JOB/'workspace')));")
 (E/name).write_text(text);provenance.append({'file':name,'origin':str(OLD/name),'origin_sha256':hashlib.sha256((OLD/name).read_bytes()).hexdigest(),'adaptation':'Allow read-only baseline package selection via AUDIT_PACKAGE_ROOT' if name=='audit.py' else 'unchanged'})
text=(P/'checks/latest_failure.py').read_text().replace('from independent import *','from audit import *')
(E/'retained-regression.py').write_text(text)
provenance.append({'file':'retained-regression.py','origin':str(P/'checks/latest_failure.py'),'adaptation':'Import prior independent audit helpers; all outputs redirected to this evidence_root.'})
(E/'prior').mkdir(exist_ok=True)
for n in ['source-math-results.json','scope-results.json','rejection-results.json','math-results.json','visual-inspection.json']:
 shutil.copy2(OLD/n,E/'prior'/n);provenance.append({'file':'prior/'+n,'origin':str(OLD/n),'sha256':hashlib.sha256((OLD/n).read_bytes()).hexdigest(),'binding':'source/engine unchanged; unchanged sampling and rendering code checked via revision-diff.json; retained as supporting historical evidence only'})
save('provenance.json',provenance)
save('package-hashes-before.json',{str(x.relative_to(P)):hashlib.sha256(x.read_bytes()).hexdigest() for x in P.rglob('*') if x.is_file()})
changes={}
for n in ['generator.py','hard_ops.py','moderate_ops.py','math_format.py','moderate_sources.json']:
 old=OLD/'relocated-package'/n
 changes[n]={'before':hashlib.sha256(old.read_bytes()).hexdigest(),'after':hashlib.sha256((P/n).read_bytes()).hexdigest(),'unchanged':old.read_bytes()==(P/n).read_bytes()}
save('revision-diff.json',{'files':changes,'generator_change':'Version and guarded explicit easy source-bank lookup/source enumeration only. sample(), generate(), rendering and identity rules unchanged. moderate_sources.json appends q-72747; prior records semantically unchanged (Unicode serialization differs).','source_hash':'c5bddd54a31534f8934f2c91fd626eb4ecb50a5ca64ccdb1d639583d0890af47','review_binding':{'package_hash':'7b5219ae418b99e2d871c04735da74eeee316a0a80b73eeefb085c5811a387eb','batch_hash':'0135b47586fae53d07216024e85c2da7882ccffb4a3f65184347fd69b5368dd3'}})
print('Saved prior helpers and provenance; package hashes captured')
