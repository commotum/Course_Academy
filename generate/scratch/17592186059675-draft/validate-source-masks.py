"""Exhaustive changed-parameter source prose/stage/whole-bank checks and native grading."""
import copy,hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('v',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g

def prose(text):return re.sub(r'\$\$.*?\$\$|\$[^$]*\$','<MATH>',text,flags=re.S)
def row_counts(text):return [len(block.split('\\\\')) for block in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',text,re.S)]
def main():
 reports=[];records=[];negatives=[]
 for t,(level,anchor) in g.PROFILES.items():
  old=g.SOURCES[t];op=g.normalize_prose(old[':question/problem']);os=g.normalize_prose(old[':question/worked-solution']);total=changed=0
  for p in g.candidates(t):
   r=g.generate(level,template=t,parameters=p);v.check(r);q=r['question'];f=q[':question/answer-fields'][0]
   assert prose(q[':question/problem'])==prose(op)
   assert prose(q[':question/worked-solution'])==prose(os)
   assert row_counts(q[':question/worked-solution'])==row_counts(os)
   _,_,_,_,bank=g.model(t,p);assert len(f[':answer-field/choices'])==len(bank)
   for a,expected in zip(f[':answer-field/choices'],bank):assert sp.simplify(v.printed.scalar(a[':answer/value'])-expected)==0
   if p==anchor:
    assert q[':question/problem']==op
    repaired=os.replace('{f}^{′}(30)',r'{y}^{′}(\frac{\pi }{6})').replace('{f}^{′}(x)','{y}^{′}(x)') if t=='q-1900' else os
    assert q[':question/worked-solution']==repaired
    assert [a[':answer/value'] for a in f[':answer-field/choices']]==[g.normalize_tex(a[':answer/value']) for a in old[':question/answer-fields'][0][':answer-field/choices']]
   else:changed+=1
   total+=1;records.append(r)
  reports.append({'source_id':t,'eligible_parameter_instances':total,'changed_instances':changed,'full_prompt_prose_and_layout':True,'full_solution_prose_and_ordered_stages':True,'every_whole_bank_option_independently_matched':True,'anchor_bytes_via_same_render_path':True})
  # Change only the formal differentiation input, holding subsequent rows/key/prompt constant.
  r=g.generate(level,template=t,parameters=list(g.candidates(t))[-1]);bad=copy.deepcopy(r);sol=bad['question'][':question/worked-solution'];prefix=r'\frac{\text{d}}{\text{d}x}(';start=sol.index(r'\begin{aligned}');index=sol.index(prefix,start)+len(prefix);bad['question'][':question/worked-solution']=sol[:index]+'1+'+sol[index:]
  try:v.check(bad)
  except AssertionError:negatives.append({'source_id':t,'stale_formal_input_rejected':True})
  else:raise AssertionError('Formal-input mutation escaped')
 for kw in ({'profile':'unrecognized'},{'field_type':'checkbox'},{'field_type':'text'},{'field_type':'radio','template':'q-341383'},{'mode':'unknown'}):
  try:g.generate('easy',**kw)
  except ValueError:negatives.append({'rejected_unsupported_contract':kw})
  else:raise AssertionError('Unsupported contract accepted')
 for l in g.SUPPORTED_LEVELS:
  r=g.generate(l,template='independent-'+l);assert r['generation']['role']=='authored extension'
 v.save('source-mask-validation.json',{'passed':True,'eligible_instances':len(records),'changed_instances':len(records)-5,'results':reports,'negative_checks':negatives,'no_original_parameter_bypass':True})
 v.save('source-mask-native-input.json',[v.native(r,t+'-'+str(i)) for i,r in enumerate(records) for t in [r['generation']['template']]])
 subprocess.run([str(HERE/'check-engine'),str(HERE/'source-mask-native-input.json'),str(HERE/'source-mask-native-grading.json')],check=True)
 (HERE/'source-mask-review.md').write_text('\n\n'.join('## '+t+' changed input\n\n'+g.markdown(g.generate(l,template=t,parameters=list(g.candidates(t))[-1])) for t,(l,p) in g.PROFILES.items())+'\n')
 print('All source masks passed:',len(records),'full prompt/solution/bank instances; negative contracts/formal inputs; native grader')
if __name__=='__main__':main()
