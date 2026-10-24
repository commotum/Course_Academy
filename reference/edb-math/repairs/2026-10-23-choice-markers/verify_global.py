"""Scan the entire committed snapshot and confirm exact repair values/controls."""
import collections,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'scripts'));from question_markers import misplaced_markers

def main():
 path=ROOT/'.local/edb/choice-marker-repair-after.jsonl';before=ROOT/'.local/edb/choice-marker-repair-current.jsonl';manifest=json.loads(path.with_suffix('.manifest.json').read_text());problems={};qfields=collections.defaultdict(set);fs=collections.defaultdict(dict);idents={};allgens={};kpgens={}
 for r in map(json.loads,path.open()):
  e,a,v=r['e'],r['a'],r['v']
  if a=='question/problem':problems[e]=v
  if a=='question/answer-fields':qfields[e].add(v)
  if a in ('answer-field/key','answer-field/type'):fs[e][':'+a]=v
  if a=='db/ident':idents[e]=v
  if a=='question-generator/script':allgens[e]=v
  if a=='knowledge-point/question-generator':kpgens[e]=v
 bad=[];marker_counts=collections.Counter()
 for e,problem in problems.items():
  fields=[{**fs[f],':answer-field/type':idents[fs[f][':answer-field/type']]} for f in qfields[e]]
  if misplaced_markers(problem,fields):bad.append(e)
  for f in fields:
   if '{{'+f[':answer-field/key']+'}}' in problem:marker_counts[f[':answer-field/type']]+=1
 assert not bad,bad
 repaired=json.loads((HERE/'fields.json').read_text());assert all(problems[f['entity']]==f['after'] for f in repaired)
 # Compare the repaired ownership closure. Other writers advanced the database
 # between the initial snapshot and our transaction; their unrelated work is
 # verified separately from the receipt's exact T6108 -> T6109 change.
 owned=set()
 for q in json.loads((HERE/'candidates.json').read_text()):
  owned.add(q['e'])
  for f in q['fields']:
   owned.add(f['entity']);owned.update(f.get('answer-field/choices',[]))
 def facts(path):return {(r['e'],r['a'],json.dumps(r['v'],sort_keys=True)) for r in map(json.loads,path.open()) if r['e'] in owned}
 old=facts(before);new=facts(path);removed=old-new;added=new-old
 assert all(a=='question/problem' for _,a,_ in removed|added)
 assert len(removed)==104 and len(added)==104,(len(removed),len(added))
 reg=json.loads((HERE/'package-publication.json').read_text());assert allgens[kpgens[reg['registration']['kp']]]==reg['new_reference']
 report={'basis_t':manifest['basis_t'],'questions_scanned':len(problems),'remaining_misplaced_markers':len(bad),'repaired_values_exact':True,'legitimate_inline_marker_counts':dict(marker_counts),'owned_domain_facts_removed':len(removed),'owned_domain_facts_added':len(added),'no_answers_solutions_or_identity_changed':True,'active_generator_replacement_verified':True}
 (HERE/'global-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
