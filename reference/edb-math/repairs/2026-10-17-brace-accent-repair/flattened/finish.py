"""Replace only source-proved accent spans; no guessing of lost scopes."""
import sys
sys.dont_write_bytecode=True
import json,re,hashlib,collections,difflib
from pathlib import Path
from source_notation import source_tex
P=Path(__file__).resolve().parent
ROWS=json.loads((P/'serialized-candidates.json').read_text())
PAT=re.compile(r'[_^]\(\s*[⏟⏞]')
MATH=re.compile(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',re.S)
def compact_indices(s):
 indices=[i for i,c in enumerate(s)if not c.isspace()]
 return ''.join(s[i]for i in indices),indices
changes=[];stats=collections.Counter()
for row in ROWS:
 before=row['before'];after=before;proofs=[]
 if row['entity']==17592186078326:
  # The archival text converter misidentified the source's absolute-value bars
  # as a matrix. Recover its two affected rows, leaving all later rows intact.
  matches=[m for m in MATH.finditer(after)if PAT.search(m.group(0))];assert len(matches)==1
  match=matches[0];block=match.group(0);source=row['accents'][0]
  oldhead=block[:block.index(r'\\'+'\n&= 16 +')]
  sourceparts=source['whole_good'].split(r' \\ ')
  newhead='$$\n'+sourceparts[0]+r' \\ '+sourceparts[1]+' '
  assert r'\begin{vmatrix}' in oldhead and oldhead.count('⏟')==1
  after=after[:match.start()]+newhead+block[len(oldhead):]+after[match.end():]
  proofs.append({'mode':'source-backed-first-two-rows','before':oldhead,'after':newhead,'mathml':source['math_source'],'source_tex':source['whole_good'],'reason':'The lost underbrace scope overlaps an erroneous matrix generated from absolute-value delimiters; source rows are restored verbatim through the repaired converter. Later rows unchanged.'})
 else:
  for a in sorted(row['accents'],key=lambda a:len(a['bad']),reverse=True):
   target=re.sub(r'\s+','',a['bad'])
   good=source_tex(a['mathml'])
   while True:
    compact,indices=compact_indices(after);at=compact.find(target)
    if at<0:break
    start=indices[at];end=indices[at+len(target)-1]+1
    old=after[start:end]
    assert re.sub(r'\s+','',old)==target
    extra={}
    if row['entity']==17592186224898:
     # The archived MathML itself omitted the leading minus from the brace.
     # Include that existing token in its scope; the equation token order stays
     # exactly the same and the annotated expression now equals its -6x label.
     assert target==r'5x-x_(⏟)_(-6x)',target
     source_match=old
     prefix=after[:start].rstrip()
     assert prefix.endswith('-'),prefix[-60:]
     start=len(prefix)-1;old=after[start:end]
     corrected_base='-5x - x'
     assert re.sub(r'\s+','',old.split('_(⏟)')[0])==re.sub(r'\s+','',corrected_base)
     import sympy
     x=sympy.Symbol('x')
     assert sympy.simplify((-5*x-x)-(-6*x))==0
     good=r'\underbrace{'+corrected_base+'}_{-6x}'
     extra={'mode':'source-scope-correction-preserving-equation-tokens',
            'source_fragment_matched_ignoring_whitespace':source_match,
            'source_scope_tex':source_tex(a['mathml']),
            'source_correction':'The original source excludes the leading minus from a brace labelled -6x. Move that existing minus into the brace without altering the equation tokens.',
            'algebra_verification':{'expression':'-5*x-x','label':'-6*x','difference':str(sympy.simplify((-5*x-x)-(-6*x))),'visible_equation_tokens_unchanged':True}}
     stats['source_annotation_scope_corrections']+=1
    after=after[:start]+good+after[end:]
    proofs.append({'mode':'exact-source-converter-output-ignoring-whitespace','before':old,'after':good,'raw_serialized_source_tex':a['good'],'notation_policy':'Historical spelling retained for non-accent math; label words use text mode and original [math] wrappers are interpreted as math.','mathml':a['mathml'],'source_bad_tex':a['bad'],'source_flattened_text':a['raw']}|extra)
 assert after!=before,(row['entity'],'unchanged')
 assert not PAT.search(after),(row['entity'],'remaining flattened marker')
 assert before.count('⏟')+before.count('⏞') == sum(p['before'].count('⏟')+p['before'].count('⏞')for p in proofs),(row['entity'],'unexpected scope')
 # Every replacement is exact and all text outside recorded spans is invariant.
 replay=before
 for proof in proofs:
  assert proof['before'] in replay
  replay=replay.replace(proof['before'],proof['after'],1)
 assert replay==after
 assert re.findall(r'\{\{[^{}]+\}\}',before)==re.findall(r'\{\{[^{}]+\}\}',after)
 changes.append({k:row[k]for k in ['entity','attribute','sourcepath','selector','source_sha256']}|{'before':before,'after':after,'proofs':proofs,'before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':hashlib.sha256(after.encode()).hexdigest()})
 stats['changed_fields']+=1;stats['replacements']+=len(proofs);stats['recovered_accents']+=before.count('⏟')+before.count('⏞')
(P/'changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
(P/'changes.diff').write_text(''.join(''.join(difflib.unified_diff(c['before'].splitlines(True),c['after'].splitlines(True),fromfile=str(c['entity'])+c['attribute']+' before',tofile=str(c['entity'])+c['attribute']+' after'))+'\n'for c in changes))
(P/'summary.json').write_text(json.dumps(dict(stats)|{'unresolved':0,'outside_replacement_spans_unchanged':True,'source_provenance_recorded':True,'source_math_label_wrapper_spans':sum('[math]'in z['before']for x in changes for z in x['proofs']),'source_math_label_wrapper_fields':sum(any('[math]'in z['before']for z in x['proofs'])for x in changes),'nonbrace_math_policy':'Historical notation preserved; source MathML determines scope except one documented source annotation correction; words in labels restored to text mode.','source_files_hash_rechecked':all(hashlib.sha256(Path(x['sourcepath']).read_bytes()).hexdigest()==x['source_sha256']for x in changes)},indent=2)+'\n')
print(dict(stats))
