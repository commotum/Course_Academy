"""Freeze the repaired maintained converter used for source-backed recovery."""
import json,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[4]
source=(ROOT/'scripts/question_capture/dom.js').read_text()
assert "braceGlyph(n.children[1], '⏟')" in source and "braceLabel(n, cs, 'mover'" in source
(P/'dom-for-source-recovery.js').write_text(source)
(P/'converter-source.json').write_text(json.dumps({'source':'scripts/question_capture/dom.js','sha256':hashlib.sha256(source.encode()).hexdigest()},indent=2)+'\n')
