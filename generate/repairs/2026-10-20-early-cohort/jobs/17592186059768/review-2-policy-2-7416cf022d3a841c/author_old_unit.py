"""Executable retained findings plus independent visible-record witnesses.
Run: context Python -B checks/regression.py. Only writes evidence/.
"""
import sys
sys.dont_write_bytecode=True
import copy,importlib.util,json,pathlib,re,collections
W=pathlib.Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186059768/review-1-policy-2-a0f21dc2de58c6f5/relocated-package');sys.path.insert(0,str(W))
sp=importlib.util.spec_from_file_location('generator',W/'17592186059768.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
E=pathlib.Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186059768/review-2-policy-2-7416cf022d3a841c/author-old-unit-check');E.mkdir(exist_ok=True)
def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
def matrix(text,captured=False):
 if captured and text.startswith('\\\\'):text=text.replace('\\\\','\\')
 return [[[int(v.strip()) for v in row.split('&')] for row in body.split('\\\\') if row.strip()] for _,body in re.findall(r'\\begin\{(array|bmatrix)\}(?:\{[^}]*\})?(.*?)\\end\{\1\}',text,re.S)]
def equations(text):return [[r.replace('&','').strip() for r in body.split('\\\\') if r.strip()] for body in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',text,re.S)]
def linear(s,n):
 s=re.sub(r'\s+','',s);out=[0]*(n+1);assert re.fullmatch(r'[+\-0-9xyz]+',s),s
 for term in re.findall(r'[+-]?[^+-]+',s):
  var=term[-1] if term[-1] in 'xyz' else None;j='xyz'.index(var) if var else n;a=term[:-1] if var else term
  out[j]+=int(a) if a not in ('','+','-') else (-1 if a=='-' else 1)
 return out
def expected(text):
 rows=equations(text)[0];n=3 if any('z' in r for r in rows) else 2;out=[]
 for row in rows:
  a,b=row.split('=');l,r=linear(a,n),linear(b,n);out.append([l[j]-r[j] for j in range(n)]+[r[-1]-l[-1]])
 return out
def field(r):return r['question'][':question/answer-fields'][0]
def key(r):return field(r)[':answer-field/correct'][1]
def bank(r):return [matrix(a[':answer/value'])[0] for a in field(r)[':answer-field/choices']]
def answer(r):return bank(r)[next(i for i,a in enumerate(field(r)[':answer-field/choices']) if a[':answer/id']==key(r))]
def mask(m):return [[(x>0)-(x<0) for x in row] for row in m]
def check(r):
 q=r['question'];want=expected(q[':question/problem']);bs=bank(r)
 assert answer(r)==want,(r['generation'],want,answer(r))
 assert len(bs)==5 and len({str(m) for m in bs})==5 and bs.count(want)==1
 assert matrix(q[':question/worked-solution'])==[[row[:-1] for row in want],want]
 for rows in equations(q[':question/worked-solution']):
  for idx,row in enumerate(rows):
   a,b=row.split('=');l,rr=linear(a,len(want[0])-1),linear(b,len(want[0])-1)
   assert [l[j]-rr[j] for j in range(len(l)-1)]+[rr[-1]-l[-1]]==want[idx]
 return want
def negative_corner(r):
 ix=[i for i,m in enumerate(bank(r)) if m[-1][-1]<0]
 return len(ix)==1 and field(r)[':answer-field/choices'][ix[0]][':answer/id']==key(r)
def probe(records):
 groups=collections.defaultdict(list)
 for r in records:groups[r['generation']['template']].append(r)
 report={}
 for name,rs in groups.items():
  src=g.PROFILES[name];target=mask(matrix(src[':question/answer-fields'][0][':answer-field/correct'][':answer/value'],True)[0]);wins=0
  for r in rs:
   matches=[i for i,m in enumerate(bank(r)) if mask(m)==target]
   wins+=len(matches)==1 and field(r)[':answer-field/choices'][matches[0]][':answer/id']==key(r)
  positions=collections.Counter(next(i for i,a in enumerate(field(r)[':answer-field/choices']) if a[':answer/id']==key(r)) for r in rs)
  report[name]={'count':len(rs),'negative_corner_successes':sum(negative_corner(r) for r in rs),'source_mask_successes':wins,'positions':dict(positions),'correct_masks':len({str(mask(answer(r))) for r in rs}),'semantic_matrices':len({str(answer(r)) for r in rs}),'same_mask_banks':sum(len({str(mask(m)) for m in bank(r)})==1 for r in rs),'variable_orders':sorted({tuple(r['generation']['variable_order']) for r in rs}),'equation_orders':sorted({tuple(r['generation']['row_order']) for r in rs})}
 return report

def main():
 replays=[];results=[];records=[];controls=[]
 supplied=json.loads((W.parent/'source/source.json').read_text())
 sources={q[':question/math-academy-id']:q for q in supplied['material']['kp'][':knowledge-point/questions']}
 assert set(g.PROFILES)==set(sources) and len(sources)==10, 'Supplied source families missing'
 for name,src in sources.items():
  level=src[':question/difficulty'][':db/ident'].split('/')[-1];params={str(n):n for n in g.slots(src)}
  r=g.generate(level,941713201,profile=name,parameters=params);check(r);replays.append(r)
  assert bank(r)==[matrix(a[':answer/value'],True)[0] for a in src[':question/answer-fields'][0][':answer-field/choices']]
  assert answer(r)==matrix(src[':question/answer-fields'][0][':answer-field/correct'][':answer/value'],True)[0]
  assert re.sub(r'\s+','',src[':question/problem'])==re.sub(r'\s+','',r['question'][':question/problem'])
  assert matrix(src[':question/worked-solution'])==matrix(r['question'][':question/worked-solution'])
  results.append({'profile':name,'source_id':src[':question/id'],'choices_matched':5,'solution_matrices_matched':True})
  sample=[g.generate(level,941713211+i,profile=name) for i in range(16)]
  for rec in sample:check(rec)
  assert all(g.generate(level,941713211+i,profile=name)==r for i,r in enumerate(sample))
  records+=sample
  base=sample[0];m=answer(base); changed=copy.deepcopy(m)
  # All other evidence fixed; reverse one signed coefficient.
  i,j=next((i,j) for i,row in enumerate(m) for j,v in enumerate(row[:-1]) if v)
  changed[i][j]*=-1
  options={'row_order':base['generation']['row_order'],'variable_order':base['generation']['variable_order']}
  cf=g.generate(level,941713211,profile=name,instance={'matrix':changed,**options});check(cf)
  assert answer(cf)!=answer(base) and cf['question'][':question/problem']!=base['question'][':question/problem']
  # Reorder terms on one side, preserving the entire keyed response and solution.
  irrelevant=copy.deepcopy(base);q=irrelevant['question'];body=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/problem'],re.S)
  rows=body[1].split('\\\\');lhs,rhs=rows[0].split('&=');parts=re.findall(r'[+-]?[^+-]+',lhs.strip());rewritten=''.join((x if x.startswith(('+','-')) else '+'+x) for x in reversed(parts)).lstrip('+');rows[0]=rewritten+' &='+rhs
  q[':question/problem']=q[':question/problem'][:body.start(1)]+'\\\\'.join(rows)+q[':question/problem'][body.end(1):];check(irrelevant);assert answer(irrelevant)==answer(base)
  controls += [base,cf,irrelevant]
 minimum=g.generate('easy',941713401,profile='q-71722',parameters={'2':2,'3':4});check(minimum);assert not negative_corner(minimum)
 signed=g.generate('easy',941713401,profile='q-71722',parameters={'2':-2,'3':4});check(signed);assert answer(signed)!=answer(minimum)
 controls += [minimum,signed]
 for p in ('q-1052','q-71722'):
  group=[r for r in records if r['generation']['template']==p]
  assert not all(negative_corner(r) for r in group)
 report=probe(records)
 for p,d in report.items():
  assert d['source_mask_successes']<d['count'] and d['correct_masks']>1 and len(d['positions'])>1 and d['same_mask_banks']>0,(p,d)
 # An independently corrupted key must fail the visible-equation witness.
 bad=copy.deepcopy(records[0]);field(bad)[':answer-field/correct'][1]=next(a[':answer/id'] for a in field(bad)[':answer-field/choices'] if a[':answer/id']!=key(bad))
 try:check(bad)
 except AssertionError:pass
 else:raise AssertionError('Key witness failed its mutation test')
 save('source-replay-results.json',results);save('source-replays.json',replays);save('records.json',records);save('counterfactual-records.json',controls);save('shortcut-before-delivery.json',report)
 save('regression-results.json',{'findings':['ab0a792d1ce906d04a69','7162d545ab516c205adc'],'passed':True,'source_banks':len(replays),'independent_records':len(records),'controlled_records':len(controls),'old_exact_counterexample_tested':True,'signed_literal_counterexample_tested':True,'stale_key_mutation_rejected':True})
 print(json.dumps({'source_banks':len(replays),'records':len(records),'controls':len(controls),'retained_findings':'passed'}))
if __name__=='__main__':main()
