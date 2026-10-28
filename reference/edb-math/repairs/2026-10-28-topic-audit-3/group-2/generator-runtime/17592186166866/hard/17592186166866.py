"""Ellipse plot reading -> standard equation -> implicit differentiation (current source basis 2563).
Raw observed profiles are evidence only; completions infer missing answer/solution.
All sampled and explicit normal parameters use the same finite workload domains.
No EDB access. Render exclusively with cached Matplotlib; never prune assets.
"""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction
import argparse,hashlib,itertools,json,math,random,re,subprocess,tempfile,uuid
import sympy as sp
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts/question_capture'))
from math_format import normalize_prose,normalize_tex,checked_math_content
HERE=Path(__file__).resolve().with_suffix('');VERSION='ellipse-3.0'
SOURCE=json.loads((HERE/'reference/source-current.json').read_text());KP=SOURCE['record'];X,Y=sp.symbols('x y')
GEOMETRIES=[(0,0,3,2),(2,-1,3,4),(0,0,1,2),(0,0,5,3),(0,0,2,5),(0,0,3,1),(-1,-1,2,1),(0,1,2,3),(3,0,3,2),(-1,2,4,2)]
CODES=[['-lXY','+rXY','+iXY','-vXY','-rXY'],['-vYX','-rXY','-lXY','+rXY','+iYX'],['-iYX','+vXY','-rXY','-lXY','+vYX'],['-rYX','+iYX','+vYX','-rXY','-lXY'],['-rXY','+lXY','-lYX','-lXY','+rYX'],['-lXY','-rXY','-vXY','-iYX','-vYX'],['-rXY','+rWV','-vYX','+rVW','-vXY'],['-vYX','+lYX','+lXY','-rXY','+vXY'],['-iYX','+lXY','-rYXt','+vXYt','-rXY'],['-iYX','-vXY','+rYX','-rXY','+lXY']]
DEFAULT=['-rXY','+rXY','-vXY','-lXY','-vYX']
CASES={q[':question/math-academy-id']:{'source_id':q[':question/math-academy-id'],'template':'origin' if p[:2]==(0,0) else 'shifted','level':q.get(':question/difficulty',{}).get(':db/ident','/easy' if p[:2]==(0,0) else '/hard' if p[0]*p[1]!=0 and min(p[2]//math.gcd(p[2],p[3]),p[3]//math.gcd(p[2],p[3]))>1 else '/moderate').split('/')[-1],'parameters':dict(zip(('h','k','a','b'),p)),'bank_profile':'observed-'+q[':question/math-academy-id'],'index':i} for i,(q,p) in enumerate(zip(KP[':knowledge-point/questions'],GEOMETRIES))}
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+v))
def tex(e):return sp.latex(sp.factor(e)).replace(' \\left','\\left').replace(' \\right','\\right')
def shifted(v,c):return v if c==0 else '('+v+('+' if c<0 else '-')+str(abs(c))+')'
def power(v,c):return '{'+v+'}^{2}' if c==0 else shifted(v,c)+'^{2}'
def divided(term,n):return term if n==1 else r'\frac{'+term+'}{'+str(n)+'}'
def derivative_factor(v,c,n):
 t=v if c==0 else shifted(v,c)
 return divided('2'+t,n)
def reduced_factor(v,c,n):
 f=Fraction(2,n);t=v if c==0 else shifted(v,c)
 return divided(('' if f.numerator==1 else str(f.numerator))+(t[1:-1] if f.numerator==1 and c else t),f.denominator)
def rational_tex(c,n,d,style='tex'):
 c=Fraction(c);sign='-' if c<0 else '';c=abs(c)
 if style=='ascii':
  n=re.sub(r'([xy])([+-])',r'\1 \2 ',n);d=re.sub(r'([xy])([+-])',r'\1 \2 ',d)
  nn=('' if c.numerator==1 else str(c.numerator))+n;dd=('' if c.denominator==1 else str(c.denominator))+d
  return sign+(' ' if sign else '')+'('+nn+')/('+dd+')'
 nn=('' if c.numerator==1 else str(c.numerator))+n;dd=('' if c.denominator==1 else str(c.denominator))+d
 # source uses unparenthesized shifted numerator if coefficient one
 if c.numerator==1 and n.startswith('('):nn=n[1:-1]
 if c.denominator==1 and d.startswith('('):dd=d[1:-1]
 return sign+r'\frac{'+nn+'}{'+dd+'}'
def bank(p,codes,style='tex'):
 h,k,a,b=[p[t] for t in ('h','k','a','b')];u=X-h;v=Y-k
 ratios={'r':Fraction(b*b,a*a),'v':Fraction(a*a,b*b),'l':Fraction(b,a),'i':Fraction(a,b)}
 vals=[]
 for code in codes:
  sg=-1 if code[0]=='-' else 1;c=sg*ratios[code[1]];pair=code[2:4]
  if pair=='XY':n,d=u,v;nt,dt=shifted('x',h),shifted('y',k)
  elif pair=='YX':n,d=v,u;nt,dt=shifted('y',k),shifted('x',h)
  elif pair=='VW':n,d=X+h,Y+k;nt,dt=shifted('x',-h),shifted('y',-k)
  elif pair=='WV':n,d=Y+k,X+h;nt,dt=shifted('y',-k),shifted('x',-h)
  else:raise ValueError(code)
  if code.endswith('t'):
   n,d=(Y-h,X) if pair=='YX' else (X,Y-h);nt,dt=(shifted('y',h),'x') if pair=='YX' else ('x',shifted('y',h))
  vals.append((code,sp.factor(sp.Rational(c.numerator,c.denominator)*n/d),rational_tex(c,nt,dt,style)))
 if any(sp.cancel(v[1]-w[1])==0 for i,v in enumerate(vals) for w in vals[i+1:]):raise ValueError('whole bank collision')
 return vals
D=r'\frac{\text{d}y}{\text{d}x}';OP=r'\frac{\text{d}}{\text{d}x}'
def solution(p,extra=False):
 h,k,a,b=[p[t] for t in ('h','k','a','b')]
 centered=h==k==0
 center='the origin' if centered else f'$({h},{k})$'
 opening=f'Since our ellipse is centered at {center} and has semiaxes ${a}$ and ${b},$ its equation is given by'
 initial=[];terms=[]
 for v,c,n in [('x',h,a),('y',k,b)]:
  base=('{'+v+'}' if centered else '('+v+'-'+('('+str(c)+')' if c<0 else str(c))+')')
  initial.append(r'\frac{'+base+'^{2}}{'+('{'+str(n)+'}')+r'^{2}}')
  terms.append(divided(power(v,c),n*n))
 eq='+'.join(terms)
 f=derivative_factor('x',h,a*a);g=derivative_factor('y',k,b*b)
 fs=reduced_factor('x',h,a*a);gs=reduced_factor('y',k,b*b)
 final=rational_tex(-Fraction(b*b,a*a),shifted('x',h),shifted('y',k))
 rows=[OP+'('+eq+') & ='+OP+'(1)',OP+'('+terms[0]+')+'+OP+'('+terms[1]+') & =0',f+'+'+g+r'\cdot '+D+' & =0']
 if extra:rows.append(fs+'+'+gs+r'\cdot '+D+' & =0')
 rows += [gs+r'\cdot '+D+' & =-'+fs,D+' & ='+final]
 return opening+'\n\n$$\n'+'+'.join(initial)+r'=1\,⟹\,'+eq+'=1.\n$$\n\nNow, to calculate $'+D+',$ we use implicit differentiation:\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
SUPPORTED_LEVELS=('easy','moderate')
KP_ID=17592186166866
KP_UUID=KP[':knowledge-point/id']
GENERATOR_UUID=str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:question-generator:'+KP_UUID))
def domain(level):
 # Observed easy: origin. Current moderate evidence includes two shifted coordinates
 # and nonunit reduced ratios. No evidence supports a separate hard workload.
 if level=='easy':return [dict(h=0,k=0,a=a,b=b) for a in range(1,6) for b in range(1,6) if a!=b]
 if level=='moderate':return [dict(h=h,k=k,a=a,b=b) for h in range(-3,4) for k in range(-3,4) for a in range(1,6) for b in range(1,6) if a!=b and (h or k)]
 raise ValueError('Unsupported difficulty: '+str(level))
def check_parameters(level,p,observed=False):
 if set(p)!=set(('h','k','a','b')) or any(type(v)!=int for v in p.values()):raise ValueError('four integer parameters required')
 if p['a']<1 or p['b']<1 or p['a']==p['b']:raise ValueError('positive unequal semiaxes required')
 if p not in domain(level):raise ValueError('parameters outside level workload')
def render_plots(p,output_dir=None):
 out=Path(output_dir or HERE/'assets');out.mkdir(parents=True,exist_ok=True)
 key=digest({'p':p,'renderer':'ellipse-1.1'});png=out/(key+'.png');side=out/(key+'.json')
 if png.exists() and side.exists():return {'prompt':str(png),'spec':str(side)}
 with tempfile.NamedTemporaryFile('w',suffix='.json',prefix='ellipse-render-',dir=out,delete=False) as f:
  json.dump({'parameters':p,'png':str(png),'side':str(side)},f);input_path=Path(f.name)
 try:subprocess.run([str(Path(__file__).resolve().parents[2]/'.venv/bin/python'),str(HERE/'render.py'),str(input_path)],check=True,capture_output=True)
 finally:input_path.unlink(missing_ok=True)
 return {'prompt':str(png),'spec':str(side)}
def domain_metadata(p):
 """Real ellipse locus; its derivative is finite away from the horizontal center line.
 Coordinate axes need not be excluded. Only positive semiaxes and y-k != 0
 enter the standard equation / slope divisions; unequal axes keep this KP an ellipse.
 """
 h,k,a,b=[p[t] for t in ('h','k','a','b')]
 equation='+'.join([divided(power('x',h),a*a),divided(power('y',k),b*b)])+'=1'
 return {'independent_variable':'x','dependent_variable':'y','variable_domains':{'x':'real','y':'real'},'real_locus_equation_tex':equation,'semiaxes':{'horizontal':a,'vertical':b,'constraints':'a > 0, b > 0, a != b'},'axis_unit_scales':[1,1],'finite_slope_condition_tex':shifted('y',k)+r'\ne 0','finite_slope_excluded_line':{'y':k},'vertical_tangent_points':[[h-a,k],[h+a,k]],'coordinate_axis_convention':'Coordinate axes x=0 and y=0 are allowed on the real locus. The derivative quotient excludes only y=k.'}
def source_metadata(p,profile=None):
 """Immutable evidence lineage and applicable source support, outside learner records."""
 case=CASES.get(profile.split('-',1)[1]) if profile and profile.startswith(('observed-','completed-')) else None
 family='origin' if p['h']==p['k']==0 else 'shifted'
 return {'database':SOURCE['database'],'basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'source_ids':[case['source_id']] if case else [c['source_id'] for c in CASES.values() if c['template']==family],'canonical_example_id':KP[':knowledge-point/canonical-example'][':question/math-academy-id'],'topic_db_id':17592186049506,'role':'observed bank provenance' if case else 'supporting family evidence for authored parameter variant'}
def dependency_metadata():
 return {'python':sys.version.split()[0],'sympy':sp.__version__}
def replay(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('level')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('radio only')
 raw=bool(profile and profile.startswith('observed-'));completed=bool(profile and profile.startswith('completed-'))
 case=CASES.get(profile.split('-',1)[1]) if raw or completed else None
 if (raw or completed) and case is None:raise ValueError('unknown source profile')
 if profile and not raw and not completed and profile!='authored-method':raise ValueError('unknown bank')
 rng=random.Random(seed);p=dict(parameters if parameters is not None else case['parameters'] if case else rng.choice(domain(level)))
 check_parameters(level,p,observed=raw or completed)
 expected_template='origin' if p['h']==p['k']==0 else 'shifted'
 if template and template!=expected_template:raise ValueError('template incompatible with geometry')
 if case and level!=case['level']:raise ValueError('replay level')
 codes=CODES[case['index']] if case else DEFAULT
 vals=bank(p,codes,'tex')
 correct=sp.factor(-sp.Rational(p['b']**2,p['a']**2)*(X-p['h'])/(Y-p['k']))
 ci=next(i for i,v in enumerate(vals) if sp.cancel(v[1]-correct)==0)
 sourceq=KP[':knowledge-point/questions'][case['index']] if case else None
 exact=bool(case and p==case['parameters'])
 # Geometry-dependent source path is replayed only for the original actual geometry.
 plot={'prompt':re.search(r'!\[\]\((.*?)\)',sourceq[':question/problem']).group(1)} if exact else render_plots(p)
 derivative=r'\frac{dy}{dx}' if case and case['source_id']=='q-127362' else D
 plot_reference=plot['prompt']
 if not exact:
  asset_hash=hashlib.sha256(Path(plot_reference).read_bytes()).hexdigest()
  plot_reference=f'images/{asset_hash[:2]}/{asset_hash}.png'
 prompt=f"![]({plot_reference})\n\nFind ${derivative}$ for the ellipse shown above."
 sol=solution(p)
 # only the canonical example contains a redundant fully simplified sum; practice rows omit it.
 if raw and ':question/worked-solution' not in sourceq:sol=None
 prompt=normalize_prose(prompt)
 sol=normalize_prose(sol) if sol is not None else None
 vals=[(code,value,normalize_tex(text)) for code,value,text in vals]
 bank_strings=[v[2] for v in vals]
 ident=digest({'version':VERSION,'difficulty':level,'problem':prompt,'solution':sol,'bank':sorted(bank_strings)})
 fid=uid(ident+'field');answers=[{':answer/id':uid(ident+'answer'+v[2]),':answer/type':':answer.type/math',':answer/value':v[2]} for v in vals]
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
 if not raw or ':answer-field/correct' in sourceq[':question/answer-fields'][0]:field[':answer-field/correct']=[':answer/id',answers[ci][':answer/id']]
 rng.shuffle(answers)
 q={':question/id':uid(ident),':question/problem':prompt,':question/answer-fields':[field]}
 if not raw or ':question/difficulty' in sourceq:q[':question/difficulty']=':question.difficulty/'+level
 if sol is not None:q[':question/worked-solution']=sol
 if raw:
  original_field=sourceq[':question/answer-fields'][0];field[':db/id']=original_field[':db/id']
  if exact:
   for a in answers:a[':db/id']=next(v[':db/id'] for v in original_field[':answer-field/choices'] if v[':answer/value']==a[':answer/value'])
  q[':db/id']=sourceq[':db/id'];q[':question/math-academy-id']=sourceq[':question/math-academy-id']
  # Captured field/answer database IDs are provenance, not generated ownership identifiers.
 return {'knowledge_point':{'db_id':KP[':db/id'],'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'seed':seed,'level':level,'parameters':p,'domain':domain_metadata(p),'source':source_metadata(p,profile),'dependencies':dependency_metadata(),'template':expected_template,'bank_profile':profile or 'authored-method','operations':codes,'origin':('raw observed evidence' if exact else 'parameterized historical bank evidence') if raw else ('supported source completion' if exact else 'generated historical bank variant') if completed else 'authored parameter variant','evidence_only':raw or completed,'eligible_for_learning':not (raw or completed),'inferred_correct_value':tex(correct) if raw and ':answer-field/correct' not in field else None,'mathematical_fingerprint':digest({'center':[p['h'],p['k']],'reduced_ratio':str(Fraction(p['b'],p['a']))}),'content_fingerprint':ident,'plot':plot}}
@checked_math_content
def generate(level='easy',seed=0,**kwargs):
 if kwargs.get('profile','authored-method') not in (None,'authored-method'):
  raise ValueError('Historical banks are evidence-only; use replay() for fidelity')
 return replay(level,seed,**kwargs)
# Individually documented entrypoints: no within-level progression.
def generate_easy(seed=0,**kwargs):
 """Observed origin ellipse; axes 1..5, same two derivative terms."""
 return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):
 """Observed moderate peers: one shift/nonunit reduced terms, or two shifts/unit reduced term."""
 return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):
 """Authored same implicit differentiation: two nonzero shifts and reduced a:b>=3."""
 return generate('hard',seed,**kwargs)
def markdown(r):
 q=r['question'];g=r['generation'];f=q[':question/answer-fields'][0];correct=f.get(':answer-field/correct',[None,None])[1]
 visible_prompt=q[':question/problem'].replace('(images/','(/media/jake/SSD/EDB/math/images/')
 visible_level=q[':question/difficulty'].split('/')[-1] if ':question/difficulty' in q else 'unrated (inferred '+g['level']+')'
 lines=[f"### {g['origin']} — {visible_level} — {g['bank_profile']}",visible_prompt]
 lines += [('- [x] ' if a[':answer/id']==correct else '- [ ] ')+ '$'+a[':answer/value']+'$' for a in f[':answer-field/choices']]
 if not correct:lines += ['Captured correct designation absent; independently inferred: $'+g['inferred_correct_value']+'$.']
 if ':question/worked-solution' in q:lines += [q[':question/worked-solution']]
 else:lines += ['Captured worked solution absent.']
 return '\n\n'.join(lines)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (SUPPORTED_LEVELS if args.difficulty=='all' else (args.difficulty,)) for i in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n'.join(map(markdown,records)))
