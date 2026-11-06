import csv,hashlib,json,re,shutil
from pathlib import Path
S=Path('/home/jake/Developer/study');V=S/'vault';W=Path('/tmp/255-final-guide-review')
source=Path('/home/jake/Downloads/255 Final Exam Guide_v1.pdf');out=V/'F26/255/Undated_SG-2.md';asset=V/'F26/source/255/SG-2'/source.name
assert not out.exists(),'Existing guide requires preservation and reconciliation'
old=json.loads(Path('/tmp/255-midterm-guide-review/inventory.json').read_text())
objectives=[x['objective']for x in old]+[
'Compute the curl of a vector field and interpret it as a measure of local rotation.',
'Compute the divergence of a vector field and interpret it as a measure of local expansion/compression.',
'Use the curl test to determine if a 3D vector field is conservative.',
'Know the important identities involving the gradient, the divergence, and the curl:\n\n- the curl of the gradient is zero.\n- the divergence of the curl is zero.',
'Calculate the Jacobian of a transformation for two and three variables.',
'Understand how a transformation maps regions to regions\n\n- a region in the $uv$-plane to a region in the $xy$-plane\n- a solid region in the $uvw$-space to a solid region in the $xyz$-space',
'Apply the Change of Variables formula to evaluate integrals over complex regions by transforming them into simpler ones.',
'Recognize that polar, cylindrical, and spherical substitutions are specific cases of the Jacobian.',
'Parametrize a surface using two parameters.',
'Calculate the surface area of a smooth parametrized surface.',
'Evaluate a scalar surface integral\n\n- over a parameterized surface\n- over an explicit surface',
'Evaluate a flux surface integral\n\n- over a parameterized surface\n- over an explicit surface',
'Understand how unit normal vectors and surface orientation are connected.',
'Understand Stokes’ Theorem as a higher-dimensional generalization of Green’s Theorem in circulation form.',
'Be able to use Stokes’ Theorem to evaluate integrals.',
'Determine the positive orientation of a boundary curve relative to a surface using the Right-Hand Rule.',
'Understand the Divergence Theorem as a higher-dimensional generalization of Green’s Theorem in flux form.',
'Be able to use the Divergence Theorem to evaluate integrals.',
'Understand important physical applications like Gauss’s Law.'
]
assert len(objectives)==40
oldnote=(V/'F26/255/Undated_SG-1.md').read_text();ms=list(re.finditer(r'^## Problem (\d+)$',oldnote,re.M))
mapdata={}
for i,x in enumerate(old):
 body=oldnote[ms[i].end():ms[i+1].start()if i+1<len(ms)else len(oldnote)]
 lines=re.search(r'^(\*\*Topics:\*\*[^\n]*\n\*\*Prerequisites:\*\*[^\n]*)',body,re.M)[1]
 mapdata[x['number']]={'direct':x['direct'],'supporting':x['supporting'],'lines':lines,'component_only':x['component_only'],'coverage_gap':None}
new={
22:([2132],[],''),23:([2131],[],''),
24:([2132,1951],[3357,3149],'No whole-task equivalent verified for the three-dimensional curl test. Component coverage: '),
25:([1934,2131,2132,1957],[],'No whole-task equivalent verified for either stated zero identity. Component coverage: '),
26:([1999,2058],[152,153],''),
27:([2832,4151],[],'No single whole-item equivalent verified for both plane and solid-region mappings. Component coverage: '),
28:([4132,4151],[1999,2058],''),
29:([2030,2059,2060],[1999,2058],'No single whole-item equivalent verified for all three coordinate substitutions as Jacobian cases. Component coverage: '),
30:([1789],[],''),31:([1790],[245],''),32:([3386,1264],[1790],''),33:([4145,4143],[3178,245],''),
34:([3178],[1790],''),35:([2138],[2116],''),36:([2138],[2132],''),37:([2138],[3178],''),
38:([2135],[3361],''),39:([2135],[2131,4146],''),
40:([2135,4162],[],'No whole-task equivalent verified for Gauss’s Law or its physical charge–flux interpretation. Component coverage: ')}
annotations={
(24,2132):'computing a three-dimensional curl',(24,1951):'three-dimensional potential functions',
(25,1934):'gradient computation',(25,2131):'divergence computation',(25,2132):'curl computation',(25,1957):'equality of mixed partial derivatives',
(26,1999):'two-variable Jacobians',(26,2058):'three-variable Jacobians',
(27,2832):'mapping plane regions',(27,4151):'transforming solid regions and their bounds',
(28,4132):'double integrals',(28,4151):'triple integrals',
(29,2030):'polar area substitution',(29,2059):'cylindrical volume substitution',(29,2060):'spherical volume substitution and its Jacobian derivation',
(32,3386):'parameterized surfaces',(32,1264):'explicit Cartesian surfaces',
(33,4145):'parameterized surfaces',(33,4143):'explicit Cartesian surfaces',
(35,2138):'generalization of Green’s circulation theorem',(37,2138):'induced positive boundary orientation',
(38,2135):'generalization of Green’s flux theorem',
(40,2135):'closed-surface flux and the volume integral of divergence',(40,4162):'outward flux through a closed surface'}
gaps={24:'The full 3D curl-test equivalence and its domain hypotheses remain a lesson-linking gap; the Cartesian-plane prerequisite is not presented as a 3D theorem.',25:'The two zero identities are not directly covered by the verified lesson examples; the links supply their differential-operator and mixed-partial components.',40:'The electric-field, enclosed-charge, and permittivity content of Gauss’s Law remains unmatched; these links cover its mathematical flux components only.'}
index={}
for r in csv.DictReader(open(S/'MA/Mathematical-Foundations/catalog.csv')):index[int(r['topic-id'])]=(r['topic-name'],S/r['lesson-path'])
root=S/'MA/Mathematical-Analysis-&-Modeling/MVC'
for r in csv.DictReader(open(root/'topics.csv')):index[int(r['topic-id'])]=(r['topic-name'],root/r['lesson-path'])
ids={t for x in mapdata.values()for t in x['direct']+x['supporting']}|{t for ds,ps,_ in new.values()for t in ds+ps};local={}
for dirname in ['Lessons','Prerequisites']:
 for p in (V/'F26/255'/dirname).rglob('*.md'):
  m=re.search(r'^lesson-id:\s*(\d+)\s*$',p.read_text(),re.M)
  if m and int(m[1])in ids:local.setdefault(int(m[1]),p)
