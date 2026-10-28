import json,re,sys,collections
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import validate_tex
s=(H/'propose_format.py').read_text();exec(s[s.index('def neutral(s):'):s.index('props=[];proof=[]')]);P=json.loads((H/'proposals.json').read_text());F=json.loads((H/'fields.json').read_text());src=collections.defaultdict(list)
for x in json.loads((H/'sources.json').read_text()):
 if x['attribute']=='answer/value':src[x['identity']].append(x)
def canon(x):return neutral(x).replace('∉',r'\notin').replace('∈',r'\in')
count=0
for e,a,before,ident,bare in F:
 if not bare or a!='answer/value':continue
 opts=[]
 for s in src[ident]:
  if len(s['formulas'])!=1 or not isinstance(s['formulas'][0],str):continue
  after=s['formulas'][0]
  if canon(before)!=canon(after):continue
  features=[]
  if r'\{'in after and r'\{'not in before:features.append('visible-set-braces')
  if r'\mathbf'in after and r'\mathbf'not in before:features.append('source-vector-notation')
  if r'\mathbb'in after and r'\mathbb'not in before:features.append('real-number-domain-font')
  if features:opts.append((source_tex(before,after),features,s['path']))
 unique={o[0]:o for o in opts}
 if len(unique)!=1:continue
 after,features,path=next(iter(unique.values()));validate_tex(after);P.append({'entity':e,'attribute':a,'before':before,'after':after,'reason':'source-choice-'+','.join(features),'evidence':{'source_identity':ident,'source_path':path,'semantic_match':'Whole choice formula matches after comparison-only font/brace/Unicode normalization. Answer entity and all correct links retained.'},'confidence':'high'});count+=1
(H/'proposals.json').write_text(json.dumps(P,indent=2)+'\n');print('restored bare math choices',count,'total proposals',len(P))
