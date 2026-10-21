"""Read-only generation probe: block networking and writes outside evidence dir."""
import contextlib, hashlib, importlib.util, inspect, io, json, os, sys, traceback
from pathlib import Path
sys.dont_write_bytecode=True
script=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();out.mkdir(parents=True,exist_ok=True)
root=next(p for p in Path(__file__).resolve().parents if (p/'Cargo.toml').exists())
os.environ['MPLCONFIGDIR']=str(out/'matplotlib');os.environ['XDG_CACHE_HOME']=str(out/'cache')
def allowed(path):
    try:return Path(path).resolve().is_relative_to(out)
    except (TypeError,ValueError):return False
def audit(event,args):
    if event.startswith('socket.') or event.startswith('subprocess.') or event in ['os.system','os.exec','os.spawn']:
        raise PermissionError('Read-only probe blocks '+event)
    if event=='open':
        path,mode,flags=args
        writing=bool(flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND))
        if writing and not isinstance(path,int) and not allowed(path):raise PermissionError('Probe blocked write: '+str(path))
    if event in ['os.mkdir','os.remove','os.rmdir','os.chmod','os.truncate'] and not allowed(args[0]):
        raise PermissionError('Probe blocked mutation: '+str(args[0]))
    if event in ['os.rename','os.link','os.symlink'] and not all(allowed(p)for p in args[:2]):
        raise PermissionError('Probe blocked mutation: '+str(args[:2]))
sys.addaudithook(audit)
sys.path.insert(0,str(root));sys.path.insert(0,str(script.parent))
report={'script':str(script),'script_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'database_writes':0,'attempts':[]}
jobs=json.loads(Path(sys.argv[3][1:]).read_text())if len(sys.argv)>3 and sys.argv[3].startswith('@')else None
levels=[]if jobs is not None else (sys.argv[3].split(',')if len(sys.argv)>3 else ['easy','medium','hard'])
if len(sys.argv)>3 and (out/'sample.json').exists():
    previous=json.loads((out/'sample.json').read_text())
    assert previous['script_sha256']==report['script_sha256'],'Generator source changed between probes'
    report['attempts']=previous['attempts']
log=io.StringIO()
try:
    with contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
        spec=importlib.util.spec_from_file_location('checkbox_generator_probe',script)
        module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
        fn=module.generate;signature=inspect.signature(fn);report['signature']=str(signature)
        calls=[]
        for level in levels:
            for seed in [0,1]:
                kwargs={}
                if 'level'in signature.parameters:kwargs['level']=level
                elif 'difficulty'in signature.parameters:kwargs['difficulty']=level
                if 'seed'in signature.parameters:kwargs['seed']=seed
                if 'output_dir'in signature.parameters:kwargs['output_dir']=out/'assets'
                calls.append(kwargs)
        calls+=jobs or []
        for kwargs in calls:
            attempt={'arguments':{k:str(v)if isinstance(v,Path)else v for k,v in kwargs.items()}}
            try:
                result=fn(**kwargs);attempt['record']=result
            except Exception as e:attempt['error']=type(e).__name__+': '+str(e)
            report['attempts'].append(attempt)
except Exception as e:report['import_error']=type(e).__name__+': '+str(e);report['traceback']=traceback.format_exc()
report['captured_log']=log.getvalue()
(out/'sample.json').write_text(json.dumps(report,indent=2,default=str)+'\n')
print(json.dumps({'script':str(script),'successful':sum('record'in a for a in report['attempts']),'attempts':len(report['attempts']),'import_error':report.get('import_error')}))
