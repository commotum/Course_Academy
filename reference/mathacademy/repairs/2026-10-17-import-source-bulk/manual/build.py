"""Recover exceptional formulas from retained SVG glyphs or exact source TeX."""
import hashlib,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
AUDIT=BASE.parent/'2026-10-16-import-root-cause'
sources={r['id']:r for r in map(json.loads,(AUDIT/'source/occurrences.jsonl').open())}
bound=json.loads((BASE/'primary/bound.json').read_text())
snapshot=Path((BASE/'snapshot-directory.txt').read_text().strip())
current={r[':db/id']:r for r in json.loads((snapshot/'entities.json').read_text())}
def stack(left,right):return r'\begin{gathered}'+left+r'\\[1em]'+right+r'\end{gathered}'
tex={
 '4306:step-156150:311050':stack(r'\begin{array}{l}n\text{ is positive and even}\\\hline\therefore\;\bbox[Gainsboro]{\color{blue}n\text{ is even}}\end{array}',r'\begin{array}{l}P\land Q\\\hline\therefore Q\end{array}'),
 '4306:step-156150:324423':stack(r'\begin{array}{l}n\text{ is even}\\\text{If }n\text{ is even, then }6\mid 3n\\\hline\therefore\;\bbox[Gainsboro]{\color{blue}6\mid 3n}\end{array}',r'\begin{array}{l}Q\\Q\Rightarrow R\\\hline\therefore R\end{array}'),
 '4306:step-156154:459478':stack(r'\begin{array}{l}\text{If }y\text{ is prime,}\\\quad\text{then }y\text{ is not divisible by }3\\y\text{ is divisible by }3\\\hline\therefore y\text{ is not prime}\end{array}',r'\begin{array}{l}P\Rightarrow\neg Q\\Q\\\hline\therefore\neg P\end{array}'),
 '4306:step-156154:480542':stack(r'\begin{array}{l}y\text{ is not prime}\\y\text{ is prime or }y\geq 3\\\hline\therefore\;\bbox[Gainsboro]{\color{blue}y\geq 3}\end{array}',r'\begin{array}{l}\neg P\\P\lor R\\\hline\therefore R\end{array}'),
 '4946:step-223793:423763':r'\begin{gathered}\underbrace{\color{blue}(\overline{x}-\overline{y})}_{\text{estimate}}\\[0.5em]\pm\;\overbrace{\underbrace{t_{\nu,\alpha/2}}_{t\text{-score}}\cdot\underbrace{\color{red}S_p\cdot\sqrt{\dfrac{1}{n_x}+\dfrac{1}{n_y}}}_{\text{standard error}}}^{\text{margin of error}}\end{gathered}',
 '4943:step-222617:194352':r'\begin{gathered}\underbrace{\color{blue}\widehat{p}_1-\widehat{p}_2}_{\text{estimate}}\\[0.5em]\pm\;\overbrace{\underbrace{z_{\alpha/2}}_{z\text{-score}}\cdot\underbrace{\color{red}\sqrt{\dfrac{\widehat{p}_1(1-\widehat{p}_1)}{n_1}+\dfrac{\widehat{p}_2(1-\widehat{p}_2)}{n_2}}}_{\text{standard error}}}^{\text{margin of error}}\end{gathered}',
}
changes=[]
for row in bound:
    spans=[s for s in row['spans'] if s['source_occurrence_id'] in tex]
    if not spans:continue
    before=current[row['entity']][row['attribute']];assert before==row['current_value']
    edits=[]
    for s in spans:
        rid=s['source_occurrence_id'];source=sources[rid]
        assert Path(source['source_file']).read_text()[source['source_offset']:source['source_offset']+len(source['source_html'])]==source['source_html']
        proof='Directly inspected original visible SVG glyphs in manual/original-logic.png; restored both concrete argument and symbolic rule, preserving horizontal inference lines and highlighted conclusions. Arranged vertically for narrow displays.' if rid.startswith('4306:') else 'Complete outer title TeX preserves the annotated confidence interval. Recovered its nested score variable and removed only the HTML span around a spacing backslash. Preserved all mathematical terms, labels and source colors; split estimate and margin across lines.'
        edits.append({**s,'before':s['old_markdown'],'after':'\n\n$$\n'+tex[rid]+'\n$$\n\n','tex':tex[rid],'manual_source_review':proof,
            'source_offset':source['source_offset'],'source_line':source['source_line']})
    after=before
    for s in reversed(edits):assert after[s['start']:s['end']]==s['before'];after=after[:s['start']]+s['after']+after[s['end']:]
    changes.append({'entity':row['entity'],'attribute':row['attribute'],'before':before,'after':after,'replacements':edits})
# The one field changed since the old audit: replace only its still-malformed cases block.
eid=17592186130324;attribute=':tutorial/content';before=current[eid][attribute]
old=r'$$'+'\n'+r'\begin{aligned}{lim}_{x\to \,c}\sqrt{x}=\{\begin{aligned}\sqrt{c} & \text{\u00a0if\u00a0}c>0 \\ \text{DNE} & \text{\u00a0if\u00a0}c\le 0\end{aligned}\end{aligned}'+'\n'+r'$$'
old=old.replace(r'\u00a0','\u00a0');assert before.count(old)==1
rid='1986:step-392:66800';source=sources[rid]
value=r'\lim_{x\to c}\sqrt{x}=\begin{cases}\sqrt{c} & \text{if }c>0\\\text{DNE} & \text{if }c\leq0\end{cases}'
start=before.index(old);new='$$\n'+value+'\n$$'
edit={'start':start,'end':start+len(old),'before':old,'after':new,'tex':value,'source_occurrence_id':rid,'source_file':source['source_file'],
    'source_html':source['source_html'],'source_sha256':source['source_sha256'],'source_offset':source['source_offset'],'source_line':source['source_line'],
    'manual_source_review':'Contextual merge at current basis3482. Source two-row cases table explicitly pairs sqrt(c) with c>0 and DNE with c<=0. Only the unique current formula block changes; later prose and punctuation edits remain byte-identical.'}
changes.append({'entity':eid,'attribute':attribute,'before':before,'after':before[:start]+new+before[start+len(old):],'replacements':[edit]})
(HERE/'changes.json').write_text(json.dumps(changes,indent=2,ensure_ascii=False)+'\n')
(HERE/'verification.json').write_text(json.dumps({'manually_restored_fields':len(changes),'source_occurrences':sum(len(x['replacements']) for x in changes),'visible_svg_contact_sheet':'manual/original-logic.png','all_source_locations_exact':True},indent=2)+'\n')
print('Manual source-backed fields:',len(changes))
