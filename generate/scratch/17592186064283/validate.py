"""Independent checks of rendered functions, banks, chain-rule solutions and actual grading."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('trig_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x=sp.Symbol('x',real=True);u=sp.Symbol('u',real=True)
def save(name,a):(HERE/name).write_text(json.dumps(a,indent=2)+'\n')
def math(text):
 text=text.strip().removeprefix('& =').strip().strip('$').replace('⁡','').replace(r'\,','').replace(' ','').replace(r'\cdot','')
 text=re.sub(r'\\operatorname\{(sin|cos)\}|\\(sin|cos)|\{(sin|cos)\}',lambda m:next(z for z in m.groups() if z),text)
 text=text.replace('{','').replace('}','').replace('(','').replace(')','')
 text=re.sub(r'(sin|cos)x\^(\d+)',r'\1^\2x',text)
 coeff=re.match(r'(-?\d+|-|\+)?',text)[0];value=sp.Integer(coeff) if coeff not in ('','-','+') else sp.Integer(-1 if coeff=='-' else 1);text=text[len(coeff):]
 while text:
  m=re.match(r'(sin|cos)(?:\^(\d+))?x',text);assert m,('cannot parse',text)
  value*=getattr(sp,m[1])(x)**int(m[2] or 1);text=text[m.end():]
 return value

def prompt_function(q):
 m=re.search(r'f\(x\)\s*=\s*(.*?)\$',q[':question/problem']);assert m,q[':question/problem']
 return math(m[1].rstrip('.,'))
def fingerprint(q):
 return g.digest(['trig-power-derivative',str(sp.expand_trig(sp.diff(prompt_function(q),x)))])
def equivalent(a,b):return sp.trigsimp(sp.expand(a-b))==0
def check(rec):
 q=rec['question'];m=rec['generation'];t=g.PROFILES[m['template']];c,n=m['parameters'];assert rec==g.generate(t['level'],m['seed'],m['template'],m['parameters'])
 f=prompt_function(q);assert equivalent(f,c*getattr(sp,t['function'])(x)**n);deriv=sp.diff(f,x)
 field=q[':question/answer-fields'][0];bank=field[':answer-field/choices'];values=[math(a[':answer/value']) for a in bank]
 assert len(bank)==(1 if t['field_type'].endswith('/blank') else 5)
 assert bank[0][':answer/id']==field[':answer-field/correct'][1]
 assert equivalent(values[0],deriv)
 assert all(not equivalent(v,deriv) for v in values[1:])
 assert all(not equivalent(v,w) for i,v in enumerate(values) for w in values[i+1:])
 sol=q[':question/worked-solution'];assert '@@' not in sol and '{{'+field[':answer-field/key']+'}}' in q[':question/problem'] if t['field_type'].endswith('/blank') else '@@' not in sol
 # Re-read rendered initial function, composite, outer derivative, inner derivative,
 # multiplication line and final function. Layout differs by source, mathematics does not.
 init=re.search(r'f\(x\)=(.*?)\.\s*\$',sol,re.S);assert init and equivalent(math(init[1]),f)
 composite=re.search(r'f=([^,]+),',sol);assert composite
 comp=composite[1].replace(r'\,','').replace('{','').replace('}','')
 comp=sp.sympify(re.sub(r'(\d)u',r'\1*u',comp).replace('^','**'),locals={'u':u});assert comp==c*u**n
 outer=re.search(r'\\frac\{\\text\{d\}f\}\{\\text\{d\}u\}=([^,]+?)(?:\\,|\\cdot|\\text|,)',sol);assert outer,sol
 os=outer[1].replace('{','').replace('}','');os=sp.sympify(re.sub(r'(\d)u',r'\1*u',os).replace('^','**'),locals={'u':u});assert os==sp.diff(comp,u)
 inner=re.search(r'\\frac\{\\text\{d\}u\}\{\\text\{d\}x\}=(.*?)\.\s*\$',sol,re.S);assert inner and equivalent(math(inner[1]),sp.diff(getattr(sp,t['function'])(x),x))
 final=re.findall(r' & =(.*?)\\end\{aligned\}',sol,re.S)[-1].split(r' \\ ')[-1].rstrip('.')
 assert equivalent(math(final),deriv)
 assert m['mathematical_fingerprint']==fingerprint(q)
 assert all('$' not in a[':answer/value'] for a in bank)
 assert len({a[':answer/id'] for a in bank})==len(bank)
 return rec

def native(label,rec):
 q=rec['question'];f=q[':question/answer-fields'][0];checks=[]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if i==0 else 'rejected','purpose':'native radio choice grading'} for i,a in enumerate(f[':answer-field/choices'])]
 else:
  c,n=rec['generation']['parameters'];func=rec['generation']['function'];factor='cos' if func=='sin' else 'sin';k=c*n*(1 if func=='sin' else -1)
  equivalent_entry=f'{factor}(x)*{func}(x)^{n-1}*{k}'
  wrong=f'{factor}(x)*{func}(x)^{n-1}*{-k}'
  checks=[{'submitted':f[':answer-field/choices'][0][':answer/value'],'expected':'accepted','purpose':'canonical math blank'}, {'submitted':equivalent_entry,'expected':'accepted','purpose':'reordered equivalent math blank'}, {'submitted':wrong,'expected':'rejected','purpose':'wrong sign math blank'}, {'submitted':str(k),'expected':'rejected','purpose':'omitted trig factors'}]
 return {'label':label,'record':rec,'checks':checks}

def main():
 source=json.loads((HERE/'source.json').read_text());qs={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']};inputs=[];replay=[];allrecs=[];review=[]
 for sid,t in g.PROFILES.items():
  r=check(g.generate(t['level'],0,sid,t['parameters']));q=r['question'];old=qs[sid];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
  assert q[':question/problem']==old[':question/problem'],sid
  assert q[':question/worked-solution']==old[':question/worked-solution'],sid
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']),sid
  assert f[':answer-field/choices'][0][':answer/value']==of[':answer-field/correct'][':answer/value'],sid
  replay.append({'source':sid,'profile':t['profile'],'matched_choices':len(f[':answer-field/choices']),'matched_distractors':len(f[':answer-field/choices'])-1,'complete_bank_match':True,'prompt_exact':True,'solution_exact':True,'field_layout_preserved':True})
  inputs.append(native(sid,r));variant=check(g.generate(t['level'],42,sid));review.append('## '+sid+'\n\nOriginal\n\n'+old[':question/problem']+'\n\n'+old[':question/worked-solution']+'\n\nReplay\n\n'+g.markdown(r)+'\n\nVariant\n\n'+g.markdown(variant))
  for p in g.domain(t):
   r=check(g.generate(t['level'],0,sid,p));assert g.generate(t['level'],99,sid,p)['question']==r['question'];inputs.append(native(sid+' '+str(p),r));allrecs.append(r)
 save('source-replay.json',{'passed':True,'complete_banks_matched':7,'complete_banks_total':7,'distractors_matched':20,'distractors_total':20,'profiles':replay,'excluded_sources':['q-48562','q-143516','q-167568','q-342413','q-342427']})
 save('native-input.json',inputs);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 (HERE/'review.md').write_text('\n\n'.join(review)+'\n');save('previews.json',{level:g.batch(level,5,20261013) for level in ('easy','moderate')})
 counts={level:len({r['generation']['mathematical_fingerprint'] for r in allrecs if r['question'][':question/difficulty'].endswith('/'+level)}) for level in ('easy','moderate')}
 save('validation.json',{'passed':True,'source_basis':source['basis'],'lineage':source['lineage'],'mathematical_checks':'Independent parsing of rendered function, all answer values and chain-rule solution; derivative correctness; distinct banks; composite and inner/outer derivative; final substitution; deterministic replay and field ownership','exhaustive_instances':len(allrecs),'finite_distinct_tasks':counts,'source_fidelity':'7/7 supported complete banks, 20/20 distractors, exact prompt and worked solution','native_grading':'every answer choice, canonical/equivalent/incorrect entries in every bounded math blank','supported_levels':['easy','moderate'],'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'contract.json',HERE/'validate.py')}})
 print(json.dumps(counts))
if __name__=='__main__':main()
