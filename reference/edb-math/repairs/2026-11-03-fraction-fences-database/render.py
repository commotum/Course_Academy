"""Render actual changed expressions across content and fence shapes."""
import json,re,sys,uuid
from collections import Counter
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.question_capture.math_format import MATH,scalable_fraction_parentheses as fix
import generate.pipeline.render_preview as r

def profile(before,after):
    kinds=[]
    for name,token in [('parentheses',r'\left('),('brackets',r'\left['),('angles',r'\left\langle')]:
        if after.count(token)>before.count(token):kinds.append(name)
    environments=','.join(sorted(set(re.findall(r'\\begin\{([^}]+)\}',before)))) or 'ordinary'
    return '+'.join(kinds),environments

def main():
    proposals=json.loads((H/'proposals.json').read_text());options={};counts=Counter()
    for change in proposals:
        spans=[change['before']] if change['attribute']=='answer/value' else [m[0] for m in MATH.finditer(change['before'])]
        for before in spans:
            after=fix(before)
            if before==after:continue
            shape,environment=profile(before,after);counts[shape]+=1
            names=[change['attribute']+'/'+shape+'/'+environment]
            # Exercise nested groups, scripts and author-selected sizes as well.
            for label,pattern in [('nested',r'\\left.*\\left'),('scripts',r'[_^]'),('manual-size',r'\\(?:big|Big)'),('dfrac',r'\\dfrac'),('tfrac',r'\\tfrac')]:
                if re.search(pattern,before if label!='nested' else after):names.append(label+'/'+shape)
            for name in names:
                score=len(before)
                if name not in options or score<options[name][0]:options[name]=(score,change,before,after)
    rows=[]
    for name,(_,change,before,after) in sorted(options.items()):
        if change['attribute']=='answer/value':after='$$\n'+after+'\n$$'
        rows.append({'question':{':question/id':str(uuid.uuid5(uuid.NAMESPACE_URL,'fraction-fences/'+name)),':question/problem':after,':question/worked-solution':'',':question/answer-fields':[]},'verification':{'profile':name,'entity':change['entity'],'attribute':change['attribute'],'before':before}})
    (H/'render-input.json').write_text(json.dumps(rows,indent=2)+'\n')
    r.render(rows,H/'desktop',[Path('/media/jake/SSD/EDB/math')])
    report=json.loads((H/'desktop/rendering.json').read_text());assert report['passed']
    result={'passed':True,'actual_changed_formula_samples':True,'profiles_rendered':len(rows),'profiles':[row['verification']['profile'] for row in rows],'changed_formula_counts_by_fences':dict(counts),'raw_tex_or_math_errors':0,'database_writes':0}
    (H/'render-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':True,'profiles_rendered':len(rows)}))

if __name__=='__main__':main()
