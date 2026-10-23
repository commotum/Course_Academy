# Reuse only independent parsers; avoid rerunning the original audit.
import ast,pathlib,json,collections,hashlib
root=pathlib.Path(__file__).resolve().parent
module=ast.parse((root/'audit.py').read_text()); nodes=[n for n in module.body if isinstance(n,(ast.Import,ast.ImportFrom)) or isinstance(n,ast.FunctionDef) and n.name in ['ops','mats','apply','check','cue']];exec(compile(ast.Module(body=nodes,type_ignores=[]),'audit-helpers','exec'))
def scan(rr):
 out=[]
 for r in rr:
  if not cue(r):continue
  f=r['question'][':question/answer-fields'][0];oo=[ops(c[':answer/value']) for c in f[':answer-field/choices']];first=collections.Counter(o[0][2] for o in oo).most_common(1)[0][0]; unit=next(o for o in oo if abs(o[1][2])==1); mag=max(abs(o[1][2]) for o in oo); predicted=(first,unit[1][2]*mag)
  idx=next(i for i,o in enumerate(oo) if (o[0][2],o[1][2])==predicted);actual=check(r)
  out.append({'question_id':r['question'][':question/id'],'profile':r['generation']['bank_profile'],'first_inferred':first,'first_correct':first==oo[actual][0][2],'matrix_free_choice_correct':idx==actual,'predicted_choice_id':f[':answer-field/choices'][idx][':answer/id']})
 return out
result={}
for name,file in [('fresh','fresh-samples.json'),('batch','batch.json'),('delivered_fresh','delivery-fresh/accepted.json'),('delivered_batch','delivery-batch/accepted.json')]:
 rr=json.load(open(file));sub=scan(rr);result[name]={'records':len(rr),'cue_count':len(sub),'first_correct':sum(x['first_correct'] for x in sub),'matrix_free_correct':sum(x['matrix_free_choice_correct'] for x in sub),'details':sub}
result['position_probe_correction']='Original authored-position probe is NOT a delivered shortcut: ui/learning.js:690-701 hashes choice IDs with item/field IDs. Rendering confirms changed order. Final findings use order-independent coefficient frequencies only.'
(root/'shortcut-followup.json').write_text(json.dumps(result,indent=2))
# Native grading cases for the strictly matrix-free guess, plus bypass first-operation strategy.
cases=[]
for r in json.load(open('fresh-samples.json'))+json.load(open('batch.json')):
 if not cue(r):continue
 f=r['question'][':question/answer-fields'][0];entry=scan([r])[0];A,B=mats(r['question'][':question/problem']);p=next(i for i in range(3) if A[i]==B[i]);targets=[i for i in range(3) if i!=p];col=next(i for i in range(3) if A[p][i] and B[targets[0]][i]==B[targets[1]][i]==0)
 second=-A[targets[1]][col]//A[p][col]
 idx=next(i for i,c in enumerate(f[':answer-field/choices']) if [o[2] for o in ops(c[':answer/value'])]==[entry['first_inferred'],second])
 cases.append({'label':'order-independent shortcut '+r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':entry['predicted_choice_id'],'expected':'accepted' if entry['matrix_free_choice_correct'] else 'rejected','purpose':'No matrix inspected: modal first coefficient and unit-distractor sign'},{'submitted_answer_id':f[':answer-field/choices'][idx][':answer/id'],'expected':'accepted','purpose':'First coefficient from bank frequency; only second operation computed'}]})
(root/'shortcut-grader-input.json').write_text(json.dumps(cases,indent=2))
# Faithful question_selection select(): all records easy, positive easy band, no learner history supplied.
sel={}
for name,file in [('fresh','delivery-fresh/accepted.json'),('batch','delivery-batch/accepted.json')]:
 rr=json.load(open(file)); picks=[]
 for i in range(40):
  seed=f'independent-review-17592186161967-{i}'; digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53);index=int(u*len(rr));picks.append({'seed':seed,'candidate_rank':index,'question_id':rr[index]['question'][':question/id'],'unit_cue':cue(rr[index])})
 sel[name]={'eligible_count':len(rr),'cue_candidates':sum(cue(r) for r in rr),'selection_draws':picks,'selected_cue_count':sum(p['unit_cue'] for p in picks)}
sel['basis']=5580;sel['rules']='Candidates deduplicated, easy band selected for any positive easy weight; uniform within band via native SHA256 offsets. Prior-seen candidates are removed by caller; absent learner history modeled as empty. Actual future entity ranking is unknown; candidate file order is a representative ranking. Every candidate has positive selection probability regardless of ordering. No policy weights or live learner history captured; no claim about a particular live task.'
(root/'selection.json').write_text(json.dumps(sel,indent=2))
print({k:{a:b for a,b in v.items() if a!='details'} for k,v in result.items() if isinstance(v,dict)})
