import sys, pathlib, json, copy, collections, itertools, subprocess, importlib.util, math
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent; W=E.parent/'workspace'
spec=importlib.util.spec_from_file_location('strict',E/'strict-regressions.py'); strict=importlib.util.module_from_spec(spec);spec.loader.exec_module(strict)
g=strict.generator
def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
def ci(r):
 f=r['question'][':question/answer-fields'][0]
 return next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])
def bank(r):return [strict.coords(a[':answer/value']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
def probes(rs):
 groups=collections.defaultdict(list)
 for r in rs:
  m=strict.matrix(r['question'][':question/problem']); b=bank(r)
  for label in ['overall','size='+str(len(b[0])),'bottom_zero='+str(not any(m[-1])),'size='+str(len(b[0]))+',bottom_zero='+str(not any(m[-1]))]:groups[label].append(r)
 out={}
 for group,rr in groups.items():
  hits=collections.Counter();trials=[]
  for r in rr:
   b=bank(r);key=ci(r);order=sorted(range(5),key=lambda i:b[i]); flat=[[4*i+j for i,j in op] for op in b];freq=collections.Counter(c for op in flat for c in op)
   ps={**{'lex_rank_'+str(k):order[k] for k in range(5)},**{'serialized_position_'+str(k):k for k in range(5)}}
   for name,scores in [('coordinate_sum',[sum(op) for op in flat]),('coordinate_frequency',[sum(freq[c] for c in op) for op in flat]),('first_row_count',[sum(c<4 for c in op) for op in flat]),('span',[max(op)-min(op) for op in flat])]:
    for side in ['min','max']:ps[name+'_'+side]=min(range(5),key=lambda k:(scores[k] if side=='min' else -scores[k],k))
   for name,pred in ps.items():hits[name]+=int(pred==key)
   trials.append({'seed':r['generation']['seed'],'question_id':r['question'][':question/id'],'key':key,'predictions':ps})
  out[group]={'n':len(rr),'hits':dict(hits),'baseline':.2,'trials':trials}
 return out
def refbits(mask,op):
 m=[[int(bool(mask & (1<<(4*i+j)))) for j in range(4)] for i in range(4)]
 return strict.ref_after(m,op)
def main():
 cmd=[sys.executable,str(W/'generator.py'),'--difficulty','moderate','--seed','932611','--count','64','--format','json']
 cli=json.loads(subprocess.check_output(cmd,text=True));save('cli-control-records.json',cli)
 fresh=[g.generate('moderate',seed) for seed in range(210721,210753)];save('fresh-control-records.json',fresh)
 last=cli[-1]['generation']['seed'];seen=set();kept=[];skipped=[];prefix=[]
 for seed in range(932611,last+1):
  r=g.generate('moderate',seed);strict.check_record(r);prefix.append(r);fp=r['generation']['mathematical_fingerprint']
  if fp in seen:skipped.append(seed)
  else:kept.append(r);seen.add(fp)
 assert kept==cli
 save('resampling-prefix-records.json',prefix)
 save('resampling-results.json',{'command':cmd,'raw_count':len(prefix),'survivors':len(cli),'skipped_fingerprint_seeds':skipped,'matches_cli':True,'prefix_probes':probes(prefix),'survivor_probes':probes(cli)})
 batch=json.loads((E/'batch-records.json').read_text())
 for r in fresh+batch:strict.check_record(r)
 # Verify bank-first support independently, without calling its support table.
 examples={}
 for r in fresh:
  m=strict.matrix(r['question'][':question/problem']);examples.setdefault((len(bank(r)[0]),not any(m[-1])),r)
 assert len(examples)==4
 controls=[];coverage=[]
 for group,r in examples.items():
  b=bank(r);found={}
  for mask in range(65536):
   if (mask>>12==0)!=group[1] or sum(bool((mask>>(4*i))&15) for i in range(4))<3:continue
   good=[k for k,op in enumerate(b) if refbits(mask,op)]
   if len(good)!=1 or good[0] in found:continue
   key=good[0];after=mask
   for i,j in b[key]:after &= ~(1<<(4*i+j))
   if sum(bool((after>>(4*i))&15) for i in range(4))<2:continue
   noops=[sum(not mask & (1<<(4*i+j)) for i,j in op) for op in b]
   if sum(n<=noops[key] for n in noops)<2:continue
   m=[[int(bool(mask & (1<<(4*i+j)))) for j in range(4)] for i in range(4)]
   rr=g.generate('moderate',63000+len(controls),parameters={'matrix':m,'bank':b});strict.check_record(rr)
   assert ci(rr)==key and bank(rr)==b
   found[key]=rr;controls.append(rr)
   if len(found)==5:break
  assert len(found)==5
  coverage.append({'group':str(group),'bank':b,'keys':sorted(found),'record_indices':{str(k):controls.index(found[k]) for k in found}})
 save('fixed-bank-records.json',controls);save('fixed-bank-results.json',coverage)
 reported=g.generate('moderate',431440325);strict.check_record(reported);save('prior-minimal-case-current.json',[reported])
 save('shortcut-results.json',{'cli':probes(cli),'fresh':probes(fresh),'batch':probes(batch),'fixed_bank':probes(controls),'construction_analysis':'sample() chooses size/bottom-zero, rejects unsupported entire banks, then draws selected=rng.randrange(5) and chooses a witness. No bank-only cue can predict the fresh key above 1/5 before key-dependent CLI fingerprint filtering. Four independently enumerated fixed banks each admit all five keys. Actual CLI filtering and delivered distributions are measured separately.'})
 # Prior failing implementation: identical independent matrix-blind probe.
 old=E.parent/'review-1-policy-2-e842d7500966db6b/relocated/generator.py'
 cmdold=[sys.executable,str(old),'--difficulty','moderate','--seed','932611','--count','64']
 oldrs=json.loads(subprocess.check_output(cmdold,text=True));save('prior-shortcut-records.json',oldrs)
 oldhits=probes(oldrs)['overall']['hits']['lex_rank_2'];newhits=probes(cli)['overall']['hits']['lex_rank_2']
 assert oldhits==24
 tail=lambda n,h:sum(math.comb(n,k)*.2**k*.8**(n-k) for k in range(h,n+1))
 assert tail(64,oldhits)<.01 and tail(64,newhits)>=.01
 save('repair-verification.json',{'old_command':cmdold,'current_command':cmd,'median_old':oldhits,'median_current':newhits,'n':64,'old_binomial_tail':tail(64,oldhits),'current_binomial_tail':tail(64,newhits),'strict_original_log':'strict-original-results.txt','strict_current_log':'strict-current-results.txt','all_three_retained_defects_tested':True})
 cases=json.loads((E/'grader-input.json').read_text())
 for r in controls:
  q=r['question'];f=q[':question/answer-fields'][0];m=strict.matrix(q[':question/problem'])
  cases.append({'label':'fixed-bank '+q[':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if strict.ref_after(m,strict.coords(a[':answer/value'])) else 'rejected','purpose':'independent fixed-bank answer role counterfactual'} for a in f[':answer-field/choices']]})
 save('grader-input.json',cases)
 rs=json.loads((E/'render-records.json').read_text());rs += [controls[i] for i in [0,1]];save('render-records.json',rs)
 (E/'session-state.md').write_text('Current source replay 15/15 and 21 fresh/batch math checks pass. Retained original failures reproduced on old packages; all repaired currently. Independent CLI, fresh, fixed-bank witness and shortcut probes complete; delivery, grader and actual UI rendering pending for control sets. Package remains unchanged.\n')
 print(json.dumps({'old_median':oldhits,'new_median':newhits,'cli':len(cli),'fresh':len(fresh),'fixed_bank_witnesses':len(controls),'groups':list(examples)}))
if __name__=='__main__':main()
