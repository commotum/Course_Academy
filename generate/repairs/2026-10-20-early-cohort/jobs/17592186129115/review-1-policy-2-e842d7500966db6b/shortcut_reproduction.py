import sys,json,pathlib,re,itertools,copy,math
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(E.parent/'workspace'));import generator as g

def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
def parse(r):
 q=r['question'];body=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',q[':question/problem'],re.S)[1];m=[[int(v.strip()) for v in row.split('&')] for row in body.split('\\\\')]
 f=q[':question/answer-fields'][0];b=[[[int(i)-1,int(j)-1] for i,j in re.findall(r'a\}?_\{([1-4])([1-4])\}',a[':answer/value'])] for a in f[':answer-field/choices']]
 return m,b,f

def ref(m,b):
 a=copy.deepcopy(m)
 for i,j in b:a[i][j]=0
 zero=False;prev=-1
 for row in a:
  cols=[j for j,v in enumerate(row) if v]
  if not cols:zero=True
  elif zero or cols[0]<=prev:return False
  else:prev=cols[0]
 return True
rs=json.load(open(E/'delivery-cue-control/accepted.json'));checks=[];trials=[]
for r in rs:
 m,b,f=parse(r);i=sorted(range(5),key=lambda i:b[i])[2];good=[j for j,bb in enumerate(b) if ref(m,bb)];assert len(good)==1
 hit=i==good[0];trials.append({'seed':r['generation']['seed'],'question_id':r['question'][':question/id'],'strategy_index':i,'valid_index':good[0],'success':hit,'has_zero_row':any(not any(row) for row in m)})
 checks.append({'label':'matrix-blind lexicographic median '+str(r['generation']['seed']),'record':r,'checks':[{'field_index':0,'submitted_answer_id':f[':answer-field/choices'][i][':answer/id'],'expected':'accepted' if hit else 'rejected','purpose':'matrix-blind coordinate-order strategy; oracle uses independently parsed row-echelon calculation'}]})
# Exact single-case witness in the actual runner batch, independently regenerated.
r=json.load(open(E/'batch-records.json'))[1];assert g.generate('moderate',431440325)==r
m,b,f=parse(r);pred=sorted(range(5),key=lambda i:b[i])[2];assert ref(m,b[pred]);save('shortcut-minimal-records.json',[r])
# Exact construction law for this instance: enough wrong operations on both sides.
cells=list(itertools.product(range(4),repeat=2));correct=b[pred];size=len(correct);zc=sum(m[i][j]==0 for i,j in correct)
wrong=[list(map(list,x)) for x in itertools.combinations(cells,size) if sum(m[i][j]==0 for i,j in x)==zc and not ref(m,x)]
lo=[x for x in wrong if x<correct][-12:];hi=[x for x in wrong if x>correct][:12];assert min(len(lo),len(hi))>=4
law={'seed':431440325,'matrix_blind_strategy':'Sort each displayed coordinate set in row-major coordinate order, sort the five sets lexicographically, select the third. Ignore the matrix and displayed radio position.','correct_option':f[':answer-field/choices'][pred][':answer/value'],'sorted_bank':[f[':answer-field/choices'][i][':answer/value'] for i in sorted(range(5),key=lambda i:b[i])],'lower_pool':len(lo),'upper_pool':len(hi),'construction':'Each distractor chooses lower versus upper pool with probability 1/2. Both sides remain nonempty through all four draws. Key is the median exactly when two distractors are below and two above.','exact_median_probability':math.comb(4,2)/16,'uniform_five_choice_baseline':.2,'limits':'Statistical leakage, not a universal answer or a guarantee for every matrix. Exact 3/8 construction statement is conditional on both side pools initially containing at least four distractors.'}
save('shortcut-construction-law.json',law);save('shortcut-trials.json',trials)
base=[x for x in json.load(open(E/'grader-input.json')) if not x['label'].startswith('matrix-blind lexicographic median ')];save('grader-input.json',base+checks)
print(json.dumps({'control_trials':len(trials),'correct':sum(x['success'] for x in trials),'minimal_case':law}))
