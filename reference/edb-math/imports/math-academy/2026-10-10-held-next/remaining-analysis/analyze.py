"""Current-held-only descriptive analysis. Does not authorize any answer or write EDB."""
import collections,hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent;BATCH=ROOT.parent;INDEX=BATCH.parent/'held-questions.json'
def read(p):return json.loads(Path(p).read_text())
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
held=read(INDEX);h={q['math_academy_id']:q for q in held['questions']};assert len(h)==1161 and held['database_basis_reviewed']==156
raw=read(BATCH/'recovery-input.json');raw={mid:q for mid,q in raw.items() if mid in h};assert set(raw)==set(h)
rad=read(BATCH/'radio-analysis-input.json')['questions'];rad={mid:q for mid,q in rad.items() if mid in h}
sel={q['id']:q for q in read(ROOT/'select-audit-input.json')['questions'] if q['id'] in h}
assert len(rad)==1086 and len(sel)==75 and set(rad).isdisjoint(sel) and set(rad)|set(sel)==set(h)
cache={};rows={};counts=collections.Counter();flags=collections.Counter();intents=collections.Counter();grades=collections.Counter();availability=collections.Counter();select_intents=collections.Counter();select_grades=collections.Counter();positions=collections.Counter();source_hashes={};proof_methods=collections.Counter()
formula=lambda s:list(re.finditer(r'\$\$([\s\S]*?)\$\$|(?<!\$)\$([^\n$]+)\$(?!\$)',s))
select_groups={
 'proof_line_justification': [335401,335420,335422,335438,335445,336106,336107,336477,336711,336716,337121],
 'variation_of_parameters_intermediate_form':[337376,337395,337466,337469,337488,352890,352895],
 'classification_or_logical_qualifier':[335460,335463,335464,338004,338082,338516,338646,338682,338686,338697,338700,338713,338982,339169,339176,339910,339913,340806,341129,342410,342657,343289,343293,343295],
 'matrix_vector_entry':[335183,335673],
 'Fourier_formula_or_convergence':[340418,340638,340645,341308,343341,343395,343438,343445,343446,343855,343860,343891,343899,343910],
 'numeric_symbolic_result_with_field_context':[335748,338837,338853,338878,338905,338907,339145,339173,340655,340669,340883,341136,341140,341448,342960,346720,365387],
}
group_for={f'q-{n}':group for group,ids in select_groups.items() for n in ids};assert set(group_for)==set(sel)
for mid in sorted(h):
 if mid in sel:path=sel[mid]['directory'];category='select_field_binding'
 else:path=rad[mid]['occurrences'][0]['directory'];category=rad[mid]['category']
 o=next(o for o in raw[mid]['occurrences'] if o['directory']==path)
 if path not in cache:
  d=Path(path);cache[path]=read(d/'state.json')
  for p in [d/'state.json',d/'content.json',d/'assets/manifest.json']:
   if p.is_file():source_hashes[str(p)]=sha(p)
 rec=cache[path]['questions'][mid];b=rec['before'];sol=rec.get(o['source_solution_stage']) or read(Path(path)/(('history-'+mid if o['source_solution_stage']=='history' else mid+'-after')+'.json'))
 assert (b.get('source_problem') or b['problem'])==o['source_problem'] and sol['worked_solution']==o['worked_solution'],mid
 fields=o['before_fields'];assert [f['key'] for f in fields]==[f['key'] for f in b['fields']]
 for a,z in zip(fields,b['fields']):assert [{k:c[k] for k in ('type','value')} for c in a['choices']]==[{k:c[k] for k in ('type','value')} for c in z['choices']]
 facts={'prompt_present':bool(o['source_problem']),'worked_solution_present':bool(o['worked_solution']),'before_HTML_present':bool(b.get('html')),'all_fields_have_original_choices':bool(fields) and all(f.get('choices') for f in fields),'all_choices_nonempty':all(c.get('value','').strip(' $\t\r\n') for f in fields for c in f['choices'])}
 availability.update(k for k,v in facts.items() if v)
 intent=rec.get('intended','unknown');grade=rec.get('actual_result',o.get('grade') or 'unknown');intents[intent]+=1;grades[grade]+=1
 row={'id':mid,'category':category,'knowledge_point':h[mid]['knowledge_point'],'topic_id':o['topic_id'],'directory':path,'source_files':o['source_files'],'source_solution_location':f'/questions/{mid}/{o["source_solution_stage"]}/worked_solution','intent':intent,'grade':grade,'source_problem':o['source_problem'],'worked_solution':o['worked_solution'],'availability':facts,'ready':False,'status':'analysis_only_unverified'}
 if mid in rad:
  analysis=next(p for p in rad[mid]['occurrences'] if p['directory']==path)
  assert analysis['source_problem']==o['source_problem'] and analysis['worked_solution']==o['worked_solution']
  row.update(candidates=analysis['candidates'],flags=rad[mid]['flags'],whole_expression_matches=analysis['whole_expression_matches'],original_choices=fields[0]['choices'])
  fs=formula(o['worked_solution']);matches=analysis['whole_expression_matches']
  if category=='math_candidate_literal_present_but_not_bound_to_answer':
   finalquote=fs[-1][0] if fs else None
   if any(x['source_quote']==finalquote for x in matches):position='includes_final_formula'
   elif matches:position='only_earlier_formulas'
   else:position='match_in_other_occurrence'
   row['literal_match_position']=position;positions[position]+=1
  cs=analysis['candidates'];values=[c['value'] for c in cs]
  extra=[]
  if any(c['type']=='text' and re.fullmatch(r'[IVX,\s]+(?:and[IVX,\s]+)?(?:only)?',c['value']) for c in cs):extra.append('roman_statement_subset_choice')
  if re.search(r'(?i)\bcorrect answer\b',o['worked_solution']):extra.append('source_has_explicit_correct_answer_phrase')
  if any(c['value'].lstrip().startswith('|') and '\n| ---' in c['value'] for c in cs):extra.append('answer_is_markdown_table')
  row['flags']=sorted(set(row['flags']+extra));flags.update(row['flags'])
 else:
  q=sel[mid];assert q['problem']==o['source_problem'] and q['solution']==o['worked_solution']
  assert len(q['fields'])==len(fields)
  row['subgroup']=group_for[mid];row['field_audit']=q['fields'];row['unconfirmed_fields']=[f['key'] for f in q['fields'] if not f['confirmed']]
  row['missing_placeholders']=sorted({f['key'] for f in fields}-set(re.findall(r'\{\{([^}]+)\}\}',o['source_problem'])))
  row['incorrect_observed_fields']={stage:[f['key'] for f in rec.get(stage,{}).get('fields',[]) if f.get('source_result')=='Incorrect'] for stage in ['before','after','history']}
  row['saved_candidate_conflicts']=[f['key'] for f in q['fields'] if len(f.get('saved_candidates',[]))>1]
  select_intents[intent]+=1;select_grades[grade]+=1
  proof_methods.update(f.get('method','unknown') for f in q['fields'] if f['confirmed'])
  for f in q['fields']:
   bf=next(bf for bf in fields if bf['key']==f['key'])
   assert f['original_choices']==[{k:c[k] for k in ('type','value')} for c in bf['choices']]
 counts[category]+=1;rows[mid]=row
