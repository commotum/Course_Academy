import sys
sys.dont_write_bytecode=True
import json,re,hashlib,copy,importlib.util,itertools
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186100869;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
reader=load('parent_conformability_dimension_helpers',R/'qa-matrix-dimensions-given-draft.py');dimension=reader.dimension;balanced=reader.balanced;prose=reader.prose
keys=('I','II','III');counts=dict(records=0,actual_array_shapes=0,printed_statement_products=0,Boolean_values=0,correct_designations=0,ordered_annotated_factor_dimensions=0,prose_inner_counts=0,source_values=0,source_fields=0,source_keys=0,source_solutions=0,changed_target_records=0)
def shape_map(text):
 arrays={}
 for m in re.finditer(r'([A-Z])\s*=\s*\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S):
  rows=[row.split('&') for row in m[2].split(chr(92)*2)];assert all(len(row)==len(rows[0]) for row in rows) and all(all(c.strip() for c in row) for row in rows);arrays[m[1]]=(len(rows),len(rows[0]))
 assert len(arrays)==3;return arrays
def annotated_factors(block):
 out=[]
 for m in re.finditer(r'\{([A-Z])\}_\{',block):
  body,end=balanced(block,m.end()-1)
  while (w:=re.search(r'\\(?:boxed|text)\{',body)):
   inner,stop=balanced(body,w.end()-1);body=body[:w.start()]+inner+body[stop:]
  out.append((m[1],dimension(body)))
 assert len(out)==2;return out

def check(record):
 q=record['question'];shapes=shape_map(q[':question/problem']);products=re.findall(r'The product \$([A-Z])([A-Z])\$',q[':question/problem']);assert len(products)==3 and len(set(products))==3 and all(a!=b for a,b in products);assert 'Select all that apply.' in q[':question/problem']
 truth=[shapes[a][1]==shapes[b][0] for a,b in products];fields=q[':question/answer-fields'];assert {f[':answer-field/key'] for f in fields}==set(keys)
 for key,want in zip(keys,truth):
  f=next(f for f in fields if f[':answer-field/key']==key);assert f[':answer-field/type']==':answer-field.type/checkbox';assert sorted(z[':answer/value'] for z in f[':answer-field/choices'])==['false','true'];correct=next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);assert correct==str(want).lower()
  counts['Boolean_values']+=2;counts['correct_designations']+=1
 solution=q[':question/worked-solution'];blocks=re.findall(r'\$\$(.*?)\$\$',solution,re.S);assert len(blocks)==3
 for (a,b),want,block in zip(products,truth,blocks):
  assert annotated_factors(block)==[(a,shapes[a]),(b,shapes[b])]
  assert (r'\text{well defined}' in block)==want and (r'\text{undefined}' in block)==(not want)
  assert (r'\boxed' in block)==want and (r'_{\ne }' in block)==(not want)
  counts['ordered_annotated_factor_dimensions']+=4
 cmp=re.findall(r'\$(\d+)\$ columns? in \$([A-Z])\$ and \$(\d+)\$ rows? in \$([A-Z])\.?\$',solution);assert len(cmp)==3
 for (m,a,n,b),(left,right),want in zip(cmp,products,truth):
  assert (a,b)==(left,right) and int(m)==shapes[a][1] and int(n)==shapes[b][0];counts['prose_inner_counts']+=2
 # Check each rule sentence against its actual prompted pair and equality.
 for (a,b),want in zip(products,truth):
  sentence='Since the number of columns in $'+a+'$ '+('equals' if want else 'does **not** equal')+' the number of rows in $'+b
  assert sentence in solution
 ending=solution.split('\n\n')[-1]
 if all(truth):assert ending=='We conclude that all three statements are true.'
 elif not any(truth):assert ending=='We conclude that all three statements are false.'
 else:
  yes,no=ending.split(', while ');assert [k for k in keys if re.search(r'\b'+k+r'\b',yes)]==[k for k,t in zip(keys,truth) if t];assert [k for k in keys if re.search(r'\b'+k+r'\b',no)]==[k for k,t in zip(keys,truth) if not t]
 opening=solution.split('\n\n')[0]
 matches=re.findall(r'\$([A-Z])\$ is a \$(.*?)\$ (matrix|row vector|column vector)',opening);assert len(matches)==3
 for label,dims,noun in matches:
  actual=shapes[label];assert dimension(dims)==actual
  assert noun==('row vector' if actual[0]==1 else 'column vector' if actual[1]==1 else 'matrix')
 counts['records']+=1;counts['actual_array_shapes']+=3;counts['printed_statement_products']+=3

if __name__=='__main__':
 g=load('parent_conformability_generation',D.with_suffix('.py'));fmt=load('parent_conformability_format',R.parents[2]/'scripts/question_capture/math_format.py');src=json.loads((R/'refresh-2026-10-14/sources'/f'{K}.json').read_text());assert src==json.loads((D/'source.json').read_text());originals={q[':question/math-academy-id']:q for q in src['record'][':knowledge-point/questions']}
 for c in json.loads((D/'source-cases.json').read_text()):
  r=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c.get('profile',c.get('bank_profile')));q=r['question'];old=originals[c.get('math_academy_id',c['source_id'])];check(r)
  assert q[':question/problem']==fmt.normalize_prose(old[':question/problem']) and q[':question/worked-solution']==fmt.normalize_prose(old[':question/worked-solution']);counts['source_solutions']+=1
  assert {f[':answer-field/key'] for f in old[':question/answer-fields']}==set(keys)
  for of in old[':question/answer-fields']:
   nf=next(f for f in q[':question/answer-fields'] if f[':answer-field/key']==of[':answer-field/key']);assert of[':answer-field/type'][':db/ident']==nf[':answer-field/type'];assert sorted(z[':answer/value'] for z in of[':answer-field/choices'])==sorted(z[':answer/value'] for z in nf[':answer-field/choices']);counts['source_values']+=2;counts['source_fields']+=1
   ans=next(z[':answer/value'] for z in nf[':answer-field/choices'] if z[':answer/id']==nf[':answer-field/correct'][1]);assert ans==of[':answer-field/correct'][':answer/value'];counts['source_keys']+=1
 samples=json.loads((R/'qa'/f'{K}-sampled.json').read_text())
 for z in samples:check(z)
 # Exercise changed requested products while preserving the printed source arrays.
 for t in g.SOURCES:
  level=g.source_level(t);pars=g.source_parameters(t)
  for pairset in itertools.combinations(itertools.permutations(range(3),2),3):
   p=copy.deepcopy(pars);p['products']=list(map(list,pairset))
   try:r=g.generate(level,template=t,parameters=p)
   except ValueError:continue
   check(r);counts['changed_target_records']+=1
 probe=copy.deepcopy(samples[0]);text=probe['question'][':question/problem'];shapes=shape_map(text);products=re.findall(r'The product \$([A-Z])([A-Z])\$',text);found=False
 for a,b in products:
  for c,d in itertools.permutations(shapes,2):
   if (c,d) not in products and (shapes[a][1]==shapes[b][0])!=(shapes[c][1]==shapes[d][0]):
    probe['question'][':question/problem']=text.replace('The product $'+a+b+'$','The product $'+c+d+'$',1);found=True;break
  if found:break
 assert found
 saved=copy.deepcopy(counts)
 try:check(probe)
 except AssertionError:pass
 else:raise AssertionError('Changed assessed product survived stale key and solution')
 counts=saved;counts.update(status='passed',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),changed_product_stale_key_rejected=True,database_writes=0)
 (R/'qa'/f'{K}-root-readback.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
