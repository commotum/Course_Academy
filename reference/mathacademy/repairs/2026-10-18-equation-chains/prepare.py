"""Source-reviewed repairs of the pinned equation-chain audit findings."""
import hashlib,importlib.util,json,re
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];AUDIT=ROOT/'reference/mathacademy/audits/2026-10-18-equation-chain-import'
spec=importlib.util.spec_from_file_location('chain_formatter',ROOT/'scripts/question_capture/math_format.py');fmt=importlib.util.module_from_spec(spec);spec.loader.exec_module(fmt)
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2,ensure_ascii=False,default=str)+'\n')
def digest(value):return hashlib.sha256(value.encode()).hexdigest()
INVENTORY=json.loads((HERE/'mixed-row-inventory.json').read_text())
# These six omitted connections were reviewed individually against the retained
# expressions and their source derivation. General capture never infers them.
GAPS={14:'Cancel the factor 1 in the numerator.',18:'Remove denominator 1.',
      63:'Rewrite 4 as 2^2, identify twice the product, then square the binomial.',
      352:'Rewrite the negative exponent as a reciprocal.',140:'Use |6|=6.'}
def reviewed_rows(text,entity):
    reviews=[]
    for index,reason in GAPS.items():
        record=INVENTORY[index]
        if record['entity']!=entity:continue
        for opening in list(re.finditer(r'\\begin\{aligned\}',text))[::-1]:
            span=fmt.environment(text,opening.start());rows=fmt.cells(text[span[0]:span[1]]) if span else None
            if rows!=record['rows']:continue
            new=[]
            for i,row in enumerate(rows):
                row=list(row)
                if i<len(rows)-1 and row[-1] not in ('=','≈') and not row[0].endswith('='):
                    if len(row)==1:row.append('=')
                    else:assert len(row)==2 and not row[1];row[1]='='
                new.append(row)
            text=text[:span[0]]+r' \\ '.join(' & '.join(r) for r in new)+text[span[1]:]
            reviews.append({'inventory_index':index,'review':reason,'expressions_unchanged':True})
    # This derivation continues in prose and a second display. The last equals
    # has no RHS in its table; the expression itself is retained exactly.
    if entity==17592186503733:
        record=INVENTORY[353]
        for opening in list(re.finditer(r'\\begin\{aligned\}',text))[::-1]:
            span=fmt.environment(text,opening.start());rows=fmt.cells(text[span[0]:span[1]]) if span else None
            if rows==record['rows']:
                rows[-1]=rows[-1][:1]
                text=text[:span[0]]+r' \\ '.join(' & '.join(r) for r in rows)+text[span[1]:]
                reviews.append({'inventory_index':353,'review':'Remove surplus final equals; retain all radical and absolute-value expressions.'})
    return text,reviews
