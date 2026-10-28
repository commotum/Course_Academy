import ast,json,re,shutil,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from generator_packages import package_digest
G=json.loads((H/'generators.json').read_text());D=json.loads((H/'generator-candidates.json').read_text());roles={17592186059716:'abnrstvu',17592186124458:'vVuij',17592186175970:'f',17592186175972:'f'}
for kp,letters in roles.items():
 g=next(g for g in G if g['kp']==kp);old=Path(g['path']);dst=H/'generators'/str(kp);dst.mkdir(parents=True,exist_ok=True);entry=old.name
 for name in g['files']:
  if name=='generator-package.json':continue
  target=dst/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(old.parent/name,target)
 if not g.get('manifest'):
  deps={'python':'3.13.5','packages':{'sympy':'1.14.0'}}
  for name in['ca_source_runtime.py','ca_source_policy.py',str(kp)+'-source-policy.json']:
   source=old.parent/name
   if source.exists():shutil.copyfile(source,dst/name)
 else:deps=g['manifest']['dependencies']
 s=(dst/entry).read_text().replace('from scripts.question_capture.math_format import','from math_format import')
 if kp==17592186175970:
  start=s.index('try:\n import sympy as sp');end=s.index('KP_ID=',start);s=s[:start]+'import sympy as sp\n'+s[end:]
 tree=ast.parse(s);node=next(n for n in tree.body if isinstance(n,ast.If)and'__name__'in ast.unparse(n.test))
 # Source-policy worker dispatch at the top must remain first. Add the notation
 # boundary immediately before the LAST __main__ entry dispatch, after definitions.
 node=[n for n in tree.body if isinstance(n,ast.If)and'__name__'in ast.unparse(n.test)][-1];lines=s.splitlines(True);lines.insert(node.lineno-1,'\nfrom source_notation import install as _install_source_notation\n_install_source_notation(globals())\n\n');(dst/entry).write_text(''.join(lines));shutil.copyfile(R/'scripts/question_capture/math_format.py',dst/'math_format.py');(dst/'source_notation.py').write_text((H/'source_notation.py').read_text().replace('ROLES=[]','ROLES='+repr(list(letters))))
 evidence={'basis':9837,'kp':kp,'roles':list(letters),'source_contract':'Explicit source vector functions f, supplied direction v and normalized direction u, or vector labels a/b/n/r/s/t/v chosen by the source-backed unit-vector family; no scalar coordinate or scalar field inferred by name.','repair':'Restore source vector-role font throughout actual normal fresh prompts/solutions/choices; final UUIDs derive normalized authored content. Preserve raw replay and all banks/domains/source guards.','scope':'This material recurrence became visible when complete private legacy dependencies enabled fresh sampling of previously unexecuted registrations.'};(dst/'repair-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n');files=sorted(str(f.relative_to(dst))for f in dst.rglob('*')if f.is_file());D=[d for d in D if d['kp']!=kp];D.append({'kp':kp,'old_reference':g['registration'][':question-generator/script'],'directory':str(dst),'entrypoint':entry,'files':files,'dependencies':deps,'approved_digest':package_digest(dst,entry,files,dependencies=deps),'smoke_band':'easy','supported_difficulties':['easy','moderate','hard']if kp==17592186059716 else['easy','moderate']})
for d in D:
 if d['kp']==17592186166866:d['supported_difficulties']=['easy','moderate']
(H/'generator-candidates.json').write_text(json.dumps(D,indent=2)+'\n')
