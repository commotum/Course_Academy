import hashlib,json,shutil,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;row=next(r for r in json.loads((H/'generators.json').read_text())if r[0]==17592186100873);src=Path('/media/jake/SSD/EDB/math')/row[2];dest=H/'generator-17592186100873';
if dest.exists():
 dest.chmod(0o755)
 for f in dest.iterdir():f.chmod(0o644)
shutil.copytree(src.parent,dest,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'));dest.chmod(0o755);(dest/src.name).chmod(0o644);text=(dest/src.name).read_text();old="full='The full matrix product is\\n\\n$$\\n'+labels[0]+'='+matrix_tex(a,augmented=False)+matrix_tex(b,augmented=False)+'\\n$$'";new="""focused_a=[[str(v) if ri==i-1 else r'{\\color{lightgray}{'+str(v)+'}}' for v in row] for ri,row in enumerate(a)]
 focused_b=[[str(v) if ci==j-1 else r'{\\color{lightgray}{'+str(v)+'}}' for ci,v in enumerate(row)] for row in b]
 full='The full matrix product is\\n\\n$$\\n'+labels[0]+'='+matrix_tex(focused_a,augmented=False)+matrix_tex(focused_b,augmented=False)+'\\n$$'""";assert old in text;text=text.replace(old,new);(dest/src.name).write_text(text)
p=subprocess.run([sys.executable,str(dest/src.name),'--difficulty','easy','--count','12','--seed','20261027','--format','json'],capture_output=True,text=True,check=True);records=json.loads(p.stdout);(H/'staged-generator-samples.json').write_text(json.dumps(records,indent=2));manifest={'kp':row[0],'entity':row[1],'registered_script':row[2],'staged_script':str(dest/src.name),'before_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'after_sha256':hashlib.sha256((dest/src.name).read_bytes()).hexdigest(),'reason':'Preserve source selected row/column focus in repeated full product; nonselected entries retain source lightgray suppression. Source-data replay paths are unchanged.','source_examples':['e-4407','q-130111','q-275547'],'fresh_samples':len(records)};(H/'generator-proposals.json').write_text(json.dumps([manifest],indent=2));print(manifest)
