"""Conservative signatures for the demonstrated equation-chain import defects."""
import importlib.util,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
IDENTITY=json.loads((HERE/'identity.json').read_text())
spec=importlib.util.spec_from_file_location('audit_math_format',ROOT/'scripts/question_capture/math_format.py');fmt=importlib.util.module_from_spec(spec);spec.loader.exec_module(fmt)
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2,ensure_ascii=False,default=str)+'\n')
def detect(text,bare=False):
 reasons=set();details=[]
 spans=[text] if bare else [m[0] for m in fmt.MATH.finditer(text)]
 # Corrupt/missing prose delimiters must not hide the TeX from this audit.
 if not spans and re.search(r'\\(?:eqalign|begin|require)\b',text):spans=[text]
 for source in spans:
  if re.search(r'\\require\s*\{',source):reasons.add('unsupported-require')
  if r'\eqalign' in source:reasons.add('legacy-eqalign')
  if ('aligned' in source or 'eqalign' in source) and re.search(r'(?<!\\)\\(?:[ \t]*\r?\n|\[\s*[+-]?(?:\d+(?:\.\d*)?|\.\d+)\s*(?:pt|pc|in|bp|cm|mm|dd|cc|sp|ex|em)\s*\])',source):reasons.add('single-backslash-row-break')
  try:
   legacy=fmt._legacy_commands(source);normalized=fmt.normalize_equality_chains(legacy)
   if normalized!=legacy:
    reasons.add('empty-rhs-equality-chain');details.append({'before':source,'proposed_layout':normalized})
   else:
    for opening in fmt.ENV.finditer(legacy):
     if opening[1]!='begin' or opening[2]!='aligned':continue
     span=fmt.environment(legacy,opening.start())
     rows=fmt.cells(legacy[span[0]:span[1]]) if span else None
     if rows and any(len(row)==2 and row[0].strip() and row[1].strip()=='=' for row in rows):
      reasons.add('partial-empty-rhs-chain');details.append({'before':source,'review':'Mixed complete/incomplete equation rows; source review required'})
      break
  except ValueError as e:reasons.add('malformed-legacy-layout');details.append({'error':str(e),'before':source})
 return sorted(reasons),details

