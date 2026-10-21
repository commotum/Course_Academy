from audit import *
import collections
# Compare captured prompts and final solution mathematics independently.
rows=json.loads((E/'source-replay.json').read_text());src=json.loads((E.parent/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions'];replay=json.loads((E/'replays.json').read_text());out=[]
for q,r in zip(src,replay):
 product=re.search(r'\$f\(x\)\s*=\s*(.*?)\$',q[':question/problem'])[1].rstrip(' ,')
 generated=re.search(r'\$f\(x\)\s*=\s*(.*?)\$',r['question'][':question/problem'])[1].rstrip(' ,')
 sol=q.get(':question/worked-solution');final=None
 if sol:
  z=sol.split('& =')[-1].split('\\end{aligned}')[0].strip()
  final=equal(parse(z),s.diff(parse(product),X))
 out.append({'source':q[':question/math-academy-id'],'product_matches':equal(parse(product),parse(generated)),'field_type_matches':q[':question/answer-fields'][0][':answer-field/type'][':db/ident']==r['question'][':question/answer-fields'][0][':answer-field/type'],'captured_solution_final_correct':final,'solution_stages':'Independently read: identifies factors, displays differentiated-factor products, substitutes factor derivatives, combines/simplifies. Missing solutions for q-1933/q-47966 are authored as disclosed.','prompt_scaffold':r['question'][':question/problem']})
save('source-content.json',out)
# Additional answer-producing action: copy the displayed known summand into the blank.
probes=json.loads((E/'shortcut-results.json').read_text())
for stage,file in [('raw','samples.json'),('delivered','delivery/accepted.json')]:
 groups=collections.defaultdict(list)
 for r in json.loads((E/file).read_text()):
  if r['question'][':question/answer-fields'][0][':answer-field/type'].endswith('blank'):groups[r['generation']['template']].append(r)
 for t,rs in groups.items():
  n=0
  for r in rs:
   pr=r['question'][':question/problem'];aa=pr.split('{{field-1}}')
   if aa[1].strip():z=re.search(r'\$(.*?)\$',aa[1])[1].replace('\\,','').lstrip(' +-')
   else:z=re.findall(r'\$(.*?)\$',aa[0],re.S)[-1].rsplit('=',1)[1].replace('\\,','').strip()[:-1]
   n+=equal(parse(z),parse(key(r)))
  probes.append({'stage':stage,'template':t,'strategy':'copy the printed known summand','correct':int(n),'total':len(rs),'baseline':0.5,'records_file':file,'baseline_explanation':'Comparison is random choice of which of the two product-rule contributions is requested; this is an action baseline, not a probability of guessing an arbitrary symbolic entry.'})
save('shortcut-results.json',probes)
# Read-only inventory summary: basis and record difficulties; no dump.
inv=json.loads((E.parent/'source/inventory.json').read_text());save('inventory-summary.json',{'basis':inv['basis'],'database':inv['database'],'lineage':inv['lineage'],'questions_count':len(inv['questions']),'fingerprints_count':len(inv['fingerprints']),'publication_preparation_exists':(E.parent/'publication/preparation.json').exists(),'selection_limits':'Captured inventory 3950; read-only shared filtering uses captured fingerprints. Existing bank questions and their captured distribution are not rewritten. No actual learner history/allocated IDs supplied.'})
# Captured commands for reproduction.
(E/'commands.md').write_text('All commands run from this evidence directory. PYTHONDONTWRITEBYTECODE=1 throughout Python imports.\n\n1. `/home/jake/Developer/Course_Academy/.venv/bin/python audit.py > audit-console.txt 2>&1` (fixed parser subsequently rechecks its five capture-syntax gaps in followup.py).\n2. `/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input samples.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery --math-root /media/jake/SSD/EDB/math`\n3. Same delivery command with `--input runner-batch.json --output batch-delivery`.\n4. `/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input.json grader-report.json` fails on the valid ln4=2ln2 response; preserved grader-console.txt.\n5. `/home/jake/Developer/Course_Academy/.venv/bin/python followup.py` then `check-engine grader-observed-input.json grader-report.json` characterizes all outcomes, recording the one mathematical acceptance failure as unresolved.\n6. `/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-input.json --output render-all --asset-root . --math-root /media/jake/SSD/EDB/math --limit 14`\n7. `/home/jake/Developer/Course_Academy/.venv/bin/python finish-evidence.py`\n\nFresh seeds and explicit parameters: requests.json. Counterfactual records: counterfactuals.json. Relocation command and out-of-domain requests: packaging.json. Native grader executable and UI are existing repository interfaces. No database or publishing command executed.\n')
print('source products',all(v['product_matches'] for v in out),'source solutions',all(v['captured_solution_final_correct'] is not False for v in out),'known-term copy',[(p['template'],p['correct'],p['total']) for p in probes if p['strategy'].startswith('copy') and p['stage']=='delivered'])
