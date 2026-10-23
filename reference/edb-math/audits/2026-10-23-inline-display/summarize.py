"""Build prioritized read-only inventories and bind the supplied examples to history."""
import collections,csv,hashlib,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def save(name,v):(HERE/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def main():
 fields=[f for f in json.loads((HERE/'inline-integrals.json').read_text()) if f['a']!='answer/value'];history=list(map(json.loads,(HERE/'example-history.jsonl').open()));supplied=json.loads((HERE/'example-ids.json').read_text());rows=[];counts=collections.Counter();first=[]
 for f in fields:
  for o in f['occurrences']:
   if not o['integral']:continue
   priority=('standalone' if o['standalone_line'] else 'embedded')+('-with-displaystyle' if o['contains_displaystyle'] else '-without-displaystyle');counts[priority]+=1
   rows.append({'entity':f['e'],'attribute':f['a'],'role':f['role'],'priority':priority,'math':o['math'],'offset':o['start'],'current_t':f['t'],'source':f['source'],'value_sha256':f['value_sha256'],'topics':[{'id':c['topic/math-academy-id'],'title':c.get('topic/title')} for c in f['context'] if 'topic/math-academy-id' in c]})
 for eid in supplied:
  current=next(f for f in fields if f['e']==eid and f['a']=='question/problem');assert current['v']==next(r['v'] for r in json.loads((HERE/'examples.json').read_text())[str(eid)] if r['a']=='question/problem')
  assertions=sorted((r for r in history if r['e']==eid and r['a']=='question/problem' and r['added']),key=lambda r:r['t']);assert assertions
  first.append({'entity':eid,'ma_id':next(c['question/math-academy-id'] for c in current['context'] if c['entity']==eid),'first_retained_assertion':assertions[0],'current_t':current['t'],'current_problem':current['v'],'inline_integrals':[o for o in current['occurrences'] if o['integral']]})
 save('prioritized-integral-occurrences.json',rows);save('supplied-example-lineage.json',first)
 with (HERE/'prioritized-integral-occurrences.csv').open('w') as stream:
  w=csv.writer(stream);w.writerow(['entity','attribute','role','priority','topic_ids','topic_titles','math','current_t','source','offset','value_sha256'])
  for r in rows:w.writerow([r['entity'],r['attribute'],r['role'],r['priority'],';'.join(str(t['id']) for t in r['topics']),';'.join(t['title'] or '' for t in r['topics']),r['math'],r['current_t'],r['source'],r['offset'],r['value_sha256']])
 other=[f for f in json.loads((HERE/'other-display-candidates.json').read_text()) if f['a']!='answer/value'];prior=[(f,o) for f in other for o in f['occurrences'] if not o['integral'] and not o['contains_displaystyle'] and o['standalone_line'] and '<table' not in f['v'] and 'matrix-operands' not in f['v']];summary=json.loads((HERE/'summary.json').read_text());summary.update({'integral_review_priorities':dict(counts),'other_primary_prose_candidate_fields':len(other),'other_primary_prose_candidate_entities':len({f['e'] for f in other}),'other_standalone_unstyled_occurrences_outside_html_tables_or_matrix_operands':len(prior),'standalone_unstyled_integral_entities':len({r['entity'] for r in rows if r['priority']=='standalone-without-displaystyle'}),'standalone_unstyled_integral_topics':len({t['id'] for r in rows if r['priority']=='standalone-without-displaystyle' for t in r['topics']}),'unstyled_integral_topics':len({t['id'] for r in rows if r['priority'].endswith('-without-displaystyle') for t in r['topics']})});save('summary.json',summary)
 selected=[17592186064480,17592186069382,17592186078742,17592186078940]
 examples=[{'entity':f['e'],'attribute':f['a'],'problem':f['v'],'topics':[c for c in f['context'] if 'topic/title' in c],'occurrences':[o for o in f['occurrences'] if o['integral']]} for f in fields if f['e'] in selected and f['a']=='question/problem'];save('additional-integral-examples.json',examples)
 assert all(not r['inline_integrals'][0]['contains_displaystyle'] for r in first[:6]);assert all(r['inline_integrals'][0]['contains_displaystyle'] for r in first[6:])
 print(json.dumps({k:v for k,v in summary.items() if k not in ['primary_occurrences_by_tx','other_candidate_reasons']},indent=2))
if __name__=='__main__':main()
