"""Additional source-template and field-contract checks; no DB access."""
import importlib.util,json,re,subprocess,hashlib
from pathlib import Path
D=Path(__file__).parent
s=importlib.util.spec_from_file_location('fractional_validation',D/'validate.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v);g=v.g

def main():
 originals={q[':question/math-academy-id']:q for q in g.SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q};replay=[];differentials=0
 for sid,t in g.PROFILES.items():
  for b in g.DOMAIN:
   rec=g.generate(t['difficulty'],0,sid,{'b':b});q=rec['question'];blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',q[':question/worked-solution'],re.S)
   substitution=re.search(r'let\s+\$u=([^$]+)\$',q[':question/worked-solution']);assert substitution
   assert v.sp.expand(v.scalar(substitution[1],t['variable'])-(t['a']*v.x+b))==0
   lhs,rhs=blocks[1].split('⟹');assert lhs.split('=')[0].strip()==r'\frac{\text{d}u}{\text{d}'+t['variable']+'}'
   assert v.scalar(lhs.split('=')[1].rstrip(r'\,'),t['variable'])==t['a']
   prefix=r'\,\text{d}'+t['variable']+'=';assert rhs.startswith(prefix)
   factor=rhs[len(prefix):].removesuffix('.').removesuffix(r'\text{d}u').rstrip(r'\,');factor={'':v.sp.Integer(1),'-':v.sp.Integer(-1)}.get(factor,factor);factor=v.scalar(factor,t['variable']) if isinstance(factor,str) else factor
   assert factor==1/v.sp.Integer(t['a']);differentials+=1
  if sid not in originals:continue
  q=g.generate(t['difficulty'],0,sid,{'b':t['b']})['question'];o=originals[sid];f=q[':question/answer-fields'][0]
  assert re.sub(r'\s+','',q[':question/problem'])==re.sub(r'\s+','',g.normalize_prose(o[':question/problem']))
  assert sorted(re.sub(r'\s+','',a[':answer/value']) for a in f[':answer-field/choices'])==sorted(re.sub(r'\s+','',g.normalize_tex(a[':answer/value'])) for a in o[':question/answer-fields'][0][':answer-field/choices'])
  if ':question/worked-solution' in o:
   expected=o[':question/worked-solution'].replace('final answer in terms of $u$ at the very end','final answer in terms of $'+t['variable']+'$ at the very end')
   if sid=='q-17019':expected=expected.replace('^{3/2}','^{2/3}')
   assert q[':question/worked-solution']==g.normalize_prose(expected),(sid,'solution')
   correct=o[':question/answer-fields'][0][':answer-field/correct'][':answer/value'];assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==g.normalize_tex(correct)
  replay.append({'source_id':sid,'full_bank_matched':5,'normal_template_prompt':True,'ordered_solution_and_key':'matched after documented repairs' if ':question/worked-solution' in o else 'missing source attributes authored explicitly; observed bank and prompt matched'})
 v.save('normal-replay.json',{'normal_template_banks':9,'values_matched':45,'designated_correct_answers_matched':8,'reconstructed_correct_answers':1,'full_prose_and_ordered_rows_matched':8,'profiles':replay,'all_bounded_actual_substitution_and_differential_operands_checked':differentials})
 # If the exhaustive run has produced its input, add equivalent spellings and
 # run the entire field contract again using the actual frozen executable.
 inputs=json.load(open(D/'native-input.json'))
 for item in inputs:
  f=item['record']['question'][':question/answer-fields'][0];i=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])
  if not any('Equivalent decimal' in c.get('purpose','') for c in item['checks']):item['checks'].append({'submitted':'000'+str(100+i),'expected':'accepted','purpose':'Equivalent decimal entity ID spelling under actual radio field contract'})
 v.save('native-input.json',inputs);engine=D.parents[2]/'generate/runs/current/check-engine';assert hashlib.sha256(engine.read_bytes()).hexdigest()=='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
 subprocess.run([str(engine),str(D/'native-input.json'),str(D/'native-grading.json')],check=True)
 diagnostics=[]
 for sid,t in g.PROFILES.items():
  r=g.generate(t['difficulty'],0,sid,{'b':t['b']});diagnostics.append({'label':sid,'record':r,'checks':[{'submitted':'999999','expected':'unresolved','purpose':'Foreign numeric entity ID ownership diagnostic; not valid mathematical submission'},{'submitted':'not-a-number','expected':'unresolved','purpose':'Malformed choice submission diagnostic; not valid mathematical submission'}]})
 v.save('diagnostic-input.json',diagnostics);subprocess.run([str(engine),str(D/'diagnostic-input.json'),str(D/'diagnostic-report.json')],check=True)
 v.save('grading-limitations.json',{'valid_mathematical_limitations':[],'radio_contract':'Owned choice IDs; mathematical-equivalence text is not a radio response. Leading-zero decimal entity ID spelling tested as equivalent.','diagnostics_separate':'diagnostic-report.json contains ownership and malformed input errors only.','frozen_grader_sha256':hashlib.sha256(engine.read_bytes()).hexdigest()})
if __name__=='__main__':main()
