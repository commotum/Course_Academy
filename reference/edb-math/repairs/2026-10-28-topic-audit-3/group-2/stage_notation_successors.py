import ast,json,shutil,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from generator_packages import package_digest
G=json.loads((H/'generators.json').read_text());existing=json.loads((H/'generator-candidates.json').read_text());by={d['kp']:d for d in existing}
roles={17592186096648:'ab',17592186115390:'fghijk',17592186115393:'fghijk',17592186124469:'rij',17592186124470:'rijk',17592186124471:'r',17592186124574:'Fijk',17592186124593:'rij',17592186133827:'rijk',17592186133828:'Frij',17592186133831:'Frij',17592186133894:'Frijk',17592186175973:'f',17592186096649:'a',17592186096700:'abcde'}
for kp,letters in roles.items():
 g=next(g for g in G if g['kp']==kp);dst=H/'generators'/str(kp);dst.mkdir(parents=True,exist_ok=True);old=Path(g['path']);entry=old.name
 if kp not in by:
  for name in g['files']:
   if name=='generator-package.json':continue
   target=dst/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(old.parent/name,target)
  if 'generate/scratch'in str(old):
   p=dst/entry;s=p.read_text().replace('from scripts.question_capture.math_format import','from math_format import');p.write_text(s)
   deps={'python':'3.13.5','packages':{'sympy':'1.14.0'}}
  else:deps=g['manifest']['dependencies']
 else:deps=by[kp]['dependencies']
 p=dst/entry;s=p.read_text();tree=ast.parse(s);node=next(n for n in tree.body if isinstance(n,ast.If)and'__name__'in ast.unparse(n.test));lines=s.splitlines(True);install="\nfrom source_notation import install as _install_source_notation\n_install_source_notation(globals())\n\n";lines.insert(node.lineno-1,install);p.write_text(''.join(lines))
 shutil.copyfile(R/'scripts/question_capture/math_format.py',dst/'math_format.py');helper=(H/'source_notation.py').read_text().replace('ROLES=[]',"ROLES="+repr(list(letters)));(dst/'source_notation.py').write_text(helper)
 evidence={'basis':9837,'kp':kp,'roles':list(letters),'source_proof':'Retained archive source-vector-font-contracts.json; explicit vector functions, vector fields, and unit-basis roles in this KP, rather than variable-name inference across topics. Scalar f in chain rule/line integrals is excluded.','repair':'Restore source bold vector notation in actual fresh prompt/solution/choice/checkbox text. Normalize final content then assign content-derived UUIDs with image-byte identities, preserving source guards, numeric values, raw replay, and truth predicates.','previous_identity_evidence':json.loads((dst/'repair-evidence.json').read_text())if(dst/'repair-evidence.json').exists()else None};(dst/'repair-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n');files=sorted(str(f.relative_to(dst))for f in dst.rglob('*')if f.is_file());dg=package_digest(dst,entry,files,dependencies=deps);by[kp]={'kp':kp,'old_reference':g['registration'][':question-generator/script'],'directory':str(dst),'entrypoint':entry,'files':files,'dependencies':deps,'approved_digest':dg,'smoke_band':'moderate'if kp in[17592186096700,17592186175973]else'easy','supported_difficulties':['moderate']if kp==17592186096700 else['easy','moderate']if kp in[17592186096648,17592186096649]else['easy','moderate','hard']}
(H/'generator-candidates.json').write_text(json.dumps(list(by.values()),indent=2)+'\n');print('staged',len(by))
