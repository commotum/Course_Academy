import json,re,sys,collections
from pathlib import Path
sys.path.insert(0,'/home/jake/Developer/Course_Academy')
from bs4 import BeautifulSoup
ROOT=Path('/home/jake/Developer/Course_Academy');A=ROOT/'reference/edb-math/audits/2026-10-30-latex-quality/topic-17592186048780';D=ROOT/'reference/edb-math/repairs/2026-10-30-vector-topic-latex/topic-17592186048780'
E=json.loads((A/'entities.json').read_text());candidates=json.loads((A/'findings.json').read_text())['findings'][1]['fields'];qids={f['entity']for f in candidates if f['attribute'].startswith(':question/')};Q={i:E[str(i)]for i in qids}
def norm(s):return re.sub(r'\s+','',re.sub(r'!\[[^\]]*\]\([^)]*\)','',s))
lookup=collections.defaultdict(list);byid=collections.defaultdict(list)
for base in [ROOT/'reference/mathacademy/question-capture']:
 for p in base.glob('*/*.json'):
  if not re.match(r'(?:q-\d+-(?:after|before)|history-q-\d+|example-\d+)\.json$',p.name):continue
  try:d=json.loads(p.read_text())
  except Exception:continue
  if not isinstance(d,dict)or 'problem'not in d:continue
  mid=re.search(r'(?:q-|example-)(\d+)',p.name).group(1);byid[('e-'if p.name.startswith('example')else'q-')+mid].append((p,d));lookup[norm(d['problem'])].append((p,d))

for p in (ROOT/'reference/mathacademy/capture').glob('*/*/content.json'):
 with p.open() as sf: head=sf.read(4096)
 if not re.search(r'"topic_id"\s*:\s*"?1106(?:"|,)',head):continue
 try:doc=json.loads(p.read_text())
 except Exception:continue
 if str(doc.get('topic_id'))!='1106':continue
 for d in doc.get('questions',[])+doc.get('canonical_examples',[]):
  if 'problem'not in d:continue
  mid=d.get('math_academy_id','');byid[mid].append((p,d));lookup[norm(d['problem'])].append((p,d))

proofs={};missing=[]
for i,q in Q.items():
 matches=lookup.get(norm(q[':question/problem']),[])or byid.get(q.get(':question/math-academy-id'),[])
 if not matches:missing.append(i);continue
 matches.sort(key=lambda x: (norm(x[1].get('worked_solution',''))==norm(q.get(':question/worked-solution','')),len(x[1].get('html',''))),reverse=True)
 p,d=matches[0];s=BeautifulSoup(d.get('html',''),'html.parser');bold=sorted({x.get_text() for x in s.select('[mathvariant=bold]') if re.fullmatch('[a-z]',x.get_text())})
 proofs[i]={'path':str(p.relative_to(ROOT)),'source_question_id':d.get('math_academy_id') or re.search(r'(q-\d+|example-\d+)',p.name).group(1),'problem_exact_ignoring_images_whitespace':norm(q[':question/problem'])==norm(d['problem']),'solution_exact_ignoring_images_whitespace':norm(q.get(':question/worked-solution',''))==norm(d.get('worked_solution','')),'bold_vector_letters':bold,'html_sha256':__import__('hashlib').sha256(d.get('html','').encode()).hexdigest()}
print('matched',len(proofs),'missing',missing);print('nonexact',[(k,v['problem_exact_ignoring_images_whitespace'],v['solution_exact_ignoring_images_whitespace'])for k,v in proofs.items()if not v['problem_exact_ignoring_images_whitespace']or not v['solution_exact_ignoring_images_whitespace']]);print('nobold',[(k,v)for k,v in proofs.items()if not v['bold_vector_letters']])
(D/'source-proofs.json').write_text(json.dumps(proofs,indent=2)+'\n');(D/'source-missing.json').write_text(json.dumps(missing,indent=2)+'\n')