# Inventory only: presence of a saved image does not establish its answer meaning.
image_rows=[]
for mid,row in rows.items():
 for url in set(re.findall(r'!\[[^\]]*\]\(([^)]+)\)',row['source_problem']+'\n'+row['worked_solution'])):
  image_rows.append({'question':mid,'reference':url,'is_local':url.startswith('/'),'exists':Path(url).is_file() if url.startswith('/') else False})
selrows=[q for q in rows.values() if q['category']=='select_field_binding']
summary={'basis':156,'held_index_sha256':sha(INDEX),'total':1161,'radio_questions':1086,'select_questions':75,'categories':dict(counts),'overlapping_radio_flags':dict(flags),'literal_match_position':dict(positions),'source_availability':dict(availability),'selected_capture_intents':dict(intents),'selected_capture_grades':dict(grades),'select_intents':dict(select_intents),'select_grades':dict(select_grades),'select_total_fields':sum(len(q['field_audit']) for q in selrows),'select_previously_source_confirmed_fields':sum(f['confirmed'] for q in selrows for f in q['field_audit']),'select_unconfirmed_fields':sum(len(q['unconfirmed_fields']) for q in selrows),'select_missing_field_count_distribution':dict(collections.Counter(len(q['unconfirmed_fields']) for q in selrows)),'select_missing_keys_distribution':dict(collections.Counter(','.join(q['unconfirmed_fields']) for q in selrows)),'select_missing_placement_ids':[q['id'] for q in selrows if q['missing_placeholders']],'select_subgroups':{k:len(v) for k,v in select_groups.items()},'select_confirmed_field_methods':dict(proof_methods),'select_multiple_unconfirmed_ids':[q['id'] for q in selrows if len(q['unconfirmed_fields'])>1],'select_saved_candidate_conflicts':[q['id'] for q in selrows if q['saved_candidate_conflicts']],'image_references':len(image_rows),'unique_image_references':len({q['reference'] for q in image_rows}),'missing_or_remote_image_references':[q for q in image_rows if not q['exists']],'no_new_ready_designations':True,'database_writes_during_analysis':0,'category_note':'Primary categories describe the previous source-audit failure and candidate representation. They are not mathematical answer validation. A literal expression match is not sufficient field/answer-role evidence. Pattern flags overlap.'}
save(ROOT/'summary.json',summary);save(ROOT/'questions.json',rows);save(ROOT/'source-hashes.json',source_hashes);save(ROOT/'image-availability.json',image_rows)
(ROOT/'held-index-at-analysis.json').write_bytes(INDEX.read_bytes())
print(json.dumps(summary,ensure_ascii=False,indent=2))
