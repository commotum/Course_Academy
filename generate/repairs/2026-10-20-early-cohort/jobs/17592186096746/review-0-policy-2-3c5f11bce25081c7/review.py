import sys,json,re,hashlib,pathlib,subprocess,shutil,collections,platform
from fractions import Fraction as F
E=pathlib.Path(__file__).resolve().parent; J=E.parent; R=pathlib.Path('/home/jake/Developer/Course_Academy'); W=J/'workspace'; PY=R/'.venv/bin/python'
sys.dont_write_bytecode=True;sys.path.insert(0,str(W));import generator as g

def save(n,x): (E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False))
def package_hashes():return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in W.iterdir() if p.is_file()}
if __name__=='__main__':save('package-before.json',package_hashes())
def scalar(s):
 s=s.strip().replace(' ','');s=re.sub(r'\\frac\{(\d+)\}\{(\d+)\}',r'(\1/\2)',s)
 if s.startswith('-('):return -F(s[2:-1])
 if s.startswith('('):s=s[1:-1]
 return F(s)
def matrix(tex):
 m=re.search(r'\\begin\{(?:bmatrix|array)\}(?:\{[^}]+\})?(.*?)\\end\{(?:bmatrix|array)\}',tex,re.S)
 return [[scalar(v) for v in row.split('&')] for row in re.split(r'\\\\',m[1])]
def coeff(expr):
 expr=expr.replace(' ','');vals=[F(0)]*4
 for m in re.finditer(r'([+-]?)(\d+(?:/\d+)?)?([xyz]?)',expr):
  if not m[0]:continue
  sign=-1 if m[1]=='-' else 1;v=F(m[2] or '1')*sign;vals['xyz'.index(m[3]) if m[3] else 3]+=v
 return vals
def equations(tex):
 body=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',tex,re.S)[1]
 rows=[]
 for s in re.split(r'\\\\',body):
  left,right=s.replace('&','').split('=');v=coeff(left);v[3]=scalar(right);rows.append(v)
 return rows
def rref(a):
 a=[r[:] for r in a];j=0
 for c in range(len(a[0])):
  i=next((i for i in range(j,len(a)) if a[i][c]),None)
  if i is None:continue
  a[j],a[i]=a[i],a[j];a[j]=[v/a[j][c] for v in a[j]]
  for k in range(len(a)):
   if k!=j:
    fac=a[k][c];a[k]=[x-fac*y for x,y in zip(a[k],a[j])]
  j+=1
  if j==len(a):break
 return a

def vector_parts(s):
 # Source captures double escape some TeX and Unicode notation.
 s=s.replace('\\\\begin','\\begin').replace('\\\\end','\\end')
 body=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',s,re.S)[1]
 return [coeff(v) for v in re.split(r'\\{2,}',body)]
def good_solution(v,rows):
 # Affine plane equality: substitution identity plus two independent direction vectors.
 for row in rows:
  if any(sum(row[j]*v[j][c] for j in range(3))!=(row[3] if c==3 else 0) for c in range(4)):return False
 directions=[[v[i][j] for j in (1,2)] for i in range(3)]
 return any(directions[i][0]*directions[j][1]-directions[i][1]*directions[j][0] for i in range(3) for j in range(i))
def analyze(rec):
 q=rec['question'];rows=equations(q[':question/problem']);rf=rref(rows);f=q[':question/answer-fields'][0];correct=f[':answer-field/correct'][1];goods=[]
 easy=q.get(':question/difficulty')==':question.difficulty/easy'
 for a in f[':answer-field/choices']:
  v=a[':answer/value'];valid=False
  if v!='No solution':valid=matrix(v)==rf if easy else good_solution(vector_parts(v),rows)
  if valid:goods.append(a[':answer/id'])
 errors=[]
 if goods!=[correct]:errors.append({'valid_ids':goods,'stored':correct})
 # Parse actual displayed intermediate matrices; verify row equivalence and final answer.
 mats=re.findall(r'\\begin\{array\}\{[^}]+\}.*?\\end\{array\}',q[':question/worked-solution'],re.S)
 for t in mats:
  if rref(matrix(t))!=rf:errors.append('non-equivalent solution matrix')
 if mats and matrix(mats[-1])!=rf:errors.append('final matrix not RREF')
 return {'id':q[':question/id'],'valid_choices':len(goods),'errors':errors,'rref':[[str(v) for v in r] for r in rf]}

