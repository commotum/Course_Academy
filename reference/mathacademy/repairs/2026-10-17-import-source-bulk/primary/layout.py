"""Source-preserving layout overrides for measured content regressions.

Only repaired spans in independently measured overflowing fields qualify.
Keep Markdown-table cells inline in their existing scroll container. Delimiter
promotion does not touch TeX; explicit chain/system layouts preserve every
source expression in order. Root applies these after overlapping queues merge.
"""
from pathlib import Path
import collections,hashlib,json,re
HERE=Path(__file__).resolve().parent;BULK=HERE.parent
INPUT=BULK/'integrated-changes.json'
FAILURES=[BULK/'review/layout-failures-v1.json',BULK/'review/layout-failures-a4fe.json']

def top_level_split(value,separator):
 pieces=[];start=0;depth=0;i=0
 while i<len(value):
  if depth==0 and value.startswith(separator,i):pieces.append(value[start:i]);i+=len(separator);start=i;continue
  if value[i]=='\\':i+=2;continue
  if value[i]=='{':depth+=1
  elif value[i]=='}':depth-=1
  assert depth>=0,('Unbalanced source braces',value)
  i+=1
 assert depth==0,('Unbalanced source braces',value)
 pieces.append(value[start:]);return pieces

def main():
 inputs=json.loads(INPUT.read_text());changes=inputs['changes'] if isinstance(inputs,dict) else inputs
 failing={(int(f['entity']),x['attribute']) for path in FAILURES for f in json.loads(path.read_text()) for x in f.get('changed_fields',f.get('changes',[])) if x['attribute']!=':answer/value'}
 overrides=[];skip=[]
 for row in changes:
  key=row['entity'],row['attribute']
  if key not in failing:continue
  for span in row['replacements']:
   prior=span['after'];reason='promote-restored-complex-inline-math-to-display'
   line=row['before'][row['before'].rfind('\n',0,span['start'])+1:span['start']]
   if line.lstrip().startswith('|'):
    skip.append({'entity':row['entity'],'attribute':row['attribute'],'source_occurrence_id':span['source_occurrence_id'],'reason':'existing-scrollable-Markdown-table-cell'});continue
   if not prior.startswith('$') or prior.startswith('$$'):
    skip.append({'entity':row['entity'],'attribute':row['attribute'],'source_occurrence_id':span['source_occurrence_id'],'reason':'already-display-or-not-inline-math'});continue
   closing=prior.rfind('$');assert closing>0
   tex=prior[1:closing];tail=prior[closing+1:];assert re.fullmatch(r'[,.;:?!\s]*',tail)
   if re.fullmatch(r'\s*\d+(?:\.\d+)?\s*\\mathrm\{\\%\s*\}\s*',tex):
    skip.append({'entity':row['entity'],'attribute':row['attribute'],'source_occurrence_id':span['source_occurrence_id'],'reason':'short-percentage-does-not-cause-overflow'});continue
   adjusted=tex;expressions=None
   if span['source_occurrence_id'] in ('242:step-15744:356301','1166:step-15792:151062'):
    expressions=[x.strip() for x in top_level_split(tex,'=')];assert len(expressions)>=3 and all(expressions)
    adjusted='\\begin{aligned}\n'+expressions[0]+' &='+expressions[1]+' \\\\\n'+' \\\\\n'.join('&='+x for x in expressions[2:])+'\n\\end{aligned}'
    assert ''.join(expressions)==re.sub(r'\s+','',tex.replace('=','')) or re.sub(r'\s+','',''.join(expressions))==re.sub(r'\s+','',tex.replace('=',''))
    reason='stack-equivalent-vector-representations-on-successive-equality-lines'
   if span['source_occurrence_id']=='2809:step-26970:229599':
    expressions=[x.strip() for x in top_level_split(tex,r'\qquad') if x.strip()];assert len(expressions)==3
    assert all(label in expr for label,expr in zip((r'\text{I.}',r'\text{II.}',r'\text{III.}'),expressions))
    adjusted='\\begin{array}{l}\n'+(' \\\\[1em]\n'.join(expressions))+'\n\\end{array}'
    reason='stack-three-distinct-labeled-congruence-systems-in-source-order'
   if span['source_occurrence_id']=='6669:question-340920:202531':
    expressions=[x.strip() for x in top_level_split(tex,r'\hspace{2em}') if x.strip()];assert len(expressions)==3
    assert all(re.match(label+r'\s*\(\s*x\s*\)\s*=',expr) for label,expr in zip(('f','g','h'),expressions))
    adjusted='\\begin{array}{l}\n'+(' \\\\[1em]\n'.join(expressions))+'\n\\end{array}'
    reason='stack-three-distinct-function-definitions-in-source-order'
   after='$$\n'+adjusted+'\n$$'+tail
   overrides.append({'entity':row['entity'],'attribute':row['attribute'],'start':span['start'],'end':span['end'],'source_occurrence_id':span['source_occurrence_id'],'before':span['before'],'before_after':prior,'after':after,'reason':reason,'original_math':tex,'layout_math':adjusted,'math_bytes_unchanged':tex==adjusted,'ordered_source_expressions':expressions,'source_sha256':span.get('source_sha256')})
 output={'input':str(INPUT),'input_sha256':hashlib.sha256(INPUT.read_bytes()).hexdigest(),'measured_failures':[str(path) for path in FAILURES],'overrides':overrides,'skipped':skip,'summary':{'fields':len({(x['entity'],x['attribute']) for x in overrides}),'overrides':len(overrides),'reasons':dict(collections.Counter(x['reason'] for x in overrides)),'skipped':dict(collections.Counter(x['reason'] for x in skip))}}
 (HERE/'layout-overrides.json').write_text(json.dumps(overrides,ensure_ascii=False,indent=2)+'\n')
 (HERE/'layout-summary.json').write_text(json.dumps({k:v for k,v in output.items() if k!='overrides'},ensure_ascii=False,indent=2)+'\n');print(json.dumps(output['summary'],indent=2))
if __name__=='__main__':main()
