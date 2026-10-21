import json,re,collections,hashlib,sys,math
from pathlib import Path
from review import parse,key,expected,eq,save,g,s
E=Path(__file__).resolve().parent
raw=json.load(open('records.json'));batch=json.load(open('runner-batch.json'))
accepted=sum([json.load(open('delivery-'+lv+'/accepted.json')) for lv in ['easy','moderate','hard']],[])
# Measure cues from the visible choices only. No use of bank-role metadata in a strategy.
def observations(records):
 out=[]
 for r in records:
  f=r['question'][':question/answer-fields'][0]
  if not f[':answer-field/type'].endswith('/radio'):continue
  opts=f[':answer-field/choices'];tex=[a[':answer/value'] for a in opts];vals=[parse(t) for t in tex];win=next(i for i,a in enumerate(opts) if a[':answer/id']==f[':answer-field/correct'][1]);qid=r['generation']['template']
  slope=[s.expand(v).coeff(g.X) for v in vals] if qid=='q-107463' else None
  # Coefficient bank common factors cancel. Choose a numeric magnitude rank,
  # the singleton/opposite-sign pair structure, and text length, without differentiating.
  co=[]
  if slope is None:
   for v in vals:
    t=v
    for xx in [2,3,5]:
     if t.subs(g.X,xx)!=0:break
    co.append(float(t.subs(g.X,xx).evalf()))
  else:co=[float(v.evalf()) for v in slope]
  magnitudes=[round(abs(v),10) for v in co];freq=collections.Counter(magnitudes)
  strategies={**{f'position {i+1}':i for i in range(5)},'longest TeX':max(range(5),key=lambda i:len(tex[i])),'shortest TeX':min(range(5),key=lambda i:len(tex[i])),'largest numeric coefficient':max(range(5),key=lambda i:co[i]),'smallest numeric coefficient':min(range(5),key=lambda i:co[i]),'largest magnitude':max(range(5),key=lambda i:magnitudes[i]),'smallest magnitude':min(range(5),key=lambda i:magnitudes[i]),'singleton magnitude':next((i for i in range(5) if freq[magnitudes[i]]==1),0)}
  # Bank repetition gives sign/magnitude cues. No source calculus used.
  out.append({'id':r['question'][':question/id'],'template':qid,'key_index':win,'sign':'negative' if co[win]<0 else 'positive','parameters':r['generation']['parameters'],'strategies':{k:i==win for k,i in strategies.items()},'tex':tex})
 return out
sets={'raw':observations(raw),'delivered':observations(accepted),'batch':observations(batch)};save('shortcut-observations.json',sets)
probes=[]
for stage,obs in sets.items():
 groups={'all radios':obs}
 for qid in sorted({v['template'] for v in obs}):
  group=[v for v in obs if v['template']==qid];groups[qid]=group
  for sign in ['positive','negative']:
   z=[v for v in group if v['sign']==sign]
   if z:groups[qid+' / '+sign]=z
 for label,group in groups.items():
  for strategy in group[0]['strategies']:
   correct=sum(z['strategies'][strategy] for z in group);total=len(group)
   probes.append({'stage':stage,'group':label,'strategy':strategy,'correct':correct,'total':total,'rate':correct/total,'baseline':.2,'perfect':correct==total})
save('shortcut-results.json',probes)
# Canonical source example is not in the sampled derivative family set.
canonical=[]
for qid,spc in g.SPECS.items():
 if spc['level']!='easy':continue
 p={'b':2,'c':3,'a':-1,'n':1,'k':0,'l':0,'d':1}
 try:r=g.generate_easy(801993,template=qid,parameters=p);canonical.append({'template':qid,'accepted':True,'record':r})
 except Exception as ex:canonical.append({'template':qid,'accepted':False,'error':str(ex)})
save('canonical-gap.json',{'source_id':'775dfc95-df31-5198-aeb2-4603b8386957 / e-728','function':'3*2**(1-x)','expected':'-3*2**(1-x)*ln(2)','attempts':canonical,'explanation':'No template includes an outside-scaled linear exponent in easy sampling; all scaled easy templates have degree 2 or 3.'})
# Distribution and actual read-only selection rule support at captured basis.
def coverage(rs):
 d={}
 for r in rs:
  q=r['generation']['template'];p=r['generation']['parameters'];z=d.setdefault(q,{'n':0,'bases':set(),'a_signs':set(),'bank_roles':set(),'points':set()});z['n']+=1;z['bases'].add(p['b']);z['a_signs'].add('negative' if p['a']<0 else 'positive');z['bank_roles'].add(r['generation'].get('bank_role'));z['points'].add(p.get('point'))
 return {q:{k:sorted(v,key=str) if isinstance(v,set) else v for k,v in z.items()} for q,z in d.items()}
inv=json.load(open('../source/inventory.json'));bands=collections.Counter((q.get(':question/difficulty') or {}).get(':db/ident','unrated') for q in inv['questions'])
# Actual selector: weighted band then uniform on sorted unique IDs; no policy/history in captured inventory.
# Conditional easy-band draw reproduced for 4096 task seeds over fresh reviewed candidate surrogate IDs.
easy=[r for r in accepted if r['question'][':question/difficulty'].endswith('/easy')]
counts=collections.Counter();seen=set()
for i in range(4096):
 digest=hashlib.sha256(('course-academy/question-selection/v1/independent-review-'+str(i)).encode()).digest();uniform=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53);index=math.floor(uniform*len(easy));seen.add(index);counts[easy[index]['generation']['template']]+=1
selection={'source_file':'engine/rust/question_selection.rs','captured_basis':inv['basis'],'captured_inventory_bands':dict(bands),'raw':coverage(raw),'delivered':coverage(accepted),'runner_batch':coverage(batch),'easy_conditional_draws':{'seeds':'independent-review-0 through independent-review-4095','algorithm':'select(): uniform(8) SHA256 53 bits, floor(U*pool.len); fresh easy-band pool','candidates':len(easy),'visited':len(seen),'template_counts':dict(counts)},'rules':['seen_before_task excludes previous task contents; caller also excludes current prefix.','select sorts and deduplicates entity IDs, picks weighted available band, then a uniform candidate in it.','With no configured weights, select returns the first candidate, not a uniform draw.','Zero-weight bands are excluded; unrated candidates fall back only when no weighted rated band remains.'],'limits':['Captured inventory lacks learner histories, active policy and future database entity IDs. Uniform configured easy-band support is conditional; no claim of actual personalized frequency.','Unconfigured or zero easy-weight policies can suppress this band; these are application policy choices, not generator sampling guarantees.','No publication preparation file exists. Used actual prepare_records read-only against captured inventory.','Concurrent inventory or history changes may remove decision cases.'],'rejections':json.load(open('boundaries.json'))['sampler_rejections']};save('selection-coverage.json',selection)
print('Perfect conditional cues (n>=4):',json.dumps([z for z in probes if z['perfect'] and z['total']>=4 and z['stage']=='delivered'],indent=2))
print('Canonical replay accepted:',sum(z['accepted'] for z in canonical))
