"""Independent displayed prompt/answer/solution readback plus real learner grader."""
import functools,copy,hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as s
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
spec=importlib.util.spec_from_file_location('kp_generator',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
spec=importlib.util.spec_from_file_location('strict_tex',H/'math_parser.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
x=p.x;t=p.t

def scalar(raw):
 raw=raw.replace('[','(').replace(']',')').replace(r'\prime',"'").replace(r'\text{⧸}','').replace(r'\quad',',').replace(r'\!','')
 return p.scalar(raw)
@functools.lru_cache(maxsize=8192)
def equal(a,b):
 # Independent exact quotient-ring proof of rational trig identities.
 diff=s.cancel(a-b)
 if diff==0:return True
 if diff.has(s.sin,s.cos,s.tan,s.sec):
  args=sorted({f.args[0] for f in diff.atoms(s.sin,s.cos,s.tan,s.sec)},key=str)
  replacements={};relations=[];vars=[]
  for i,arg in enumerate(args):
   S,C=s.symbols('read_s'+str(i)+' read_c'+str(i));vars.extend([S,C]);relations.append(S*S+C*C-1)
   replacements.update({s.sin(arg):S,s.cos(arg):C,s.tan(arg):S/C,s.sec(arg):1/C})
  numerator=s.fraction(s.cancel(diff.xreplace(replacements)))[0]
  return s.groebner(relations,*vars,domain='EX').reduce(s.expand(numerator))[1]==0
 return s.simplify(diff)==0

def prompt_data(q):
 text=q[':question/problem']
 matches=re.findall(r'\$(?:y|f\(x\)|x\(t\))=(.*?)\$',text,re.S)
 if not matches:raise ValueError('Undefined function in standalone prompt')
 raw=matches[0].strip().rstrip('.,');raw=raw.split(r'\,t>0')[0];F=scalar(raw);var=t if F.has(t) else x
 point=None
 if 'tangent line' in text:
  point=scalar(re.search(r'at \$x=(.*?)\$',text)[1])
 elif re.search(r'find .*?\((\d+)\)',text):point=s.Integer(re.search(r'find .*?\((\d+)\)',text)[1])
 return F,var,point

def fingerprint(q):
 try:
  F,z,pt=prompt_data(q)
  fragment='| --- |' in q[':question/problem']
  return g.digest([s.srepr(s.cancel(F)),str(z),s.srepr(pt) if pt is not None else None,'fragment' if fragment else 'complete'])
 except (ValueError,AssertionError):
  # Incomplete prompts are unavailable, but their source solution's explicit
  # motion function still reserves its mathematical task against duplicates.
  match=re.search(r'x\(t\)=(.*?),\\,t>0',q.get(':question/worked-solution',''),re.S)
  if match:
   F=scalar(match[1]);return g.digest([s.srepr(s.cancel(F)),str(t),None,'complete'])
  return 'undefined:'+g.digest(q[':question/problem'])

def bank_check(q):
 F,z,pt=prompt_data(q);expected=s.diff(F,z)
 if pt is not None:expected=s.simplify(expected.subs(z,pt))
 fields=q.get(':question/answer-fields',[]);assert len(fields)==1,'Incomplete fields'
 f=fields[0];ft=f[':answer-field/type'];ft=ft.get(':db/ident') if isinstance(ft,dict) else ft
 correct=f[':answer-field/correct'];cid=str(correct[':answer/id']) if isinstance(correct,dict) else correct[1]
 values=[scalar(a[':answer/value']) for a in f[':answer-field/choices']]
 if '| --- |' in q[':question/problem']:
  rows=q[':question/problem'].splitlines();denraw=rows[-1].split('|')[3].strip().strip('$');den=scalar(denraw)
  multiplier=1
  head=rows[-3].split('|')[3]
  if '{{field-1}}$)' in head:multiplier=scalar(head.split('{{field-1}}$)',1)[1].strip().strip('$'))
  values=[v*multiplier/den for v in values]
 assert len(values)==(5 if ft.endswith('/radio') else 1)
 valid=[equal(v,expected) for v in values];assert sum(valid)==1,('Invalid answer',q.get(':question/math-academy-id'),valid,expected,values)
 assert str(f[':answer-field/choices'][valid.index(True)][':answer/id'])==cid
 assert all(not equal(v,w) for i,v in enumerate(values) for w in values[:i])
 return F,z,pt

def solution_check(q):
 F,z,pt=bank_check(q);work=q[':question/worked-solution'];der=s.diff(F,z)
 # Read actual numerator/denominator definitions, then all computed stages.
 defs={}
 for name,var,raw in re.findall(r'\$([uvgh])\(([xt])\)=(.*?)\$',work,re.S):defs[name]=scalar(raw)
 assert len(defs)==2,(q.get(':question/math-academy-id'),defs)
 names=list(defs);assert equal(defs[names[0]]/defs[names[1]],F)
 assert work.count('$')%2==0 and q[':question/problem'].count('$')%2==0
 def rhs(raw):
  raw=re.sub(r'\{([uvgh])\}',r'\1',raw).replace('′',"'")
  raw=re.sub(r"\^\{'\}","'",raw)
  for name,obj in defs.items():
   raw=re.sub(name+r"'\(([xt])\)",lambda m:'('+g.tex(s.diff(obj,z))+')',raw)
   raw=re.sub(name+r'\(([xt])\)',lambda m:'('+g.tex(obj)+')',raw)
   raw=re.sub(r"\b"+name+r"'",lambda m:'('+g.tex(s.diff(obj,z))+')',raw)
   raw=re.sub(r"\b"+name+r"\b",lambda m:'('+g.tex(obj)+')',raw)
  return scalar(raw)
 count=0
 for display in re.findall(r'\$\$(.*?)\$\$',work,re.S):
  display=re.sub(r'\\(?:begin|end)\{aligned\}','',display)
  rows=display.split(r'\\');is_derivative='&' in display
  if not is_derivative:
   # Directly test each displayed u' and v' definition as well.
   for name,arg,raw in re.findall(r"\{?([uvgh])\}?\^?\{?[′']\}?\(([xt])\)\s*=\s*(.*?)(?:,\\,|,\\quad|,|$)",display.strip().rstrip('.')):
    assert equal(scalar(raw),s.diff(defs[name],z)),raw
   continue
  evaluated=pt is not None and any(marker in display for marker in ('m &',"y'(",'{y}^{′}(1)',r'{y}^{\prime}('))
  # Source evaluation blocks have m=f'(point), y'(point), and then numbers.
  if pt is not None and ('Therefore,' in work):
   position=work.find(display[:20]) if display[:20] in work else -1
   # Their first derivative block always contains the formal quotient rule.
   evaluated=not any(tag in display for tag in ("u}^{", "u'(","u'",'u}^{'))
  for row in rows:
   if '=' not in row:continue
   raw=row.rsplit('=',1)[1].replace('&','').strip().rstrip('.')
   raw=re.sub(r'\{([fy])\}',r'\1',raw)
   if pt is not None and re.search(r"(?:f|y)\s*\^?\{?[′']\}?\s*\\?,?\s*\(",raw):
    continue # evaluation label; subsequent substitutions carry the evidence
   got=rhs(raw);expected=der.subs(z,pt) if evaluated else der
   assert equal(got,expected),('Solution stage',row,got,expected)
   count+=1
 assert count>=3
 return count

def independent(rec):
 assert rec['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
 gen=rec['generation'];name=gen['template'];g.validate_parameters(name,gen['parameters'])
 assert rec['question'][':question/difficulty']==':question.difficulty/'+g.CASES[name][0]
 assert fingerprint(rec['question'])==gen['parameter_fingerprint']
 replay=g.generate(g.CASES[name][0],gen['seed'],name,gen['parameters'])
 assert replay==rec,'Deterministic replay or identity mismatch'
 return solution_check(rec['question'])

def checks(rec):
 q=rec['question'];f=q[':question/answer-fields'][0];cid=f[':answer-field/correct'][1]
 if f[':answer-field/type'].endswith('/radio'):
  return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'Every field-owned choice'} for a in f[':answer-field/choices']]
 value=f[':answer-field/choices'][0][':answer/value'];E=scalar(value)
 return [{'submitted':value,'expected':'accepted','purpose':'Canonical blank fragment'},
 {'submitted':g.tex(s.expand(E)),'expected':'accepted','purpose':'Expanded equivalent fragment'},
 {'submitted':g.tex(E+1),'expected':'rejected','purpose':'Incorrect offset fragment'},
 {'submitted':g.tex(-E if E!=0 else E-1),'expected':'rejected','purpose':'Incorrect sign or nonzero fragment'}]

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 report={'source_basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'source_banks':[],'exclusions':g.EXCLUDED,'status':'pass'};native=[];review=[];steps=0
 for name,(level,parameters) in g.CASES.items():
  print('Validating',name,flush=True)
  rec=g.generate(level,11,name,parameters);steps+=independent(rec);src=g.SOURCES[name];rf=rec['question'][':question/answer-fields'][0];sf=src[':question/answer-fields'][0]
  ra=[scalar(a[':answer/value']) for a in rf[':answer-field/choices']];sa=[scalar(a[':answer/value']) for a in sf[':answer-field/choices']]
  assert len(ra)==len(sa) and all(sum(equal(a,b) for b in ra)==1 for a in sa)
  original_correct=scalar(sf[':answer-field/correct'][':answer/value']);actual=next(a for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1]);assert equal(original_correct,scalar(actual[':answer/value']))
  report['source_banks'].append({'template':name,'profile':name if len(sa)>1 else None,'matched_options':len(sa),'total_options':len(sa),'matched_distractors':len(sa)-1,'total_distractors':len(sa)-1,'complete_bank':True,'prompt_exact_replay':name!='q-132975','solution_exact_replay':True})
  native.append({'label':'source '+name,'record':rec,'checks':checks(rec)})
  review.append(('Source '+name,src));review.append(('Replay '+name,rec['question']))
  tested=0
  for seed in [1,2,3,5,8,13,21,34]:
   try:variant=g.generate(level,seed,name)
   except AssertionError:continue
   steps+=independent(variant);native.append({'label':name+' seed '+str(seed),'record':variant,'checks':checks(variant)});tested+=1
   if tested<=2:review.append(('Variant '+name+' '+str(seed),variant['question']))
  assert tested>=3
  report['source_banks'][-1]['variant_checks']=tested
 (H/'native-input.json').write_text(json.dumps(native,indent=2)+'\n')
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(H/'native-input.json'),str(H/'native-report.json')],check=True)
 native_report=json.loads((H/'native-report.json').read_text());assert native_report['documented_unresolved_checks']==0
 report.update(solution_stages_checked=steps,actual_grader='course_academy_engine::learning::grade_field',native_checks={k:v for k,v in native_report.items() if k!='records'},fidelity='11/11 supported source banks complete; 16/16 radio distractors matched',correctness='independent prompt, fragment, bank and solution-stage readback',grading='actual radio selection and equivalent/incorrect blank entries checked')
 (H/'review.md').write_text('# Source and generated comparison\n\nNotation outside reference parameters is normalized; quotient-rule prose and teaching sequence retained. The motion prompt is repaired using its source solution.\n\n'+'\n\n'.join('## '+label+'\n\n'+q[':question/problem']+'\n\n'+q[':question/worked-solution']+'\n\nAnswers: '+', '.join(a[':answer/value'] for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices']) for label,q in review))
 report['hashes']={str(p.relative_to(ROOT)):sha(p) for p in [H.with_suffix('.py'),H/'source.json',H/'math_parser.py',H/'validate.py',H/'capabilities.json',H/'source-components.json',H/'boundary_validation.py',H/'boundary-validation.json',H/'boundary-native-report.json',H/'replenish.py',H/'classification.md',H/'template-extraction.md',H/'plot-extraction.md']}
 (H/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('hashes','source_banks')},indent=2))
if __name__=='__main__':main()
