"""Verify the fresh full database after repair, including complete field contracts."""
import collections,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/outer-fences-2026-10-29';sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import MATH,ENV,environment,scalable_table_fences,_matrix_layouts
read=lambda p:json.loads(p.read_text());A=H.parent/'2026-10-29-array-fences';qs=list({q[':db/id']:q for q in read(A/'questions.json')+read(H/'questions.json')}.values());ps=read(A/'proposals.json')+read(H/'proposals.json');changes={(p['entity'],p['attribute']):p['after']for p in ps};initial=read(R/'reference/edb-math/repairs/2026-10-29-q17592186551286/preview.json');changes[17592186551286,'question/worked-solution']=initial['after'];original_meta={int(k):v for k,v in read(W/'metadata.json').items()};identids={v['db/ident']:e for e,v in original_meta.items()if'db/ident'in v}
expected=collections.defaultdict(set);bank_fields={};scope_questions={q[':db/id']for q in qs}
for q in qs:
 e=q[':db/id'];expected[e,'question/id']={q[':question/id']};expected[e,'question/answer-fields']={f[':db/id']for f in q.get(':question/answer-fields',[])}
 for f in q.get(':question/answer-fields',[]):
  eid=f[':db/id'];kind=f[':answer-field/type'][':db/ident'];bank_fields[eid]=kind
  expected[eid,'answer-field/id']={f[':answer-field/id']};expected[eid,'answer-field/key']={changes.get((eid,'answer-field/key'),f[':answer-field/key'])};expected[eid,'answer-field/type']={identids[kind]};expected[eid,'answer-field/correct']={f[':answer-field/correct'][':db/id']}if f.get(':answer-field/correct')else set();expected[eid,'answer-field/choices']={a[':db/id']for a in f.get(':answer-field/choices',[])}
  for a in f.get(':answer-field/choices',[]):
   aid=a[':db/id'];expected[aid,'answer/id']={a[':answer/id']};expected[aid,'answer/type']={identids[a[':answer/type'][':db/ident']]};expected[aid,'answer/value']={changes.get((aid,'answer/value'),a[':answer/value'])}
for pair,value in changes.items():expected[pair]={value}
actual=collections.defaultdict(set);meta=collections.defaultdict(dict);parents=collections.defaultdict(list);values=[];counts=collections.Counter();types={'answer/type','answer-field/type','answer-field/correct','db/ident'};links={'answer-field/choices','question/answer-fields','task-item/responses','knowledge-point/questions','knowledge-point/canonical-example'};layout_names={'array','aligned','alignedat','gathered','matrix','bmatrix','pmatrix','vmatrix','Bmatrix','Vmatrix','cases'};odd_spellings=[]
for line in(W/'after.jsonl').open():
 d=json.loads(line);e,a,v=d['e'],d['a'],d['v'];counts['facts']+=1
 if(e,a)in expected:actual[e,a].add(v)
 if a in types:meta[e][a]=v
 if a in links and isinstance(v,int):parents[v].append((e,a))
 if not isinstance(v,str):continue
 counts['strings']+=1
 if r'\begin'in v and 'array'in v and re.search(r'\\begin\s+\{\s*array\s*\}',v):odd_spellings.append(d)
 if any(r'\begin{'+name+'}'in v for name in layout_names):values.append(d)
extra=[]
for pair,want in expected.items():
 got=actual[pair]
 if pair[1]=='answer-field/choices'and want<=got:
  for a in got-want:
   assert bank_fields[pair[0]]==':answer-field.type/blank'
   assert any(attr=='task-item/responses'for e,attr in parents.get(a,[]))
   assert {(e,attr)for e,attr in parents.get(a,[])if attr=='answer-field/choices'}=={(pair[0],'answer-field/choices')}
   extra.append({'field':pair[0],'answer':a})
 else:assert got==want,(pair,got,want)
names={e:v['db/ident']for e,v in meta.items()if'db/ident'in v};remaining=[];preserved=[];visible={'question/problem','question/worked-solution','tutorial/content','answer/value','answer/feedback','answer-field/feedback','answer-field/display-key','multistep/context','multistep/content','assigned-problem/instructions','activity/description','step/content'}
def norm(v):return scalable_table_fences(_matrix_layouts(v))
for d in values:
 e,a,v=d['e'],d['a'],d['v'];bare=a=='answer/value'and names.get(meta[e].get('answer/type'),'').endswith('/math')
 if a=='answer/value':
  owners=[f for f,link in parents.get(e,[])if link=='answer-field/choices']
  if not owners or any(names.get(meta[f].get('answer-field/type'),'').endswith('/blank')and meta[f].get('answer-field/correct')!=e for f in owners):
   if norm(v)!=v:preserved.append({**d,'reason':'Unowned or noncanonical blank response value retained'})
   continue
 if a not in visible and not(a=='answer-field/key'and names.get(meta[e].get('answer-field/type'),'').endswith('/checkbox')):continue
 new=norm(v)if bare else MATH.sub(lambda m:norm(m[0]),v)
 if new!=v:remaining.append(d)
(H/'postscan-remaining.json').write_text(json.dumps(remaining,indent=2)+'\n');(H/'postscan-unusual-spellings.json').write_text(json.dumps(odd_spellings,indent=2)+'\n');assert not remaining,('Remaining authored presentation defects',len(remaining));assert not odd_spellings,('Review noncanonical array environment spellings',len(odd_spellings))
report={'passed':True,'basis_t':read(W/'after.manifest.json')['basis_t'],**counts,'table_bearing_fields':len(values),'repaired_field_values_verified':len(changes),'remaining_authored_fence_defects':len(remaining),'unusual_array_spellings':len(odd_spellings),'question_records_with_full_contract_verification':len(qs),'UUIDs_field_links_answer_types_correct_links_and_banks_preserved':True,'additional_live_learner_blank_answers_preserved':extra,'preserved_noncanonical_values':len(preserved),'database_writes':0};(H/'postscan.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
