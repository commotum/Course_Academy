import sys,pathlib,json,subprocess,hashlib,collections,re
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;W=E.parent/'workspace'
def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
args=[sys.executable,str(W/'generator.py'),'--difficulty','moderate','--seed','932611','--count','64'];p=subprocess.run(args,capture_output=True,text=True,check=True);cli=json.loads(p.stdout);save('cli-control-records.json',cli)
raw=json.load(open(E/'cue-control-records.json'));last=cli[-1]['generation']['seed'];prefix=[r for r in raw if r['generation']['seed']<=last];seen=set();kept=[];skips=[]
for r in prefix:
 fp=r['generation']['mathematical_fingerprint']
 if fp in seen:skips.append(r['generation']['seed'])
 else:kept.append(r);seen.add(fp)
assert kept==cli
trials={r['seed']:r for r in json.load(open(E/'shortcut-trials.json'))};hits=sum(trials[r['generation']['seed']]['success'] for r in cli)
save('resampling-results.json',{'command':args,'candidate_prefix_count':len(prefix),'duplicate_fingerprint_seeds':skips,'survivor_count':len(cli),'matches_actual_cli':True,'lex_median_correct':hits,'lex_median_total':len(cli),'prefix_correct':sum(trials[r['generation']['seed']]['success'] for r in prefix),'prefix_total':len(prefix)})
# Reuse prior independent learner-selection simulation under matching engine/source/inventory bindings.
old=E.parent/'review-0-policy-2-e45bbb237eaca1f1';selection=json.load(open(old/'selection-analysis.json'));selection['provenance']={'copied_from':str(old/'selection-analysis.json'),'engine_binding':'3ff71b034befe7cdf143a5966ba2414f24b22cea78016f9cca37823e58fcc7ec','inventory_binding':'b084dc11482df3e53d22fd80b1e073ed72697ba6e9ee94008ae9b46c07ae9ab8','confirmed':'Read current select and seen_before_task; unchanged difficulty-first rule and captured 20-question pool.'};selection['new_batch']='Five exact batch records survive; median strategy wins 2/5. All are moderate. With positive moderate weight and all eligible, band selection is uniform so it preserves this rate in expectation. Default unconfigured selection chooses lowest fresh ID; history can change the eligible subset. No future IDs/history are invented.';selection['control_survivors']={'count':len(cli),'median_successes':hits,'conditional_uniform_success_rate':hits/len(cli)};save('selection-analysis.json',selection)
print(json.dumps(json.load(open(E/'resampling-results.json'))))
