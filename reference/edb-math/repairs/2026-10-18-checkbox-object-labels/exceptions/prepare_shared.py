"""Document visually reviewed, genuinely shared coordinate-plot exceptions."""
import copy,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
IDS={17592186055125,17592186055296,17592186124814,17592186284447,17592186284448,17592186284449,17592186402902,17592186402909,17592186434757,17592186434763,17592186434765}

def main():
    qs={q[':db/id']:q for q in json.loads((ROOT/'questions.json').read_text())}
    evidence={q['id']:q for q in json.loads((HERE/'current-image-evidence.json').read_text())}
    cases=[]
    for eid in sorted(IDS):
        q=qs[eid];e=evidence[eid];after=copy.deepcopy(q);objects=[]
        digest=hashlib.sha256(Path(e['path']).read_bytes()).hexdigest()
        assert Path(e['path']).stem==digest
        for f in after[':question/answer-fields']:
            label=f[':answer-field/key'];assert label in ('A','B','C','D')
            content=f'Point ${label}$';f[':answer-field/key']=content
            objects.append({'source_label':label,'field_id':f[':db/id'],'content':content,'shared_image':{'image':e['image'],'evidence':{'path':e['path'],'sha256':digest,'visual_review':'Opened original raster in full. All selectable point labels are visible at their actual marked locations in one common graph.'},'reason':'These options are locations within a single graph. Their coordinates, extrema, or comparison depend on the common axes and surrounding curve or surface; separating a point from that context would lose its mathematical meaning.'}})
        cases.append({'question_eid':eid,'math_academy_id':q.get(':question/math-academy-id'),'problem_before':q[':question/problem'],'problem_after':q[':question/problem'],'solution_before':q.get(':question/worked-solution',''),'solution_after':q.get(':question/worked-solution',''),'objects':objects,'solution_reference_edits':[],'extraction':'shared_coordinate_graph_points','question_before':q,'question_after':after})
    (HERE/'shared-cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')
    (HERE/'shared-lint-input.json').write_text(json.dumps({'cases':[{'question':c['question_after'],'objects':c['objects']}for c in cases]},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'questions':len(cases),'fields':sum(len(c['objects'])for c in cases)}))
if __name__=='__main__':main()
