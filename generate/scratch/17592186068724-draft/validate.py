"""Independent displayed-content, source-fidelity, finite capacity and native checks."""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent

def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
g=load('generator',D.with_suffix('.py'));p=load('independent',D/'parser.py')
import sympy as sp
U=sp.Symbol('u',real=True)
def same(a,b):return sp.cancel(a-b)==0
def parse(text):return p.scalar(text.strip().rstrip('.,'))
def check(rec):
 q=rec['question'];meta=rec['generation'];params=meta['parameters'];z=p.T if params['variable']=='t'else p.X
 # Independently read the actual givens, not generator data/bank helpers.
 integrand=p.prompt(q[':question/problem']);sol=q[':question/worked-solution'];u=parse(re.search(r'Let \$u=(.*?)\.\$',sol)[1]);v=sp.diff(u,z)
 b=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);assert len(b)==2
 derivative,relation=b[0].split(r'\,⟹\,');displayed=parse(derivative.split('=',1)[1]);assert same(displayed,v)
 lhs,rhs=relation.split('=',1);rhs=rhs.split(r'\text{d}')[0].replace(r'\,','').strip()
 if lhs.startswith(r'\text{d}u'):assert same(parse(rhs),v)
 else:
  coef=parse(lhs.split(r'\text{d}u')[0]);assert same(coef*v,parse(rhs))
 rows=b[1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
 expected=4 if meta['bank_profile'].startswith('q-1137')or meta['bank_profile']=='q-72566'else 6 if meta['bank_profile']=='q-72605'else 5
 assert len(rows)==expected
 # The original integral on the first row is an independently parsed given.
 assert same(p.prompt('$'+rows[0].split('&')[0]+'$'),integrand)
 for row in rows:
  value=row.split('& =',1)[1].strip()
  if r'\int'in value:
   prefix,body=value.split(r'\int',1);mult=parse(prefix)if prefix else sp.Integer(1)
   m=re.search(r'(.*?)\\(?:,\s*)?\\?text\{d\}([xtu])',body)
   # Source includes both \,\text{d}u and \text{d}u.
   if not m:m=re.search(r'(.*?)\\text\{d\}([xtu])',body)
   assert m,(row,body)
   val=parse(m[1].replace(r'\,',''));var=m[2]
   if var=='u':val=val.subs(U,u)*v
   assert same(mult*val,integrand),(meta,row)
  else:
   val=parse(value).subs(U,u);assert same(sp.diff(val,z),integrand),(meta,row)
 f=q[':question/answer-fields'][0];values=[parse(a[':answer/value'])for a in f[':answer-field/choices']];ds=[sp.cancel(sp.diff(a,z))for a in values]
 assert all(not same(a,b)for i,a in enumerate(ds)for b in ds[i+1:])
 ids=[a[':answer/id']for a in f[':answer-field/choices']];correct=f[':answer-field/correct'][1];assert correct in ids and len(ids)==len(set(ids));assert [i for i,d in enumerate(ds)if same(d,integrand)]==[ids.index(correct)]
 assert g.task_fingerprint(q)==meta['mathematical_fingerprint']
 g.FORMAT.validate_generated_record(rec)
 # Negative-denominator intervals require the displayed abs bars; positive
 # quadratics alone may omit them, and this follows from the actual polynomial.
 final=f[':answer-field/choices'][ids.index(correct)][':answer/value']
 if f[':answer-field/type']==':answer-field.type/blank':assert sp.Poly(u,z).degree()==2 and sp.Poly(u,z).LC()>0 and u.subs(z,0)>0
 elif not any(bar in final for bar in ('|',r'\mid')):assert sp.Poly(u,z).degree()%2==0 and sp.Poly(u,z).LC()>0 and len(sp.Poly(u,z).terms())==2 and u.subs(z,0)>0
 return z,u,integrand

def native(rec):
 f=rec['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1];checks=[]
 if f[':answer-field/type']==':answer-field.type/radio':
  for a in f[':answer-field/choices']:checks.append({'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==correct else'rejected','purpose':'every field-owned radio choice'})
 else:
  z,u,_=check(rec);canonical=f[':answer-field/choices'][0][':answer/value'];eq='-4*ln('+str(u).replace('**','^')+')'
  checks=[{'submitted':v,'expected':outcome,'purpose':purpose}for v,outcome,purpose in [(canonical,'accepted','canonical'),(eq,'accepted','equivalent explicit multiplication'),(eq+'+0','accepted','equivalent additive zero'),('4*ln('+str(u).replace('**','^')+')','rejected','wrong sign'),('-3*ln('+str(u).replace('**','^')+')','rejected','wrong factor'),('0','rejected','constant wrong')]]
 return {'label':rec['question'][':question/id'],'record':rec,'checks':checks}

def main():
 allrecords=[];replay=[];cases=[];review=[];capacities={};slots={}
 for c in g.CASES:
  t,level=c[:2];r=g.generate(level,0,t,g.defaults(c));check(r);q=r['question'];o=g.SOURCES[t]
  assert q[':question/problem']==o[':question/problem'];assert q[':question/worked-solution']==o[':question/worked-solution']
  f=q[':question/answer-fields'][0];sf=o[':question/answer-fields'][0];assert [a[':answer/value']for a in f[':answer-field/choices']]==[a[':answer/value']for a in sf[':answer-field/choices']];assert f[':answer-field/key']==sf[':answer-field/key'];assert f[':answer-field/type']==sf[':answer-field/type'][':db/ident'];assert next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])==sf[':answer-field/correct'][':answer/value']
  cases.append({'source_id':t,'math_academy_id':t,'level':level,'template':t,'parameters':g.defaults(c),'profile':'source'})
  replay.append({'source_id':t,'prompt_exact':True,'solution_exact':True,'fields_exact':True,'complete_bank_exact':True,'values':len(f[':answer-field/choices']),'distractors':len(f[':answer-field/choices'])-1,'correct_designation':True})
  variant=g.generate(level,441,t);check(variant);review.append({'source':o,'served_anchor':r,'variant':variant})
 # Legacy metadata omissions are retained in the explicit reference API.
 q=g.generate('easy',template='q-12500',profile='reference')['question'];assert q==g.SOURCES['q-12500'];cases.append({'source_id':'q-12500','math_academy_id':'q-12500','level':'easy','template':'q-12500','parameters':{},'profile':'reference'})
 for level in g.SUPPORTED_LEVELS:
  seen=set();counts={};level_records=[]
  for t,params in g.all_instances(level):
   rec=g.generate(level,0,t,params);check(rec);fp=rec['generation']['mathematical_fingerprint'];counts[t]=counts.get(t,0)+1
   allrecords.append(rec)
   if fp not in seen:level_records.append(rec);seen.add(fp)
  capacities[level]={'profile_instances':sum(counts.values()),'distinct_math_tasks':len(seen),'profiles':counts};slots[level]=[r['generation']['parameters']for r in level_records]
  # Full finite batch, genuine math deduplication and exact explicit replay.
  items=g.batch(level,len(seen),123);assert len({x['generation']['mathematical_fingerprint']for x in items})==len(seen)
  try:g.batch(level,len(seen)+1)
  except ValueError:pass
  else:raise AssertionError('overflow silently returned')
  for rec in level_records[:3]:
   m=rec['generation'];assert rec['question']==g.generate(level,987,m['template'],m['parameters'])['question'];sh=g.generate(level,0,m['template'],m['parameters'],option_seed=33);assert sh['question'][':question/id']==rec['question'][':question/id'];assert sorted(sh['question'][':question/answer-fields'][0][':answer-field/choices'],key=lambda a:a[':answer/id'])==sorted(rec['question'][':question/answer-fields'][0][':answer-field/choices'],key=lambda a:a[':answer/id'])
 for bad in (True,1.0,'1',None):
  for action in (lambda:g.generate('easy',seed=bad),lambda:g.batch('easy',bad),lambda:g.batch('easy',1,seed=bad)):
   try:action()
   except TypeError:pass
   else:raise AssertionError('non-integer accepted')
 params=g.defaults(g.case('q-132982'));params['c']=True
 try:g.generate('easy',template='q-132982',parameters=params)
 except TypeError:pass
 else:raise AssertionError('bool parameter accepted')
 # Exercise every public mathematical instance through frozen native grader.
 inputs=[native(r)for r in allrecords];(D/'native-input.json').write_text(json.dumps(inputs,indent=2));subprocess.run([str(D/'check-engine'),str(D/'native-input.json'),str(D/'native-report.json')],check=True)
 report=json.loads((D/'native-report.json').read_text());assert report['documented_unresolved_checks']==0
 cli=json.loads(subprocess.check_output([sys.executable,str(D.with_suffix('.py')),'--difficulty','all','--count','3']));assert len(cli)==9 and all(sum(r['question'][':question/difficulty']==':question.difficulty/'+l for r in cli)==3 for l in g.SUPPORTED_LEVELS)
 for name,data in [('source-cases',cases),('source-replay',replay),('review',review),('capacity',capacities),('slot-coverage',slots)]: (D/(name+'.json')).write_text(json.dumps(data,indent=2))
 baseline=json.loads((D/'registered-baseline.json').read_text())['paths'];assert {str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in [D.with_name('17592186068724.py'),*sorted(p for p in D.with_name('17592186068724').rglob('*')if p.is_file())]}==baseline
 result={'passed':True,'basis':2275,'ma_rated_anchors':9,'ma_unrated_reference':1,'full_banks_exact':9,'options_exact':sum(x['values']for x in replay),'distractors_exact':sum(x['distractors']for x in replay),'every_public_profile_instance_checked':len(allrecords),'capacities':capacities,'native':{k:report[k]for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'registered_baseline_unchanged':True,'hard':'authored conservative same-backbone extension; no observed hard source','limitations':[]}
 (D/'validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
