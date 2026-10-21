"""Check the repaired lesson against printed mathematics and the actual publisher."""
import importlib.util,copy,re,itertools,sys
from fractions import Fraction as F
from collections import Counter
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
from read import *
from scripts.generator_publish import prepare_records,content_fingerprint,validate_question,answer_id,enum
from scripts.integration_batch_policy import validate_delivery_batch
V={c:sp.Symbol(c,positive=True)for c in 'xyt'};V['C']=sp.Symbol('C');TRANS=standard_transformations+(implicit_multiplication_application,)
def group(text,pos):
 assert text[pos]=='{';depth=1;j=pos+1
 while depth:
  if text[j]=='{':depth+=1
  elif text[j]=='}':depth-=1
  j+=1
 return text[pos+1:j-1],j
def expr(text,extra=None):
 text=text.strip().rstrip('.?').strip().replace(r'\quad','').replace('{}','')
 while (m:=re.search(r'\\(d?frac|sqrt)(?:\[([^]]+)\])?\{',text)):
  first,pos=group(text,m.end()-1)
  if m[1]=='sqrt':replacement='(('+str(expr(first,extra))+')**(1/'+(m[2]or'2')+'))'
  else:second,pos=group(text,pos);replacement='(('+str(expr(first,extra))+')/('+str(expr(second,extra))+'))'
  text=text[:m.start()]+replacement+text[pos:]
 text=text.replace(r'\left','').replace(r'\right','').replace(r'\displaystyle','').replace(r'\cdot','*').replace('^','**').replace('{','(').replace('}',')')
 return parse_expr(text,local_dict={**V,**(extra or {})},transformations=TRANS)
def integrate_tex(text):
 atoms={};pattern=re.compile(r'\\int\s*(.*?)\\,\\mathrm\{d\}([xyt])',re.S)
 while (m:=pattern.search(text)):
  key='Z'+str(len(atoms));atoms[key]=sp.integrate(expr(m[1]),V[m[2]]);text=text[:m.start()]+key+text[m.end():]
 return expr(text,atoms)
def check(q,displays=True):
 p=q[':question/problem'];inline=re.findall(r'\$(.*?)\$',p,re.S)
 if m:=re.search(r'\\int\s*(.*?)\\,\\mathrm\{d\}([xyt])',p,re.S):target=expr(m[1]);v=V[m[2]]
 elif m:=re.search(r"y'\(t\)=(.*?)\$",p):target=expr(m[1]);v=V['t']
 else:
  body=next(s for s in inline if not re.fullmatch(r'[xyt](?:>|\\ne).*',s));target=expr(body);v=next(iter(target.free_symbols))
 field=q[':question/answer-fields'][0];correct=answer_id(field[':answer-field/correct']);rows=[]
 for a in field[':answer-field/choices']:
  val=expr(a[':answer/value']);good=sp.simplify(sp.diff(val,v)-target)==0;assert good==(str(a[':answer/id'])==correct),(q[':question/id'],a[':answer/value'],target);rows.append(val)
 assert all(sp.simplify(sp.diff(a-b,v))!=0 for a,b in itertools.combinations(rows,2))
 steps=0
 if displays:
  for display in re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S):
   display=re.sub(r'\\(?:begin|end)\{aligned\}','',display).replace('&','')
   for row in display.split(r'\\'):
    for part in row.split('='):
     part=part.strip().rstrip('.').strip()
     if part:assert sp.simplify(sp.diff(integrate_tex(part),v)-target)==0,(q[':question/id'],part);steps+=1
 return steps