def box(value):return r'\bbox[2pt,border:1pt solid]{\phantom{'+value+'}}'
def special(text,entity,attr):
    reviews=[]
    replacements=[]
    if entity==17592186082928 and attr==':question/problem':
        replacements=[(r'\begin{aligned}{a}_{1} & =\end{aligned}',r'\begin{aligned}{a}_{1} &= '+box('4(1)-2')+r'\end{aligned}')]
    if entity==17592186082929 and attr==':question/problem':
        replacements=[
            (r'\begin{aligned}{a}_{1} & = \\ {a}_{2} & =\end{aligned}',r'\begin{aligned}{a}_{1} &= '+box('10^1-5')+r' \\ {a}_{2} &= '+box('10^3-5')+r'\end{aligned}'),
            (r'\begin{aligned}{a}_{k}= \\ {a}_{k-1}=\end{aligned}',r'\begin{aligned}{a}_{k} &= '+box('10^{k-1}')+r' \\ {a}_{k-1} &= '+box('10^{k-1}')+r'\end{aligned}')]
    for before,after in replacements:
        assert text.count(before)==1,(entity,attr,before)
        text=text.replace(before,after)
        reviews.append({'review':'Recover bordered phantom blanks exactly from archived MathML; invisible source content retained.', 'before':before,'after':after})
    if entity in {17592186054476,17592186054477,17592186054478,17592186056070,17592186056076}:
        match=re.search(r'\\begin\{bmatrix\}([\s\S]*?)\\end\{bmatrix\}',text);assert match
        rows=fmt.cells(match[1]);new=[]
        for row in rows:
            expression=''.join(row[:-1]).replace('|=','=');position=expression.index('=')
            # The archived table has red crosses, not multiplication dots.
            marker=r'\color{green}{\checkmark}' if row[-1]=='✓' else r'\color{red}{\times}'
            new.append(expression[:position]+' &='+expression[position+1:]+' && '+marker)
        replacement=r'\begin{aligned}'+r' \\ '.join(new)+r'\end{aligned}'
        text=text[:match.start()]+replacement+text[match.end():]
        reviews.append({'review':'Restore the archived factor-pair comparison table, equalities, crosses, and checkmark; remove invented matrix brackets.', 'before':match[0],'after':replacement})
    if entity==17592186130434:
        match=next(m for m in fmt.MATH.finditer(text) if 'Step 1:' in m[0]);replacement=(r'\begin{aligned}(x-5)^2+10x &= (x^2-2\cdot x\cdot5+5^2)+10x && \color{gray}{\text{Step 1:}}'
            r' \\ &= (x^2-10x+25)+10x && \color{gray}{\text{Step 2:}}'
            r' \\ &= x^2+(-10x+10x)+25 && \color{gray}{\text{Step 3:}}'
            r' \\ &= x^2+25 && \color{gray}{\text{Step 4:}}\end{aligned}')
        text=text[:match.start()]+'$$\n'+replacement+'\n$$'+text[match.end():]
        reviews.append({'review':'Restore the archived annotated polynomial identity derivation; preserve all four steps.', 'before':match[0],'after':replacement})
    if entity==17592186214282:
        match=next(m for m in fmt.MATH.finditer(text) if '# participants' in m[0])
        replacement=(r'\begin{aligned}&P(\text{Exercised}\ge60\mid\text{Exercised}\ge40)'
            r' \\ &= \frac{\substack{\text{\# participants who exercised}\\\text{at least 40 and at least 60}}}{\substack{\text{\# participants who exercised}\\\text{at least 40}}}'
            r' \\ &= \frac{\substack{\text{\# participants who exercised}\\\text{at least 60}}}{\substack{\text{\# participants who exercised}\\\text{at least 40}}}\end{aligned}')
        text=text[:match.start()]+'$$\n'+replacement+'\n$$'+text[match.end():]
        reviews.append({'review':'Keep conditional-count descriptions as text, escape count markers, and remove leaked [math] tags; retain all words and thresholds.', 'before':match[0],'after':replacement})
    if entity==17592186193849:
        before=r'9\times {10}^{-1}\times {10}^{8} \\ 0.9\times {10}^{8}';after=r'9\times {10}^{-1}\times {10}^{8} &= \\ 0.9\times {10}^{8}'
        assert text.count(before)==1;text=text.replace(before,after)
        reviews.append({'review':'Recover equality omitted between 9 times 10^-1 times 10^8 and 0.9 times 10^8. Preserve intervening repairs.', 'expressions_unchanged':True})
    if entity==17592186069968:
        before=r'0 & \,✓ \\ x=-3';after='0 & \\,✓\\end{aligned}\n$$\n\n$$\n\\begin{aligned}x=-3'
        assert text.count(before)==1;text=text.replace(before,after)
        reviews.append({'review':'Separate the independent positive- and negative-root checks; preserve conditional prefixes and result markers.', 'expressions_unchanged':True})
    if entity in {17592186083066,17592186138255,17592186138281,17592186232023}:
        before=text;text=text.replace(r'\[math]',r'\$').replace(r'\[/math]',r'\$')
        assert text!=before
        reviews.append({'review':'Restore escaped dollar currency markers damaged by the old text-to-Markdown conversion.', 'before_sha256':digest(before),'before':'currency-marker-recovery'})
    if entity==17592186234097:
        before=text
        text=re.sub(r'\\begin\{(align\*?)\}([\s\S]*?)\\end\{\1\}',lambda m:'$$\n'+r'\begin{aligned}'+m[2]+r'\end{aligned}'+'\n$$',text)
        assert text!=before
        reviews.append({'review':'Wrap bare equation environments in display delimiters and use aligned inside them; prevent row-spacing markers being mistaken for math delimiters.', 'before':'bare-align-environments'})
    if entity in {17592186138255,17592186138281} and attr==':question/worked-solution':
        def division(quotient,divisor,dividend,rows):
            return (r'\begin{array}{r@{\,}r} & '+quotient+r' \\ '+divisor+r' & \enclose{longdiv}{'+dividend+'}'+''.join(r' \\ & '+r for r in rows)+r'\end{array}')
        if entity==17592186138255:
            formulas=[
                division('121','5','607',[r'\underline{-5\phantom{00}}',r'10\phantom{0}',r'\underline{-10\phantom{0}}','07',r'\underline{-5}',r'\color{red}{2}']),
                division(r'121\bbox[2pt,lightgray]{\color{blue}{.}}','5',r'607\bbox[2pt,lightgray]{\color{blue}{.}}\color{blue}{0}',[r'\underline{-5\phantom{00.0}}\quad\color{lightgray}{\downarrow}',r'10\phantom{0.0}\quad\color{lightgray}{\downarrow}',r'\underline{-10\phantom{0.0}}\quad\color{lightgray}{\downarrow}',r'07\phantom{.0}\quad\color{lightgray}{\downarrow}',r'\underline{-5\phantom{.0}}\quad\color{lightgray}{\downarrow}',r'{\color{red}{2}}{\color{lightgray}{0}}']),
                division('121.4','5','607.0',[r'\underline{-5\phantom{00.0}}',r'10\phantom{0.0}',r'\underline{-10\phantom{0.0}}',r'07\phantom{.0}',r'\underline{-5\phantom{.0}}','20',r'\underline{-20}',r'\boxed{0}'])]
        else:
            formulas=[
                division('','12',r'74{\bbox[2pt,lightgray]{\color{blue}{.}}}7',[]),
                division(r'\phantom{6}{\bbox[2pt,lightgray]{\color{blue}{.}}}\phantom{225}','12',r'74{\bbox[2pt,lightgray]{\color{blue}{.}}}7',[]),
                division('6.225','12','74.700',[r'\underline{-72\phantom{.000}}',r'27\phantom{00}',r'\underline{-24\phantom{00}}',r'30\phantom{0}',r'\underline{-24\phantom{0}}','60',r'\underline{-60}','0'])]
        matches=list(re.finditer(r'(?m)^\| .* \|\n\| --- \|',text));assert len(matches)==3
        for match,formula in reversed(list(zip(matches,formulas))):text=text[:match.start()]+'$$\n'+formula+'\n$$'+text[match.end():]
        reviews.append({'review':'Reconstruct the three long-division stages from archived table rows, retaining quotient, divisor, dividend, subtraction steps, remainder, decimal markers and source colors.', 'before':'flattened-long-division-tables','source':str(HERE/'sources'/f'{entity}-worked-solution-archive.html')})
    if entity==17592186129058:
        if attr==':question/problem':
            final=r'-x^{2}+6x+(9+9)';tail=r' \\ &= -x^{2}+6x+18 && \color{gray}{\text{Step 4:}}'
        else:
            final=r'-x^{2}+6x+(9\bbox[2pt,background:Gainsboro]{\color{red}{-}}9)';tail=r' \\ &= \vdots'
        formula=(r'\begin{aligned}9-(x-3)^{2} &= 9-(x^{2}-2\cdot x\cdot3+3^{2}) && \color{gray}{\text{Step 1:}}'
                 r' \\ &= 9-(x^{2}-6x+9) && \color{gray}{\text{Step 2:}}'
                 r' \\ &= '+final+r' && \color{gray}{\text{Step 3:}}'+tail+r'\end{aligned}')
        spans=list(fmt.MATH.finditer(text));target=next(m for m in spans if 'Step 1:' in m[0]);old=target[0]
        text=text[:target.start()]+'$$\n'+formula+'\n$$'+text[target.end():]
        reviews.append({'review':'Recover the four-column annotated derivation from archived MathML. Keep the intentionally wrong + in the prompt, corrected highlighted minus in the solution, every step label, and solution ellipsis.', 'before':old,'after':formula})
    return text,reviews
