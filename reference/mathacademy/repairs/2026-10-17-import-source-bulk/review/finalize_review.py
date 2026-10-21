"""Combine exact edit guards, renderer differences, and source-tree evidence."""
import collections,hashlib,json,pathlib
import source_features as sf
HERE=pathlib.Path(__file__).resolve().parent;BULK=HERE.parent;ROOT=HERE.parents[4]
def read(n):return json.loads((HERE/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def case_hash(c):return hashlib.sha256(json.dumps(c,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def current_ui():return {p:sha(ROOT/p) for p in ['ui/learning.js','ui/learning.css','ui/question-fields.js','ui/mathjax-config.js','ui/prose-lists.js']}
def report_rows(report,cases):
    positions=collections.Counter();rows={}
    for batch in report['measurements']:
        width=batch['width']
        for item in batch['items']:
            assert positions[width]<len(cases),'too many report cases'
            case=cases[positions[width]];positions[width]+=1
            assert case['id']==item['id'],'report case/order mismatch'
            rows[(width,case_hash(case))]=item
    assert positions and all(n==len(cases) for n in positions.values()),'incomplete rendering coverage'
    return rows,set(positions)
def validate_render_report(case_name,report_name,expected_widths):
    case_path=HERE/case_name;report_path=HERE/report_name
    cases=read(case_name);report=read(report_name)
    assert report['input_sha256']==sha(case_path),f'{report_name}: stale input hash'
    assert report.get('ui_unchanged') and report['ui_sha256']==current_ui(),f'{report_name}: stale UI hashes'
    rows,widths=report_rows(report,cases)
    assert widths==set(expected_widths),f'{report_name}: wrong viewport coverage'
    proof=report.get('reuse_proof')
    if proof:
        evidence={}
        for kind in ('baseline','fresh'):
            if not proof.get(f'{kind}_report'):continue
            cp=pathlib.Path(proof[f'{kind}_cases']);rp=pathlib.Path(proof[f'{kind}_report'])
            assert sha(cp)==proof[f'{kind}_cases_sha256'] and sha(rp)==proof[f'{kind}_report_sha256'],f'{report_name}: stale {kind} evidence'
            er=json.loads(rp.read_text());ec=json.loads(cp.read_text())
            assert er['input_sha256']==sha(cp) and er.get('ui_unchanged') and er['ui_sha256']==current_ui(),f'{report_name}: invalid {kind} evidence'
            erows,_=report_rows(er,ec);evidence[sha(rp)]=erows
        for key,item in rows.items():
            assert item['case_sha256']==key[1],f'{report_name}: case hash mismatch'
            original=evidence[item['evidence_report_sha256']][key]
            actual={k:v for k,v in item.items() if k not in ('case_sha256','evidence_report_sha256')}
            assert actual==original,f'{report_name}: reused measurement differs from its evidence'
    return report,{'cases_sha256':sha(case_path),'report_sha256':sha(report_path),'widths':sorted(widths),'case_count':len(cases),'reuse_verified':bool(proof)}
def main():
    static=read('static-verification.json');plan=json.loads((BULK/'integrated-changes.json').read_text())
    assert static['input_sha256']==sha(BULK/'integrated-changes.json'),'plan changed after review preparation'
    source_report,source_gate=validate_render_report('source-tex-cases.json','source-tex-rendering.json',[893])
    for batch in source_report['measurements']:
        for item in batch['items']:
            if len(item['math'])==1:sf.SOURCE_TEX_TREES[item['math'][0]['tex'].strip()]=item['math'][0]['tree']
    manual=read('manual-review.json') if (HERE/'manual-review.json').exists() else {'accepted_occurrences':[],'passed':False}
    visual_report,visual_gate=validate_render_report('visual-cases-final.json','visual-rendering-final.json',[893,375])
    assert manual.get('input_sha256')==static['input_sha256'],'manual review not bound to current plan'
    assert manual.get('visual_cases_sha256')==sha(HERE/'visual-cases-final.json') and manual.get('visual_report_sha256')==sha(HERE/'visual-rendering-final.json'),'manual visual evidence changed'
    accepted=set(manual['accepted_occurrences'])
    cases={r['id']:r for r in read('formula-cases.json')};formula_report,formula_gate=validate_render_report('formula-cases.json','formula-rendering.json',[893])
    visual_cases=read('visual-cases-final.json')
    assert accepted.issubset({c['id'] for c in visual_cases}),'manual occurrence missing visual evidence'
    assert all(c['problem']==cases[c['id']]['problem'] for c in visual_cases),'visual evidence does not match current formula'
    fidelity=[];formula_errors=[];checked=0
    for batch in formula_report['measurements']:
        for item in batch['items']:
            rid=item['id'];checked+=1
            if item['errors'] or len(item['math'])!=1:formula_errors.append({'id':rid,'errors':item['errors'],'formula_count':len(item['math'])})
            elif rid not in accepted:
                try:issues=sf.compare(cases[rid]['source_html'],item['math'][0]['tree'])
                except Exception as exc:issues=[{'feature':'independent-comparison','error':str(exc)}]
                if issues:fidelity.append({'id':rid,'issues':issues})
    full,full_gate=validate_render_report('full-cases.json','full-rendering.json',[893,375]);pairs=collections.defaultdict(dict)
    for batch in full['measurements']:
        for item in batch['items']:
            entity,state=item['id'].rsplit('-',1);pairs[(batch['width'],entity)][state]=item
    introduced_errors=[];control_changes=[];new_clipping=[];existing_errors=[]
    for (width,entity),pair in pairs.items():
        before,after=pair['before'],pair['after']
        new=collections.Counter(after['errors'])-collections.Counter(before['errors'])
        if new:introduced_errors.append({'entity':entity,'width':width,'errors':dict(new)})
        if after['errors']:existing_errors.append({'entity':entity,'width':width,'before':before['errors'],'after':after['errors']})
        if before['controls']!=after['controls']:control_changes.append({'entity':entity,'width':width,'before':before['controls'],'after':after['controls']})
        if after['clipped']>before['clipped'] or after['scrollWidth']>max(after['width']+1,before['scrollWidth']):new_clipping.append({'entity':entity,'width':width,'before':{k:before[k] for k in ('width','scrollWidth','clipped')},'after':{k:after[k] for k in ('width','scrollWidth','clipped')},'overflow':after['overflow']})
    report={'input_sha256':static['input_sha256'],'fields':static['fields'],'source_replacements':static['source_replacements'],'ui_sha256':full.get('ui_sha256'),
        'independently_checked_replacement_renders':checked,'whole_content_before_after_pairs':len(pairs),'widths':sorted(set(w for w,e in pairs)),
        'static_failures':static['failures'],'formula_errors':formula_errors,'source_fidelity_issues':fidelity,'introduced_full_content_errors':introduced_errors,
        'control_changes':control_changes,'new_clipping':new_clipping,'preexisting_full_content_errors':existing_errors,
        'preexisting_full_content_error_case_count':len({r['entity'] for r in existing_errors}),
        'browser_errors':source_report['errors']+formula_report['errors']+full['errors']+visual_report['errors'],'manual_review':manual,
        'rendering_input_gates':{'source_tex':source_gate,'formulas':formula_gate,'full_content':full_gate,'visuals':visual_gate},
        'scope':'Source restoration and display; preexisting missing answer keys are preserved and not certified as complete questions.'}
    report['passed']=not any(report[k] for k in ('static_failures','formula_errors','source_fidelity_issues','introduced_full_content_errors','control_changes','new_clipping','browser_errors')) and manual['passed'] and full.get('ui_unchanged') and formula_report.get('ui_unchanged')
    (HERE/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:len(v) if isinstance(v,list) else v for k,v in report.items() if k not in ('manual_review','scope')},indent=2))
if __name__=='__main__':main()
