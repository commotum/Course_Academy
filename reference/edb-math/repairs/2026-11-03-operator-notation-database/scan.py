"""Classify the complete fixed-basis operator census before proposing writes."""
import collections,gzip,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.question_capture.math_format import MATH,normalize_inverse_trig_operators as fix
OPS=('arcsin','arccos','arctan','sinh','cosh','tanh','sin','cos','tan','sec','csc','cot','ln','log','exp','arg','lim','min','max','det')

def run():
    path=H/'snapshot.jsonl';stream=path.open() if path.exists() else gzip.open(path.with_suffix('.jsonl.gz'),'rt')
    candidates={};marked=collections.Counter();legacy=collections.Counter();bare=collections.Counter();examples={};counts=collections.Counter();fields={}
    for line in stream:
        row=json.loads(line);e,a,text=row['e'],row['a'],row['raw_string']
        if not isinstance(text,str):continue
        key=(e,a)
        if key in fields:assert fields[key]==text;continue
        fields[key]=text;counts[a]+=1
        spans=[text] if a=='answer/value' else [m[0] for m in MATH.finditer(text)]
        after=fix(text) if a=='answer/value' else MATH.sub(lambda m:fix(m[0]),text)
        if after!=text:candidates[key]={'entity':e,'attribute':a,'before':text,'after':after,'source':row['source'],'tx':row['tx']}
        for block in spans:
            # Ignore correctly wrapped names and literal prose before looking
            # for the exact missing-command forms; retain examples for review.
            clean=re.sub(r'\\(?:operatorname|text|textrm|mathrm|mathit|mathbf)\*?\s*\{[^{}]*\}',lambda m:' '*len(m[0]),block)
            for m in re.finditer(r'(?<![A-Za-z\\])('+'|'.join(OPS)+r')(?=\}?(?:[_^]\{[^{}]*\})*(?:\u2061|\\u2061))',clean):
                marked[m[1]]+=1;examples.setdefault('marked/'+m[1],[])
                if len(examples['marked/'+m[1]])<3:examples['marked/'+m[1]].append({'entity':e,'attribute':a,'text':text[:900]})
            for m in re.finditer(r'\\([A-Za-z]+)',clean):
                if m[1] in OPS:continue
                for op in OPS:
                    if m[1].startswith(op) and len(m[1])==len(op)+1:
                        legacy[m[1]]+=1;examples.setdefault('legacy/'+m[1],[])
                        if len(examples['legacy/'+m[1]])<3:examples['legacy/'+m[1]].append({'entity':e,'attribute':a,'text':text[:900]})
                        break
            for m in re.finditer(r'(?<![A-Za-z\\])('+'|'.join(OPS)+r')(?=x(?:[^A-Za-z]|$)|\s*[({])',clean):
                bare[m[1]]+=1;examples.setdefault('bare/'+m[1],[])
                if len(examples['bare/'+m[1]])<3:examples['bare/'+m[1]].append({'entity':e,'attribute':a,'text':text[:900]})
    stream.close()
    (H/'inverse-candidates.json').write_text(json.dumps(list(candidates.values()),indent=2)+'\n')
    (H/'operator-examples.json').write_text(json.dumps(examples,indent=2)+'\n')
    report={'unique_operator_bearing_fields_scanned':sum(counts.values()),'by_attribute':dict(counts),'inverse_candidate_fields':len(candidates),
        'marked_missing_operators':dict(marked),'legacy_joined_commands':dict(legacy),'bare_function_patterns_for_review':dict(bare)}
    (H/'scan.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':run()
