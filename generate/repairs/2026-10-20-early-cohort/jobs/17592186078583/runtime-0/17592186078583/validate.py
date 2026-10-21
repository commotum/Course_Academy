#!/usr/bin/env python3
"""Independent checks of displayed Newton cooling stories, full banks and stages."""
import copy,hashlib,importlib.util,json,pathlib,re,subprocess,sys,uuid
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=pathlib.Path(__file__).parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
U,C,A=sp.symbols('T k A',positive=True)
def require(ok,msg):
 if not ok:raise AssertionError(msg)
def rhs(value):
 require(value.count('=')==1,'Complete equation required')
 lhs,right=value.replace('\\\\','\\').split('=')
 require(lhs in (r'\frac{\text{d}T}{\text{d}t}','T^{′}(t) ','{T}^{′}(t)','T^{′}(t)'), 'Derivative must use the displayed temperature T and minutes t')
 right=right.replace('{T}_{S}','A').replace('{','').replace('}','').replace(' ','').rstrip('.,')
 return parse_expr(right,local_dict={'T':U,'k':C,'A':A},transformations=standard_transformations+(implicit_multiplication_application,))
def temperatures(text):
 return [(int(n),unit or 'C') for n,unit in re.findall(r'\{?(\d+)\}?\^\{(?:∘|\\circ)\}(?:\\text\{([CF])\}|C)',text)]
def formatted(text):
 require(text.count('$')%2==0,'Balanced math delimiters')
 depth=0
 for character in text:
  if character=='{':depth+=1
  if character=='}':depth-=1
  require(depth>=0,'Balanced TeX braces')
 require(depth==0 and '@@' not in text,'No unfilled braces/slots')
 require('+-' not in text and '--' not in text,'Grouped signed operations')
