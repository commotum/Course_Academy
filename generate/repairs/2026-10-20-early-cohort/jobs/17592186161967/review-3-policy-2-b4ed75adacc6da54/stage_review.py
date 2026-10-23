import ast,collections,hashlib,importlib.util,json,pathlib,subprocess,sys
sys.dont_write_bytecode=True
from helpers import check,mats,ops
ROOT=pathlib.Path(__file__).resolve().parent;JOB=ROOT.parent;PKG=JOB/'workspace'
s=importlib.util.spec_from_file_location('subject',PKG/'17592186161967.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
a=ast.parse((ROOT/'review.py').read_text());exec(compile(ast.Module(body=[n for n in a.body if isinstance(n,ast.FunctionDef) and n.name in ['bank','analyze','metrics']],type_ignores=[]),'analysis-functions','exec'))
def save(n,x):(ROOT/n).write_text(json.dumps(x,indent=2)+'\n')
rr=[];counts=[]
original=g.generate
for seed,count in [(881901,5),(881902,9),(881903,12)]:
 attempts=[]
 def traced(*args,**kwargs):
  r=original(*args,**kwargs);attempts.append(r);return r
 g.generate=traced;out=g.batch('easy',count,seed);g.generate=original
 assert out==g.batch('easy',count,seed)
 for r in out:check(r)
 save(f'batch-attempts-{seed}.json',attempts)
 counts.append({'seed':seed,'count':count,'candidate_count':len(attempts),'accepted_count':len(out),'before':metrics(attempts),'after':metrics(out)})
 rr+=out
save('fresh-batches.json',rr);save('batch-sampling.json',counts)
cmd=[sys.executable,'-B',str(PKG/'17592186161967.py'),'--count','5','--seed','1278010737','--difficulty','easy']
cli=json.loads(subprocess.check_output(cmd));assert cli==json.load(open(ROOT/'batch.json'));save('cli-replay.json',{'command':cmd,'matches_runner_batch':True,'records':cli})
relcmd=[sys.executable,'-B',str(ROOT/'relocated/17592186161967.py'),'--count','5','--seed','1278010737','--difficulty','easy']
rel=json.loads(subprocess.check_output(relcmd,cwd=ROOT));assert rel==cli;save('relocated-output.json',rel)
p=json.load(open('packaging.json'));p.pop('relocation_pending',None);p.update(relocation_equal=True,cli_batch_matches_runner=True);save('packaging.json',p)
save('scope-review.json',{'observed':'All independent records use two integer row additions in 3x3 matrices, one unchanged pivot row, five radio choices and easy difficulty. All ten source profiles replay. Moderate/hard rejected.', 'justified_restrictions':'Swapped magnitude banks need unequal magnitudes; unit-error banks need one coefficient magnitude >1. These maintain distinct source-type choices. Small batches choose one visible error shape to preserve independent sign decisions, while larger batches sample all three; no source family removed from generator.', 'limits':'Explicit arbitrary out-of-scope parameters are not claimed supported. Canonical example lacks captured bank.'})
print(json.dumps({'fresh_cli_records':len(rr),'attempt_counts':[(x['seed'],x['candidate_count']) for x in counts],'runner_replay':True,'relocation':True}))
(ROOT/'session-state.md').write_text('Source analysis, 101 exact arithmetic cases, both retained old/current regressions, batch delivery 5/5, fresh CLI sample and relocation complete. Actual renderer running. Post-delivery probes, combined native grading and final evidence report pending.\n')
