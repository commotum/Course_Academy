import json,pathlib,re,hashlib
from fractions import Fraction
from math import isqrt
from collections import Counter,defaultdict
E=pathlib.Path(__file__).resolve().parent
J=E.parent;W=J/'workspace'
def load(n):return json.load(open(E/n))
def save(n,d):(E/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def signature(tex):
 t=tex.replace(' ','').replace('\\dfrac','\\frac');s=-1 if t.startswith('-') else 1;t=t.lstrip('-')
 if '\\pi' in t:
  m=re.fullmatch(r'\\frac\{\\pi\}\{(\d+)\}',t)
  return 'pi',str(Fraction(s,int(m[1]) if m else 1))
 m=re.fullmatch(r'(\d*)\\sqrt\{(\d+)\}',t)
 if m:
  a=s*int(m[1] or 1);b=int(m[2]);factor=1
  for n in range(2,isqrt(b)+1):
   while b%(n*n)==0:factor*=n;b//=n*n
  if b==1:return 'rational',str(Fraction(a*factor))
  return 'root',str(b),str(a*factor)
 m=re.fullmatch(r'\\frac\{(\d+)\}\{(\d+)\}',t)
 return 'rational',str(Fraction(s*int(m[1]),int(m[2])) if m else s*Fraction(t))
def truth(r):
 q=r['question'];return [next(a[':answer/value']=='true' for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]) for f in q[':question/answer-fields']]
records=load('batch-records.json')+load('fresh-records.json')+load('controlled-records.json')+load('counterfactual-records.json')
fail=[];eqs=0;bullets=0
for ix,r in enumerate(records):
 q=r['question'];sol=q[':question/worked-solution'];lines=[l for l in sol.splitlines() if l.startswith('- ')];assert len(lines)==4
 for i,line in enumerate(lines):
  bullets+=1;m=re.search(r'^- \$([^$]+)\$',line);parts=m[1].split('=')
  for a,b in zip(parts,parts[1:]):
   eqs+=1
   if signature(a)!=signature(b):fail.append({'index':ix,'line':line,'problem':'false displayed equality'})
  selected='Therefore, it belongs to' in line
  if selected != truth(r)[i]:fail.append({'index':ix,'line':line,'problem':'solution/key discrepancy'})
  head=signature(parts[0]);rat=head[0]=='rational';integer=rat and Fraction(head[1]).denominator==1
  if 'it is an integer' in line and not integer:fail.append({'index':ix,'line':line,'problem':'false integer claim'})
  if 'it is an irrational real number' in line and rat:fail.append({'index':ix,'line':line,'problem':'false irrational claim'})
  if 'it is a rational number but not an integer' in line and (not rat or integer):fail.append({'index':ix,'line':line,'problem':'false rational noninteger claim'})
  # Decimal explanation includes a second rational representation after the first display.
  if 'since it can be written as $' in line:
   rhs=re.search(r'since it can be written as \$([^$]+)\$',line)[1];eqs+=1
   if signature(parts[0])!=signature(rhs):fail.append({'index':ix,'line':line,'problem':'false decimal conversion'})
 selected=[f[':answer-field/key'] for f,v in zip(q[':question/answer-fields'][:4],truth(r)[:4]) if v]
 expected='; '.join(selected)+'.' if selected else 'None of those listed.'
 if not sol.endswith(expected):fail.append({'index':ix,'problem':'conclusion does not name exactly selected values'})
save('solution-checks.json',{'records':len(records),'bullets':bullets,'exact_equalities':eqs,'failures':fail,'method':'Independent square-factor extraction and Fraction identities; visible solution membership conclusions and number classifications checked against independently audited keys.'})
# Repeat decision probes on delivered records, and faithfully reproduce question_selection.rs::select for all-easy pools.
def mask(r):return sum(1<<i for i,v in enumerate(truth(r)[:4]) if v)
def probes(rs):
 result=[]
 groups={'all':rs}
 for r in rs:groups.setdefault(r['generation']['profile'],[]).append(r)
 for t,rr in groups.items():
  for name,pred in [('first only',lambda r:1),('last only',lambda r:8),('none',lambda r:0),('all',lambda r:15),('positions III and IV',lambda r:12),('sign and zero only, ignoring base class',lambda r:signmask(r))]:
   result.append({'subgroup':t,'strategy':name,'correct':sum(mask(r)==pred(r) for r in rr),'total':len(rr),'baseline':1/16})
 return result
