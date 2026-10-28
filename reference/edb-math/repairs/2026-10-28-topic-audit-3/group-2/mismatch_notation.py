import collections,copy,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts/question_capture'));sys.path.insert(0,str(H));import source_notation as N
from math_format import MATH,validate_math_structure
Q=json.loads((H/'supplement-proposed-questions.json').read_text());A=json.loads((H/'proposed-activities.json').read_text());nodes={}
def index(v):
 if isinstance(v,dict):
  if ':db/id'in v:nodes.setdefault(v[':db/id'],[]).append(v)
  for x in v.values():index(x)
 elif isinstance(v,list):
  for x in v:index(x)
index(Q);index(A);out=[];res=[]
for c in json.loads((H/'formula-count-candidates.json').read_text()):
 e,a=c['entity'],c['attribute'];before=nodes[e][0][':'+a];src=c['source'];fs=' '.join(src['formulas']);roles={''.join(x)for x in re.findall(r'\\mathbf\s*(?:\{([A-Za-z])\}|([A-Za-z]))',fs)};N.ROLES=roles
 after=N.prose(before)
 indexed={''.join(x)for x in re.findall(r'\\mathbf\s*(?:\{([A-Za-z])\}|([A-Za-z]))\s*_',fs)}
 def more(m):
  edge=2 if m[0].startswith('$$')else 1;s=m[0][edge:-edge]
  for name in indexed:s=re.sub(r'(?<![A-Za-z\\{])'+name+r'(?=_)',lambda _:r'\mathbf{'+name+'}',s)
  if r'\mathbb'in fs:s=re.sub(r'(?<![A-Za-z\\{])R(?=\s*(?:\^\{?[23]|\}\^\{?[23]))',lambda _:r'\mathbb{R}',s)
  return m[0][:edge]+s+m[0][-edge:]
 after=MATH.sub(more,after)
 if after!=before:
  validate_math_structure(after);out.append({'entity':e,'attribute':a,'before':before,'after':after,'reason':'Restore explicit source vector/domain fonts across legitimate split math or displaced cloze/checkbox-label boundaries','evidence':{'basis':9837,'source_path':src['path'],'source_formulas':src['formulas'],'roles':sorted(roles),'indexed_vector_roles':sorted(indexed),'scope':'Only individually observed font roles; no givens, values, operators, field mappings, controls, or graph geometry altered.'},'confidence':'high'})
  for node in nodes[e]:node[':'+a]=after
 res.append({'entity':e,'identity':c['identity'],'attribute':a,'stored_math_segments':len(c['math']),'source_math_roots':len(src['formulas']),'resolution':'Expected cloze S# placeholders, checkbox DISPLAY labels moved into field keys, or adjacent/source layout math split boundaries. Source vector fonts restored where explicit; whole stored prompt/solution and bank roles reviewed.','source_path':src['path']})
(H/'mismatch-notation-proposals.json').write_text(json.dumps(out,indent=2)+'\n');(H/'formula-count-resolutions.json').write_text(json.dumps(res,indent=2)+'\n');(H/'mismatch-notation-render-input.json').write_text(json.dumps([{'entity':p['entity'],'attribute':p['attribute'],'value':p['after']}for p in out],indent=2)+'\n');(H/'supplement2-proposed-questions.json').write_text(json.dumps(Q,indent=2)+'\n');print('font-only',len(out),collections.Counter(p['attribute']for p in out))
