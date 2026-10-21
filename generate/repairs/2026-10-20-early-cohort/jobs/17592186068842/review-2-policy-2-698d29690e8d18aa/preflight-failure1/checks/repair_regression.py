"""Strict regression for f1832733ee777b3c1e25; no services or runtime writes."""
import importlib.util,json,pathlib,sys
sys.dont_write_bytecode=True
ROOT=pathlib.Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('target',ROOT/'17592186068842.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
D=r'\frac{\text{d}y}{\text{d}x}'
def probe(r):
 q=r['question'];f=q[':question/answer-fields'][0];cs=f[':answer-field/choices'];key=f[':answer-field/correct'][1]
 bare=[a for a in cs if r'\frac' not in a[':answer/value'].replace(D,'D')]
 correct=next(a for a in cs if a[':answer/id']==key)
 return {'question_id':q[':question/id'],'template':r['generation']['template'],'parameters':r['generation']['parameters'],'bank_profile':r['generation'].get('bank_profile'),'fractionless_count':len(bare),'shortcut_success':len(bare)==1 and bare[0][':answer/id']==key,'equal_length_wrong':any(a[':answer/id']!=key and len(a[':answer/value'])==len(correct[':answer/value']) for a in cs)}
def records():
 rs=[g.generate_easy(17,'simple_quotient',parameters={'n':1}),g.generate_easy(2404317989,'exp_quotient',parameters={'base':4,'a':3,'n':4})]
 rs += [g.generate_easy(seed,t) for t in ('simple_quotient','exp_quotient') for seed in range(27011,27017)]
 # These seeds select the two profiles before values; test every supported y power.
 for t in ('simple_quotient','exp_quotient'):
  for n in range(1,5):
   for seed in (0,1):
    p={'n':n} if t=='simple_quotient' else {'n':n,'base':2 if n%2 else 5,'a':1 if n%2 else 5}
    rs.append(g.generate_easy(seed,t,parameters=p))
 return rs
if __name__=='__main__':
 from visible_math import check_record,sep
 rs=records();out=[probe(r) for r in rs]
 assert not any(v['shortcut_success'] for v in out), 'unique fractionless shortcut persists'
 assert all(v['fractionless_count']>=2 and v['equal_length_wrong'] for v in out), 'replacement layout cue'
 for r in rs:
  cs=r['question'][':question/answer-fields'][0][':answer-field/choices']
  assert sum(sep(a[':answer/value']) and r'\frac' not in a[':answer/value'].replace(D,'D') for a in cs)>=2, 'layout plus form shortcut'
 math=[check_record(r) for r in rs];assert all(v['passed'] for v in math), 'invalid bank or worked stage'
 for t in ('simple_quotient','exp_quotient'):
  assert len({v['bank_profile'] for v in out if v['template']==t})==2
 (ROOT/'evidence/repair-records.json').write_text(json.dumps(rs,indent=2,ensure_ascii=False))
 (ROOT/'evidence/repair-regression.json').write_text(json.dumps({'finding':'f1832733ee777b3c1e25','tested':len(rs),'passed':True,'probes':out,'math':math},indent=2,ensure_ascii=False))
 print('repair regression:',len(rs),'cases passed; exact minimal and batch parameters retained')