if __name__=='__main__':
 batch=json.loads((J/'samples.json').read_text());save('batch.json',batch)
 easy=g.generate('easy',96,913771);moderate=g.generate('moderate',32,557291);replay=g.replay()
 save('fresh-easy.json',easy);save('fresh-moderate.json',moderate);save('source-replay.json',replay)
 math=[analyze(r) for r in batch+easy+moderate+replay];save('math-results.json',{'command':f'{PY} {E}/review.py','tested':len(math),'failures':[x for x in math if x['errors']],'results':math})
 # Full mathematical bank comparison permits normalization of capture artifacts and algebraic order.
 src=json.loads((J/'source/source.json').read_text());qs=src['material']['kp'][':knowledge-point/questions'];mapped={r['generation']['parameters']['source_id']:r for r in replay};rep=[]
 def normbank(s,easy):
  s=s.replace('\\\\begin','\\begin').replace('\\\\end','\\end').replace('\\\\\\\\','\\\\')
  if s=='No solution':return s
  return str(matrix(s) if easy else vector_parts(s))
 for q in qs:
  qid=q[':question/id'];r=mapped.get(qid);item={'source_id':qid,'reproduced':r is not None}
  if r:
   f=q[':question/answer-fields'][0];out=r['question'];is_easy=q.get(':question/difficulty',{}).get(':db/ident')==':question.difficulty/easy'
   item.update(prompt_math_equal=equations(q[':question/problem'])==equations(out[':question/problem']),bank_equal=[normbank(a[':answer/value'],is_easy) for a in f[':answer-field/choices']]==[normbank(a[':answer/value'],is_easy) for a in out[':question/answer-fields'][0][':answer-field/choices']],bank_size=len(f[':answer-field/choices']))
  rep.append(item)
 save('source-replay-results.json',{'results':rep,'missing':[q[':question/id'] for q in qs if q[':question/id'] not in mapped],'corrections':'Source 693512da has erroneous +16 row annotation; no replay supplied to verify correction. q74534 key/solution inferred because absent.'})
 # Controlled same-bank relevant and irrelevant changes, including a magnitudes-only change.
 base=easy[0];p=base['generation']['parameters'];sb=base['generation']['sign_bank'];ci=base['generation']['correct_index']
 other=next(i for i in range(5) if i!=ci)
 pairs=[{'name':'base','record':base},{'name':'relevant-sign-assignment','record':g.authored(p,sb,other)}]
 p2=dict(p);p2['scales']=[s*2 for s in p['scales']];pairs.append({'name':'irrelevant-row-scaling','record':g.authored(p2,sb,ci)})
 p3=dict(p);p3['b']=abs(p['b'])+1;pairs.append({'name':'relevant-magnitude','record':g.authored(p3,sb,ci)})
 save('counterfactuals.json',pairs);save('counterfactual-records.json',[x['record'] for x in pairs]);save('counterfactual-math.json',[dict(name=x['name'],result=analyze(x['record'])) for x in pairs])
 # Grading every choice is tractable in one native invocation, and exercises keys and distractors.
 cases=[]
 for name,rs in [('batch',batch),('fresh',easy[:8]+moderate[:8]),('replay',replay),('counterfactual',[x['record'] for x in pairs])]:
  for i,r in enumerate(rs):
   f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
   cases.append({'label':f'{name}-{i}','record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'independently computed unique solution / distractor'} for a in f[':answer-field/choices']]})
 save('grader-cases.json',cases)
 # Packaging tests: relocation and deterministic CLI; output must remain external.
 rel=E/'relocated';rel.mkdir(exist_ok=True)
 for n in json.loads((W/'package.json').read_text())['files']:shutil.copyfile(W/n,rel/n)
 def run(args,cwd):return subprocess.run([str(PY),*args],cwd=cwd,text=True,capture_output=True)
 a=run([str(W/'generator.py'),'--seed','913771','--count','3'],'/tmp');b=run([str(rel/'generator.py'),'--seed','913771','--count','3'],str(E))
 checks={'python':platform.python_version(),'dependencies':json.loads((W/'package.json').read_text())['dependencies'],'relocation_equal':a.returncode==b.returncode==0 and a.stdout==b.stdout,'deterministic':g.generate('easy',3,913771)==easy[:3],'zero_count':g.generate('easy',0,1)==[],'boundary_parameters':[r['generation']['parameters'] for r in easy if abs(r['generation']['parameters']['b']) in (1,10) or abs(r['generation']['parameters']['d']) in (1,18)],'rejections':sum(r['generation']['rejections'] for r in easy+moderate)}
 for label,args in [('negative',['--count','-1']),('hard',['--difficulty','hard'])]:
  x=run([str(W/'generator.py'),*args],str(E));checks[label]={'returncode':x.returncode,'stderr':x.stderr}
 save('packaging.json',checks)
 # Stored inventory: generated records only; do not relabel instructional questions.
 inv=json.loads((J/'source/inventory.json').read_text());save('inventory-summary.json',{'basis':inv['basis'],'questions':[{'id':q[':question/id'],'entity':q[':db/id'],'keys':list(q),'generation_metadata':{k:v for k,v in q.items() if 'generation' in k or 'generator' in k}} for q in inv['questions']]})
 (E/'session-state.md').write_text('Completed source analysis, fresh samples, source replay comparison, independent exact arithmetic, counterfactual records, and packaging checks. Run grader-cases.json through native harness, delivery filters on batch/fresh, and actual UI rendering next. Source replay omits 693512da. Sign-only bank restriction under investigation. Package untouched.\n')
 print(json.dumps({'math_tested':len(math),'math_failures':sum(bool(x['errors']) for x in math),'source_replay':rep,'packaging':{k:v for k,v in checks.items() if k!='boundary_parameters'}},indent=2))