def link(t):
 title,p=index[t];assert p.is_file();assert re.search(r'^lesson-id:\s*'+str(t)+r'\s*$',p.read_text(),re.M)
 target=local[t].relative_to(out.parent).as_posix()if t in local else p.resolve().as_uri()
 return f'[{title}](<{target}>)'
for n,(ds,ps,prefix)in new.items():
 topics=prefix+'; '.join(link(t)+(' ('+annotations[n,t]+')'if(n,t)in annotations else'')for t in ds)
 if n in gaps:topics+=' '+gaps[n]
 lines='**Topics:** '+topics+'\n**Prerequisites:** '+('; '.join(link(t)for t in ps)if ps else'No additional prerequisite links needed.')
 mapdata[n]={'direct':ds,'supporting':ps,'lines':lines,'component_only':bool(prefix),'coverage_gap':gaps.get(n)}
def section(n):
 if n<=6:return 'Section 6.1: Vector Fields'
 if n<=10:return 'Section 6.2: Line Integrals'
 if n<=14:return 'Section 6.3: Conservative Vector Fields'
 if n<=21:return 'Section 6.4: Green’s Theorem'
 if n<=25:return 'Section 6.5: Divergence and Curl'
 if n<=29:return 'Section 5.7: Change of Variables in Multiple Integrals'
 if n<=34:return 'Section 6.6: Surface Integrals'
 if n<=37:return 'Section 6.7: Stokes’ Theorem'
 return 'Section 6.8: The Divergence Theorem'
asset.parent.mkdir(parents=True,exist_ok=True)
if asset.exists():assert asset.read_bytes()==source.read_bytes()
else:shutil.copy2(source,asset)
text='''
**MTH 255 — Final Exam Study Guide**

Due: unknown
Exam schedule from source: Week 11 according to the Final Exam Schedule, in the usual classroom. Exact calendar date and time are not specified in this PDF.
Date imported: 2026-11-06
Source: [255 Final Exam Guide_v1.pdf](<../source/255/SG-2/255 Final Exam Guide_v1.pdf>)
Study format: These 40 study objectives do not require submitted answers. Study links are added navigation; component-only matches and remaining coverage gaps are labeled below.

## Topics

'''
text+='\n'.join('- '+link(t)for t in sorted({t for x in mapdata.values()for t in x['direct']}))+'\n\n## Prerequisites\n\n'
text+='\n'.join('- '+link(t)for t in sorted({t for x in mapdata.values()for t in x['supporting']}))
text+='''

## Instructions

### Exam information

- **When:** Week 11 according to the Final Exam Schedule.
- **Where:** Our usual classroom.
- **Duration:** 110 minutes.
- **Resources:** You are not allowed to use any resource (calculator, notes, etc.) for the exam. Bring a pencil and an eraser.
- **Sections covered:** 5.7 and 6.1–6.8.

### Question formats

The exam will have two classes of problems:

- Multiple-choice, choose many, true/false, fill-in-the-blank, and matching problems. For most of these problems you do not receive partial credit.
- Show-your-work problems. These are similar to the ones appearing on written homework in terms of appearance and difficulty. You receive partial credit for partial progress toward the answer on these problems.

### Preparation advice

- Look back to what you’ve done in class:
  - Review problems in Achieve.
  - Revisit the written homework problems (and keys).
  - Revisit the recitation worksheets (and keys).
- Look at the exercises at the end of each section in the textbook.
- Look at the review exercises at the end of each chapter in the textbook.

### Topic list

The source states: **This is NOT a comprehensive list of topics appearing on the exam.**

| Source section | Study objectives |
| --- | --- |
| Section 6.1: Vector Fields | 1–6 |
| Section 6.2: Line Integrals | 7–10 |
| Section 6.3: Conservative Vector Fields | 11–14 |
| Section 6.4: Green’s Theorem | 15–21 |
| Section 6.5: Divergence and Curl | 22–25 |
| Section 5.7: Change of Variables in Multiple Integrals | 26–29 |
| Section 6.6: Surface Integrals | 30–34 |
| Section 6.7: Stokes’ Theorem | 35–37 |
| Section 6.8: The Divergence Theorem | 38–40 |
'''
inventory=[]
for n,objective in enumerate(objectives,1):
 page=2 if n<=25 else 3;x=mapdata[n]
 text+=f'\n---\n\n## Problem {n}\n\nSource study objective: ({n}), PDF page {page}. {section(n)}.\n\n{objective}\n\n'+x['lines']+'\n\n\n'
 inventory.append({'number':n,'source_page':page,'section':section(n),'objective':objective,'direct':x['direct'],'supporting':x['supporting'],'component_only':x['component_only'],'coverage_gap':x['coverage_gap']})
out.write_text(text.rstrip()+'\n');(W/'inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'note':str(out),'items':40,'unique_topics_and_prerequisites':len(ids),'component_only_items':[n for n,x in mapdata.items()if x['component_only']],'remaining_linking_gaps':gaps,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest()},indent=2))