def independent(record):
 require(record['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE},'Exact outer knowledge_point shape')
 q=record['question'];meta=record['generation'];prompt=q[':question/problem'];level=q[':question/difficulty'].split('/')[-1]
 require(level in g.LEVELS,'Valid level enum')
 formatted(prompt);formatted(q[':question/worked-solution'])
 require('temperature' in prompt and 'minutes' in prompt and '$T(t)$' in prompt and 'constant of proportionality' in prompt,'Displayed thermal model variables and units')
 require('degrees Celsius' in prompt or 'degrees Fahrenheit' in prompt,'Declared temperature scale')
 scale='F' if 'degrees Fahrenheit' in prompt else 'C';temps=temperatures(prompt)
 require(all(unit==scale for _,unit in temps),'All temperature scales match story')
 require(len(temps)==({'easy':1,'moderate':2,'hard':3}[level]),'All source/displayed thermal givens recovered')
 if level=='easy':S=temps[0][0]
 elif level=='moderate':
  I,S=[n for n,_ in temps];require(I>S,'Cooling initial value above ambient')
  context_bounds={'thermometer':(90,110),'turkey':(120,180),'soup':(140,212),'water':(40,99),'straightener':(200,450)}
  context=next((name for name in context_bounds if name in prompt),None);require(context is not None,'Recognizable thermal context')
  low,high=context_bounds[context];require(low<=I<=high,'Actual displayed initial physically consistent with object context')
 else:
  I,S,M=[n for n,_ in temps];require(I>M>S,'Later observed reading strictly between initial and ambient')
  observed=re.search(r'After \$(\d+)\$ minutes?',prompt);require(observed is not None,'Actual observation prose time')
  h=int(observed[1]);require(1<=h<=20,'Positive bounded observation time')
  require(('After $1$ minute in' in prompt) if h==1 else ('After $'+str(h)+'$ minutes in' in prompt),'Observation time unit inflection')
  require(40<=I<=99 and M<=99,'Ordinary water container temperature below boiling')
  require(meta['parameters']['h']==h,'Time prose and selected parameter match')
  # A physical positive k exists for every displayed hard observation; not asked
  # of students, this verifies the consistency of the complete story.
  kval=sp.log(sp.Rational(I-S,M-S))/h;require(kval>0,'Observed cooling is physically realizable')
 require('t>0' in prompt or 't > 0' in prompt,'Positive time domain')
 require('k>0' in prompt or 'k > 0' in prompt,'Positive proportionality constant')
 require(meta['parameters']['S']==S,'Displayed ambient matches parameter slot')
 task={'model':'Newton cooling','ambient':S,'ambient_unit':scale,'ambient_selection_from':1 if level=='easy' else 2 if level=='moderate' else 3}
 require(meta['parameter_fingerprint']==g.digest(task),'Actual displayed assessed-task fingerprint excludes incidental numeric context and banks')
 if level in ('moderate','hard'):require(meta['parameters']['I']==I,'Displayed initial matches parameter slot')
 if level=='hard':require(meta['parameters']['M']==M,'Displayed later reading matches parameter slot')
 fields=q[':question/answer-fields'];require(len(fields)==1,'Single source field layout');f=fields[0]
 require(f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio','Observed field key/type')
 choices=f[':answer-field/choices'];require(len(choices)==5,'Complete five-member bank')
 expressions=[]
 for answer in choices:
  formatted(answer[':answer/value']);require('$' not in answer[':answer/value'],'Delimiter-free math choices')
  expressions.append(rhs(answer[':answer/value']))
 target=-C*(U-S);valid=[i for i,e in enumerate(expressions) if sp.expand(e-target)==0]
 require(len(valid)==1,'Exactly one equation preserves stated constant k, difference and sign')
 require(sp.simplify(target.subs(U,S))==0 and target.subs(U,S+1)<0,'Equilibrium and negative derivative above ambient')
 duplicates=[(i,j) for i,a in enumerate(expressions) for j,b in enumerate(expressions) if i<j and sp.expand(a-b)==0]
 if meta['bank_profile']=='q-106936':require(len(duplicates)==1 and all(valid[0] not in pair for pair in duplicates),'Only documented duplicate WRONG pair')
 else:require(not duplicates,'Whole bank rejected on mathematical equivalence')
 correct=choices[valid[0]];require(f[':answer-field/correct']==[':answer/id',correct[':answer/id']],'Correct lookup is field-owned and mathematically correct')
 solution=q[':question/worked-solution'];blocks=re.findall(r'\$\$\n(.*?)\n\$\$',solution,re.S)
 require(len(blocks)==2,'Original generic/substitution two-stage sequence')
 require(sp.expand(rhs(blocks[0].strip()).subs(A,S)-target)==0,'Actual generic worked equation')
 require(sp.expand(rhs(blocks[1].strip())-target)==0,'Actual substituted worked equation')
 require(temperatures(solution)==[(S,scale)],'Actual solution surrounding-temperature statement')
 require(solution.startswith("Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the differential equation"),'Shared source opening prose')
 require('where ${T}_{S}$ is the temperature of the surroundings, and $k>0$ is a constant of proportionality.' in solution,'Shared constant/surroundings prose')
 content=g.digest({'version':g.VERSION,'prompt':prompt,'solution':solution,'bank':sorted(a[':answer/value'] for a in choices)})
 require(content==meta['content_fingerprint'],'Content fingerprint from actual learner content')
 qid=uuid.uuid5(uuid.NAMESPACE_URL,f'course-academy/{g.KP_UUID}/{g.VERSION}/{content}');fid=uuid.uuid5(qid,'selection')
 require(q[':question/id']==str(qid) and f[':answer-field/id']==str(fid),'Stable question/field identity')
 for a in choices:
  require(a[':answer/type']==':answer.type/math' and a[':answer/id']==str(uuid.uuid5(fid,'math:'+a[':answer/value'])),'Field-owned answer identity/type')
 return expressions

def fidelity(old,new):
 q=new['question'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
 require(q[':question/problem']==old[':question/problem'],'Exact original problem wording')
 require(f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident'],'Original field key/type')
 ov=[a[':answer/value'] for a in of[':answer-field/choices']];nv=[a[':answer/value'] for a in f[':answer-field/choices']]
 require(sorted(ov)==sorted(nv),'Exact complete original bank')
 # One-to-one multiset comparison, including documented duplicate values. No
 # false claim that raw oil bank has uniquely different mathematical options.
 old_math=[rhs(v) for v in ov];new_math=[rhs(v) for v in nv]
 for value in old_math:
  matches=[i for i,e in enumerate(new_math) if sp.expand(e-value)==0];require(bool(matches),'Whole equation matched');new_math.pop(matches[0])
 require(not new_math,'No unmatched source options')
 if ':answer-field/correct' in of:
  chosen=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);require(chosen==of[':answer-field/correct'][':answer/value'],'Observed key designation match')
 if ':question/worked-solution' in old:require(q[':question/worked-solution']==old[':question/worked-solution'],'Full original solution sequence/prose match')

def failure(fn,label):
 try:fn()
 except (AssertionError,ValueError):return
 raise AssertionError('Negative control passed: '+label)


def checks(record):
 f=record['question'][':question/answer-fields'][0]
 return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Exact complete cooling model with the given k'} for a in f[':answer-field/choices']]

def fingerprint(q):
 temps=[int(n) for n in re.findall(r'\{?(\d+)\}?\^\{(?:∘|\\circ)\}',q[':question/problem'])]
 require(len(temps) in (1,2),'Observed one or two temperature givens')
 S=temps[-1];scale='F' if 'Fahrenheit' in q[':question/problem'] else 'C'
 return g.digest({'model':'Newton cooling','ambient':S,'ambient_unit':scale,'ambient_selection_from':len(temps)})

def main():
 source=json.loads((HERE/'reference/current/source.json').read_text())
 cases=json.loads((HERE/'source-cases.json').read_text())
 sources={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
 originals=[];variants=[];coverage={};sweep=0
 for case in cases:
  rec=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])
  independent(rec);fidelity(sources[case['source_id']],rec);originals.append(rec)
  # Normal bank is the observed profile in full, or the documented oil repair.
  normal=g.generate(case['level'],template=case['template'],parameters=case['parameters'])
  independent(normal);variants.append(normal)
  expected=[a[':answer/value'].replace('\\\\','\\') for a in sources[case['source_id']][':question/answer-fields'][0][':answer-field/choices']]
  actual=[a[':answer/value'] for a in normal['question'][':question/answer-fields'][0][':answer-field/choices']]
  if case['source_id']=='q-106936':
   expected.remove(r'\frac{\text{d}T}{\text{d}t}=-k(30-T)');expected.append(r'\frac{\text{d}T}{\text{d}t}=-kT')
  require(sorted(expected)==sorted(actual),'Whole normal source bank with only recorded repair')
 for level,templates in g.DEFAULT_TEMPLATES.items():
  coverage[level]={}
  for template in templates:
   unit=g.TEMPLATES[template]['unit'];ambient=range(10,41) if unit=='C' else range(50,86)
   seenS=set();seenI=set()
   for S in ambient:
    bounds=g.INITIAL_BOUNDS.get(template)
    initial=[None] if bounds is None else [max(bounds[0],S+10),bounds[1]]
    for I in initial:
     params={'S':S,**({'I':I} if I is not None else {})}
     rec=g.generate(level,template=template,parameters=params);independent(rec);sweep+=1
     require(fingerprint(rec['question'])==rec['generation']['parameter_fingerprint'],'Independent task identity')
     again=g.generate(level,seed=819,template=template,parameters=params)
     require(rec['question'][':question/id']==again['question'][':question/id'],'Stable identity independent of seed/order')
     seenS.add(S)
     if I is not None:seenI.add(I)
   coverage[level][template]={'ambient_values':sorted(seenS),'initial_boundary_values':sorted(seenI)}
   for seed in (2,19):
    rec=g.generate(level,seed=seed,template=template);independent(rec);variants.append(rec)
 # Hold initial/context fixed and change only the answer-relevant ambient slot.
 for level,template,p in [('easy','q-106932',{'S':16}),('moderate','q-106935',{'S':19,'I':90})]:
  a=g.generate(level,template=template,parameters=p);b=g.generate(level,template=template,parameters={**p,'S':p['S']+1})
  independent(a);independent(b);require(fingerprint(a['question'])!=fingerprint(b['question']),'Changed assessed ambient')
  require(a['question'][':question/worked-solution']!=b['question'][':question/worked-solution'],'Updated solution')
 # Incidental I/context/bank changes never create another task fingerprint.
 a=g.generate('moderate',template='q-106935',parameters={'S':19,'I':90})
 b=g.generate('moderate',template='q-106935',parameters={'S':19,'I':80})
 require(fingerprint(a['question'])==fingerprint(b['question']),'Initial alone is not a new assessed task')
 failure(lambda:g.generate('hard'),'Unsupported hard rejected')
 failure(lambda:g.generate('easy',parameters={'S':9}),'Ambient lower boundary')
 failure(lambda:g.generate('moderate',template='q-106935',parameters={'S':30,'I':35}),'Cooling separation boundary')
 wrong=copy.deepcopy(variants[0]);wrong['question'][':answer-fields']=[]
 # Verify actual correct-reference, solution, and displayed prompt mutations fail.
 for kind in ('key','solution','prompt'):
  bad=copy.deepcopy(variants[0]);f=bad['question'][':question/answer-fields'][0]
  if kind=='key':f[':answer-field/correct']=[':answer/id',next(x[':answer/id'] for x in f[':answer-field/choices'] if x[':answer/id']!=f[':answer-field/correct'][1])]
  if kind=='solution':bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('-k(T-', 'k(T-')
  if kind=='prompt':bad['question'][':question/problem']=bad['question'][':question/problem'].replace('{25}', '{26}')
  failure(lambda:independent(bad),'Negative '+kind)
 rows=[{'label':str(i),'record':r,'checks':checks(r)} for i,r in enumerate(originals+variants)]
 (HERE/'engine-input.json').write_text(json.dumps(rows,indent=2)+'\n')
 engine=ROOT/'generate/runs/current/check-engine'
 subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 (HERE/'review.json').write_text(json.dumps({'original_replays':originals,'generated_variants':variants},indent=2)+'\n')
 parts=['# Current source and normal output comparison','Source basis 2710. Raw oil replay keeps its duplicate wrong option as evidence; normal output repairs it. Hard is unsupported.']
 for case,a,b in zip(cases,originals,variants):parts += ['## '+case['source_id']+' source replay',g.markdown(a),'### Normal output at the same parameters',g.markdown(b)]
 for r in variants[len(cases):]:parts += ['## Changed '+r['generation']['template'],g.markdown(r)]
 (HERE/'review.md').write_text('\n\n'.join(parts)+'\n')
 files=[HERE.with_suffix('.py'),HERE/'templates.json',HERE/'source-cases.json',HERE/'validate.py']
 report={'passed':True,'status':'pass','source':{k:source[k] for k in ('database','basis','lineage')},'original_questions':len(cases),'complete_banks_exact_matched':len(cases),'source_options_matched':5*len(cases),'source_options_total':5*len(cases),'available_designations_matched':len(cases),'available_full_solutions_matched':len(cases),'sweep_records':sweep,'slot_coverage':coverage,'native_grading':json.loads((HERE/'engine-report.json').read_text()),'supported_levels':list(g.LEVELS),'unsupported_levels':['hard'],'source_errors':['Raw oil profile contains two equivalent wrong equations; normal oil bank replaces -k(S-T) with -kT.','Captured derivative fractions in five source banks have doubled TeX escapes; normal output uses single escapes.','Source body/soup/oil/chocolate wording corrected only in generated output.'],'hashes':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'no_database_writes':True}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 print(f'PASS: {len(cases)} complete source banks, {len(cases)*5} choices, {sweep} boundary records and actual native grading.')
if __name__=='__main__':main()
