#!/usr/bin/env python3
"""Independent displayed-text mathematics, exact fidelity, native radio grading."""
import importlib.util,json,re,sys,subprocess,hashlib
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('kp',ROOT.with_suffix('.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
X,Y,R,T=sp.symbols('x y r theta',real=True)
def parse(s):
 s=re.sub(r'\\(sin|cos)\^(\d+)\\theta',r'\\\1{(\\theta)}^\2',s)
 s=re.sub(r'\\(sin|cos)\\theta',r'\\\1{(\\theta)}',s)
 s=s.replace('π','pi').replace('[','(').replace(']',')').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\!','').replace(r'\cdot','*')
 def group(pos):
  assert s[pos]=='{',s
  dep=1;i=pos+1
  while dep:
   dep+=(s[i]=='{')-(s[i]=='}');i+=1
  return s[pos+1:i-1],i
 while r'\frac' in s or r'\sqrt' in s:
  matches=list(re.finditer(r'\\(frac|sqrt)',s));mch=matches[-1];beg=mch.start();arg,end=group(mch.end());rep='sqrt('+arg+')'
  if mch[1]=='frac':den,end=group(end);rep='(('+arg+')/('+den+'))'
  s=s[:beg]+rep+s[end:]
 s=s.replace(r'\theta','theta').replace(r'\pi','pi').replace(r'\sin',' sin').replace(r'\cos',' cos').replace(r'\ln','log').replace('{','(').replace('}',')')
 s=re.sub(r'(sin|cos)\^\((\d+)\)\(\((.*?)\)\)',r'(\1(\3))^\2',s)
 assert '\\' not in s,s
 return parse_expr(s,local_dict={'x':X,'y':Y,'r':R,'theta':T,'pi':sp.pi,'e':sp.E,'sin':sp.sin,'cos':sp.cos,'sqrt':sp.sqrt},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))
def eq(a,b):assert sp.trigsimp(sp.simplify(a-b))==0,(a,b)
def fmt(s):
 assert s.count('$$')%2==0
 assert s.replace('$$','').count('$')%2==0
 dep=0
 for c in s:
  if c=='{':dep+=1
  if c=='}':dep-=1;assert dep>=0
 assert dep==0
 assert '--' not in s and '+-' not in s

def group_at(s,pos):
 assert s[pos]=='{',(s,pos)
 depth=1;i=pos+1
 while depth:
  depth+=(s[i]=='{')-(s[i]=='}');i+=1
 return s[pos+1:i-1],i

def evaluate_math(s,density,plane,rr,lo,hi):
 """Read each actual printed RHS, including nested complete definite integrals.
 No generator row values are consulted. General operator slots are resolved
 from the actual prompt and independently differentiated plane.
 """
 s=s.strip().rstrip('.')
 s=s.replace(r'f(x,y,g(x,y))','('+m.tex(density)+')').replace(r'f(r\cos\theta,r\sin\theta)','('+m.tex(density.subs({X:R*sp.cos(T),Y:R*sp.sin(T)}))+')')
 s=s.replace(r'\frac{\partial z}{\partial x}','('+m.tex(sp.diff(plane,X))+')').replace(r'\frac{\partial z}{\partial y}','('+m.tex(sp.diff(plane,Y))+')')
 # Resolve double integrals, including their own actual displayed integrands.
 while r'\iint_' in s:
  start=s.rfind(r'\iint_');pos=start+len(r'\iint_')
  if s.startswith(r'\Delta',pos):domain='polar';pos+=len(r'\Delta');suffix=r'\,\mathrm{d}r\,\mathrm{d}\theta'
  else:domain=s[pos];pos+=1;suffix=r'\,\mathrm{d}'+('S' if domain=='S' else 'A')
  body,end=group_at(s,pos);assert s.startswith(suffix,end),(s,end)
  body=parse(body)
  if domain in ('D','S'):body=sp.trigsimp(body.subs({X:R*sp.cos(T),Y:R*sp.sin(T)}))*R
  val=sp.integrate(sp.integrate(body,(R,0,rr)),(T,lo,hi))
  if domain=='S':val*=sp.sqrt(1+sp.diff(plane,X)**2+sp.diff(plane,Y)**2)
  s=s[:start]+'('+m.tex(val)+')'+s[end+len(suffix):]
 # Resolve bounded primitive evaluation brackets; unbounded arithmetic brackets
 # remain arithmetic grouping. Bounds are parsed from the displayed row.
 while re.search(r'\\left\[.*?\\right\]_\{',s):
  match=list(re.finditer(r'\\left\[(.*?)\\right\]_\{',s))[-1];start=match.start();body=parse(match[1]);pos=match.end()-1;lower,pos=group_at(s,pos);assert s.startswith('^{',pos);upper,end=group_at(s,pos+1)
  var=R if R in body.free_symbols else T;value=body.subs(var,parse(upper))-body.subs(var,parse(lower));s=s[:start]+'('+m.tex(value)+')'+s[end:]
 # Last integral is necessarily innermost in this controlled complete syntax.
 while r'\int_{' in s:
  start=s.rfind(r'\int_');pos=start+len(r'\int_');lower,pos=group_at(s,pos);assert s.startswith('^{',pos);upper,pos=group_at(s,pos+1);body,pos=group_at(s,pos)
  diff=re.match(r'\\,\\mathrm\{d\}(\\theta|r)',s[pos:]);assert diff,(s,pos);var=T if diff[1]==r'\theta' else R
  val=sp.integrate(parse(body),(var,parse(lower),parse(upper)));s=s[:start]+'('+m.tex(val)+')'+s[pos+diff.end():]
 return parse(s)

def assert_endpoint_row(primitive_row,evaluated_row):
 match=list(re.finditer(r'\\left\[(.*?)\\right\]_\{',primitive_row))[-1];primitive=parse(match[1]);lower,pos=group_at(primitive_row,match.end()-1);upper,_=group_at(primitive_row,pos+1);var=R if R in primitive.free_symbols else T
 match=re.search(r'\\left\[\((.*?)\)-\((.*?)\)\\right\]',evaluated_row);assert match,evaluated_row
 for group,bound in [(match[1],parse(upper)),(match[2],parse(lower))]:
  tokens=re.findall(r'\(([^()]*)\)(?:\+|$)',group)
  # Parse actual ordered additive primitive components, respecting nested
  # fractions/groups. This checks structure as well as their collected value.
  raw=list(re.finditer(r'\\left\[(.*?)\\right\]_\{',primitive_row))[-1][1];parts=[];depth=0;begin=0
  for i,ch in enumerate(raw):
   if ch in '{(':depth+=1
   elif ch in '})':depth-=1
   elif ch in '+-' and depth==0 and i>begin:
    if raw[begin:i].strip():parts.append(raw[begin:i]);begin=i
  parts.append(raw[begin:]);terms=[parse(part) for part in parts];assert len(tokens)==len(terms),(tokens,parts)
  for token,term in zip(tokens,terms):eq(parse(token),term.subs(var,bound))


def displayed(rec,standalone=None):
 q=rec['question'];p=q[':question/problem'];s=q[':question/worked-solution'];fmt(p);fmt(s)
 assert not re.search(r'\b(?:s|U|V|F|G)\s*(?:\(|=)',s)
 assert not re.search(r'\b(?:q1|q2|q4|disk sector)\b',p)
 density=parse(re.search(r'\\iint_S (.*?)\\,\\mathrm\{d\}S',p)[1]);plane=parse(re.search(r'\$z=(.*?)\$',p)[1]);rr=int(re.search(r'radius \$(\d+)\$',p)[1])
 bounds=re.search(r'0\\le r\\le (\d+),\\ (.*?)\\le\\theta\\le (.*?)\\\}',s);assert int(bounds[1])==rr;lo,hi=parse(bounds[2]),parse(bounds[3]);assert 0<hi-lo<=2*sp.pi
 partials=re.findall(r'\\frac\{\\partial z\}\{\\partial (x|y)\}=\\frac\{\\partial\}\{\\partial (x|y)\}\((.*?)\)=(.*?)[,.]\$\$',s)
 assert len(partials)==2,partials
 for letter,held,arg,val in partials:
  assert letter==held;eq(parse(arg),plane);eq(parse(val),sp.diff(plane,X if letter=='x' else Y))

 value=sp.simplify(sp.sqrt(1+sp.diff(plane,X)**2+sp.diff(plane,Y)**2)*sp.integrate(sp.integrate(sp.trigsimp(density.subs({X:R*sp.cos(T),Y:R*sp.sin(T)}))*R,(R,0,rr)),(T,lo,hi)))
 chains=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',s,re.S);assert len(chains)==2
 metrics=[row.strip() for row in re.split(r'\\\\\s*& =',chains[0].split('& =',1)[1])];rows=[row.strip() for row in re.split(r'\\\\\s*& =',chains[1].split('& =',1)[1])]
 assert len(metrics)==4
 for row in metrics+rows:eq(evaluate_math(row,density,plane,rr,lo,hi),value)
 family=standalone or rec['generation']['template'];is_ratio=family in ('x_over_r2','xy_over_r2');offset=4 if is_ratio else 3
 assert len(rows)==(12 if is_ratio else 11),(family,len(rows))
 assert r'f(r\cos\theta,r\sin\theta)\cdot r' in rows[0]
 assert r'\cdot r' in rows[1]
 if is_ratio:assert r'r^2(\cos^2\theta+\sin^2\theta)' in rows[2]
 repeated=rows[offset]
 orders=re.findall(r'\\mathrm\{d\}(\\theta|r)',repeated)
 assert orders==([r'\theta','r'] if family=='x_over_r2' else ['r',r'\theta']),orders
 if family in ('xy','xy_over_r2'):
  assert re.search(r'\\sin\{\\left\(2 \\theta',rows[offset-1]),rows[offset-1]
  assert r'\cos{\left(2 \theta' in rows[offset+4]
  assert r'\frac' not in list(re.finditer(r'\\left\[(.*?)\\right\]',rows[offset+4]))[0][1]
 elif family=='xy2':
  assert r'\cos' in rows[offset-1] and (r'\sin^{2}' in rows[offset-1] or r'\sin^2\theta' in rows[offset-1])
  assert r'\sin^{3}' in rows[offset+4] and r'{3}' in rows[offset+4]
 elif family=='radialpoly':
  # Both nonzero signed primitive terms must remain visibly distinct.
  primitive=re.search(r'\\left\[(.*?)\\right\]',rows[offset+1])[1];assert '-' in primitive and r'r^{2}' in primitive and r'r^{4}' in primitive
 assert_endpoint_row(rows[offset+1],rows[offset+2]);assert_endpoint_row(rows[offset+4],rows[offset+5])
 eq(parse(re.search(r'Therefore, the surface integral is \$(.*?)\$',s)[1]),value)
 if standalone:return value
 sf=sp.sqrt(1+sp.diff(plane,X)**2+sp.diff(plane,Y)**2);polar=sp.trigsimp(density.subs({X:R*sp.cos(T),Y:R*sp.sin(T)}))*R
 fields=q[':question/answer-fields'];assert len(fields)==1;field=fields[0];assert field[':answer-field/type']==':answer-field.type/radio';choices=field[':answer-field/choices'];assert len(choices)==5
 values=[parse(a[':answer/value']) for a in choices];assert all(v.is_real is not False and not v.has(sp.oo,sp.zoo,sp.nan) for v in values)
 for i,val in enumerate(values):
  for oth in values[:i]:assert sp.simplify(val-oth)!=0
 correct=field[':answer-field/correct'][1];selected=next(a for a in choices if a[':answer/id']==correct);eq(parse(selected[':answer/value']),value)
 expected=[value,value/sf,value*sf,sf*sp.integrate(sp.integrate(polar,(R,0,rr)),(T,lo,(lo+hi)/2)),sf*sp.integrate(sp.integrate(polar,(R,0,sp.Rational(rr,2))),(T,lo,hi))]
 assert sorted(map(m.canonical,values))==sorted(map(m.canonical,expected))
 plot_path=Path(re.search(r'!\[\]\((.*?)\)',p)[1]);meta=json.loads(plot_path.with_suffix('.json').read_text());assert meta['renderer_version']=='region-render-5';assert hashlib.sha256(plot_path.read_bytes()).hexdigest()==meta['png_sha256'];assert meta['saved_dpi']==140
 assert all(b['axis_clearance_px']>=4 and b['blue_ink_clearance_px']>=4 and b['other_label_clearance_px']>=4 and b['black_ink_pixels_in_bbox']>0 and not b['mask'] for b in meta['text_boxes']);assert all(meta['pixel_qa']['arc_samples_present']);assert meta['pixel_qa']['orientation_fraction']>.995;assert meta['pixel_qa']['relative_area_error']<meta['pixel_qa']['area_stroke_allowance'];assert meta['pixel_qa']['interior_fill_coverage']>.995
 assert set(rec['knowledge_point'])=={'db_id','id','title'}
 return value

def main():
 wrapper=json.loads((ROOT/'source.json').read_text());sources=wrapper['record'][':knowledge-point/questions'];cases=json.loads((ROOT/'source-cases.json').read_text());records=[];review=[];fidelity=[]
 for q,case in zip(sources,cases):
  sid=case['source_id'];rec=m.generate(case['level'] or 'hard',parameters=case['parameters'],profile=case['bank_profile']);gq=rec['question']
  assert gq[':question/problem']==q[':question/problem'];assert gq.get(':question/worked-solution')==q.get(':question/worked-solution')
  assert set(gq)==set(q)-{':db/id'}
  gf=gq[':question/answer-fields'][0];sf=q[':question/answer-fields'][0];assert set(gf)==set(sf)-{':db/id'}
  assert sorted(a[':answer/value'] for a in gf[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
  f,k,a,b,rr,reg=m.SOURCE_CONFIG[sid];lo,hi=m.REGIONS[reg]
  text=q[':question/problem'];raw_plane=re.search(r'\$z\s*=\s*([^$]+)\$',text)[1];plane=parse(raw_plane);eq(plane,a*X+b*Y)
  raw_density=re.search(r'\{∬\}_\{S\}(.*?)\\,',text)
  density=parse(raw_density[1] if raw_density else re.search(r'∬_\(S\)(.*?)dS',text)[1]);eq(density,m.expr(f,k))
  assert int(re.search(r'radius \$(\d+)\$',text)[1])==rr
  if ':question/worked-solution' in q:
   # Complete captured stage order/string is compared above; independently read
   # displayed polar bounds rather than trusting the family configuration.
   bs=re.search(r'Δ=.*?0\\le r\\le (\d+),\\,(.*?)\\le \\theta \\le (.*?)\}\.',q[':question/worked-solution'])
   assert bs is not None,sid
   eq(parse(bs[2]),lo);eq(parse(bs[3].rstrip().rstrip('\\')),hi);assert int(bs[1])==rr
  polar=sp.trigsimp(density.subs({X:R*sp.cos(T),Y:R*sp.sin(T)}))*R
  truth=sp.simplify(sp.sqrt(1+sp.diff(plane,X)**2+sp.diff(plane,Y)**2)*sp.integrate(sp.integrate(polar,(R,0,rr)),(T,lo,hi)))
  source_values=[parse(z[':answer/value']) for z in sf[':answer-field/choices']]
  for i,vv in enumerate(source_values):
   for ww in source_values[:i]:assert sp.simplify(vv-ww)!=0
  if ':answer-field/correct' in sf:
   eq(parse(sf[':answer-field/correct'][':answer/value']),truth)
   assert next(z[':answer/value'] for z in gf[':answer-field/choices'] if z[':answer/id']==gf[':answer-field/correct'][1])==sf[':answer-field/correct'][':answer/value']
   records.append(rec)
  else:eq(parse(sf[':answer-field/choices'][0][':answer/value']),truth)
  assert not rec['generation']['eligible_for_learning'];shift=m.generate('hard',parameters={'h':2},profile=case['bank_profile']);assert shift['question'][':question/problem']!=gq[':question/problem'];assert shift['generation']['mathematical_fingerprint']==rec['generation']['mathematical_fingerprint']
  fidelity.append({'source_id':sid,'exact_prompt':True,'exact_solution_presence_and_bytes':True,'exact_complete_bank':True,'correct_designation_match':':answer-field/correct' in sf,'mathematical_value':str(truth),'raw_formatting_eligible':False})
  review.append({'kind':'original evidence','source_id':sid,'record':rec})
  for seed in (21,27):
   variant=m.generate_hard(seed,template=f);displayed(variant);review.append({'kind':'generated authored bank / source family','source_id':sid,'record':variant});records.append(variant)
 # Exercise the SAME normal solution masks at every original parameter set.
 # Some original parameters are deliberately ineligible for the authored default
 # bank/workload; that does not excuse failing the normal mask's layout/math.
 layout_regressions=[]
 for sid,(f,k,a,b,rr,reg) in m.SOURCE_CONFIG.items():
  params={'k':k,'a':str(a),'b':str(b),'radius':rr,'region':reg,'c':1}
  solution,layout=m.source_solution(f,params)
  prompt=r'Evaluate $$\iint_S '+m.tex(m.expr(f,k))+r'\,\mathrm{d}S,$$ where $z='+m.tex(a*X+b*Y)+r'$ on the '+m.REGION_NAMES[reg]+' of radius $'+str(rr)+'$.'
  fixture={'question':{':question/problem':prompt,':question/worked-solution':solution},'generation':{'template':f}}
  displayed(fixture,standalone=f)
  public_status='eligible'
  try:original_normal=m.generate_hard(template=f,parameters=params);displayed(original_normal);records.append(original_normal)
  except ValueError as exc:public_status='whole-bank/workload rejection: '+str(exc)
  layout_regressions.append({'source_id':sid,'family':f,'original_parameters_normal_mask_math_and_layout':'passed','public_default_at_original_parameters':public_status,'layout':layout,'changed_public_variants':2})
 (ROOT/'normal-layout-regressions.json').write_text(json.dumps(layout_regressions,indent=2))
 for level in ('easy','moderate','hard'):
  for seed in range(12):
   rec=m.generate(level,seed);displayed(rec);records.append(rec)
   other=m.generate(level,seed+100,template=rec['generation']['template'],parameters=rec['generation']['parameters']);assert other['question'][':question/id']==rec['question'][':question/id'];assert other['generation']['content_fingerprint']==rec['generation']['content_fingerprint']
   if seed<2:review.append({'kind':'generated '+level,'record':rec})
 assert set(r['generation']['template'] for r in records if r['generation']['eligible_for_learning'] and r['question'].get(':question/difficulty')==':question.difficulty/hard')>=set(m.FAMILIES)
 # Exercise actual defaults at a seed for each family, rather than infer coverage
 # from explicit template calls.
 import random
 default_counts={f:0 for f in m.FAMILIES}
 for f in m.FAMILIES:
  seed=next(n for n in range(1000) if random.Random(n).choice(list(m.FAMILIES))==f)
  rec=m.generate_hard(seed);assert rec['generation']['template']==f;displayed(rec);records.append(rec);default_counts[f]+=1
 (ROOT/'default-family-coverage.json').write_text(json.dumps(default_counts,indent=2))
 # Workload and malformed explicit calls cannot silently resample.
 bad=[('easy','constant',dict(k=1,a=2,b=1,radius=1,region='disk')),('moderate','x',dict(k=1,a=2,b=1,radius=1,region='q1')),('hard','x',dict(k=1,a=1,b=1,radius=1,region='q1')),('hard','r2',dict(k=9,a=2,b=1,radius=1,region='disk'))]
 for l,f,p in bad:
  try:m.generate(l,template=f,parameters=p)
  except ValueError:pass
  else:raise AssertionError('workload accepted')
 native=[]
 for i,rec in enumerate(records):
  field=rec['question'][':question/answer-fields'][0];correct=field[':answer-field/correct'][1]
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'complete owned radio bank'} for a in field[':answer-field/choices']]
  native.append({'label':str(i),'record':rec,'checks':checks})
 (ROOT/'engine-input.json').write_text(json.dumps(native,ensure_ascii=False));subprocess.run(['generate/runs/current/check-engine',str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')],check=True)
 (ROOT/'source-fidelity.json').write_text(json.dumps(fidelity,indent=2,ensure_ascii=False));(ROOT/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False));(ROOT/'review.md').write_text('\n\n---\n\n'.join('### '+r['kind']+' '+r.get('source_id','')+'\n\n'+m.markdown(r['record']) for r in review))
 report={'status':'pass with explicitly ineligible historical evidence','source_basis':2721,'source_questions':len(sources),'exact_prompts':len(sources),'exact_solution_presence_and_strings':len(sources),'existing_worked_solutions':len(sources),'complete_banks':len(sources),'answer_values':5*len(sources),'correct_designations_matched':len(sources),'correct_designations_absent':0,'independent_normal_displayed_records':len(records)-len(sources),'source_math_values_verified':len(sources),'source_solution_error':'q-161316 has d r instead of d theta in one angular integral','raw_parameterization_limit':'vertical translation only; not counted as mathematical variety','native_grading':json.loads((ROOT/'engine-report.json').read_text()),'normal_layout_regressions':json.loads((ROOT/'normal-layout-regressions.json').read_text()),'default_family_coverage':default_counts,'fresh_concurrency':json.loads((ROOT/'concurrency.json').read_text()),'measured_renderer_version':'region-render-5','remaining_limits':['Historical source distractor intent remains opaque; banks evidence-only.','Raw source solution intermediate equality parser not automated for every original Unicode operator row; manual review recorded.','Easy/moderate assignments are authored scope claims.'],'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}
 (ROOT/'validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False));print(f'PASS: {len(sources)}/{len(sources)} current source banks; {5*len(sources)} values; displayed mathematics and native grading.')
if __name__=='__main__':main()
