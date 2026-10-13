import json,re,collections,hashlib
from pathlib import Path
BASE=Path('reference/edb-math/imports/authored-checkboxes/2026-10-12/discovery-next');OUT=BASE/'reviews'
DISC=json.load(open(BASE/'audit-input.json'));HELD={q['id'] for q in json.load(open('generate/reports/checkbox-discovery-2026-10-12/direct-candidates.json'))['held']}
S=json.load(open(BASE/'review-snapshot.json'));SNAP={r[0][':db/id']:r[0] for r in S['questions']}
ROM=['I','II','III','IV','V','VI','VII','VIII','IX','X']
LABEL=r'(?:VIII|VII|VI|IV|III|II|IX|X|V|I|[A-Z])'
def subset(v,universe):
 t=re.sub(r'\$|\*','',v).strip().rstrip('.');low=t.lower()
 if low.startswith(('none','neither')):return []
 if low.startswith('all'):return universe[:]
 names=re.findall(r'\b'+LABEL+r'\b',t)
 rest=re.sub(r'\b'+LABEL+r'\b|\b(?:and|or|only|both|statements?)\b|[,\s&]','',t,flags=re.I)
 if names and not rest and set(names)<=set(universe):return list(dict.fromkeys(names))
 return None

def extract(p,bank):
 # Source-order line blocks preserve multiline mathematics, including matrix rows.
 marker=re.compile(r'(?m)^\s*(?:[-•]\s+|(?:\*\*)?('+LABEL+r')[.)](?:\*\*)?\s+)')
 ms=list(marker.finditer(p));items=[]
 if len(ms)>=2:
  for i,m in enumerate(ms):
   end=ms[i+1].start() if i+1<len(ms) else len(p)
   txt=p[m.end():end].strip()
   if i+1==len(ms):txt=re.split(r'\n\n(?=\*?Hint:|Select all|\*Hint|Note:)',txt)[0].rstrip()
   items.append({'label':m.group(1),'text':txt,'span':[m.start(),m.end()]})
  names=set(l for v in bank for l in (subset(v,ROM+list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))or []))
  if all(a['label'] is None for a in items):
   if names<=set(ROM):
    for i,a in enumerate(items):a['label']=ROM[i]
   else:
    for a in items:
     # A named object must occur at the start of its source block.
     m=re.match(r'\$?('+LABEL+r')(?=[:=(\s$])',a['text']);a['label']=m.group(1) if m else None
  if any(a['label'] is None for a in items):return items,'unresolved_label_extraction'
  if len({a['label'] for a in items})!=len(items):return items,'duplicate_source_labels'
  return items,'finite_line_list'
 # Named matrices in shared display math: extract complete aligned expression.
 matrices=list(re.finditer(r'\b([A-Z])\s*=\s*\[\\begin\{aligned\}.*?\\end\{aligned\}\]',p,re.S))
 if len(matrices)>=2:
  return [{'label':m.group(1),'text':'$'+m.group(0)+'$'} for m in matrices],'finite_named_matrices'
 if re.search(r'N,\\,Z,\\,Q,\\,R,\\,C',p):return [{'label':l,'text':'$'+l+'$'} for l in ['N','Z','Q','R','C']],'finite_named_special_sets'
 inline=list(re.finditer(r'\\text\{('+LABEL+r')\.\}\\,',p))
 if len(inline)>=2:
  out=[]
  for i,m in enumerate(inline):
   t=p[m.end():inline[i+1].start() if i+1<len(inline) else len(p)].strip();t=t.removesuffix('$$').strip().rstrip('\\,')
   out.append({'label':m.group(1),'text':'$'+t+'$'})
  return out,'finite_inline_roman_systems'
 occur=list(re.finditer(r'↑\s*\\\\\s*\\text\{('+LABEL+r')\}',p))
 if len(occur)>=2:return [{'label':m.group(1),'text':'Occurrence '+m.group(1)+' in the displayed expression'} for m in occur],'finite_annotated_occurrences'
 return [],'unresolved_source_universe'