def lexical(text):
    text=fmt._legacy_commands(text)
    text=re.sub(r'\\require\s*\{(?:cancel|enclose)\}\s*','',text)
    text=re.sub(r'\\(?:begin|end)\{aligned\}','',text)
    text=text.replace(r'\qquad','')
    text=re.sub(r'\\\\(?:\[[^\]]+\])?','',text)
    return re.sub(r'[\s&=]','',text)
def transform(value,entity,attr):
    text,reviews=special(value,entity,attr)
    def math(match):
        source=match[0];size=2 if source.startswith(('$$',r'\[',r'\(')) else 1
        body=source[size:-size]
        body=fmt._legacy_commands(body)
        body,notes=reviewed_rows(body,entity);reviews.extend(notes)
        body=re.sub(r'\\require\s*\{(?:cancel|enclose)\}\s*','',body)
        body=fmt.normalize_equality_chains(body)
        return source[:size]+body+source[-size:] if body.strip() else ''
    result=fmt.MATH.sub(math,text)
    if not any('before' in r for r in reviews):assert lexical(value).replace('$','')==lexical(result).replace('$',''),(entity,attr,'Changed expression tokens')
    # Source proof blanks are explicitly recovered above, never guessed by the
    # generic formatter. Prose and every untargeted formula remain byte exact.
    fmt.validate_prose(result)
    return result,reviews
