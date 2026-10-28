import ast,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from generator_packages import package_digest
D=json.loads((H/'generator-candidates.json').read_text())
for d in D:
 p=Path(d['directory']);e=p/d['entrypoint'];s=e.read_text();s=__import__('re').sub(r'from source_notation import[^\n]+','from source_notation import install as _install_source_notation, apply as _apply_source_notation',s)
 tree=ast.parse(s);edits=[];offsets=[0]
 for line in s.splitlines(True):offsets.append(offsets[-1]+len(line))
 main=tree
 for node in ast.walk(main):
  if isinstance(node,ast.Call)and isinstance(node.func,ast.Name)and node.func.id=='print':
   for call in ast.walk(node):
    if isinstance(call,ast.Call)and isinstance(call.func,ast.Attribute)and isinstance(call.func.value,ast.Name)and call.func.value.id=='json'and call.func.attr=='dumps'and call.args:
     arg=call.args[0]
     if isinstance(arg,ast.Call)and isinstance(arg.func,ast.Name)and arg.func.id=='_apply_source_notation':continue
     start=offsets[arg.lineno-1]+arg.col_offset;end=offsets[arg.end_lineno-1]+arg.end_col_offset;edits.append((start,end,'_apply_source_notation('+s[start:end]+')'))
 for call in ast.walk(tree):
  if isinstance(call,ast.Call)and isinstance(call.func,ast.Attribute)and isinstance(call.func.value,ast.Name)and call.func.value.id=='json'and call.func.attr=='dump'and call.args:
   arg=call.args[0]
   if isinstance(arg,ast.Call)and isinstance(arg.func,ast.Name)and arg.func.id=='_apply_source_notation':continue
   start=offsets[arg.lineno-1]+arg.col_offset;end=offsets[arg.end_lineno-1]+arg.end_col_offset;edits.append((start,end,'_apply_source_notation('+s[start:end]+')'))
 assert edits or '_apply_source_notation('in s
 for start,end,new in sorted(edits,reverse=True):s=s[:start]+new+s[end:]
 e.write_text(s);roles=json.loads((p/'repair-evidence.json').read_text())['roles'];(p/'source_notation.py').write_text((H/'source_notation.py').read_text().replace('ROLES=[]','ROLES='+repr(roles)))
 d['files']=sorted(str(f.relative_to(p))for f in p.rglob('*')if f.is_file());d['approved_digest']=package_digest(p,d['entrypoint'],d['files'],dependencies=d['dependencies'])
(H/'generator-candidates.json').write_text(json.dumps(D,indent=2)+'\n')
