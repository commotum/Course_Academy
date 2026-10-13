from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
s=(ROOT/'generate/scratch/17592186119772/replenish.py').read_text()
s=s.replace('04b158888fe91b88534a40aca8e5248e3961b748423640dc09c15de4efed8271','ff60d30ca04b04ca856b8a87c47a3d9796c0303d13a302294801ad90397ffef3').replace("'triangular-recognition-'","'normal-line-replenish-'").replace("'triangular-recognition'","'normal-line-replenish'")
a=s.index('def fingerprint(q):');b=s.index('USAGE=',a)
s=s[:a]+'''def known_records():
 out={r['question'][':question/id']:r for r in json.loads((H/'source-replay.json').read_text())}
 for path in OUT.glob('basis-*/generated.json'):
  for r in json.loads(path.read_text()):out[r['question'][':question/id']]=r
 return out
KNOWN=known_records()
def fingerprint(q):
 sid=q.get(':question/math-academy-id')
 if sid in g.CONFIG:
  c=g.CONFIG[sid];return g.generate('moderate',0,profile=sid,parameters={'scale':'1','point':c['point']})['generation']['mathematical_key']
 r=KNOWN.get(str(q.get(':question/id')))
 return r['generation']['mathematical_key'] if r else None
''' +s[b:]
a=s.index('def counts(');b=s.index('\ndef tx(',a)
s=s[:a]+'''def counts(kp,path,basis):
 shown={r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'ever-shown',basis,history=True)}
 reserved={r[0] for r in DB.query(RESERVED,[KP,LEARNER],path,'reserved',basis)}
 out={level:set() for level in ['easy','moderate','hard']};excluded=[]
 captured=loads((H/'source.edn').read_text());source={q[':db/id']:q for q in captured[':knowledge-point/questions']}
 for q in kp[':knowledge-point/questions']:
  if q[':db/id'] in shown|reserved:continue
  sid=q.get(':question/math-academy-id');key=fingerprint(q)
  if key is None:
   excluded.append({'question_id':str(q[':question/id']),'reason':'Excluded source template or unknown generated content; see capability.json'});continue
  if sid in g.CONFIG:
   assert canonical(q)==canonical(source[q[':db/id']]);c=g.CONFIG[sid]
   r=g.generate('moderate',0,profile=sid,parameters={'scale':'1','point':c['point']});v.check(r)
  else:
   r=KNOWN[str(q[':question/id'])];v.check(r);assert normalized(q)==canonical(r['question'])
  level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
  if level in out:out[level].add(key)
 result={'basis':basis,'distinct_available':{l:len(z) for l,z in out.items()},'shown_or_reserved':sorted(shown|reserved),'excluded':excluded};save(path/'available-counts.json',result);return result
''' +s[b:]
a=s.index('def finish(');b=s.index('\ndef main():',a)
s=s[:a]+'''def finish(path,verified,inv):
 caps=json.loads((H/'capability.json').read_text());remaining={l:max(0,5-verified['distinct_available_after'][l]) for l in ['easy','moderate','hard']}
 result={'outcome':'finite-limit' if remaining['moderate'] else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':g.GENERATOR_ID,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':['moderate'],'available_after':verified['distinct_available_after'],'shortage_remaining':remaining,'capability_exceptions':caps['unsupported_levels'],'unsupported_levels_filled':False,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [H/'validation.json',H/'classification.md',H/'template-extraction.md',H/'source-components.json',H/'source-bank-replay.json',H/'engine-report.json',H/'capability.json',path/'preparation.json',path/'transaction.edn',path/'commit-intent.json',path/'commit.edn',path/'verification.json',path/'inventory-after.json'] if p.exists()],'note':'Moderate supported blank-template reserve verified. Easy/hard unsupported with nominal shortage five each. Radio profiles and incomplete/context-dependent originals excluded from this bounded generator; all originals and learner history preserved.'}
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps(result),flush=True)
''' +s[b:]
s=s.replace("for l in ['easy','moderate']}","for l in ['moderate']}")
s=s.replace("used={fingerprint(q) for q in kp[':knowledge-point/questions']};records=[]", """used={fingerprint(q) for q in kp[':knowledge-point/questions']};records=[]
  historical=DB.query('[:find ?id :in $ ?kp :where [?kp :knowledge-point/questions ?q] [?q :question/id ?id]]',[KP],path,'historical-question-ids',b,history=True)
  historical_ids={str(row[0]) for row in historical}
  for qid,r in KNOWN.items():
   if qid in historical_ids:used.add(r['generation']['mathematical_key'])""")
s=s.replace("if needed[level]>0 and key not in used:","if needed[level]>0 and key not in used and r['question'][':question/id'] not in historical_ids:")
s=s.replace("if key in used:continue", "if key in used or r['question'][':question/id'] in historical_ids:continue")
s=s.replace("save(path/'generated.json',records);save(path/'native-input.json'", "save(path/'generated.json',records);KNOWN.update({r['question'][':question/id']:r for r in records});save(path/'native-input.json'")
s=s.replace("if not forms:raise RuntimeError('No changes required; current registration already complete')", "if not forms:\n   finish(path,{'basis_after':b,'new_questions':0,'distinct_available_after':counts_before['distinct_available']},inv);return")
s=s.replace("'triangular-recognition-'+str(b)","'normal-line-replenish-'+str(b)")
s=s.replace("'Native grading'", "'Native grading'")
# Protocol execution is retained even when no new content is required.
s=s.replace("used={fingerprint", """protocol=subprocess.run([str(ROOT/'.venv/bin/python'),str(H.with_suffix('.py')),'--difficulty','moderate','--count','1','--seed','421019372','--format','json'],capture_output=True,text=True,check=True)
  protocol_records=json.loads(protocol.stdout)
  for r in protocol_records:v.check(r)
  save(path/'generator-execution.json',{'command':[str(ROOT/'.venv/bin/python'),SCRIPT,'--difficulty','moderate','--count','1','--seed','421019372','--format','json'],'instances':protocol_records})
  used={fingerprint""")
# Freeze generator and validator at commit and include transport identity on recovery.
s=s.replace("intent['source']==SOURCE and intent['exact_edn']", "intent['source']==SOURCE and intent['endpoint']==DB.args.endpoint and intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest() and intent['exact_edn']")
s=s.replace("save(path/'commit-intent.json',intent)","(path/'generator-at-commit.py').write_bytes(H.with_suffix('.py').read_bytes());(path/'contract-at-commit.json').write_bytes((H/'contract.json').read_bytes())\n  save(path/'commit-intent.json',intent)")
(H/'replenish.py').write_text(s)