def run():
    findings=json.loads((AUDIT/'findings.json').read_text());current={e[':db/id']:e for group in ('questions','tutorials') for [e] in json.loads((HERE/(group+'.json')).read_text())}
    if (HERE/'current-field-overlays.json').exists():
        for c in json.loads((HERE/'current-field-overlays.json').read_text()):
            assert current[c['entity']][c['attribute']]==c['prepared_before']
            current[c['entity']][c['attribute']]=c['current']
    changes=[];unchanged=[];failures=[]
    targets={(f['entity'],f['attribute']):f for f in findings}
    targets[(17592186129058,':question/problem')]={'reasons':['source-confirmed-corrupted-step-annotations'],'lessons':next(f['lessons'] for f in findings if f['entity']==17592186129058)}
    for entity in (17592186083066,17592186138255,17592186138281):
        targets[(entity,':question/problem')]={'reasons':['currency-markers-corrupted-in-matching-prompt'],'lessons':next(f['lessons'] for f in findings if f['entity']==entity)}
    for (entity,attr),f in targets.items():
        before=current[entity][attr]
        try:after,reviews=transform(before,entity,attr)
        except Exception as e:
            failures.append({'entity':entity,'attribute':attr,'error':str(e)});continue
        if before==after:unchanged.append({'entity':entity,'attribute':attr,'reasons':f['reasons']});continue
        changes.append({'entity':entity,'attribute':attr,'before':before,'after':after,'before_sha256':digest(before),'after_sha256':digest(after),'reasons':f['reasons'],'lessons':f['lessons'],'source_id':f.get('source_id'),'individual_reviews':reviews})
    save('changes.json',changes);save('unchanged.json',unchanged);save('preparation-failures.json',failures)
    summary={'basis':json.loads((HERE/'identity.json').read_text())['basis'],'fields':len(changes),'entities':len({c['entity'] for c in changes}),'attributes':dict(Counter(c['attribute'] for c in changes)),'lessons':len({l[':db/id'] for c in changes for l in c['lessons']}),'unchanged_fields':len(unchanged),'failures':failures,'individually_reviewed_fields':len([c for c in changes if c['individual_reviews']]),'all_other_repairs_preserve_expression_tokens':True}
    save('preparation-summary.json',summary);print(json.dumps(summary,indent=2));assert not failures
if __name__=='__main__':run()
