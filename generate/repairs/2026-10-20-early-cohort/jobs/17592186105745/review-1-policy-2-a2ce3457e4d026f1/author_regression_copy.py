#!/usr/bin/env python3
"""Retained findings: visible-bank counterfactuals and complete source fidelity."""
import sys
sys.dont_write_bytecode=True
import argparse,collections,copy,importlib.util,json,pathlib
import independent_math as witness
ROOT=pathlib.Path(__import__('os').environ['REVIEW_PACKAGE'])
OUT=pathlib.Path(__import__('os').environ['REVIEW_OUTPUT']);OUT.mkdir(exist_ok=True)
SOURCE=pathlib.Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186105745/source/source.json')
def save(name,data):(OUT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def load():
 spec=importlib.util.spec_from_file_location('generator',ROOT/'17592186105745.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);return g

def bank(r):return [a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
def key(r):return bank(r)[witness.keypos(r)]
def level(q):return q[':question/difficulty'][':db/ident'].split('/')[-1]
def source_replay(g):
 source=json.loads(SOURCE.read_text())['material']['kp'][':knowledge-point/questions'];results=[];records=[]
 for q in source:
  sid=q[':question/math-academy-id'];r=g.generate(level(q),71923,sid,{'rhs_scale':1,'bank_profile':'source'});records.append(r)
  f=next(f for f in q[':question/answer-fields'] if ':answer-field/correct' in f)
  z={'template':sid,'source_id':q[':question/id'],'prompt_equal':r['question'][':question/problem']==q[':question/problem'],'solution_equal':r['question'][':question/worked-solution']==q[':question/worked-solution'],'complete_bank_equal':sorted(bank(r))==sorted(a[':answer/value'] for a in f[':answer-field/choices']),'key_equal':key(r)==f[':answer-field/correct'][':answer/value'],'single_keyed_field':len(r['question'][':question/answer-fields'])==1,'math':witness.math_record(r)}
  results.append(z)
 save('source-replay-records.json',records);save('source-replay.json',results)
 assert len(results)==16 and all(all(z[k] for k in ['prompt_equal','solution_equal','complete_bank_equal','key_equal','single_keyed_field']) and z['math']['pass'] for z in results)
 # The original missing-case call itself must also work in ordinary practice.
 for sid,d in [('q-42156','easy'),('q-73524','easy'),('q-20959','easy'),('q-20962','moderate')]:
  assert witness.math_record(g.generate(d,71923,sid,{'rhs_scale':1}))['pass']
 return records

def shortcuts(g):
 minimal=[g.generate('easy',71923,'q-73743',{'rhs_scale':v}) for v in [1,-1]]
 hits=[witness.shortcut(r)[0]==[witness.keypos(r)] for r in minimal]
 save('minimal-shortcut-records.json',minimal);save('minimal-shortcut-results.json',{'successes':hits,'reported_rule_solves_both':all(hits)})
 assert not all(hits),'Reported exact minimal shortcut persists'
 records=[];groups=[]
 # This single bank includes both reported RHS signs plus slope counterfactuals.
 pairs=[[1,1],[1,-1],[-1,1],[-1,-1],[1,2]]
 for sid,q in g.CASES.items():
  rs=[g.generate(level(q),71923,sid,{'bank_pairs':pairs,'target_index':i}) for i in range(5)]
  bs=[bank(r) for r in rs];keys=[key(r) for r in rs]
  math=[witness.math_record(r) for r in rs]
  assert all(v==bs[0] for v in bs) and len(set(keys))==5
  assert len(set(r['question'][':question/problem'] for r in rs))==5
  assert len(set(r['question'][':question/worked-solution'] for r in rs))==5
  assert all(z['pass'] for z in math),[z for z in math if not z['pass']]
  # Sign/magnitude/row frequency strategies, positions, and any other deterministic
  # bank-only selector see exactly the same visible bank but five different keys.
  picks=[witness.shortcut(r)[0] for r in rs]
  assert all(p==picks[0] for p in picks)
  assert sum(p==[witness.keypos(r)] for p,r in zip(picks,rs))<=1
  groups.append({'template':sid,'target_positions':[witness.keypos(r) for r in rs],'distinct_answers':len(set(keys)),'bank_identical':True,'reported_probe_picks':picks[0],'reported_probe_hits':sum(p==[witness.keypos(r)] for p,r in zip(picks,rs)),'any_single_bank_only_pick_max_hits':1,'cases':5,'math':math})
  records.extend(rs)
 save('counterfactual-records.json',records);save('shortcut-results.json',groups)
 return records

def additional(g,records):
 batch=g.batch('easy',5,71923);save('runner-batch.json',batch)
 sample=g.batch('easy',15,88031);save('fresh-sample.json',sample)
 for r in records+batch+sample:
  assert witness.math_record(r)['pass']
  meta=r['generation'];replayed=g.generate(r['question'][':question/difficulty'].split('/')[-1],meta['seed'],meta['template'],meta['parameters'])
  assert r==replayed,'Metadata does not reproduce the current instance'
 # Redundant-row multiplier is irrelevant to the requested general solution.
 a=g.generate('moderate',71923,'q-20963',{'rhs_scale':-1});b=g.generate('moderate',71923,'q-73740',{'rhs_scale':-1})
 assert witness.family(key(a))==witness.family(key(b))
 assert a['question'][':question/problem']!=b['question'][':question/problem']
 save('irrelevant-records.json',[a,b])
 cases=[]
 for i,r in enumerate(records+batch+[a,b]):
  z=witness.math_record(r);choices=r['question'][':question/answer-fields'][0][':answer-field/choices']
  checks=[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if z['valid_choices'][j] else 'rejected','purpose':'independent rendered-math classification'} for j,c in enumerate(choices)]
  cases.append({'label':str(i)+'-'+r['generation']['template'],'record':r,'checks':checks})
 save('grader-input.json',cases)
 save('render-records.json',[next(r for r in records if r['generation']['template']==sid and r['generation']['parameters']['target_index']==i) for sid,i in [('q-42156',2),('q-73524',1),('q-73743',4),('q-20962',3)]])
 boundaries=[]
 for params in [{'rhs_scale':v} for v in [0,5,-5,'1',None]]+[{'column_scale':2},{'target_index':5}]:
  try:g.generate('easy',71923,'q-42158',params)
  except (ValueError,TypeError):boundaries.append({'parameters':params,'rejected':True})
  else:raise AssertionError('Invalid domain accepted: '+repr(params))
 save('boundary-results.json',boundaries)
 save('pedagogical-variation.json',{'counterfactual_profiles':16,'targets_per_identical_bank':5,'decision_cases':'RHS sign, slope sign, and constant magnitude change independently; 5 different prompt/solution/key triples for each identical bank.','bank_only_baseline':'Any deterministic bank-only single pick can solve at most 1 of the 5 controlled cases per profile.','irrelevant_change':'q-20963 to q-73740 changes second-row multiplier from 8 to -5; independent solution families agree.','normal_sampler':'Bank and target use independent random streams. Same mathematical tasks are deduplicated by normalized equation and requested role; no value/sign/position balancing rejection.','fresh_sample':len(sample),'runner_batch':len(batch),'fidelity':'Explicit source-bank replay is deliberately separate from authored default practice.'})
 return batch

def main():
 p=argparse.ArgumentParser();p.add_argument('--case',choices=['all','shortcut','source-replay'],default='all');args=p.parse_args();g=load()
 records=[]
 if args.case in ['all','source-replay']:records+=source_replay(g)
 if args.case in ['all','shortcut']:records+=shortcuts(g)
 if args.case=='all':additional(g,records)
 print(json.dumps({'case':args.case,'passed':True,'records_independently_checked':len(records)}))
if __name__=='__main__':main()
