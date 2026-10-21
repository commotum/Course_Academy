import pathlib,json,shutil,hashlib,subprocess,os,sys
E=pathlib.Path(__file__).resolve().parent
J=E.parent; R=pathlib.Path('/home/jake/Developer/Course_Academy'); P=R/'.venv/bin/python'; W=J/'workspace'; RT=E/'runtime'; PK=RT/'package'; KP='17592186172040'
def dump(p,d):
 p=E/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
def hashes(root):return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
def sandbox(args,extra=()):return ['bwrap','--ro-bind','/','/','--dev-bind','/dev','/dev','--bind',str(E),str(E),'--bind',str(RT/'tmp'),'/tmp',*extra,'--',*map(str,args)]
def run(label,args,extra=()):
 c=sandbox(args,extra);p=subprocess.run(c,cwd=E,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','TMPDIR':str(RT/'tmp'),'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(E/'assets')})
 dump(label,{'command':c,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr});return p
