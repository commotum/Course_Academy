import shutil,json,hashlib,re
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];g=next(g for g in json.loads((H/'generators.json').read_text())if g['kp']==17592186064245);old=Path(g['path']);out=H/'generators'/str(g['kp']);out.mkdir(parents=True,exist_ok=True)
for p in old.parent.rglob('*'):
 if p.is_file()and'__pycache__'not in p.parts:
  dest=out/p.relative_to(old.parent);dest.parent.mkdir(parents=True,exist_ok=True);dest.chmod(0o644) if dest.exists() else None;shutil.copy2(p,dest);dest.chmod(0o644)
s=(out/old.name).read_text().replace("VERSION='exponential-parts-2'", "VERSION='exponential-parts-3-display-integrals'")
s=s.replace('  prompt=normalize_prose(prompt);worked=normalize_prose(worked)', "  # Display standalone calculations before deriving content identities.\n  prompt=re.sub(r'(?<!\\$)\\$(?!\\$)([^$]*\\\\int[^$]*)\\$(?!\\$)',lambda m:'\\n\\n$$\\n'+m[1]+'\\n$$\\n\\n',prompt)\n  prompt=normalize_prose(prompt);worked=normalize_prose(worked)")
(out/old.name).write_text(s);shutil.copy2(R/'scripts/question_capture/math_format.py',out/'math_format.py')
evidence={'basis':9122,'kp':g['kp'],'old_reference':g['registration'][':question-generator/script'],'change':'Display standalone integral calculations in every fresh/template/observed prompt before normalization, hashing and UUID creation. Source JSON retained read-only as evidence. All numerical mathematics preserved.','identity':'Full final normalized prompt, worked solution, sorted choices, field type/key and version included before SHA256→UUID5; version bumped as additional immutable-generation separation.'}
(out/'repair-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n');print(out)
