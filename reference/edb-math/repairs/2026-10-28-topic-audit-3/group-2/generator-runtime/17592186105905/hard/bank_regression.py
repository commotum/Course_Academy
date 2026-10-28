import sys,json,collections,math,argparse
from pathlib import Path
W=Path(__file__).resolve().parent
E=Path(__import__('tempfile').mkdtemp(prefix='quadrilateral-bank-check-'))
sys.path.insert(0,str(W));import generator as g

def key(r):
 f=r['question'][':question/answer-fields'][0];c=f[':answer-field/correct'];cid=c[1] if isinstance(c,list) else c[':answer/id'];return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==cid)
def cues(vals):
 # Allowed inputs: five displayed positive numeric values, no target, key, geometry or output catalog.
 vals=list(map(float,vals));edges=[(i,j) for i,x in enumerate(vals) for j,y in enumerate(vals) if i!=j and abs(2*x-y)<=.151]
 centers=[i for i in range(len(vals)) if any(b==i for a,b in edges) and any(a==i for a,b in edges)]
 touched=set(i for e in edges for i in e);isolated=[i for i in range(len(vals)) if i not in touched]
 return {'double_chain_center':centers[0] if len(centers)==1 else None,'isolated_among_two_double_pairs':isolated[0] if len(edges)==2 and len(touched)==4 and len(isolated)==1 else None}
def audit(rs):
 out={}
 for fam in ['para','general']:
  rows=[r for r in rs if r.get('generation',{}).get('parameters',{}).get('family')==fam and len(r['question'][':question/answer-fields'][0][':answer-field/choices'])==5]
  for cue in ['double_chain_center','isolated_among_two_double_pairs']:
   hits=total=0
   for r in rows:
    vals=[a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']];ix=cues(vals)[cue]
    if ix is not None:total+=1;hits+=vals[ix]==key(r)
   out[fam+'/'+cue]={'correct':hits,'total':total,'available':len(rows)}
 return out
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--candidate-records',type=Path);ap.add_argument('--name',default='before');ap.add_argument('--require-safe',action='store_true');a=ap.parse_args();a.require_safe=True
 rs=json.loads(a.candidate_records.read_text()) if a.candidate_records else g.generate_batch('moderate',200,260104,E/'probe-assets',render=False)
 (E/(a.name+'-records.json')).write_text(json.dumps(rs,indent=2));result=audit(rs);(E/(a.name+'-bank-probes.json')).write_text(json.dumps(result,indent=2));print(json.dumps(result))
 if a.require_safe:assert not any(x['total']>=4 and x['correct']==x['total'] for x in result.values()),'Universal conditional bank-only cue'
