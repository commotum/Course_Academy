"""Source replay, printed mathematics, deterministic boundaries and actual grader."""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE))
from math_tools import expr,function,equivalent
s=importlib.util.spec_from_file_location('second_derivative_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
x=g.x;ENGINE=HERE/'check-current-engine'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,v):(HERE/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def build_engine():
 subprocess.run(['cargo','build','--release','--lib'],cwd=ROOT,check=True)
 deps=ROOT/'target/release/deps';edb=ROOT.parent/'EDB/target/release/deps';harness=ROOT/'generate/runs/current/check-engine.rs'
 libraries={name:max(deps.glob('lib'+name+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns) for name in ('course_academy_engine','serde_json')}
 cmd=['rustc','--edition=2024','-O',str(harness)]
 for name,p in libraries.items():cmd+=['--extern',name+'='+str(p)]
 cmd+=['-L','dependency='+str(edb),'-L','dependency='+str(deps),'-o',str(ENGINE)];subprocess.run(cmd,check=True)
 save('engine-build.json',{'harness_sha256':sha(harness),'libraries':{str(p):sha(p) for p in libraries.values()},'executable_sha256':sha(ENGINE)})
def fingerprint(q):return g.digest(str(g.sp.expand(g.sp.diff(function(q),x,2))))
def expected(q):
 val=g.sp.diff(function(q),x,2)
 # The partial blank's fixed suffix is part of the displayed equation, not the field.
 m=re.search(r'\{\{field-1\}\}\s*\$(.*?)\$',q[':question/problem'],re.S)
 return g.sp.simplify(val-expr(m[1])) if m else val

def check_question(q):
 f=function(q);target=expected(q)
 for text in (q[':question/problem'],q[':question/worked-solution']):
  assert text.count('$')%2==0 and text.count('{')==text.count('}'),'unbalanced formatting'
 fields=q[':question/answer-fields'];assert len(fields)==1
 field=fields[0];bank=field[':answer-field/choices'];vals=[expr(a[':answer/value']) for a in bank]
 assert len(bank)==(5 if field[':answer-field/type']==':answer-field.type/radio' else 1)
 assert all(a[':answer/type']==':answer.type/math' and '$' not in a[':answer/value'] for a in bank)
 assert all(not equivalent(a,z) for i,a in enumerate(vals) for z in vals[i+1:]),'equivalent choices'
 assert [a[':answer/id'] for a,z in zip(bank,vals) if equivalent(z,target)]==[field[':answer-field/correct'][1]],'incorrect canonical answer'
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S);assert len(blocks)==2
 for bi,block in enumerate(blocks):
  rhs_target=g.sp.diff(f,x,bi+1)
  for row in block.split(r' \\ '):
   if '& =' not in row:continue
   rhs=row.split('& =',1)[1].strip();prefix=r'\frac{\text{d}}{\text{d}x}('
   if rhs.startswith(prefix):
    assert rhs.endswith(')');z=g.sp.diff(expr(rhs[len(prefix):-1]),x)
   else:z=expr(rhs)
   assert equivalent(z,rhs_target),(bi,rhs,z,rhs_target)
 if field[':answer-field/type']==':answer-field.type/blank':assert '{{'+field[':answer-field/key']+'}}' in q[':question/problem']
 return q

def check(rec):
 q=rec['question'];m=rec['generation']
 assert rec==g.generate(q[':question/difficulty'].split('/')[-1],m['seed'],m['template'],m['parameters']),'not exact generator replay'
 check_question(q);assert fingerprint(q)==m['mathematical_fingerprint']
 return rec

def native(label,rec):
 f=rec['question'][':question/answer-fields'][0]
 if f[':answer-field/type']==':answer-field.type/radio':checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual radio grading'} for a in f[':answer-field/choices']]
 else:
  val=f[':answer-field/choices'][0][':answer/value'];z=expr(val)
  checks=[{'submitted':val,'expected':'accepted','purpose':'canonical blank fragment'}, {'submitted':'('+val+')','expected':'accepted','purpose':'parenthesized equivalent'}, {'submitted':g.sp.sstr(z).replace('**','^'),'expected':'accepted','purpose':'equivalent simplified expression'}, {'submitted':val+'+1','expected':'rejected','purpose':'wrong fragment'}, {'submitted':'0','expected':'rejected','purpose':'wrong zero'}]
  if rec['generation']['template']=='q-342970':checks.append({'submitted':g.sp.latex(g.sp.diff(function(rec['question']),x,2)),'expected':'rejected','purpose':'full derivative is wrong for partial blank'})
 return {'label':label,'record':rec,'checks':checks}

def main():
 build_engine();inputs=[];replay=[];review=[];bylevel={l:set() for l in g.SUPPORTED_LEVELS};distractors=0
 for sid,(level,p) in g.PROFILES.items():
  rec=check(g.generate(level,0,sid,p));old=g.SOURCES[sid];q=rec['question'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
  assert q[':question/problem']==old[':question/problem'] and q[':question/worked-solution']==old[':question/worked-solution']
  assert [a[':answer/value'] for a in f[':answer-field/choices']]==[a[':answer/value'] for a in of[':answer-field/choices']]
  idx=next(i for i,a in enumerate(of[':answer-field/choices']) if a[':answer/id']==of[':answer-field/correct'][':answer/id']);assert f[':answer-field/correct'][1]==f[':answer-field/choices'][idx][':answer/id']
  nd=len(f[':answer-field/choices'])-1;distractors+=nd;replay.append({'source':sid,'matched_choices':len(f[':answer-field/choices']),'matched_distractors':nd,'complete_bank_match':True,'prompt_exact':True,'solution_exact':True})
  variant=check(g.generate(level,7,sid,{'k':2}));review.append('## '+sid+'\n\nOriginal\n\n'+g.markdown(rec)+'\n\nVariant (k=2)\n\n'+g.markdown(variant))
  for params in g.candidates(sid):
   r=check(g.generate(level,0,sid,params));assert g.generate(level,99,sid,params)['question']==r['question']
   assert r['generation']['mathematical_fingerprint'] not in bylevel[level],'duplicate mathematical task'
   bylevel[level].add(r['generation']['mathematical_fingerprint']);inputs.append(native(sid+' '+str(params),r))
  for invalid in ({'k':0},{'k':7},{'k':-1},{'k':1.5}):
   try:g.generate(level,0,sid,invalid)
   except ValueError:pass
   else:raise AssertionError('Invalid parameter accepted')
 for level in ('hard','unclassified'):
  try:g.batch(level,1,0)
  except ValueError:pass
  else:raise AssertionError('Unsupported level accepted')
 save('source-replay.json',{'passed':True,'complete_banks_matched':len(replay),'complete_banks_total':len(replay),'distractors_matched':distractors,'distractors_total':distractors,'profiles':replay,'excluded_incomplete_sources':{'q-10894':'no difficulty, solution, or correct designation','q-1873':'no answer fields'},'all_source_questions_retained':True})
 save('native-input.json',inputs);subprocess.run([str(ENGINE),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 save('previews.json',{l:g.batch(l,5,1917) for l in g.SUPPORTED_LEVELS});(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 save('capabilities.json',{'supported_levels':list(g.SUPPORTED_LEVELS),'unsupported_levels':['hard'],'reason':'No hard-rated source template is established by the 10 practice sources (7 easy, 2 moderate, 1 unrated) or the unrated canonical example. k=1..6 scaling does not introduce a hard method. This is a bounded evidence limitation, not a proof that hard questions are impossible; new sources reopen classification.','finite_distinct_tasks':{l:len(v) for l,v in bylevel.items()},'sampling':'k in 1..6, same positive factor applied to every coefficient and complete source bank; explicit extension','shortage_remaining':{'hard':5},'unsupported_levels_filled':False})
 files=(HERE.with_suffix('.py'),HERE/'validate.py',HERE/'math_tools.py',HERE/'source.json')
 save('validation.json',{'passed':True,'exhaustive_instances':len(inputs),'mathematical_checks':'Independent printed prompt differentiation twice; full bank equivalence and uniqueness; every solution row including derivative inputs; partial blank suffix; boundaries and deterministic replay','source_fidelity':f'{len(replay)}/{len(replay)} complete source banks; {distractors}/{distractors} distractors; exact prompt/solution/value notation at source parameters','native_grading':'Real grade_field for all source and generated banks, canonical/equivalent/wrong blank fragments','supported_levels':list(g.SUPPORTED_LEVELS),'distinct_tasks_by_level':{l:len(v) for l,v in bylevel.items()},'actual_engine_build':json.loads((HERE/'engine-build.json').read_text()),'hashes':{str(p.relative_to(ROOT)):sha(p) for p in files}})
 print('Validated',len(inputs),'bounded instances')
if __name__=='__main__':main()
