from pathlib import Path
import json
prev=Path('../review-0-policy-2-8b996ed7d80a08a9')
t=(prev/'review.py').read_text()
# Reuse the independent mathematical parser/checker, with its provenance intact.
start=t.index('x,y,z=sp.symbols');end=t.index('source=load(')
header=t[:t.index("save('package-before.json'")]
Path('review_lib.py').write_text(header+t[start:end])
Path('reused-provenance.json').write_text(json.dumps({'source_analysis':str(prev/'source-analysis.json'),'math_parser':str(prev/'review.py'),'method':'Copied independent exact equation/vector and solution-chain checker; current checks rerun. No prior package result treated as current evidence.'},indent=2))
