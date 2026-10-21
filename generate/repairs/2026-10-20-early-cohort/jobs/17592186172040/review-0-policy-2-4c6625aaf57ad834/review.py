import pathlib,json,shutil,hashlib,subprocess,os,sys
E=pathlib.Path(__file__).resolve().parent
J=E.parent; R=pathlib.Path('/home/jake/Developer/Course_Academy'); P=R/'.venv/bin/python'; W=J/'workspace'; RT=E/'runtime'; PK=RT/'package'; KP='17592186172040'
def dump(p,d):
 p=E/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
def hashes(root):return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
def sandbox(args,extra=()):return ['bwrap','--ro-bind','/','/','--dev-bind','/dev','/dev','--bind',str(E),str(E),'--bind',str(RT/'tmp'),'/tmp',*extra,'--',*map(str,args)]
def run(label,args,extra=()):
 c=sandbox(args,extra);p=subprocess.run(c,cwd=E,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','TMPDIR':str(RT/'tmp')})
 dump(label,{'command':c,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr});return p
if __name__=='__main__':
 dump('package-before.json',hashes(W)); RT.mkdir(exist_ok=True); (RT/'tmp').mkdir(exist_ok=True)
 if not PK.exists():shutil.copytree(W,PK)
 shutil.copyfile(J/'samples.json',E/'batch-records.json')
 # Sampling code runs the original module from an exact relocated package. bwrap redirects renderer /tmp writes physically under evidence_root.
 p=run('sampling-command.json',[P,E/'sample.py']);print('sampling exit',p.returncode,p.stdout[-600:],p.stderr[-1200:])
 (RT/'no-exec').write_text('external Python deliberately unavailable in declared-dependency isolation test\n')
 (RT/'cold-plots').mkdir(exist_ok=True)
 p=run('cold-declared-environment.json',[P,PK/(KP+'.py'),'--difficulty','moderate','--seed','801239','--count','1','--format','json'],['--bind',str(RT/'cold-plots'),str(PK/KP/'plots'),'--ro-bind',str(RT/'no-exec'),'/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10'])
 print('cold declared dependency exit',p.returncode,p.stderr[-700:])
 dump('session-state.json',{'completed':['independent source analysis','package immutable snapshot','fresh sampling','source replay','independent point math','cold dependency test'],'next':['delivery','native grading','UI rendering','variation report']})
 (E/'session-state.md').write_text('Independent source analysis saved before package inspection. Fresh samples, source replay and cold dependency reproduction saved. Original package snapshot: package-before.json. Next: delivery, native grader, actual UI, decision variation and final report. No repair history/preflight files exist.\n')
