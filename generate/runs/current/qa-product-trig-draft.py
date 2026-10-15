import sys
sys.dont_write_bytecode=True
"""Parent product-rule readback including supplied answer fragments."""
import importlib.util,json,re,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186096617;D=R.parents[2]/f'generate/scratch/{K}-draft'
def module(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_product_readback',R/'product-readback.py');g=module('reviewed_trig_product',D.with_suffix('.py'));s=p.s;x=p.x
counts=dict(instances=0,complete_values=0,source_values=0,source_fields=0,existing_refs=0,missing_refs=0,fieldless_repair=0,source_prompts_raw_exact=0,source_prompt_prose=0,source_exact_solutions=0,source_ordered_solution_prose=0,source_derived_solutions=0,raw_wrong_lhs_instances=0)
def prose(text):return re.sub(r'\$\$.*?\$\$|(?<!\$)\$(?!\$).*?(?<!\$)\$(?!\$)','[MATH]',text,flags=re.S)
def signatures(text):
 block=re.search(r'\$\$(.*?)\$\$',text,re.S)[1];return [p.normalize(row).count("'") for row in block.split(r'\\')]
def top_additions(z):
 out=[];depth=0;start=0
 for i,ch in enumerate(z):
  if ch in '({[':depth+=1
  elif ch in ')}]':depth-=1
  elif ch=='+' and depth==0:out.append(z[start:i]);start=i+1
 assert depth==0
 out.append(z[start:]);return out
def check(record):
 q=record['question'];meta=record['generation'];prompt=q[':question/problem'];F=p.question_function(prompt);df=s.diff(F,x);worked=q[':question/worked-solution'];raw=(meta['template']=='q-319350' and meta['profile']=='observed_raw')
 stages=p.stages(worked,F,raw);assert stages['derivative_rows']==4 and stages['formal_rows']==2;counts['raw_wrong_lhs_instances']+=int(raw)
 for name,n in stages.items():counts[name]=counts.get(name,0)+n
 fields=q[':question/answer-fields'];assert len(fields)==1;f=fields[0];vals=[p.scalar(z[':answer/value']) for z in f[':answer-field/choices']]
 if f[':answer-field/type'].endswith('/radio'):
  good=[p.same(v,df) for v in vals];assert sum(good)==1
  for n,a in enumerate(vals):assert all(not p.same(a,b) for b in vals[:n])
 else:
  assert '{{'+f[':answer-field/key']+'}}' in prompt
  if prompt.split('\n\n',1)[1].lstrip().startswith("$f'(x)"):
   good=[p.same(v,df) for v in vals]
  else:
   good=[]
   for z in f[':answer-field/choices']:
    lhs,rhs=p.blank_complete(prompt,z[':answer/value']);assert p.same(lhs,df);good.append(p.same(rhs,df))
  assert all(good)
 assert good[next(n for n,z in enumerate(f[':answer-field/choices']) if z[':answer/id']==f[':answer-field/correct'][1])]
 functions=p.definitions(worked);u,v=functions['u'],functions['v']
 du,dv=s.diff(u,x),s.diff(v,x);template=meta['template']
 block=re.search(r'\$\$(.*?)\$\$',worked,re.S)[1];rendered_rows=block.split(chr(92)*2);assert len(rendered_rows)==4
 for row_index in (1,2):
  shown=rendered_rows[row_index].split('=',1)[1];shown=shown.replace(r'\end{aligned}','');terms=top_additions(shown);assert len(terms)==2,(template,row_index,terms)
  for term,want in zip(terms,(du*v,u*dv)):assert p.same(p.scalar(term,functions),want),(template,row_index,term,want)
  counts['individually_ordered_product_terms']=counts.get('individually_ordered_product_terms',0)+2

 if len(vals)==5:
  if template=='q-1907':expected=[u*s.cos(x)-u*s.sin(x),du*s.cos(x)-du*s.sin(x),du*s.cos(x)-u*s.sin(x),u*s.cos(x)-du*s.sin(x),du*s.cos(x)+u*s.sin(x)]
  elif template=='q-104297':expected=[-u*s.cos(x)-u*s.sin(x),u*s.cos(x)+s.sin(x),df,-u*s.cos(x)+s.sin(x),u*s.cos(x)+u*s.sin(x)]
  elif template=='q-1931':expected=[u*s.sec(x)+u*s.sec(x)**2,s.sec(x)**2+u*s.tan(x),u*s.csc(x)**2+u*s.tan(x),u*s.sec(x)**2+s.tan(x),df]
  else:expected=[df,du*dv,du*v,u*dv,du*v-u*dv]
  assert all(sum(p.same(a,b) for b in expected)==1 for a in vals),(template,vals,expected)
  counts['independently_read_whole_banks']=counts.get('independently_read_whole_banks',0)+1

 if not meta['template'].startswith('q-'):
  assert u.is_polynomial(x) and len(s.Poly(u,x).terms())==2
  trig=[node for node in s.preorder_traversal(v) if node.func in (s.sin,s.cos,s.tan)];assert len(trig)==1 and trig[0].args==(x,)
  if q[':question/difficulty'].endswith('/moderate'):assert v==trig[0] and s.Poly(u,x).degree() in (2,3,4) and s.Poly(u,x).coeff_monomial(1)!=0
  else:assert v-trig[0]!=0 and not (v-trig[0]).has(x) and s.Poly(u,x).coeff_monomial(x)!=0
  final=rendered_rows[3].split('=',1)[1].replace(r'\end{aligned}','');term_count=len(s.Add.make_args(s.expand(p.scalar(final))))
  assert term_count==(3 if q[':question/difficulty'].endswith('/moderate') else 6),(template,term_count,final)
  counts['authored_distributed_term_counts']=counts.get('authored_distributed_term_counts',0)+1

 counts['instances']+=1;counts['complete_values']+=len(vals);return q
F=module('root_product_source',R/'root-source-fidelity.py');sources,source_fidelity=F.check(g,K,D)
for c in json.loads((D/'source-cases.json').read_text()):
 old=sources[c['source_id']];q=check(g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile='repaired'))
 if old.get(':question/worked-solution'):
  assert prose(q[':question/worked-solution'])==prose(old[':question/worked-solution'])
  if c['source_id']!='q-319350':assert signatures(q[':question/worked-solution'])==signatures(old[':question/worked-solution'])
  counts['source_ordered_solution_prose']+=1
 else:counts['source_derived_solutions']+=1
counts['raw_source_fidelity']=source_fidelity
review=json.loads((D/'review.json').read_text())
for record in review['generated_variants']:check(record.get('record',record))
for record in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(record)
counts['database_writes']=0;counts['status']='passed';counts['script_sha256']=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest();(R/'qa'/f'{K}-root-readback.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
