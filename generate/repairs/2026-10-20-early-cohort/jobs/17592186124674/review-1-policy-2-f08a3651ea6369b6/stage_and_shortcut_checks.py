import pathlib,json,re,collections,hashlib,subprocess,sys
from html.parser import HTMLParser
E=pathlib.Path(__file__).resolve().parent;J=E.parent;P='/home/jake/Developer/Course_Academy/.venv/bin/python'
def load(p):return json.loads((E/p).read_text())
def save(n,x):(E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def f(r):return r['question'][':question/answer-fields'][0]
def opts(r):return f(r)[':answer-field/choices']
def key(r):return f(r).get(':answer-field/correct',[None,None])[1]
def visible(r):
 prompt=r['question'][':question/problem'];nums=sorted({int(x) for x in re.findall(r'\d+',prompt) if int(x)>0});xs=opts(r);sole=[c for c in xs if len(nums)==1 and nums[0] in list(map(int,re.findall(r'\d+',c[':answer/value'])))];lengths=[len(re.sub(r'\s+','',c[':answer/value'].replace('\\\\','\\'))) for c in xs];linear=[]
 for c in xs:
  value=c[':answer/value'].replace('\\\\','\\');m=re.fullmatch(r'k\((\d+)-([A-Z])\)',re.sub(r'\s+','',value.split('=')[1]))
  if m:linear.append((int(m[1]),c[':answer/id']))
 kind='mixed' if len(linear)==3 else 'capacities' if len(linear)==5 else 'source_structural'
 return {'id':r['question'][':question/id'],'template':r['generation']['template'],'kind':kind,'sole_numeral':nums[0] if len(nums)==1 else None,'sole_match_count':len(sole),'sole_match_correct':len(sole)==1 and sole[0][':answer/id']==key(r),'unique_shortest':lengths.count(min(lengths))==1 and xs[lengths.index(min(lengths))][':answer/id']==key(r),'shortest_first':xs[lengths.index(min(lengths))][':answer/id']==key(r),'position':next((i for i,c in enumerate(xs) if c[':answer/id']==key(r)),None),'linear_target_rank':next((i for i,(_,k) in enumerate(sorted(linear)) if k==key(r)),None),'linear_count':len(linear),'minimum_linear':sorted(linear)[0][1]==key(r),'middle_linear':sorted(linear)[len(linear)//2][1]==key(r),'maximum_linear':sorted(linear)[-1][1]==key(r)}
sets={'fresh':load('fresh-records.json'),'batch':load('runner-batch.json'),'delivered_fresh':load('delivery-fresh/accepted.json'),'delivered_batch':load('delivery-batch/accepted.json'),'source':load('source-replay-records.json'),'controlled':load('author-check-rerun/regression-records.json')[2:66]}
results={};probes=[]
refs={'fresh':'fresh-records.json','batch':'runner-batch.json','delivered_fresh':'delivery-fresh/accepted.json','delivered_batch':'delivery-batch/accepted.json','source':'source-replay-records.json','controlled':'author-check-rerun/regression-records.json'}
for stage,rs in sets.items():
 rows=[visible(r) for r in rs];groups=collections.defaultdict(list)
 for x in rows:groups[(x['template'],x['kind'])].append(x)
 results[stage]={'count':len(rs),'bank_counts':dict(collections.Counter(x['kind'] for x in rows)),'sole_copy_correct':sum(x['sole_match_correct'] for x in rows),'unique_shortest_correct':sum(x['unique_shortest'] for x in rows),'rows':rows,'conditional_groups':[{'template':t,'kind':k,'count':len(xs),'sole_copy_correct':sum(x['sole_match_correct'] for x in xs),'shortest_first_correct':sum(x['shortest_first'] for x in xs),'positions':dict(collections.Counter(x['position'] for x in xs)),'linear_ranks':dict(collections.Counter(x['linear_target_rank'] for x in xs))} for (t,k),xs in groups.items()]}
 if stage in ('fresh','batch','delivered_batch','controlled'):
  mixed=[x for x in rows if x['kind']=='mixed'];scopes=[('all mixed banks',mixed,'other_recognizable_subgroup')]+[(t,xs,'within_template') for (t,k),xs in groups.items() if k=='mixed']
  for name,xs,scope in scopes:
   if not xs:continue
   successes=sum(x['sole_match_correct'] for x in xs)
   probes.append({'cue':'sole positive numeral uniquely appears in one option','subgroup':stage+': '+name,'scope':scope,'strategy':'Copy the sole positive numeral; choose its unique matching equation without reading operators.','correct':successes,'total':len(xs),'baseline':0.2,'disposition':'defect','conclusion':'Uniform guessing among five equations succeeds at 0.2. Numeral copying is perfect here and never inspects sign or population factors; source structural banks repeat the capacity and do require those distinctions.','sample_refs':[refs[stage],'shortcut-stage-results.json']})
  probes.append({'cue':'unique shortest equation','subgroup':stage,'scope':'overall','strategy':'Choose a uniquely shortest option; abstain on ties.','correct':sum(x['unique_shortest'] for x in rows),'total':len(rows),'baseline':0.2,'disposition':'not_predictive','conclusion':'Baseline is uniform five-option guessing. The earlier unique-shortest defect is absent; this does not waive the distinct numeral-copy defect.','sample_refs':[refs[stage],'shortcut-stage-results.json']})
 # Do not infer perfect template-position cues from one observation; controlled fixed-bank role cases disprove fixed target rank.
 if stage=='controlled':
  for (template,kind),xs in groups.items():
   for strategy in ['minimum_linear','middle_linear','maximum_linear']:
    probes.append({'cue':'numeric rank within positive linear alternatives','subgroup':template+' / '+kind,'scope':'within_template','strategy':strategy,'correct':sum(x[strategy] for x in xs),'total':len(xs),'baseline':1/xs[0]['linear_count'],'disposition':'not_predictive','conclusion':'Comparison baseline is uniform selection after recognizing the positive linear form: 1/3 mixed, 1/5 all-capacity. Every eligible equilibrium role is reassigned while the bank is held fixed; no fixed rank predicts the target.','sample_refs':[refs[stage],'shortcut-stage-results.json']})
save('shortcut-stage-results.json',results);save('shortcut-probes.json',probes)
# Exact learner-selection rules in easy-only hypothetical candidate pool, draw and exclusions.
accepted=sets['delivered_batch'];sequence=[];remaining=list(range(len(accepted)))
for step in range(len(accepted)):
 seed=f'independent-review/947/{step}';digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53);index=remaining[min(int(u*len(remaining)),len(remaining)-1)];sequence.append({'seed':seed,'eligible_indices_before':remaining.copy(),'selected_index':index,'question_id':accepted[index]['question'][':question/id'],'sole_numeral_correct':visible(accepted[index])['sole_match_correct']});remaining.remove(index)
save('selection-results.json',{'source':'engine/rust/question_selection.rs select and seen_before_task; inspected current code','captured_basis':5380,'method':'Faithful SHA256 within-band selection over accepted easy candidates, synthetic ordered indices, positive easy weight renormalized to1; prior task/current prefix exclusions remove chosen members. No actual database identities or learner sequence claimed.','sequences':sequence,'unconfigured_policy':'select picks smallest entity ID; any of five generated candidates is numeral-copy vulnerable.','captured_inventory':'14 original questions (13 easy,1 unrated),10 generated moderate/hard. With mixed-band weights original questions/other bands can also be drawn; they do not repair the five-member generated batch.','result':'All five successive fresh selections retain the numeral-copy cue. Normal easy construction has no rejection loop. Shared delivery retained fresh24/24 and exact batch5/5; cue survives both filters.','limits':['Live policy weights, actual new entity IDs and learner histories unavailable. All possible selected members of this batch have the defect, so ordering cannot remove it.','Captured inventory may change after basis5380. No publication or database writes.']})
# Actual UI choice order: read rendered controls rather than assuming generator order.
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.radios=[]
 def handle_starttag(self,t,attrs):
  d=dict(attrs)
  if t=='input' and d.get('type')=='radio':self.radios.append(d)
ui=[]
for group,n in [('render-batch',5),('render-pairs',6)]:
 for index in range(n):
  p=Parser();p.feed((E/group/f'question-{index+1:03}.html').read_text());assert len(p.radios)==5
  record=load('runner-batch.json' if group=='render-batch' else 'counterfactual-records.json')[index]
  ui.append({'file':f'{group}/question-{index+1:03}.html','radio_choice_ids':[x['value'] for x in p.radios],'correct_ui_position':next(i for i,x in enumerate(p.radios) if x['value']==key(record))})
save('ui-order-results.json',{'method':'Read actual unmodified UI HTML. learning.js choiceOrder hashes itemId,field.id,choice.id; raw generator order is not delivered order. Numeral-copy cue is order independent.','cases':ui,'batch_correct_ui_positions':dict(collections.Counter(x['correct_ui_position'] for x in ui[:5]))})
# Capture exact rerunnable failures and successes with exit codes.
commands=[([P,'-B','prior-reproduce_shortcut.py','--input','prior-boundary-records.json','--index','0','--output','prior-failure-shortcut.json'],1),([P,'-B','author_repair_check.py','--records','prior-boundary-records.json','--output','old-failure.json'],1),([P,'-B','prior-reproduce_shortcut.py','--input','boundary-records.json','--index','0','--output','current-shortest-minimal.json'],0),([P,'-B','reproduce_number_match.py','--output','number-match-results.json'],1),([P,'-B','reproduce_number_match.py','--input','delivery-batch/accepted.json','--output','number-match-delivered-batch.json'],1)]
execution=[]
for cmd,expected in commands:
 p=subprocess.run(cmd,cwd=E,capture_output=True,text=True);assert p.returncode==expected;execution.append({'command':cmd,'expected_exit':expected,'actual_exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
save('execution.json',execution)
(E/'session-state.md').write_text('All native grader checks pass:38 correct accepted,152 wrong rejected. Delivery accepts batch5/5 and fresh24/24. New mixed-bank numeral-copy cue demonstrated on minimal seed3/cap60 and batch5/5 before/after filtering; strict reproduction saved. Source structural banks require sign/factor discrimination because capacities repeat. Current distinct-capacity rule rejects that eligible role. Rendering batch and relevant/irrelevant pairs inspected; final new-cue fixture rendering pending. All ten stored generated moderate/hard records reproduce, no generated easy inventory affected. Next: final variation/report and unchanged-package verification.\n')
print(json.dumps({k:{x:v[x] for x in ['count','bank_counts','sole_copy_correct','unique_shortest_correct']} for k,v in results.items()}))
