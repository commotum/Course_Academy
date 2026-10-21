"""Classify every mixed-row finding and preserve exact row text for review."""
import importlib.util,json,re
from collections import Counter,defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];AUDIT=ROOT/'reference/mathacademy/audits/2026-10-18-equation-chain-import'
spec=importlib.util.spec_from_file_location('chain_formatter',ROOT/'scripts/question_capture/math_format.py');fmt=importlib.util.module_from_spec(spec);spec.loader.exec_module(fmt)
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2,ensure_ascii=False,default=str)+'\n')
def classify(row):
 if len(row)==2 and row[0] and row[1]=='=':return 'dangling'
 if len(row)==1:return 'expression' if row[0] else 'empty'
 if len(row)==2 and not row[0] and row[1].startswith('='):return 'continuation'
 if len(row)==2 and row[1].startswith('='):return 'equation'
 if len(row)==2 and not row[1]:return 'expression-empty-cell'
 return 'other-'+str(len(row))
def run():
 findings=json.loads((AUDIT/'findings.json').read_text());mixed=[f for f in findings if 'partial-empty-rhs-chain' in f['reasons']];records=[];groups=defaultdict(list)
 for f in mixed:
  for n,m in enumerate(fmt.MATH.finditer(f['value'])):
   tex=fmt._legacy_commands(m[0])
   for opening in fmt.ENV.finditer(tex):
    if opening[1]!='begin' or opening[2]!='aligned':continue
    span=fmt.environment(tex,opening.start());rows=fmt.cells(tex[span[0]:span[1]]) if span else None
    if not rows or not any(classify(r)=='dangling' for r in rows):continue
    shapes=[classify(r) for r in rows];record={'entity':f['entity'],'attribute':f['attribute'],'source_id':f.get('source_id'),'lessons':f['lessons'],'formula_index':n,'shape':shapes,'rows':rows,'tex':tex,'provenance':f['provenance']};records.append(record)
    key=' -> '.join(dict.fromkeys(shapes));groups[key].append(len(records)-1)
 save('mixed-row-inventory.json',records);save('mixed-row-groups.json',{'fields':len(mixed),'formulas':len(records),'groups':{k:{'count':len(v),'record_indices':v} for k,v in sorted(groups.items(),key=lambda x:-len(x[1]))}})
 print('Fields',len(mixed),'formulas',len(records))
 for k,indices in sorted(groups.items(),key=lambda x:-len(x[1])):
  print('\nGROUP',len(indices),k)
  for index in indices[:4]:
   r=records[index];print(index,r['entity'],r['source_id'],r['lessons'][0].get(':topic/title'));print(repr(r['rows']))
 print('sources',Counter(str(f.get('source_id'))[:2] for f in mixed))
if __name__=='__main__':run()
