"""Independent displayed-value checks, complete bank replay and native grading."""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path.insert(0,str(HERE))
from parser import scalar,prompt,same,X,T,equivalent
s=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
native=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def engine_item(label,rec):
 f=rec['question'][':question/answer-fields'][0];cid=f[':answer-field/correct'][1]
 if f[':answer-field/type']==':answer-field.type/radio':checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==cid else'rejected','purpose':'every field-owned radio answer'}for a in f[':answer-field/choices']]
 else:
  p=rec['generation']['parameters'];z,u,v,num,integrand,r=g.data(p,'easy');canonical=f[':answer-field/choices'][0][':answer/value'];equiv=g.tex(r)+'*ln('+g.tex(u)+')'
  checks=[{'submitted':canonical,'expected':'accepted','purpose':'canonical blank'},{'submitted':equiv,'expected':'accepted','purpose':'equivalent ln spelling and explicit multiplication'},{'submitted':g.tex(r)+'*ln('+g.tex(u)+')+0','expected':'accepted','purpose':'equivalent +0'},{'submitted':g.tex(-r)+'*ln('+g.tex(u)+')','expected':'rejected','purpose':'wrong sign'},{'submitted':g.tex(r+1)+'*ln('+g.tex(u)+')','expected':'rejected','purpose':'wrong factor'},{'submitted':'0','expected':'rejected','purpose':'incorrect constant'}]
 return {'label':label,'record':rec,'checks':checks}
