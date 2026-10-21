"""Compose exact SVG viewports around unchanged source raster panels.

No pixels are changed or regenerated. Each self-contained SVG embeds all original
PNG bytes and selects a visually reviewed panel with its viewBox.
"""
import base64,copy,hashlib,html,json,re,sys
from pathlib import Path
from PIL import Image
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'mapping'))
from extract import clean_prompt
ROMANS=('I','II','III','IV')

def blank_split(im,axis,target):
    """A genuine blank separating column/row nearest the reviewed panel division."""
    rgba=im.convert('RGBA');w,h=im.size;px=rgba.load()
    bound=w if axis==0 else h;other=h if axis==0 else w
    candidates=[]
    for i in range(max(1,int(target-bound*.10)),min(bound,int(target+bound*.10)+1)):
        blank=True
        for j in range(other):
            r,g,b,a=px[i,j]if axis==0 else px[j,i]
            if a and min(r,g,b)<250:blank=False;break
        if blank:candidates.append(i)
    assert candidates,(im.size,axis,target)
    return min(candidates,key=lambda i:abs(i-target))

def main():
    qs={q[':db/id']:q for q in json.loads((ROOT/'questions.json').read_text())}
    evidence=json.loads((HERE/'current-image-evidence.json').read_text())
    shared={c['question_eid']for c in json.loads((HERE/'shared-cases.json').read_text())}
    assets=HERE/'assets';assets.mkdir(exist_ok=True)
    cases=[];manifest=[]
    for e in evidence:
        eid=e['id']
        if eid in shared:continue
        q=qs[eid];raw=Path(e['path']).read_bytes();source_hash=hashlib.sha256(raw).hexdigest()
        assert source_hash==Path(e['path']).stem
        im=Image.open(e['path']);w,h=im.size;count=len(e['fields'])
        assert count in (3,4)
        if count==3:
            x1=blank_split(im,0,w/3);x2=blank_split(im,0,w*2/3)
            rects=[(0,0,x1,h),(x1,0,x2-x1,h),(x2,0,w-x2,h)]
        else:
            x1=blank_split(im,0,w/2);y1=blank_split(im,1,h/2)
            rects=[(0,0,x1,y1),(x1,0,w-x1,y1),(0,y1,x1,h-y1),(x1,y1,w-x1,h-y1)]
        bylabel={f[':answer-field/key']:f for f in q[':question/answer-fields']}
        assert set(bylabel)==set(ROMANS[:count])
        objects=[];kinds={'curves':'Curve','polygons':'Polygon','regions':'Region','digraphs':'Digraph','diagrams':'Diagram','plots':'Plot','graphs':'Graph'}
        noun=next((value for word,value in kinds.items()if word in e['prompt']),'Diagram')
        for label,rect in zip(ROMANS,rects):
            x,y,cw,ch=rect
            svg=(f'<svg xmlns="http://www.w3.org/2000/svg" width="{cw}" height="{ch}" viewBox="{x} {y} {cw} {ch}" role="img" aria-label="{noun} {label}">\n'
                 f'<title>{noun} {label}</title>\n'
                 f'<image x="0" y="0" width="{w}" height="{h}" href="data:image/png;base64,{base64.b64encode(raw).decode()}"/>\n</svg>\n').encode()
            digest=hashlib.sha256(svg).hexdigest();local=assets/f'{digest}.svg';local.write_bytes(svg)
            canonical=f'images/{digest[:2]}/{digest}.svg'
            content=f'![{noun} {label}]({canonical})'
            objects.append({'source_label':label,'field_id':bylabel[label][':db/id'],'content':content,'source_fragment':f'![]({e["image"]})','image_evidence':{'source':e['path'],'source_sha256':source_hash,'viewport':list(rect),'asset':str(local),'asset_sha256':digest,'source_label_retained':'The original panel identifier remains within its image, so references to that named graph/diagram in the mathematical explanation still identify a visible object.'}})
            manifest.append({'question_eid':eid,'source_label':label,'source':e['path'],'source_sha256':source_hash,'source_dimensions':[w,h],'viewport':list(rect),'svg':str(local),'svg_sha256':digest,'canonical_path':canonical,'bytes':len(svg)})
        before=q[':question/problem'];image_re=r'!\[[^]]*\]\('+re.escape(e['image'])+r'\)'
        after,n=re.subn(image_re,'',before);assert n==1
        after=re.sub(r'\n*Graph positions: \*\*I\.\*\* upper left; \*\*II\.\*\* upper right; \*\*III\.\*\* lower left; \*\*IV\.\*\* lower right\.','',after)
        after=re.sub(r'\babove\b','below',after)
        after=clean_prompt(after)
        sol=q.get(':question/worked-solution','');solution=sol
        # The source identifiers remain visibly printed inside their complete
        # images. Use named-object prose rather than legacy quoted radio options.
        def old_choice(m):
            labels=re.findall(r'\b(?:III|II|IV|I)\b',m[1]);only=m[1].strip().endswith('only')
            return (noun.lower() if len(labels)==1 else noun.lower()+'s')+' '+(', '.join(labels[:-1])+(' and 'if len(labels)>1 else '')+labels[-1]) + (' only'if only else '')
        solution=re.sub(r'["“\']((?:III|II|IV|I)(?:\s*(?:,\s*(?:and\s+)?|and\s+)(?:III|II|IV|I))*(?:\s+only)?)[.]?["”\']',old_choice,solution)
        aq=copy.deepcopy(q);aq[':question/problem']=after;aq[':question/worked-solution']=solution
        lookup={o['field_id']:o['content']for o in objects}
        for f in aq[':question/answer-fields']:f[':answer-field/key']=lookup[f[':db/id']]
        cases.append({'question_eid':eid,'math_academy_id':q.get(':question/math-academy-id'),'problem_before':before,'problem_after':after,'solution_before':sol,'solution_after':solution,'objects':objects,'extraction':'independent_image_panel_svg_viewport','solution_reference_edits':[],'question_before':q,'question_after':aq})
    (HERE/'panel-cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')
    (HERE/'panel-assets.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    (HERE/'panel-lint-input.json').write_text(json.dumps({'cases':[{'question':c['question_after'],'objects':c['objects']}for c in cases]},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'questions':len(cases),'assets':len(manifest)}))
if __name__=='__main__':main()
