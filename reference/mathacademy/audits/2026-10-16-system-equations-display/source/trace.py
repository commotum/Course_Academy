from pathlib import Path
import importlib.util, sys, json, hashlib, shutil
from bs4 import BeautifulSoup
ROOT = Path('/home/jake/Developer/Course_Academy')
OUT = ROOT/'reference/mathacademy/audits/2026-10-16-system-equations-display/source'
MA = Path('/home/jake/Developer/MA')
LESSON = MA/'DATA/Lessons/493/Source'
EXTRACTOR = MA/'PIPELINE/Math-Academy/3-Capture/1-Source/3-JSON/lesson-json.py'
MARKDOWN = MA/'PIPELINE/Math-Academy/3-Capture/1-Source/5-MD/md.py'
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m)
    return m
lj,md=load('trace_lesson_json',EXTRACTOR),load('trace_ma_md',MARKDOWN)
soup=BeautifulSoup((LESSON/'493.html').read_text(),'html.parser')
traces=[]
for domid,index,label in [
    ('question-211984',0,'source-practice-question'),
    ('step-229009',0,'canonical-example-system'),
    ('step-229009',1,'canonical-example-operation'),
    ('step-229008',1,'tutorial-operation'),
    ('step-229019',1,'general-solutions-canonical-operation')]:
    node=soup.select_one('#'+domid).select('mjx-assistive-mml math')[index]
    mathml=str(node)
    path=OUT/(label+'.mathml')
    path.write_text(mathml+'\n')
    flattened=lj.mathml_to_text(node)
    traces.append({'label':label,'source_html':str(LESSON/'493.html'),'dom_id':domid,'math_index':index,
                  'mathml_evidence':str(path.relative_to(ROOT)), 'source_display':node.get('display'),
                  'source_rows':[[td.get_text('',strip=True) for td in tr.find_all('mtd',recursive=False)] for tr in node.select('mtable > mtr')],
                  'source_literal_bar_count':sum(mo.get_text('',strip=True)=='|' for mo in node.find_all('mo')),
                  'extracted_text_reproduced':flattened,
                  'markdown_inline_reproduced':md.math_to_markdown(flattened,display=False),
                  'markdown_display_reproduced':md.math_to_markdown(flattened,display=True)})
for name,original in [('source-practice-question.png','04-question-211984.png'),('source-single-bar-operation.png','02-step-229008.png')]:
    shutil.copyfile(LESSON/'Sections'/original,OUT/name)
generated=json.loads((ROOT/'generate/scratch/17592186073776/reference/replenishment/basis-2486/generated.json').read_text())
def find_id(x,id):
    if isinstance(x,dict):
        if x.get(':question/id')==id:return x
        for v in x.values():
            found=find_id(v,id)
            if found:return found
    elif isinstance(x,list):
        for v in x:
            found=find_id(v,id)
            if found:return found
record=find_id(generated,'a7d7084c-4c14-5312-a22d-dc6fe1986a2c')
assert record, 'Generated record missing'
(OUT/'seed-generated-record.json').write_text(json.dumps(record,indent=2)+'\n')
paths=[LESSON/'493.html',LESSON/'493.json',EXTRACTOR,MARKDOWN,ROOT/'generate/scratch/17592186073776.py',ROOT/'generate/scratch/17592186073778.py',ROOT/'scripts/question_capture/math_format.py']
report={
 'question_entity':17592186529306,'question_uuid':'a7d7084c-4c14-5312-a22d-dc6fe1986a2c',
 'question_origin':'Locally generated; no Math Academy question identifier.',
 'topic_entity':17592186050240,'math_academy_topic':493,'kp_entity':17592186073776,
 'evidence_chain':[
    'Original Math Academy source screenshot and MathML show display:block systems with a separate mtr for each equation and one scalable left brace.',
    'The old lesson-json.py mathml_to_text mapper serializes mtable rows with semicolons and mtr cells with a vertical-bar delimiter, losing structural layout.',
    'Old Markdown conversion reconstitutes some aligned calculations using |= but leaves these one-cell-per-row systems as a bare unmatched brace plus semicolon-separated equations.',
    'Generator source.json at basis1356 retained this flattened Markdown. Generator17592186073776.py copies semicolon joins into prompt and annotated solution and treats escaping the brace as the presentation repair.',
    'The generated record at basis2486 is an exact match for the malformed problem and solution of question17592186529306, later committed at basis2487 according to the parent database-history audit.',
    'The shared formatter legacy_choice recognizes only an unescaped opening brace, so the generated escaped-brace form is outside its current repair path.'
 ],
 'double_bar_finding':'Source operation annotations have one literal vertical bar in their second mtd. The extractor adds its own cell delimiter bar, yielding two adjacent bars. Markdown maps both to mid; generators73776 and73778 preserve the duplicate.',
 'traces':traces,
 'generator_locations':{'prompt':'generate/scratch/17592186073776.py:83','annotated_solution':'generate/scratch/17592186073776.py:146','source_repair_claim':'generate/scratch/17592186073776/classification.md:14','sibling_duplicated_bar':'generate/scratch/17592186073778.py:83'},
 'source_hashes':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
 'mutations':'Evidence artifacts only; no source content, generator, capture process, or database writes.'
}
(OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'saved':str(OUT/'verification.json'),'traces':len(traces),'seed_prompt':record[':question/problem']},indent=2))
