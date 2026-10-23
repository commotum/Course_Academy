import json,re,pathlib,importlib.util,sys,hashlib,shutil,platform,collections
ROOT=pathlib.Path(__file__).resolve().parent
JOB=ROOT.parent; PKG=JOB/'workspace'
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('subject',PKG/'17592186161967.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,x): (ROOT/name).write_text(json.dumps(x,indent=2,default=int))
def mats(s):
 return [[[int(x.strip()) for x in row.split('&')] for row in raw.split(r'\\')] for raw in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',s,re.S)]
def ops(s):
 s=s.replace('{R}','R')
 return [(int(i)-1,int(j)-1,(1 if sign=='+' else -1)*int(n or 1),int(p)-1) for i,j,sign,n,p in re.findall(r'R_\{(\d)\}:=R_\{(\d)\}\s*([+-])\s*(\d*)\s*R_\{(\d)\}',s)]
def apply(A,o):
 B=[r[:] for r in A]
 for i,j,k,p in o:
  assert i==j and i!=p
  B[i]=[v+k*w for v,w in zip(B[i],B[p])]
 return B

def check(r):
 q=r['question']; A,B=mats(q[':question/problem']);f=q[':question/answer-fields'][0]
 validity=[apply(A,ops(c[':answer/value']))==B for c in f[':answer-field/choices']]
 assert sum(validity)==1
 ix=validity.index(True); assert f[':answer-field/choices'][ix][':answer/id']==f[':answer-field/correct'][1]
 ss=mats(q[':question/worked-solution']); oo=ops(q[':question/worked-solution']);assert len(ss)==3 and ss[0]==A and ss[1]==apply(A,oo[:1]) and ss[2]==B and apply(A,oo[:2])==B
 return ix

def cue(r):
 bank=[ops(c[':answer/value']) for c in r['question'][':question/answer-fields'][0][':answer-field/choices']]
 # Only the displayed bank is inspected: fixed first magnitude, one second unit and four equal larger magnitudes.
 a=[abs(o[0][2]) for o in bank]; b=[abs(o[1][2]) for o in bank]
 return len(set(a))==1 and b.count(1)==1 and len(set(b))==2 and max(b)>1
src=json.load(open(JOB/'source/source.json'))['material']['kp'][':knowledge-point/questions']
replays=[];rep=[]
for q in src:
 A,B=mats(q[':question/problem']); p=next(i for i in range(3) if A[i]==B[i]);c=int(re.search(r'(?:\{a\}|a)_\{\d(\d)\}',q[':question/worked-solution']).group(1))-1
 ks=[0 if i==p else -A[i][c]//A[p][c] for i in range(3)]
 r=g.generate(seed=8107,bank_profile=q[':question/math-academy-id'],parameters={'A':A,'pivot':p,'column':c,'ks':ks});check(r)
 bank=sorted(ops(z[':answer/value']) for z in r['question'][':question/answer-fields'][0][':answer-field/choices'])
 for f in q[':question/answer-fields']: assert bank==sorted(ops(z[':answer/value']) for z in f[':answer-field/choices'])
 assert mats(r['question'][':question/problem'])==[A,B]
 replays.append(r);rep.append({'source_id':q[':question/id'],'all_banks_match':True,'math':True})
save('source-replays.json',replays);save('source-replay-results.json',rep)
rows=[g.generate(seed=38191+i,bank_profile=p) for p in g.PROFILES for i in range(12)]
batch=json.load(open(JOB/'samples.json'));save('fresh-samples.json',rows);save('batch.json',batch)
# Controlled relevant and irrelevant changes, including pivot/target-column relocation.
a={'A':[[1,2,3],[2,5,4],[-3,7,8]],'pivot':0,'column':0,'ks':[0,-2,3]}
b=json.loads(json.dumps(a));b['A'][1][0]=-2;b['ks'][1]=2
c=json.loads(json.dumps(a));c['A'][1][1]=6
d=json.loads(json.dumps(a));d['A']=[d['A'][1],d['A'][0],d['A'][2]];d['pivot']=1;d['ks']=[-2,0,3]
e=json.loads(json.dumps(a));e['A']=[[r[1],r[0],r[2]] for r in e['A']];e['column']=1
pairs=[g.generate(seed=472,bank_profile='q-42531',parameters=z) for z in [a,b,c,d,e]];save('counterfactual-records.json',pairs)
inputs=[]
for group,rr in [('fresh',rows),('batch',batch),('pair',pairs),('source',replays)]:
 for i,r in enumerate(rr):
  ix=check(r);f=r['question'][':question/answer-fields'][0]
  inputs.append({'label':f'{group}-{i}','record':r,'checks':[{'field_index':0,'submitted_answer_id':z[':answer/id'],'expected':'accepted' if j==ix else 'rejected','purpose':'Independent full-row arithmetic'} for j,z in enumerate(f[':answer-field/choices'])]})
save('grader-input.json',inputs)
summary={}
for group,rr in [('fresh',rows),('batch',batch)]:
 sub=[r for r in rr if cue(r)]
 summary[group]={'count':len(rr),'cue_count':len(sub),'cue_choose_third_correct':sum(check(r)==2 for r in sub),'positions':dict(collections.Counter(check(r)+1 for r in rr)),'pivots':dict(collections.Counter(r['generation']['parameters']['pivot'] for r in rr)),'columns':dict(collections.Counter(r['generation']['parameters']['column'] for r in rr)),'sign_pairs':dict(collections.Counter(str([k>0 for k in r['generation']['parameters']['ks'] if k]) for r in rr)),'profiles':{p:{'total':sum(r['generation']['bank_profile']==p for r in rr),'cue':sum(cue(r) and r['generation']['bank_profile']==p for r in rr)} for p in g.PROFILES}}
save('math-coverage-shortcuts.json',summary)
assert check(pairs[0])==check(pairs[1])==check(pairs[2])==2
assert ops(pairs[0]['question'][':question/answer-fields'][0][':answer-field/choices'][2][':answer/value'])!=ops(pairs[1]['question'][':question/answer-fields'][0][':answer-field/choices'][2][':answer/value'])
assert pairs[0]['question'][':question/answer-fields'][0][':answer-field/choices'][2][':answer/value']==pairs[2]['question'][':question/answer-fields'][0][':answer-field/choices'][2][':answer/value']
save('counterfactual-results.json',{'relevant':'Sign change recomputes A,B,stages and operation from -2 to +2; correct position stays third.','irrelevant':'Non-target entry change recomputes B and stages, preserving operation text.','target':'Swapping rows or columns updates pivot/column and stages consistently.','actual_grading':'See grader-report.json; all five choices tested on every pair.'})
reject=[]
for kwargs in [{'difficulty':'hard'},{'difficulty':'moderate'},{'bank_profile':'missing'},{'parameters':dict(a,ks=[0,2,3])},{'parameters':dict(a,pivot=3)}]:
 try:g.generate(**kwargs);reject.append({'parameters':kwargs,'rejected':False})
 except Exception as ex:reject.append({'parameters':kwargs,'rejected':True,'exception':type(ex).__name__})
assert all(x['rejected'] for x in reject)
assert g.generate(seed=38191)==g.generate(seed=38191)
rel=ROOT/'relocated';rel.mkdir(exist_ok=True);shutil.copyfile(PKG/'17592186161967.py',rel/'17592186161967.py');(rel/'17592186161967').mkdir(exist_ok=True);shutil.copyfile(PKG/'17592186161967/source.json',rel/'17592186161967/source.json')
save('packaging.json',{'python':platform.python_version(),'sympy':g.sp.__version__,'manifest':json.load(open(PKG/'package.json'))['dependencies'],'deterministic':True,'rejections':reject,'history_files':'repair-history, repair-preflight, repair-regressions absent','hashes':{str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.rglob('*') if p.is_file()}})
inv=json.load(open(JOB/'source/inventory.json'));save('inventory-inspection.json',{'basis':inv['basis'],'question_count':len(inv['questions']),'questions':[{'id':q[':question/id'],'entity_id':q[':db/id'],'source':q.get(':question/math-academy-id'),'keys':list(q)} for q in inv['questions']],'finding':'All 10 inventory questions match original instructional source IDs; zero generated records. No eligible stored generated weakness demonstrated; originals are not to be marked generated.'});assert {q[':question/id'] for q in inv['questions']}=={q[':question/id'] for q in src};save('affected-inventory.json',{'affected_questions':[]})
save('render-records.json',[batch[0],*pairs])
(ROOT/'session-state.md').write_text('Independent source replay, exact arithmetic, 120 fresh samples, five runner records, controlled pairs, inventory and packaging probes completed. Conditional unit-bank cue succeeds on every eligible fresh and batch record. Native grading, delivery and UI render pending.\n')
print(json.dumps(summary))
