"""Extract immutable complete source masks; never import a numeric generator."""
import sys
sys.dont_write_bytecode=True
import json,re,shutil,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent;R=D.parents[2]
ref=D/'reference';ref.mkdir(exist_ok=True)
for path in ['generate/principles.md','docs/math-content.md','generate/runs/current/worker-instructions.md']+[f'generate/docs/{x}' for x in ['3-classify.md','4-template-extraction.md','5-plot-extraction.md','6-template-generator.md','7-plot-generator.md']]:shutil.copy2(R/path,ref/Path(path).name)
for kind in ['topics','lessons']:shutil.copy2(R/f'generate/runs/current/refresh-2026-10-14/{kind}/17592186049125.json',D/('topic.json' if kind=='topics' else 'lesson.json'))
shutil.copy2('/home/jake/Developer/MA/DATA/Lessons/863/Source/863.json',ref/'863.json')
shutil.copy2(R/'generate/scratch/17592186059716-draft/reference/grader-build.json',ref/'grader-build.json')
shutil.copy2(R/'generate/scratch/17592186059716-draft/check-engine',D/'check-engine')
build=json.loads((ref/'grader-build.json').read_text()); checks={}
for section in ['engine_sources','dependencies']:
 for path,expected in build[section].items():checks[path]={'expected':expected,'actual':hashlib.sha256((R/path).read_bytes()).hexdigest()}
for key in ['source','library','binary']:
 path=build[key];checks[path]={'expected':build[key+'_sha256'],'actual':hashlib.sha256((R/path).read_bytes()).hexdigest()}
assert len(checks)==42 and all(v['expected']==v['actual'] for v in checks.values())
assert hashlib.sha256((D/'check-engine').read_bytes()).hexdigest()==build['binary_sha256']
(ref/'grader-verification.json').write_text(json.dumps({'verified':len(checks),'all_match':True,'hashes':checks},indent=2)+'\n')
r=json.loads((D/'source.json').read_text());k=r['record'];out={};cases=[]
mat=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
def rows(s):return [[x.strip() for x in row.split('&')] for row in s.split('\\\\')]
for q in [k[':knowledge-point/canonical-example']]+k[':knowledge-point/questions']:
 sid=q[':question/math-academy-id'];can=sid.startswith('e-');p=q[':question/problem'];s=q.get(':question/worked-solution')
 named=list(re.finditer(r'([A-Z])\s*=\s*(\\begin\{bmatrix\}.*?\\end\{bmatrix\})',p,re.S))
 labels=['A','B'] if can else [m[1] for m in named]
 orig=[rows(m[1]) for m in mat.finditer(p)]
 if can:orig=[rows(m[1]) for m in list(mat.finditer(s))[:2]]
 n=[0]
 def mask(m):i=n[0];n[0]+=1;return '@@M'+str(i)+'@@'
 pm=mat.sub(mask,p)
 blocks=[]
 def block(m):
  text=m[0];pair=re.search(r'\\begin\{aligned\}([A-Z]{2})',text)[1];ms=list(mat.finditer(text));assert len(ms)==3
  witness=[i for i,v in enumerate(sum(rows(ms[2][1]),[])) if v!='∗'] if '∗' in ms[2][1] else None
  idx=len(blocks);blocks.append({'pair':[labels.index(c) for c in pair],'witness':witness[0] if witness else None,'identity':witness is None})
  replacements=['@@M'+str(labels.index(c))+'@@' for c in pair]+['@@P'+str(idx)+'@@']
  it=iter(replacements);return mat.sub(lambda _:next(it),text)
 sm=re.sub(r'\\begin\{aligned\}.*?\\end\{aligned\}',block,s,flags=re.S) if s else None
 fields=[]
 for f in q.get(':question/answer-fields',[]):fields.append({'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'],'choices':[{'type':a[':answer/type'][':db/ident'],'value':a[':answer/value']} for a in f[':answer-field/choices']],'correct':f.get(':answer-field/correct',{}).get(':answer/value')})
 out[sid]={'source_id':sid,'canonical':can,'labels':labels,'original_matrices':orig,'prompt_mask':pm,'solution_mask':sm,'blocks':blocks,'fields':fields,'has_difficulty':':question/difficulty' in q,'has_fields':':question/answer-fields' in q,'has_solution':s is not None}
 cases.append({'source_id':sid,'record':q})
(D/'templates.json').write_text(json.dumps(out,indent=2)+'\n')
(D/'source-cases.json').write_text(json.dumps([x for x in cases if x['source_id'].startswith('q-')],indent=2)+'\n')
(D/'canonical.json').write_text(json.dumps(cases[0],indent=2)+'\n')
(D/'independent-inventory.json').write_text(json.dumps({**{x:r[x] for x in ['database','basis','lineage']},'questions':[]},indent=2)+'\n')
print('Extracted',len(out),'complete source masks; verified grader hashes',len(checks))