records=[]
for d in DISC:
 if d['id']in HELD or 'image_based_case_list_requires_inspection'in d['review_flags']:continue
 q=SNAP[d['id']];p=q[':question/problem'];sol=q.get(':question/worked-solution','');fs=q.get(':question/answer-fields',[]);bank=[a for f in fs for a in f.get(':answer-field/choices',[])];items,cl=extract(p,[a[':answer/value']for a in bank]);labels=[a['label']for a in items];reasons=[]
 if cl.startswith('unresolved')or cl=='duplicate_source_labels':reasons.append(cl)
 if len(fs)!=1:reasons.append('multiple_fields_require_ownership_review')
 key=fs[0].get(':answer-field/correct',{}) if len(fs)==1 else {};keylabels=subset(key.get(':answer/value',''),labels)
 mappings=[{'answer_eid':a[':db/id'],'value':a[':answer/value'],'labels':subset(a[':answer/value'],labels)}for a in bank]
 if any(a['labels']is None for a in mappings):reasons.append('unmapped_old_choice')
 if keylabels is None:reasons.append('unmapped_or_missing_key')
 if key.get(':db/id')not in {a[':db/id']for a in bank}:reasons.append('key_not_owned_by_bank')
 # An unrestricted value/category task is retained if source list is not supplied.
 decision='needs_evidence' if reasons else 'convert'
 if 'None of the forms could be positive-definite'in [a[':answer/value']for a in bank]:reasons.append('none_option_is_universal_negative_not_empty_subset');decision='needs_evidence'
 normal=re.sub(r'\*|\$','',sol)
 confirms=[];conflicts=[]
 for m in re.finditer(r'(?:correct answer is|answer is|answer:|answer would be)\s*[:,]?\s*["“‘\']([^"”’\'\n]+)["”’\']',normal,re.I):
  x=subset(m.group(1).strip().rstrip('.'),labels)
  if x is not None:
   (confirms if set(x)==set(keylabels or [])else conflicts).append(m.group(0))
 if conflicts:reasons.append('worked_solution_final_answer_conflicts');decision='needs_evidence'
 # Record evidence even when no formulaic final-answer sentence is available; exceptions are read separately.
 keyev={'source':'existing_database_key','snapshot_path':str(BASE/'review-snapshot.json'),'answer_eid':key.get(':db/id'),'value':key.get(':answer/value'),'mapped_labels':keylabels,'solution_confirmation':confirms,'solution_conflicts':conflicts,'worked_solution':sol,'verification':'Source-order universe and each old option decoded; existing key semantics preserved. Mathematical truth not independently recalculated unless an exception proof is recorded.'}
 proof='Selected under the question predicate exactly when present in the existing database-key subset. See full captured worked solution in key_evidence; format conversion preserves that key.'
 for a in items:a.pop('span',None);a['truth']=a['label']in(keylabels or []);a['proof']=proof
 proposed=p
 # Explicit labels for unlabelled bullets while retaining the original mathematical source.
 if cl=='finite_line_list':
  ms=list(re.finditer(r'(?m)^\s*[-•]\s+',p))
  if len(ms)==len(items):
   for m,a in reversed(list(zip(ms,items))):proposed=proposed[:m.start()]+'- **'+a['label']+'.** '+proposed[m.end():]
 if not re.search(r'select all (?:that apply|applicable|correct)',proposed,re.I):proposed=proposed.rstrip()+'\n\nSelect all that apply.'
 if any(a['labels']==[]for a in mappings):proposed+=' If none apply, leave all boxes unchecked.'
 records.append({'id':d['id'],'ma_id':d['ma_id'],'decision':decision,'classification':cl,'atomic_options':items,'correct_labels':keylabels,'choice_mapping':mappings,'proposed_prompt':proposed if decision=='convert'else p,'reason':'; '.join(reasons)if reasons else 'Finite explicitly supplied independent cases; complete old-choice subsets; preserve database key.','key_evidence':keyev,'content_repairs':[],'review_flags':d['review_flags'],'solution_needs_manual_review':not confirms,'source_problem':p,'kps':d['kps']})
counts={'scope':len(records),'decisions':dict(collections.Counter(q['decision']for q in records)),'classes':dict(collections.Counter(q['classification']for q in records)),'without_formulaic_solution_confirmation':sum(q['solution_needs_manual_review']for q in records)}
result={'counts':counts,'verification_limit':'Systematic format/source-key resolution; individual mathematical correctness is not asserted beyond captured source-key evidence and separately recorded manual proofs.','questions':records}
(OUT/'text-cases.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
(OUT/'text-exceptions.json').write_text(json.dumps([q for q in records if q['decision']!='convert'or q['solution_needs_manual_review']],indent=2,ensure_ascii=False)+'\n')
print(json.dumps(counts,indent=2));print('Exclusions:');print('\n'.join(q['ma_id']+' '+q['reason'] for q in records if q['decision']!='convert'))