def validate(rec,collect=True):
 q=rec['question'];assert rec['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
 t=rec['generation']['template'];c=g.case(t);level=q[':question/difficulty'].split('/')[-1];assert c[1]==level
 p=rec['generation']['parameters'];z,u,v,num,integrand,r=g.data(p,level)
 assert same(prompt(q[':question/problem']),integrand)
 assert len(q[':question/answer-fields'])==1
 f=q[':question/answer-fields'][0];assert f[':answer-field/key']==('field-1'if t=='q-132982'else'selection')
 assert f[':answer-field/type']==(':answer-field.type/blank'if t=='q-132982'else':answer-field.type/radio')
 vals=[scalar(a[':answer/value'])for a in f[':answer-field/choices']];assert len(vals)==(1 if t=='q-132982'else 5)
 assert all(not equivalent(a,b,z)for i,a in enumerate(vals)for b in vals[i+1:])
 cid=f[':answer-field/correct'][1];ans=next(scalar(a[':answer/value'])for a in f[':answer-field/choices']if a[':answer/id']==cid)
 assert same(g.sp.diff(ans,z),integrand);assert sum(same(g.sp.diff(a,z),integrand)for a in vals)==1
 assert g.fingerprint(q)==rec['generation']['mathematical_fingerprint']
 # Validate displayed substitution, derivative relation and every solution RHS.
 sol=q[':question/worked-solution'];inner=scalar(re.search(r'Let \$u=(.*?)\.\$',sol).group(1));assert same(inner,u)
 blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);assert len(blocks)==2
 derivative=scalar(blocks[0].split('=',1)[1].split(r'\,⟹')[0]);assert same(derivative,v)
 relation=blocks[0].split(r'\,⟹\,')[1]
 if level=='easy':
  coef=scalar(relation.split(r'\text{d}u=')[0]);rhs=scalar(relation.split('=',1)[1].split(r'\,\text{d}')[0]);assert same(coef*v,rhs)
 else:
  rhs=scalar(relation.split('=',1)[1].split(r'\,\text{d}')[0]);assert same(rhs,v)
 rows=blocks[1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
 assert len(rows)==(4 if level=='moderate'else 6 if t=='q-72605'else 5)
 for row in rows:
  rhs=row.split('& =',1)[1].strip()
  if r'\int'in rhs:
   prefix,body=rhs.split(r'\int',1);mult=scalar(prefix)if prefix else g.sp.Integer(1)
   match=re.search(r'(.*?)\\,\\text\{d\}([xtu])',body);assert match,row
   val=scalar(match[1]);dvar=match[2]
   if dvar=='u':val=val.subs(g.sp.Symbol('u',real=True),u)*v
   assert same(mult*val,integrand),(t,row)
  else:
   val=scalar(rhs).subs(g.sp.Symbol('u',real=True),u);assert same(g.sp.diff(val,z),integrand),(t,row)
 for text in (q[':question/problem'],sol):assert text.count('$')%2==0 and text.count('{')==text.count('}')
 assert (':question/math-academy-id'not in q)
 if collect:native.append(engine_item(q[':question/id'],rec))
def build_engine():
 deps=ROOT/'target/release/deps';edb=ROOT.parent/'EDB/target/release/deps';harness=ROOT/'generate/runs/current/check-engine.rs';libs={n:max(deps.glob('lib'+n+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns)for n in ('course_academy_engine','serde_json')};cmd=['rustc','--edition=2024','-O',str(harness)]
 for n,p in libs.items():cmd+=['--extern',n+'='+str(p)]
 cmd+=['-L','dependency='+str(edb),'-L','dependency='+str(deps),'-o',str(HERE/'check-current-engine')];subprocess.run(cmd,check=True)
 (HERE/'engine-build.json').write_text(json.dumps({'harness_sha256':sha(harness),'libraries':{str(p):sha(p)for p in libs.values()},'executable_sha256':sha(HERE/'check-current-engine')},indent=2))
def main():
 replay=[];review=[];distinct=set()
 for c in g.CASES:
  source=g.SOURCES[c[0]];rec=g.generate(c[1],0,c[0],g.defaults(c));validate(rec);z=g.data(g.defaults(c),c[1])[0]
  assert same(prompt(source[':question/problem']),prompt(rec['question'][':question/problem']))
  f=source[':question/answer-fields'][0];original=[scalar(a[':answer/value'])for a in f[':answer-field/choices']];new=[scalar(a[':answer/value'])for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']];mapping=[]
  for a,v in zip(f[':answer-field/choices'],original):
   matches=[i for i,w in enumerate(new)if equivalent(v,w,z)];assert len(matches)==1,(c[0],a,new)
   matched=new.pop(matches[0]);assert same(v,matched)or equivalent(v,matched,z);mapping.append({'source_answer_eid':a[':db/id'],'source_value':a[':answer/value'],'equivalent_modulo_integration_constant':True})
  assert not new
  assert same(g.sp.diff(scalar(f[':answer-field/correct'][':answer/value']),z),prompt(source[':question/problem']))
  replay.append({'source':c[0],'matched_options':len(original),'matched_distractors':len(original)-1,'complete_bank':True,'correct_designation_matched':True,'mapping':mapping})
  variant=g.generate(c[1],41,c[0]);validate(variant);review.append({'source':source,'replay':rec,'variant':variant})
  for seed in range(6):
   r=g.generate(c[1],seed,c[0]);validate(r);distinct.add(r['generation']['mathematical_fingerprint']);again=g.generate(c[1],seed+987,c[0],r['generation']['parameters']);assert again['question']==r['question']
  for boundary in (1,19 if c[0]=='q-132982'else 20 if c[1]=='easy'or c[0]=='q-113719'else 12):
   p=g.defaults(c)
   if c[1]=='easy'or c[0]=='q-113719':p['c']=boundary
   else:p['b']=boundary*(1 if p['b']>0 else -1)
   try:validate(g.generate(c[1],0,c[0],p))
   except ValueError as e:assert str(e)=='whole-bank antiderivative collision'
 build_engine();(HERE/'native-input.json').write_text(json.dumps(native,indent=2));subprocess.run([str(HERE/'check-current-engine'),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
 report=json.loads((HERE/'native-report.json').read_text());assert report['documented_unresolved_checks']==0
 (HERE/'source-replay.json').write_text(json.dumps(replay,indent=2));(HERE/'review.json').write_text(json.dumps(review,indent=2))
 md=['# Source replay and variant review','All nine rated source banks match modulo integration constants; correct designations match. Polynomial TeX is standardized separately from source wording and solution sequence. All displayed solution rows are checked independently. No plots occur.']
 for item in review:
  md+=['## '+item['source'][':question/math-academy-id']]
  for label,q in [('Source',item['source']),('Replay',item['replay']['question']),('Variant',item['variant']['question'])]:md+=[label,q[':question/problem'],str([a[':answer/value']for a in q[':question/answer-fields'][0][':answer-field/choices']]),q.get(':question/worked-solution','Missing')]
 (HERE/'review.md').write_text('\n\n'.join(md))
 result={'passed':True,'source_basis':1934,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','complete_banks_matched':len(replay),'source_options_matched':sum(x['matched_options']for x in replay),'source_distractors_matched':sum(x['matched_distractors']for x in replay),'supported_levels':['easy','moderate'],'unsupported_levels':['hard'],'distinct_sample_tasks':len(distinct),'native':{k:report[k]for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'fidelity':{'mathematical_banks':'complete','notation':'polynomial TeX normalized; bank order normalized in shared moderate profile','solution_sequence':'same shared instructional sentences and substitution steps; q-72605 includes unreduced coefficient row','source_preservation':'originals untouched'},'hashes':{str(p.relative_to(ROOT)):sha(p)for p in (HERE.with_suffix('.py'),HERE/'parser.py',HERE/'validate.py',HERE/'reference/source.json',HERE/'check-current-engine')}}
 (HERE/'validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
