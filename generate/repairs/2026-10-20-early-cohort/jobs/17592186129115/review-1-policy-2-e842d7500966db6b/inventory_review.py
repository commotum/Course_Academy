import sys,pathlib,json,re
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(E.parent/'workspace'));import generator as g
sys.path.insert(0,'/home/jake/Developer/Course_Academy');from scripts.generator_publish import stable_identities
s=json.load(open(E.parent/'source/source.json'));inv=json.load(open(E.parent/'source/inventory.json'));ids={q[':question/id'] for q in s['material']['kp'][':knowledge-point/questions']}
def coords(t):return [[int(i)-1,int(j)-1] for i,j in re.findall(r'a\}?_\{([1-4])([1-4])\}',t)]
def matrix(t):return [[int(v.strip()) for v in row.split('&')] for row in re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',t,re.S)[1].split('\\\\')]
rows=[];attempts=[]
for q in inv['questions']:
 if q[':question/id'] in ids:continue
 p={'matrix':matrix(q[':question/problem']),'bank':[coords(a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices']]}
 r=g.generate('moderate',0,parameters=p);r['question']=stable_identities(r['question'],g.KP_UUID);attempts.append(r)
 lex=sorted(range(5),key=lambda i:p['bank'][i])[2];f=q[':question/answer-fields'][0];correct=f[':answer-field/correct'];cid=correct.get(':answer/id') if isinstance(correct,dict) else correct[1];ci=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==cid)
 rows.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'reconstructed_id':r['question'][':question/id'],'identity_matches':r['question'][':question/id']==q[':question/id'],'matrix_blind_median_success':lex==ci,'historical_generation_metadata_present':any('generation' in k or 'generator' in k for k in q),'captured_optimization_wording':'fewest' in q[':question/problem'].lower()})
assert not any(x['identity_matches'] for x in rows)
for n,x in [('inventory-attempt-records.json',attempts),('inventory-reproduction.json',{'basis':inv['basis'],'source_originals_excluded':len(ids),'non_source_candidates_inspected':rows,'new_defect':'Current keyed lexicographic-neighborhood bank construction. No matching complete generated identity/metadata for captured non-source candidates demonstrated. Historical optimization wording is a prior fixed defect, not relabeled as a fresh finding.','limits':'All 20 captured prompts/banks inspected; five non-source candidates attempted. No historical generation metadata. Empty affected list means no certified reproduction, not verified absence of affected stored questions. No claim about later changing inventory.'}),('generated-records.json',[]),('affected-inventory.json',{'affected_questions':[]})]:
 (E/n).write_text(json.dumps(x,indent=2)+'\n')
print(json.dumps({'candidates':len(rows),'certified_matches':sum(x['identity_matches'] for x in rows),'median_successes':sum(x['matrix_blind_median_success'] for x in rows)}))