def signmask(r):
 p=r['question'][':question/problem'];sg='+' if '^{+}' in p else '-';zero='_0' in p;out=0
 for i,f in enumerate(r['question'][':question/answer-fields'][:4]):
  tex=f[':answer-field/key'].replace('$','');sign=0 if signature(tex)==('rational','0') else -1 if tex.startswith('-') else 1
  if (sign==0 and zero) or sign==(1 if sg=='+' else -1):out|=1<<i
 return out
stages={}
for name,raw,delivered in [('batch','batch-records.json','delivery-batch/accepted.json'),('fresh','fresh-records.json','delivery-fresh/accepted.json')]:
 before=load(raw);after=load(delivered)
 # all records easy; real positively weighted easy band yields uniform pool draw from second digest chunk.
 selections=[]
 for k in range(128):
  seed='independent-selection-'+str(k);digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53);index=int(u*len(after));r=after[index]
  selections.append({'seed':seed,'synthetic_order_index':index,'question_id':r['question'][':question/id'],'mask':mask(r),'profile':r['generation']['profile']})
 stages[name]={'raw_count':len(before),'accepted_count':len(after),'raw_masks':dict(Counter(str(mask(r)) for r in before)),'delivered_masks':dict(Counter(str(mask(r)) for r in after)),'raw_probes':probes(before),'delivered_probes':probes(after),'learner_selection':selections,'selected_masks':dict(Counter(str(r['mask']) for r in selections))}
save('delivery-selection-checks.json',{'command':'python3 finish_checks.py','source':'engine/rust/question_selection.rs::select and seen_before_task','stages':stages,'generator_rejection':'sample excludes already-used exact semantic values before drawing; no rejection/resampling of masks. Each target/mask 0..15 generated successfully. explicit None preserves mask 0; nonempty policy does not remove it. All delivered and sampled records easy.','selection_basis':'Captured inventory basis 5456, no learner history supplied. For each all-easy proposed pool, uniform positively weighted easy-band branch reproduced from Rust SHA256 draw. Local order stands for an explicitly specified candidate ordering; database entity IDs for new records do not yet exist. Any entity ordering still gives every fresh usable easy member positive probability. Prefix/history excludes already seen questions; unknown actual exclusions cannot be predicted. No configured weights chooses smallest entity instead, so no random-coverage guarantee in that branch.','limitations':['No live database or learner history accessed; original inventory has no generation metadata for five non-source records, preventing exact regeneration attribution.','Publication preparation absent. Actual normalization, difficulty and deduplication executed read-only against captured inventory; concurrent inventory can change.','Uniform branch tested with synthetic ordered eligible candidates; actual future entity assignment and arbitrary history not claimed.']})
save('render-inspection.json',{'report':'render/rendering.json','screenshots_inspected':['render/question-001.png','render/question-002.png','render/question-003.png','render/question-005.png','render/question-006.png'],'observations':['Target Q0+ -> R0+ visibly changes only the target in the prompt, adds sqrt2 to selection, and updates explanation/conclusion.','Replacing 1/2 by 3/4 visibly preserves selection pattern and updates the value in explanation/conclusion.','Empty-mask case clearly presents a selected explicit None checkbox, readable radicals and full worked explanation.','Exact runner batch first record renders sqrt9=3, pi, zero, negative integer and all five checkbox controls correctly.'],'passed':True,'limits':'Only six representative generated checkbox records rendered; absent radio source construction cannot be certified.'})
save('scope-checks.json',{'source_refs':['tutorial 05d0929b-b494-531b-9eea-35af04606555','ce8a56c1-709e-50e8-ac10-d3f92bf15db0','0e62d29f-2834-5b4e-b720-bc361e2a5dc0','ac020dea-1486-5e82-bd01-29594c8fbf7a'],'judgment':'Actual generated families retain four simple real candidates and independent sign/class/zero membership; fractions can reduce to integers, roots can simplify or remain irrational, pi and terminating decimals stay within lesson. No new operators or prerequisites or free-entry requirements. Missing source families are coverage/fidelity failures, separately recorded.','records_examined':['batch-records.json','fresh-records.json','controlled-records.json','counterfactual-records.json'],'difficulty':'easy','workload':'four classifications per question; explicit None equivalent empty-subset action grounded in two original checkbox sources'})
save('package-integrity.json',{'unchanged':load('package-hashes-before.json')=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in W.iterdir() if p.is_file()},'after':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in W.iterdir() if p.is_file()},'unlisted_files':sorted(p.name for p in W.iterdir() if p.is_dir())})
print(json.dumps({'solution_failures':len(fail),'equalities_checked':eqs,'batch_sign_only':stages['batch']['delivered_probes'][5],'fresh_sign_only':stages['fresh']['delivered_probes'][5],'integrity':load('package-integrity.json')['unchanged']},indent=2))