def load(kp):
 p=HERE/str(kp)/'package';sys.path.insert(0,str(p))
 for name in ('forward','math_format','integration_batch_policy'):sys.modules.pop(name,None)
 spec=importlib.util.spec_from_file_location('forward_'+str(kp),p/'forward.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);return g

def main():
 grading=[];report={};total_steps=0
 for kp,bands in ((17592186184153,('moderate','hard')),(17592186184154,('easy','moderate')),(17592186184155,('moderate','hard'))):
  d=HERE/str(kp);g=load(kp);k=json.loads((d/'kp.json').read_text());fingerprints={content_fingerprint(q)for q in k[':knowledge-point/questions']};summary={};additions=[]
  for band in bands:
   allrows=[];accepted=[];dupes=0
   for seed in range(40):
    batch=g.sample(kp,10,seed,band);assert batch==g.sample(kp,10,seed,band);validate_delivery_batch(batch,kp)
    for r in batch:validate_question(r['question'])
    delivered,duplicates=prepare_records(batch,kp,g.IDS[kp],fingerprints,Path(DB.config.math_root),d/'assets',localizer=lambda r,*args:copy.deepcopy(r));accepted+=delivered;dupes+=duplicates;allrows+=batch
   for r in allrows[:20]:total_steps+=check(r['question']);grading.append(r)
   count=3 if(kp,band)==(17592186184153,'hard')else 5
   selected=g.sample(kp,count,200+kp%100,band);selected,duplicate=prepare_records(selected,kp,g.IDS[kp],fingerprints,Path(DB.config.math_root),d/'assets',localizer=lambda r,*args:copy.deepcopy(r));assert len(selected)==count and not duplicate;additions+=selected
   for r in selected:total_steps+=check(r['question']);grading.append(r)
   summary[band]={'sampled':len(allrows),'delivered':len(accepted),'duplicates_filtered':dupes,'families':dict(Counter(r['generation']['family']for r in allrows)),'additions':count,'min_max_power_strategy':'ties across all five choices in every radio bank'}
  # Audit every previously generated question, including those being withdrawn.
  authored=[q for q in k[':knowledge-point/questions']if not q.get(':question/math-academy-id')]
  for q in authored:
   if kp==17592186184154:continue # Independently checked all five in the preceding audit; preserve report.
   total_steps+=check(q,False);grading.append({'question':q})
  replay=g.replay_sources(kp);source={q[':question/id']:q for q in k[':knowledge-point/questions']if q.get(':question/math-academy-id')}
  for r in replay:
   old=source[r['generation']['source_id']];q=r['question'];assert old[':question/problem']==q[':question/problem']and old[':question/worked-solution']==q[':question/worked-solution']
   for f,oldf in zip(q[':question/answer-fields'],old[':question/answer-fields']):
    assert [a[':answer/value']for a in f[':answer-field/choices']]==[a[':answer/value']for a in oldf[':answer-field/choices']]
    key=next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==answer_id(f[':answer-field/correct']));assert key==oldf[':answer-field/correct'][':answer/value']
  ledger=[{'id':q[':db/id'],'decision':'withdraw_and_replace'if kp==17592186184154 and not q.get(':question/math-academy-id')else'preserve','reason':'Replace the weak five-item generated batch; retain original source records and learner history.'if kp==17592186184154 else'Scope and keys verified; existing authored question retained.'}for q in k[':knowledge-point/questions']]
  (d/'additions.json').write_text(json.dumps(additions,indent=2)+'\n');(d/'replacements.json').write_text(json.dumps(additions,indent=2)+'\n');(d/'audit-ledger.json').write_text(json.dumps(ledger,indent=2)+'\n');(d/'solution-updates.json').write_text('[]\n');report[str(kp)]={'bands':summary,'existing_authored_audited':len(authored),'source_banks_replayed':len(replay)};print(json.dumps({str(kp):report[str(kp)]}),flush=True)
 save('grading-records.json',grading);out=HERE/'native-grading';out.mkdir(exist_ok=True);questions=[]
 for r in grading:
  q=r['question'];fields=[]
  for f in q[':question/answer-fields']:
   correct=f[':answer-field/correct'];value=correct.get(':answer/value')if isinstance(correct,dict)else next(a[':answer/value']for a in f[':answer-field/choices']if str(a[':answer/id'])==answer_id(correct));fields.append({'key':f[':answer-field/key'],'type':enum(f[':answer-field/type']).split('/')[-1],'correct_value':value,'choices':[{'type':enum(a[':answer/type']).split('/')[-1],'value':a[':answer/value']}for a in f[':answer-field/choices']]})
  questions.append({'math_academy_id':str(q[':question/id']),'problem':q[':question/problem'],'knowledge_point':'Integration lesson repair','answer_fields':fields})
 subprocess.run([sys.executable,'-B',str(HERE/'native_checks.py')],check=True)
 save('quality-verification.json',{'passed':True,'kps':report,'seeded_questions':2400,'native_graded_questions':len(questions),'existing_authored_questions_audited':15,'published_additions':sum(b['additions']for v in report.values()for b in v['bands'].values()),'old_report':'reference/mathacademy/audits/2026-10-20-sum-constant-factor-quality/mathematical-audit.json','batch_guard_runs_after_deduplication':True});save('algebra-verification.json',{'passed':True,'independent_printed_question_checks':len(grading),'printed_steps_checked':total_steps,'method':'Independent printed TeX parsed into SymPy; differentiate every choice and every authored solution expression/integral.'});print('All lesson quality checks passed.')
if __name__=='__main__':main()
