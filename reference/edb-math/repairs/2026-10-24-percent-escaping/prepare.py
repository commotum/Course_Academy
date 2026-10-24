"""Review every percent token; compile only literal-symbol insertions into CAS."""
import collections,hashlib,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/percent-escaping';sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import dumps,kw
sys.path.insert(0,str(R/'scripts/question_capture'));from math_format import MATH
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
COMMENTS={17592186107120:'Macro definition block ends with an empty comment.',17592186121008:'Commented alternative curvature formula.',17592186124217:'Commented-out explicit function expression.',17592186130458:'Entire optional integral derivation is commented out.',17592186135085:'Commented-out equivalent iterated integral.',17592186151842:'Commented-out implication arrow before the visible congruence.',17592186198106:'Commented alternative set-complement expressions.',17592186199471:'Commented-out alternative integral notation.',17592186199504:'Commented alternative parameterization.'}
def main():
 rows=json.loads((H/'percent-inventory.json').read_text());meta=json.loads((W/'metadata.json').read_text());owners=json.loads((W/'owners.json').read_text());idents={int(k):v for k,v in json.loads((W/'idents.json').read_text()).items()};values={(r['e'],r['a']):r['v'] for r in json.loads((W/'values.json').read_text())};fields=[];review=[];affected_fields=set()
 allowed={'answer/value','question/problem','question/worked-solution','tutorial/content','multistep/context','answer-field/key'}
 for r in rows:
  offsets=r['unescaped_math_offsets']
  if not offsets:continue
  assert r['a']in allowed
  if r['e']in COMMENTS:
   review.extend({'entity':r['e'],'attribute':r['a'],'offset':p,'decision':'retain-comment','reason':COMMENTS[r['e']],'context':r['v'][max(0,p-65):p+100]}for p in offsets);continue
  for p in offsets:
   v=r['v'];before=v[:p];after=v[p+1:];span=next((m[0]for m in MATH.finditer(v)if m.start()<=p<m.end()),v)
   if before[-1:].isdigit():reason='Numeric percentage, including decimal and signed values.'
   elif span==r'$[100(1-\alpha )]%$':reason='Symbolic confidence percentage, not a comment.'
   elif span==r'$p%$':reason='The question explicitly defines p as a percentage.'
   elif before.endswith(r'\,'):reason='Percentage after TeX spacing/answer box in a percentage calculation.'
   elif span in [r'$%$',r'$%.$',r'$%,$',r'$%\,(y)$',r'$%=7$']:reason='Standalone percentage unit or label beside a numeric answer/input.'
   else:raise ValueError(('Unreviewed percent context',r['e'],r['a'],p,span))
   review.append({'entity':r['e'],'attribute':r['a'],'offset':p,'decision':'escape-literal-percent','reason':reason,'context':v[max(0,p-65):p+100]})
  after=r['v']
  for p in reversed(offsets):after=after[:p]+'\\'+after[p:]
  # This repair may insert backslashes only at the individually reviewed glyphs.
  assert len(after)==len(r['v'])+len(offsets)
  assert after.replace(r'\%', '%')==r['v'].replace(r'\%','%')
  f={'entity':r['e'],'attribute':r['a'],'before':r['v'],'after':after,'percent_edits':len(offsets),'before_sha256':hashlib.sha256(r['v'].encode()).hexdigest(),'after_sha256':hashlib.sha256(after.encode()).hexdigest(),'source_t':r['t'],'render_type':'text'}
  if r['a']=='answer/value':
   fs=[p for p,a in owners.get(str(r['e']),[])if a=='answer-field/choices'];assert fs
   assert all(idents[meta[str(p)]['answer-field/type']]in [':answer-field.type/radio',':answer-field.type/select']for p in fs)
   affected_fields.update(fs);f['answer_fields']=fs;f['render_type']=idents[meta[str(r['e'])]['answer/type']].split('/')[-1]
  elif r['a']=='answer-field/key':
   assert idents[meta[str(r['e'])]['answer-field/type']]==':answer-field.type/checkbox'
   parents=[p for p,a in owners[str(r['e'])]if a=='question/answer-fields'];assert parents
   assert all(r['v'] not in values[p,'question/problem']for p in parents),'Do not break a literal blank placeholder key'
   affected_fields.add(r['e']);f['answer_fields']=[r['e']]
  fields.append(f)
 changed={f['entity']:f['after']for f in fields if f['attribute']=='answer/value'}
 banks=collections.defaultdict(list)
 for child,refs in owners.items():
  for parent,a in refs:
   if a=='answer-field/choices'and parent in affected_fields:banks[parent].append(int(child))
 for parent,choices in banks.items():
  signatures=[(meta[str(e)]['answer/type'],changed.get(e,values[e,'answer/value']))for e in choices]
  assert len(set(signatures))==len(signatures),('Choice collision',parent)
 fields.sort(key=lambda f:(f['entity'],f['attribute']));batches=[]
 for offset in range(0,len(fields),200):
  chunk=fields[offset:offset+200];folder=H/f'batch-{offset//200+1:02}';folder.mkdir(exist_ok=True)
  forms=[[kw('db/cas'),f['entity'],kw(f['attribute']),f['before'],f['after']]for f in chunk]
  affected=sorted({field for f in chunk for field in f.get('answer_fields',[])})
  # Seven imported fields already have no correct-answer link. Do not invent
  # keys as part of a display repair; native preview verifies their state stays
  # incomplete for exactly that preexisting reason.
  ensured=[field for field in affected if 'answer-field/correct'in meta[str(field)]]
  forms.extend([kw('db/ensure'),field,kw('answer-field/validate')]for field in ensured)
  payload=dumps(forms)+'\n';assert len(payload.encode())<3_500_000;(folder/'transaction.edn').write_text(payload);save(folder/'fields.json',chunk)
  (folder/'read-query.edn').write_text('[:find ?e ?a ?v :in $ [[?e ?a]] :where [?e ?a ?v]]\n');(folder/'read-inputs.edn').write_text(dumps([[[f['entity'],kw(f['attribute'])]for f in chunk]])+'\n')
  batches.append({'name':folder.name,'fields':len(chunk),'sha256':hashlib.sha256(payload.encode()).hexdigest(),'field_keys':[[f['entity'],f['attribute']]for f in chunk],'ensured_fields':ensured,'preexisting_incomplete_fields':[field for field in affected if field not in ensured]})
 save(H/'fields.json',fields);save(H/'token-review.json',review);save(H/'batches.json',batches)
 report={'database':'math','basis_t':json.loads((W/'current.manifest.json').read_text())['basis_t'],'fields':len(fields),'entities':len({f['entity']for f in fields}),'percent_edits':sum(f['percent_edits']for f in fields),'attributes':dict(collections.Counter(f['attribute']for f in fields)),'answer_fields':len(affected_fields),'retained_comment_tokens':sum(r['decision']=='retain-comment'for r in review),'retained_comment_fields':len(COMMENTS),'batches':len(batches),'only_backslashes_inserted_at_reviewed_percent_glyphs':True,'answer_value_changes_only_in_id_graded_selection_fields':True,'checkbox_labels_have_no_problem_placeholders':True}
 save(H/'preparation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
