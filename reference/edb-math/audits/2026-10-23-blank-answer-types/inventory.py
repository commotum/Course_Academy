import json,re,collections
from pathlib import Path
H=Path('reference/edb-math/audits/2026-10-23-blank-answer-types');P=Path('.local/edb/blank-answer-type-current.jsonl');e=collections.defaultdict(dict);qf=collections.defaultdict(set);owners=collections.defaultdict(set);banks=collections.defaultdict(set)
keep={'answer-field/key','answer-field/type','answer-field/correct','answer/type','answer/value','question/id','question/math-academy-id','question/problem','question/worked-solution','knowledge-point/title','db/ident'}
for r in map(json.loads,P.open()):
 n,a,v=r['e'],r['a'],r['v']
 if a in keep:e[n][a]=v
 if a=='question/answer-fields':qf[n].add(v)
 if a in ('knowledge-point/questions','knowledge-point/canonical-example'):owners[v].add(n)
 if a=='answer-field/choices':banks[n].add(v)
for q,fs in qf.items():
 for f in fs:e[f].setdefault('questions',[]).append(q)
text_id=next(n for n,d in e.items() if d.get('db/ident')==':answer.type/text');math_id=next(n for n,d in e.items() if d.get('db/ident')==':answer.type/math');blank_id=next(n for n,d in e.items() if d.get('db/ident')==':answer-field.type/blank');rows=[];stats=collections.Counter();unattached=[]
for f,d in list(e.items()):
 if d.get('answer-field/type')!=blank_id:continue
 stats['blank_fields']+=1;a=d.get('answer-field/correct')
 if not a:stats['missing_correct_link']+=1;continue
 typ=e[a].get('answer/type');stats['correct_type:'+e[typ].get('db/ident',str(typ))]+=1
 if typ!=text_id:continue
 value=e[a].get('answer/value','');flags=[]
 if re.search(r'\$|\\\[|\\\(',value):flags.append('tex-delimiter')
 if re.search(r'\\[A-Za-z]+',value):flags.append('tex-command')
 if re.search(r'[=^_√π∞∫∑≤≥±×÷∈∪∩≠{}]',value):flags.append('math-symbol')
 if re.fullmatch(r'\s*[+−-]?\d+(?:[.,]\d+)?\s*(?:/\s*[+−-]?\d+)?\s*',value):flags.append('numeric')
 if re.fullmatch(r'\s*[A-Za-z]\s*',value):flags.append('single-letter')
 qs=[]
 for q in d.get('questions',[]):
  qs.append({'entity':q,**e[q],'knowledge_points':[{'entity':kp,'title':e[kp].get('knowledge-point/title')} for kp in owners[q]]})
 row={'field':f,'key':d.get('answer-field/key'),'answer':a,'value':value,'flags':flags,'questions':qs,'other_bank_values':[{'entity':b,'value':e[b].get('answer/value'),'type':e[e[b].get('answer/type')].get('db/ident')} for b in banks[f] if b!=a]}
 rows.append(row)
(H/'text-blank-fields.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n');candidates=[r for r in rows if 'tex-delimiter' in r['flags'] or 'tex-command' in r['flags'] or 'math-symbol' in r['flags']];(H/'candidates.json').write_text(json.dumps(candidates,indent=2,ensure_ascii=False)+'\n');summary={'basis_t':json.loads(P.with_suffix('.manifest.json').read_text())['basis_t'],'stats':dict(stats),'text_blank_fields':len(rows),'candidate_fields':len(candidates),'candidate_answers':len({r['answer'] for r in candidates}),'flags':dict(collections.Counter(f for r in rows for f in r['flags'])),'text_type_entity':text_id,'math_type_entity':math_id};(H/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
for r in candidates[:30]:print(r['field'],r['answer'],repr(r['value']),[q.get('question/math-academy-id') for q in r['questions']])
