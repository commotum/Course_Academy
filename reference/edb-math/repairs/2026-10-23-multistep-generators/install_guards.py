"""Stage source guards for every registered KP owning excluded source material."""
import ast
import hashlib
import json
from pathlib import Path
import shutil
import sys

H=Path(__file__).resolve().parent;ROOT=H.parents[3];MATH=Path('/media/jake/SSD/EDB/math')
sys.path.insert(0,str(ROOT))
from scripts.generator_packages import build_manifest,manifest_digest


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def instrument(text,kp):
    tree=ast.parse(text);lines=text.splitlines(keepends=True)
    insertion=0
    for node in tree.body:
        if (isinstance(node,ast.Expr) and isinstance(node.value,ast.Constant) and isinstance(node.value.value,str)) or (isinstance(node,ast.ImportFrom) and node.module=='__future__'):
            insertion=node.end_lineno
        else:break
    guards=[n for n in tree.body if isinstance(n,ast.If) and isinstance(n.test,ast.Compare)
            and isinstance(n.test.left,ast.Name) and n.test.left.id=='__name__'
            and any(isinstance(c,ast.Constant) and c.value=='__main__' for c in n.test.comparators)]
    if not guards:raise ValueError('No standard CLI guard; inspect '+str(kp))
    policy=str(kp)+'-source-policy.json'
    early=('\n# Standalone source eligibility: immutable policy ledger, seeded CLI guard.\n'
           'import sys as _ca_sys, os as _ca_os\nfrom pathlib import Path as _ca_Path\n'
           '_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))\n'
           'if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):\n'
           '    from ca_source_runtime import cli as _ca_source_cli\n'
           f'    _ca_source_cli(__file__,_ca_Path(__file__).with_name({policy!r}))\n'
           '    raise SystemExit(0)\n\n')
    late=('\nfrom ca_source_runtime import install as _ca_source_install\n'
          f'_ca_source_install(globals(),_ca_Path(__file__).with_name({policy!r}))\n\n')
    lines.insert(guards[0].lineno-1,late)
    lines.insert(insertion,early)
    result=''.join(lines);ast.parse(result);return result


def main():
    captured=json.loads((H/'excluded-sources.json').read_text());excluded=captured['records']
    owners={k[':db/id'] for q in excluded for k in q.get(':knowledge-point/_questions',[])}
    aliases={str(q[k]) for q in excluded for k in (':db/id',':question/id',':question/math-academy-id') if k in q}
    registrations=json.loads((H/'registrations.json').read_text());plan=[]
    for row in registrations:
        kp=row[':db/id']
        if kp not in owners:continue
        reg=row[':knowledge-point/question-generator'];ref=reg[':question-generator/script'];packaged=ref.startswith('generators/')
        entry=(MATH if packaged else ROOT)/ref
        policy={'version':1,'basis':captured['basis'],'excluded':[{k:q[k] for k in (':db/id',':question/id',':question/math-academy-id',':question/retired') if k in q} for q in excluded],
                'independent_support':{}}
        if kp==17592186087693:
            eligible=[q for q in ['q-11454','q-7806','q-125527','q-125528','q-125529','q-319310','q-69542'] if q not in aliases]
            for template in ('radio','blank'):
                policy['independent_support'][template]={'source_ids':eligible,
                    'justification':'Normal authored matrix-dimension questions count rows/columns in an explicitly supplied matrix, supported independently by eligible standalone matrix examples. Historical source_ids cited the entire captured pool; q-139406 is not needed or used to supply a missing prior matrix. Raw replay remains excluded.'}
        if packaged:
            oldroot=MATH/Path(*Path(ref).parts[:3]);old=json.loads((oldroot/'generator-package.json').read_text());stage=H/'packages'/str(kp);stage.mkdir(parents=True,exist_ok=True)
            for name in old['files']:
                target=stage/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(oldroot/name,target);target.chmod(target.stat().st_mode|0o200)
            path=stage/Path(*Path(ref).parts[3:]);package_root=stage
            files=list(old['files'])
        else:
            path=entry;package_root=entry.parent
            backup=H/'originals'/str(kp)/entry.name;backup.parent.mkdir(parents=True,exist_ok=True)
            if backup.exists():raise ValueError('Original already retained; do not reinstrument')
            shutil.copy2(entry,backup);files=[]
        oldsha=sha(path);path.write_text(instrument(path.read_text(),kp))
        for filename,source in [('ca_source_runtime.py','generator_source_runtime.py'),('ca_source_policy.py','generator_source_policy.py')]:
            target=path.parent/filename;shutil.copyfile(ROOT/'scripts'/source,target)
            if packaged:files.append(str(target.relative_to(package_root)))
        policy_path=path.with_name(str(kp)+'-source-policy.json');policy_path.write_text(json.dumps(policy,indent=2)+'\n')
        if packaged:
            files.append(str(policy_path.relative_to(package_root)))
            manifest=build_manifest(package_root,old['entrypoint'],sorted(set(files)),dependencies=old['dependencies'])
            digest=manifest_digest(manifest)
        else:manifest=None;digest=None
        plan.append({'kp':kp,'title':row[':knowledge-point/title'],'registration':reg,'packaged':packaged,
                     'entrypoint':str(path),'original_sha256':oldsha,'new_sha256':sha(path),
                     'manifest':manifest,'digest':digest,'policy_file':str(policy_path)})
    (H/'installation-plan.json').write_text(json.dumps(plan,indent=2)+'\n')
    print('Guarded',len(plan),'KPs;',sum(r['packaged'] for r in plan),'immutable successors staged;',sum(not r['packaged'] for r in plan),'legacy entrypoints repaired')


if __name__=='__main__':main()
