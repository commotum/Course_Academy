"""One-time extraction; reads only the immutable capture, not a numeric generator."""
import json,re,pathlib,shutil,hashlib
H=pathlib.Path(__file__).resolve().parent
S=json.loads((H/'source.json').read_text());R=S['record'];MAT=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
def rows(body):return [[x.strip() for x in r.split('&')] for r in body.split('\\\\')]
T={};cases=[]
for q in R[':knowledge-point/questions']:
 key=q[':question/math-academy-id'];p=q[':question/problem'];s=q[':question/worked-solution'];ms=list(MAT.finditer(p));names=[];bases=[];scales=[]
 for i,m in enumerate(ms):
  before=p[ms[i-1].end() if i else 0:m.start()];a=re.search(r'([A-Z])=(.*)$',before,re.S);names.append(a[1]);scales.append(a[2]);bases.append(rows(m[1]))
 pm=p
 for i,m in reversed(list(enumerate(ms))):pm=pm[:m.start()]+f'@@M{i}@@'+pm[m.end():]
 blocks=[];sm=s
 spans=list(re.finditer(r'\$\$\n(.*?)\n\$\$',s,re.S))
 for b,span in reversed(list(enumerate(spans))):
  content=span[1];mm=list(MAT.finditer(content));assert len(mm)==3
  before=s[:span.start()];pair=re.findall(r'computing \$([A-Z]{2})',before,re.I)[-1];pair=[names.index(x) for x in pair]
  result=rows(mm[2][1]);w=[i*len(result)+j for i,row in enumerate(result) for j,x in enumerate(row) if x!='∗'];identity=len(w)==len(result)**2
  resultpre=content[mm[1].end():mm[2].start()];scale=resultpre.split('=')[-1].strip()
  block={'pair':pair,'identity':identity,'witness':None if identity else w[0],'result_scale':scale,'raw_operands':[rows(mm[0][1]),rows(mm[1][1])]}
  blocks.insert(0,block)
  masked=content
  for j,m in reversed(list(enumerate(mm))):masked=masked[:m.start()]+(f'@@P{b}@@' if j==2 else f'@@O{b}_{j}@@')+masked[m.end():]
  sm=sm[:span.start(1)]+masked+sm[span.end(1):]
 T[key]={'source_id':q[':db/id'],'level':q[':question/difficulty'][':db/ident'].split('/')[-1],'labels':names,'bases':bases,'scales':scales,'blocks':blocks,'prompt_mask':pm,'solution_mask':sm,'raw_question':q}
 cases.append({'source_id':q[':db/id'],'record':q,'template':key,'profile':'raw-source','parameters':{'permutation':list(range(len(bases[0]))),'signs':[1]*len(bases[0]),'witnesses':[b['witness'] for b in blocks]}})
(H/'templates.json').write_text(json.dumps(T,indent=2)+'\n');(H/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
(H/'canonical.json').write_text(json.dumps({'database':S['database'],'basis':S['basis'],'lineage':S['lineage'],'record':R[':knowledge-point/canonical-example']},indent=2)+'\n')
(H/'independent-inventory.json').write_text(json.dumps({'database':S['database'],'basis':S['basis'],'lineage':S['lineage'],'questions':[]},indent=2)+'\n')
for path in ['generate/principles.md','generate/runs/current/worker-instructions.md','docs/math-content.md']+[f'generate/docs/{x}' for x in ['3-classify.md','4-template-extraction.md','5-plot-extraction.md','6-template-generator.md','7-plot-generator.md']]:shutil.copyfile(path,H/'reference'/pathlib.Path(path).name)
ref=pathlib.Path('generate/scratch/17592186059716-draft/reference/grader-build.json');g=json.loads(ref.read_text());checks={g['source']:g['source_sha256'],g['library']:g['library_sha256'],g['binary']:g['binary_sha256'],**g['engine_sources'],**g['dependencies']};out=[]
for path,expected in checks.items():
 got=hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest();assert got==expected,(path,got,expected);out.append({'path':path,'sha256':got})
assert len(out)==42
shutil.copyfile(g['binary'],H/'check-engine');(H/'check-engine').chmod(0o555);shutil.copyfile(ref,H/'reference/grader-build.json');(H/'reference/grader-verification.json').write_text(json.dumps({'verified_count':len(out),'files':out},indent=2)+'\n')
