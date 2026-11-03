"""Rebuild the reviewed shorthand plan from the fixed-basis residual census."""
import json,re,sys
from collections import Counter
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.question_capture.math_format import scalable_fraction_parentheses as fix,normalize_fraction_fences_prose as prose

def skeleton(text):
    text=text.replace(r'\left','').replace(r'\right','').replace(r'\langle','⟨').replace(r'\rangle','⟩')
    return re.sub(r'\s+','',text)

def main():
    parent=H.with_name('2026-11-03-fraction-fences-database');rows=json.loads((parent/'shorthand-residuals.json').read_text());basis=json.loads((parent/'intermediate-census.json').read_text())['basis'];types=json.loads((H/'types.json').read_text())
    for row in rows:
        f=fix if row['attribute']=='answer/value' else prose
        if row['attribute']=='answer/value':assert types[str(row['entity'])][':answer/type'][':db/ident']==':answer.type/math'
        assert f(row['before'])==row['after'] and f(row['after'])==row['after']
        assert skeleton(row['before'])==skeleton(row['after'])
    report={'passed':True,'basis':basis,'repair_fields':len(rows),'repair_entities':len({r['entity'] for r in rows}),'by_attribute_repaired':dict(Counter(r['attribute'] for r in rows)),'only_fence_sizing_equivalent_angle_spelling_and_spacing_changed':True,'idempotent':True}
    (H/'proposals.json').write_text(json.dumps(rows,indent=2)+'\n');(H/'audit.json').write_text(json.dumps(report,indent=2)+'\n');(H/'excluded.json').write_text('[]\n');print(json.dumps(report))

if __name__=='__main__':main()
