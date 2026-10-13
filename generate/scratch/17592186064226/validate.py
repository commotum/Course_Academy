"""Complete bank replay, independent displayed mathematics and actual learner grading."""
import importlib.util,json,hashlib,sys,subprocess,re,functools
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path.insert(0,str(HERE))
import printed as p
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
scalar=p.scalar;prompt=lambda t:p.integral(t)[0];same=p.same;X=p.x;native=[]
def normalize_value(v):return g.sp.trigsimp(v.rewrite(g.sp.sin))
def checks_for(q):
 f=q[':question/answer-fields'][0];cid=f[':answer-field/correct'][1];ans=next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==cid)
 if f[':answer-field/type']==':answer-field.type/radio':return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==cid else'rejected','purpose':'all owned radio choices'}for a in f[':answer-field/choices']]
 return [{'submitted':ans,'expected':'accepted','purpose':'canonical exact blank'},{'submitted':'('+ans+')+0','expected':'accepted','purpose':'equivalent exact blank'},{'submitted':g.sp.latex(scalar(ans)+1),'expected':'rejected','purpose':'incorrect blank'}]
def validate(rec,collect=True):
 q=rec['question'];assert rec['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
 t=rec['generation']['template'];r=rec['generation']['parameters']['r'];l=q[':question/difficulty'].split('/')[-1];assert l in g.SUPPORTED_LEVELS and l==g.level(t)
 assert len(q[':question/answer-fields'])==1
 f=q[':question/answer-fields'][0];of=g.SOURCES[t][':question/answer-fields'][0]
 assert f[':answer-field/type']==of[':answer-field/type'][':db/ident']and f[':answer-field/key']==of[':answer-field/key']
 assert len(f[':answer-field/choices'])==len(of[':answer-field/choices'])
 vals=[scalar(a[':answer/value'])for a in f[':answer-field/choices']];assert all(not same(a,b)for i,a in enumerate(vals)for b in vals[i+1:])
 expr,a,b=p.integral(q[':question/problem']);old,lo,hi=p.integral(g.SOURCES[t][':question/problem'])
 assert same(expr,old.subs(X,r*X));assert (a,b)==(None if lo is None else lo/r,None if hi is None else hi/r)
 anti=g.PRIMITIVES[t].subs(X,r*X)/r;assert same(g.sp.diff(anti,X),expr)
 expected=anti+p.C if a is None else g.sp.simplify(anti.subs(X,b)-g.sp.limit(anti,X,a,dir='+'))
 cid=f[':answer-field/correct'][1];ans=next(scalar(z[':answer/value'])for z in f[':answer-field/choices']if z[':answer/id']==cid);assert same(ans,expected)
 assert sum(same(z,expected)for z in vals)==1
 # Full mathematical bank transport, including every distractor, at all bounds.
 transported=[scalar(z[':answer/value']).subs(p.C,0).subs(X,r*X)/r+(p.C if a is None else 0)for z in of[':answer-field/choices']]
 remaining=list(vals)
 for z in transported:
  matches=[i for i,w in enumerate(remaining)if same(z,w)];assert len(matches)==1;remaining.pop(matches[0])
 assert not remaining
 assert g.fingerprint(q)==rec['generation']['mathematical_fingerprint']
 if r>1:
  last=re.findall(r'\$\$\s*(.*?)\s*\$\$',q[':question/worked-solution'],re.S)[-1];lhs,rhs=last.split('=',1)
  assert p.integral(lhs)==(expr,a,b)and same(scalar(rhs),expected)
  assert re.sub(r'(?<![A-Za-z])x(?![A-Za-z])','t',g.SOURCES[t][':question/worked-solution'])in q[':question/worked-solution']
 else:assert q[':question/worked-solution']==g.SOURCES[t][':question/worked-solution']
 for text in (q[':question/problem'],q[':question/worked-solution']):assert text.count('$')%2==0 and text.count('{')==text.count('}')
 replay=g.generate(l,rec['generation']['seed']+999,t,{'r':r});assert replay['question']==q,'identity/order must not depend on seed'
 if collect:native.append({'label':q[':question/id'],'record':rec,'checks':checks_for(q)})
def validate_current(q,collect=True,mid=None):
 # Source capture or authored UUID, never infer a level from missing facts.
 mid=mid or q.get(':question/math-academy-id')
 if mid in g.SOURCES:
  rec=g.generate(g.level(mid),0,mid,{'r':1});expected=rec['question']
  assert q[':question/problem']==expected[':question/problem'] and q[':question/worked-solution']==expected[':question/worked-solution']
  f=q[':question/answer-fields'][0];ef=expected[':question/answer-fields'][0]
  assert f[':answer-field/type']==ef[':answer-field/type']and len(f[':answer-field/choices'])==len(ef[':answer-field/choices'])
  cid=f[':answer-field/correct'][1];correct=next(scalar(z[':answer/value'])for z in f[':answer-field/choices']if z[':answer/id']==cid)
  ecid=ef[':answer-field/correct'][1];ecorrect=next(scalar(z[':answer/value'])for z in ef[':answer-field/choices']if z[':answer/id']==ecid)
  assert same(correct,ecorrect)
  vals=[scalar(z[':answer/value'])for z in f[':answer-field/choices']];assert all(not same(a,b)for i,a in enumerate(vals)for b in vals[i+1:])
  validate(rec,False)
  rec['question']=q
 else:
  rows=json.loads((HERE/'validated-records.json').read_text());rec=next(z for z in rows if z['question'][':question/id']==q[':question/id']);assert q==rec['question'];validate(rec,False)
 if collect:native.append({'label':q[':question/id'],'record':rec,'checks':checks_for(q)})
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build_engine():
 deps=ROOT/'target/release/deps';edb=ROOT.parent/'EDB/target/release/deps';harness=ROOT/'generate/runs/current/check-engine.rs';libraries={name:max(deps.glob('lib'+name+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns)for name in ('course_academy_engine','serde_json')};cmd=['rustc','--edition=2024','-O',str(harness)]
 for name,path in libraries.items():cmd+=['--extern',name+'='+str(path)]
 cmd+=['-L','dependency='+str(edb),'-L','dependency='+str(deps),'-o',str(HERE/'check-current-engine')];subprocess.run(cmd,check=True)
 (HERE/'engine-build.json').write_text(json.dumps({'harness_sha256':sha(harness),'libraries':{str(p):sha(p)for p in libraries.values()},'executable_sha256':sha(HERE/'check-current-engine')},indent=2))
def main():
 rows=[];replay=[];review=[];unique={l:set()for l in g.SUPPORTED_LEVELS}
 canonical=g.SOURCE['kp'][':knowledge-point/canonical-example'];ce,cl,ch=p.integral(canonical[':question/problem']);assert same(ce,g.sp.sin(X)/g.sp.cos(X)**2)and cl==0 and ch==g.sp.pi/3;assert g.fingerprint(canonical)
 for t,old in g.SOURCES.items():
  print('Validate',t,flush=True)
  for r in range(1,7):
   rec=g.generate(g.level(t),19,t,{'r':r});validate(rec);rows.append(rec)
   if r>1:unique[g.level(t)].add(rec['generation']['mathematical_fingerprint'])
   if r==1:
    f=rec['question'][':question/answer-fields'][0];of=old[':question/answer-fields'][0]
    assert [z[':answer/value']for z in f[':answer-field/choices']]==[z[':answer/value']for z in of[':answer-field/choices']]
    assert f[':answer-field/choices'][[z[':answer/id']for z in f[':answer-field/choices']].index(f[':answer-field/correct'][1])][':answer/value']==of[':answer-field/correct'][':answer/value']
    replay.append({'source':t,'field':of[':answer-field/type'][':db/ident'],'profile':t,'complete_bank':True,'matched_options':len(f[':answer-field/choices']),'matched_distractors':len(f[':answer-field/choices'])-1,'missing':[],'extra':[],'correct_designation':True,'markdown_replay':'exact'})
   if r==2:review.append({'source':old,'variant':rec})
 try:g.generate('hard')
 except ValueError:pass
 else:raise AssertionError('hard accepted')
 build_engine();(HERE/'native-input.json').write_text(json.dumps(native,indent=2));subprocess.run([str(HERE/'check-current-engine'),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
 report=json.loads((HERE/'native-report.json').read_text());assert report['documented_unresolved_checks']==0
 (HERE/'validated-records.json').write_text(json.dumps(rows,indent=2));(HERE/'source-replay.json').write_text(json.dumps(replay,indent=2));(HERE/'review.json').write_text(json.dumps(review,indent=2))
 md=['# Source and variant review','Frequency transport preserves the entire source identity-reduction sequence using substitution t=r*x. Source bank values are transported as complete mathematical objects. Prompt rendering uses standard SymPy TeX. The blank and radio versions of a mathematical task share one novelty fingerprint. All original banks and correct designations replay exactly.']
 for z in review:
  md+=['## '+z['source'][':question/math-academy-id']]
  for label,q in [('Source',z['source']),('Variant',z['variant']['question'])]:md+=[label,q[':question/problem'],str([a[':answer/value']for a in q[':question/answer-fields'][0][':answer-field/choices']]),q[':question/worked-solution']]
 (HERE/'review.md').write_text('\n\n'.join(md))
 files=[HERE.with_suffix('.py'),HERE/'printed.py',HERE/'validate.py',HERE/'source.json',HERE/'check-current-engine',HERE/'validated-records.json']
 result={'passed':True,'source_basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'complete_banks_matched':len(replay),'source_options_matched':sum(z['matched_options']for z in replay),'source_distractors_matched':sum(z['matched_distractors']for z in replay),'supported_levels':list(g.SUPPORTED_LEVELS),'unsupported_levels':['hard'],'finite_distinct_tasks':{l:len(s)for l,s in unique.items()},'validated_instances':len(rows),'native':{k:report[k]for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'hashes':{str(p.relative_to(ROOT)):sha(p)for p in files}}
 (HERE/'validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
