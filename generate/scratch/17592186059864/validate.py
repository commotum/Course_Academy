"""Independent printed-math validation, complete source replay, actual app grading."""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path.insert(0,str(HERE))
from math_tools import expr,function,equivalent
s=importlib.util.spec_from_file_location('sum_rule_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
x=g.x;ENGINE=HERE/'check-current-engine'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,v):(HERE/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def build_engine():
 subprocess.run(['cargo','build','--release','--lib'],cwd=ROOT,check=True)
 deps=ROOT/'target/release/deps';edb=ROOT.parent/'EDB/target/release/deps';harness=ROOT/'generate/runs/current/check-engine.rs';libraries={name:max(deps.glob('lib'+name+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns) for name in ('course_academy_engine','serde_json')};cmd=['rustc','--edition=2024','-O',str(harness)]
 for name,p in libraries.items():cmd+=['--extern',name+'='+str(p)]
 cmd+=['-L','dependency='+str(edb),'-L','dependency='+str(deps),'-o',str(ENGINE)];subprocess.run(cmd,check=True);save('engine-build.json',{'harness_sha256':sha(harness),'libraries':{str(p):sha(p) for p in libraries.values()},'executable_sha256':sha(ENGINE)})
def fingerprint(q):return g.digest(str(g.sp.expand(function(q))))
def enum(v):return v[':db/ident'] if isinstance(v,dict) else v
def check_question(q):
 f=function(q);target=g.sp.diff(f,x);fields=q[':question/answer-fields'];assert len(fields)==1
 for text in (q[':question/problem'],q[':question/worked-solution']):assert text.count('$')%2==0 and text.count('{')==text.count('}'),'unbalanced formatting'
 field=fields[0];bank=field[':answer-field/choices'];vals=[expr(a[':answer/value']) for a in bank];kind=enum(field[':answer-field/type']);assert len(bank)==(5 if kind==':answer-field.type/radio' else 1)
 assert all(enum(a[':answer/type'])==':answer.type/math' and '$' not in a[':answer/value'] for a in bank)
 assert all(not equivalent(a,z) for i,a in enumerate(vals) for z in vals[i+1:]),'equivalent choices'
 correct=field[':answer-field/correct'];cid=correct[':answer/id'] if isinstance(correct,dict) else correct[1]
 assert [a[':answer/id'] for a,z in zip(bank,vals) if equivalent(z,target)]==[cid],'incorrect canonical answer'
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S);assert len(blocks)==1
 for row in blocks[0].split(r' \\ '):
  assert '& =' in row,'unrecognized solution row'
  rhs=row.split('& =',1)[1].strip().rstrip('.')
  def derivative(m):return '('+g.sp.sstr(g.sp.diff(expr(m[1]),x)).replace('**','^')+')'
  rhs=re.sub(r'\\frac\{\\text\{d\}\}\{\\text\{d\}x\}\((.*?)\)',derivative,rhs)
  assert equivalent(expr(rhs),target),('incorrect solution row',row)
 if kind==':answer-field.type/blank':assert '{{'+field[':answer-field/key']+'}}' in q[':question/problem']
 return q

def check(rec):
 q=rec['question'];m=rec['generation'];assert rec==g.generate(q[':question/difficulty'].split('/')[-1],m['seed'],m['template'],m['parameters']),'not exact generator replay';check_question(q);assert fingerprint(q)==m['mathematical_fingerprint'];return rec

def native(label,rec):
 f=rec['question'][':question/answer-fields'][0]
 if f[':answer-field/type']==':answer-field.type/radio':checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual radio grading'} for a in f[':answer-field/choices']]
 else:
  val=f[':answer-field/choices'][0][':answer/value'];z=expr(val);checks=[{'submitted':val,'expected':'accepted','purpose':'canonical blank'}, {'submitted':'('+val+')','expected':'accepted','purpose':'parenthesized equivalent'}, {'submitted':g.sp.sstr(z).replace('**','^'),'expected':'accepted','purpose':'simplified equivalent'}, {'submitted':val+'+1','expected':'rejected','purpose':'wrong constant'}, {'submitted':'0','expected':'rejected','purpose':'wrong zero'}]
 return {'label':label,'record':rec,'checks':checks}

def main():
 build_engine();inputs=[];replay=[];review=[];seen=set()
 for sid,(level,p) in g.PROFILES.items():
  rec=check(g.generate(level,0,sid,p));old=g.SOURCES[sid];q=rec['question'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
  assert q[':question/problem']==old[':question/problem'] and q[':question/worked-solution']==old[':question/worked-solution']
  assert [a[':answer/value'] for a in f[':answer-field/choices']]==[a[':answer/value'] for a in of[':answer-field/choices']]
  idx=next(i for i,a in enumerate(of[':answer-field/choices']) if a[':answer/id']==of[':answer-field/correct'][':answer/id']);assert f[':answer-field/correct'][1]==f[':answer-field/choices'][idx][':answer/id']
  replay.append({'source':sid,'matched_choices':len(f[':answer-field/choices']),'matched_distractors':len(f[':answer-field/choices'])-1,'complete_bank_match':True,'prompt_exact':True,'solution_exact':True})
  variant=check(g.generate(level,9,sid,g.candidates(sid)[0]));review.append('## '+sid+'\n\nOriginal\n\n'+g.markdown(rec)+'\n\nVariant\n\n'+g.markdown(variant))
  for params in g.candidates(sid):
   r=check(g.generate(level,0,sid,params));assert g.generate(level,99,sid,params)['question']==r['question'];assert fingerprint(r['question']) not in seen;seen.add(fingerprint(r['question']));inputs.append(native(sid+' '+str(params),r))
   # Independent real branch checks at negative x for odd cube-root sources.
   if sid=='q-339462':
    a=params['a']
    for z in (-8,-1,0,1,8):
     real_f=lambda t:t**a+g.sp.real_root(t,3)**4
     expected=a*g.sp.Integer(z)**(a-1)+g.sp.Rational(4,3)*g.sp.real_root(z,3)
     if z:assert g.sp.simplify(g.sp.limit((real_f(g.sp.Integer(z)+g.sp.Symbol('h',real=True))-real_f(g.sp.Integer(z)))/g.sp.Symbol('h',real=True),g.sp.Symbol('h',real=True),0)-expected)==0
     else:assert expected==0
 for level in ('easy','hard','unclassified'):
  try:g.batch(level,1,0)
  except ValueError:pass
  else:raise AssertionError('unsupported level accepted')
 for invalid in ({'a':0,'b':2},{'a':3,'b':1},{'a':3.0,'b':2}):
  try:g.generate('moderate',0,'q-10291',invalid)
  except ValueError:pass
  else:raise AssertionError('invalid parameters accepted')
 try:g.batch('moderate',21,0)
 except ValueError:pass
 else:raise AssertionError('finite count overrun accepted')
 save('source-replay.json',{'passed':True,'complete_banks_matched':2,'complete_banks_total':2,'distractors_matched':4,'distractors_total':4,'profiles':replay,'excluded_incomplete_sources':['q-1867','q-70476','q-70512'],'all_source_questions_retained':True});save('native-input.json',inputs);subprocess.run([str(ENGINE),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 save('previews.json',{'moderate':g.batch('moderate',5,1930)});(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 save('capabilities.json',{'supported_levels':['moderate'],'unsupported_levels':['easy','hard'],'reason':'Only moderate-rated complete source templates are established. Changing powers within the observed sum-rule structures supplies moderate variants; it does not establish easy/hard difficulty. This is a bounded source-evidence exception; new complete rated sources reopen classification.','finite_distinct_tasks':{'moderate':20},'unsupported_levels_filled':False,'shortage_remaining':{'easy':5,'hard':5}})
 files=(HERE.with_suffix('.py'),HERE/'validate.py',HERE/'math_tools.py',HERE/'source.json');save('validation.json',{'passed':True,'exhaustive_instances':len(inputs),'supported_levels':['moderate'],'distinct_tasks_by_level':{'moderate':len(seen)},'mathematical_checks':'Independent printed-function differentiation; every worked solution row; unique complete banks; real cube-root negative branch checks; deterministic seed invariance; boundaries and finite count limits','source_fidelity':'2/2 complete banks; 4/4 distractors; exact problem/solution/value notation at original parameters','native_grading':'Actual grade_field canonical, equivalent, incorrect entries and every radio choice','actual_engine_build':json.loads((HERE/'engine-build.json').read_text()),'hashes':{str(p.relative_to(ROOT)):sha(p) for p in files}})
 print('Validated',len(inputs),'bounded distinct instances')
if __name__=='__main__':main()
