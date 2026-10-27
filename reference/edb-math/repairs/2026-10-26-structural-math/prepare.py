"""Compile reviewed structural recoveries and operator repairs as exact CAS."""
import collections,hashlib,json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/structural-math-2026-10-26';sys.path[:0]=[str(R/'scripts'),str(R/'reference/edb-math/repairs/2026-10-24-mathml-tables')]
from migrate_learner_history import dumps,kw
from question_capture.math_format import MATH,ENV,environment,cells,normalize_limit_operators,mathml_ruled_table,mathml_unruled_table,validate_math_structure
from layout import grid_key
values={(d['e'],d['a']):d['v']for d in json.loads((W/'values.json').read_text())};meta=json.loads((W/'metadata.json').read_text());parents=json.loads((W/'parents.json').read_text());edits=collections.defaultdict(list);review=[];skips=[];counts=collections.Counter();malformed={(x['e'],x['a'],x['start'])for x in json.loads((H/'malformed-structure.json').read_text())}
def signature(tex):
 out=[]
 for m in ENV.finditer(tex):
  if m[1]!='begin'or m[2]not in ('bmatrix','pmatrix','vmatrix','matrix','cases','array'):continue
  b=environment(tex,m.start());body=tex[b[0]:b[1]]if b else''
  if m[2]=='array':body=re.sub(r'^\s*\{[^{}]*\}','',body,count=1)
  g=cells(body)
  out.append((m[2],str(grid_key(g))if g else'INVALID'))
 return out
for proposal in json.loads((H/'source-formula-proposals.json').read_text()):
 key=(proposal['e'],proposal['a']);before=values[key]
 for c in proposal['changes']:
  a,b=c['span'];old=c['before'];new=c['after'];assert before[a:b]==old
  isbroken=any(e==key[0]and attr==key[1]and a<=start<b for e,attr,start in malformed)
  if not isbroken and signature(old)==signature(new):skips.append({'e':key[0],'a':key[1],'span':[a,b],'reason':'Current matrix/grid structure agrees with source; formatting differences are not defects'});continue
  if old==new:continue
  edits[key].append((a,b,new,'source-formula-recovery'));review.append({**c,'e':key[0],'a':key[1],'source_path':proposal['source_path'],'source_identity':proposal['identity'],'reason':'Identity-bound original formula restores a malformed or incorrect layout role'});counts['source_formula_blocks']+=1
for d in json.loads((H/'inverse-answer-repairs.json').read_text()):
 key=d['e'],d['a'];assert values[key]==d['before'];assert not edits[key]
 edits[key].append((0,len(d['before']),d['after'],'reversible-absolute-value-repair'));counts['reversible_answer_values']+=1
for d in json.loads((H/'source-matches.json').read_text()):
 if d['env']!='aligned':continue
 key=d['e'],d['a'];a,b=d['span']
 if any(s<=a and b<=z for s,z,_,_ in edits[key]):continue
 rows=[list(r)for r in d['rows']];attrs=d['source']['source_attributes'];new=mathml_ruled_table(rows,attrs)or mathml_unruled_table(rows,attrs)
 if not new:
  skips.append({'e':key[0],'a':key[1],'span':[a,b],'reason':'Source equation alignment or unsupported data-layout attributes; preserve'});continue
 # If a source cell explicitly contains a zero-rule fraction, recover that
 # stack's role while retaining the current numerator/denominator bytes.
 zero=0
 source=BeautifulSoup(d['source']['source_mathml'],'html.parser').find('mtable')
 if source:
  trs=source.find_all('mtr',recursive=False)
  for i,tr in enumerate(trs):
   for j,td in enumerate(tr.find_all('mtd',recursive=False)):
    fs=td.find_all('mfrac')
    if len(fs)==1 and re.fullmatch(r'0(?:\.0+)?(?:[A-Za-z%]+)?',fs[0].get('linethickness',''))and i<len(rows)and j<len(rows[i])and rows[i][j].count(r'\frac')==1:
     rows[i][j]=rows[i][j].replace(r'\frac',r'\genfrac{}{}{0pt}{}',1);zero+=1
 if zero:new=mathml_ruled_table(rows,attrs)or mathml_unruled_table(rows,attrs)
 edits[key].append((a,b,new,'source-table-layout'));counts['source_table_blocks']+=1;counts['source_zero_rule_stacks']+=zero;review.append({'e':key[0],'a':key[1],'span':[a,b],'before':values[key][a:b],'after':new,'source_path':d['source']['path'],'source_identity':d['source']['identity'],'source_attributes':attrs,'ordered_cells_preserved':not zero,'zero_rule_stacks_recovered':zero})
fields=[];validation=[]
for key,before in values.items():
 e,a=key;changes=sorted(edits.get(key,[]));last=-1
 for s,z,new,reason in changes:assert s>=last,(key,changes);last=z
 after=before
 for s,z,new,reason in reversed(changes):after=after[:s]+new+after[z:]
 math_answer=a=='answer/value'and meta[str(e)].get('answer/type')==17592186045498
 nlim=[0]
 def limit(m):
  result=normalize_limit_operators(m[0]);nlim[0]+=result!=m[0];return result
 if math_answer:
  fixed=normalize_limit_operators(after);nlim[0]+=fixed!=after;after=fixed
 else:after=MATH.sub(limit,after)
 counts['limit_operator_math_blocks']+=nlim[0]
 if after==before:continue
 assert re.findall(r'\{\{[^{}]+\}\}',before)==re.findall(r'\{\{[^{}]+\}\}',after),(key,'field markers')
 assert re.findall(r'!\[[^\]]*\]\([^)]*\)|<img\b[^>]*>',before)==re.findall(r'!\[[^\]]*\]\([^)]*\)|<img\b[^>]*>',after),(key,'image references')
 reasons=sorted({r for _,_,_,r in changes}|({'limit-operator'}if nlim[0]else set()))
 fs=sorted({p for p,attr in parents.get(str(e),[])if attr in ('answer-field/choices','answer-field/correct')})
 fields.append({'entity':e,'attribute':a,'before':before,'after':after,'before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':hashlib.sha256(after.encode()).hexdigest(),'math_answer':math_answer,'answer_fields':fs,'reasons':reasons})
 try:validate_math_structure(after,bare_math=math_answer)
 except ValueError as ex:validation.append({'e':e,'a':a,'error':str(ex),'reasons':reasons})
(H/'fields.json').write_text(json.dumps(fields,indent=2)+'\n');(H/'reviewed-edits.json').write_text(json.dumps(review,indent=2)+'\n');(H/'reviewed-nonrepairs.json').write_text(json.dumps(skips,indent=2)+'\n');(H/'structural-validation-candidates.json').write_text(json.dumps(validation,indent=2)+'\n');(H/'transaction.edn').write_text(dumps([[kw('db/cas'),f['entity'],kw(f['attribute']),f['before'],f['after']]for f in fields])+'\n')
report={'basis_t':8557,'fields':len(fields),'entities':len({f['entity']for f in fields}),**counts,'attributes':dict(collections.Counter(f['attribute']for f in fields)),'answer_fields':len({e for f in fields for e in f['answer_fields']}),'remaining_structural_validation_candidates':len(validation),'images_and_field_markers_preserved':True};(H/'preparation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
