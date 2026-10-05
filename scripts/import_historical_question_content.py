#!/usr/bin/env python3
"""Reconstruct content-only question records from saved MA history evidence."""
import argparse
import json
import re
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup, NavigableString, Tag

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reference/mathacademy/history-question-import-2026-10-04'
HISTORY=ROOT/'reference/mathacademy/progress-history-2026-10-04/observations.json'
AUDIT=ROOT/'.local/edb/missing-question-kp-audit-2026-10-04/audit.json'
GREEK=dict(zip('αβγδθλμπρσφω∞',['\\alpha ','\\beta ','\\gamma ','\\delta ','\\theta ','\\lambda ','\\mu ','\\pi ','\\rho ','\\sigma ','\\phi ','\\omega ','\\infty ']))
OPS={'∫':'\\int ','∑':'\\sum ','∏':'\\prod ','⋅':'\\cdot ','×':'\\times ','−':'-','±':'\\pm ','≤':'\\le ','≥':'\\ge ','≠':'\\ne ','→':'\\to ','∈':'\\in ','∉':'\\notin ','∪':'\\cup ','∩':'\\cap ','≈':'\\approx ','∅':'\\emptyset ','↔':'\\leftrightarrow ','⇒':'\\Rightarrow ','∴':'\\therefore ','′':"'",'″':"''",'⁡':'','⁢':''}

class Renderer:
    def __init__(self,topic):
        self.topic=topic;self.errors=[];self.assets=[];self.fields=[];self.formulas=[]
    def m(self,n):
        if isinstance(n,NavigableString):return GREEK.get(str(n),OPS.get(str(n),str(n)))
        if not isinstance(n,Tag):return ''
        t=n.name.lower()
        if t in ('mphantom','annotation','annotation-xml'):return ''
        cs=[self.m(c) for c in n.children];base=cs[0] if cs and cs[0] in (')',']','}') else '{'+(cs[0] if cs else '')+'}'
        if t=='mfrac':return '\\frac{'+cs[0]+'}{'+cs[1]+'}'
        if t=='msup':return base+'^{'+cs[1]+'}'
        if t=='msub':return base+'_{'+cs[1]+'}'
        if t=='msubsup':return base+'_{'+cs[1]+'}^{'+cs[2]+'}'
        if t=='munder':return base+'_{'+cs[1]+'}'
        if t=='mover':return '\\overset{'+cs[1]+'}{'+cs[0]+'}'
        if t=='munderover':return base+'_{'+cs[1]+'}^{'+cs[2]+'}'
        if t=='msqrt':return '\\sqrt{'+''.join(cs)+'}'
        if t=='mroot':return '\\sqrt['+cs[1]+']{'+cs[0]+'}'
        if t=='mspace':return '\\,'
        if t=='mtext':return '\\text{'+n.get_text()+'}'
        if t=='mo':return OPS.get(n.get_text(),GREEK.get(n.get_text(),n.get_text()))
        if t=='mi':
            nxt=n.find_next_sibling()
            if re.fullmatch('[A-Za-z]+',n.get_text()) and nxt is not None and nxt.name=='mo' and nxt.get_text()=='\u2061':return '\\operatorname{'+n.get_text()+'}'
            return GREEK.get(n.get_text(),n.get_text())
        if t=='mtable':return '\\begin{aligned}'+' \\\\ '.join(cs)+'\\end{aligned}'
        if t in ('mtr','mlabeledtr'):return ' & '.join(cs)
        if t=='menclose':
            if 'strike' in n.get('notation',''):return '\\cancel{'+''.join(cs)+'}'
            if 'box' in n.get('notation',''):return '\\boxed{'+''.join(cs)+'}'
            self.errors.append('Unsupported enclosure: '+str(n));return ''.join(cs)
        if t=='mfenced':return n.get('open','(')+n.get('separators',',').join(cs)+n.get('close',')')
        if t=='semantics':return cs[0] if cs else ''
        if t in ('math','mrow','mn','mtd','mstyle','mpadded','none'):return ''.join(cs)
        self.errors.append('Unsupported MathML: '+t);return ''.join(cs)
    def asset(self,src):
        full=urljoin('https://mathacademy.com',src)
        local=Path('/home/jake/Developer/MA/DATA/Lessons')/str(self.topic)/'Source/Images'/(Path(src).name+'.png')
        if local.exists():full=str(local)
        self.assets.append({'source_url':urljoin('https://mathacademy.com',src),'stored_path':full})
        return full
    def render(self,n,extract_fields=False):
        if isinstance(n,NavigableString):return str(n)
        if not isinstance(n,Tag):return ''
        t=n.name.lower();classes=n.get('class',[])
        if t in ('style','script','mjx-math','mjx-assistive-mml') or any(c in classes for c in ('studentAnswer','studentAnswerHeader','answerDetails','questionHeader')):return ''
        if extract_fields and 'freeResponseTextbox' in classes:
            key='field-'+str(len(self.fields)+1);value=self.text(n,False)
            maths=n.find_all('math');kind='math' if len(maths)==1 and value.startswith('$') and value.endswith('$') else 'text'
            if kind=='math':value=value[1:-1]
            self.fields.append({'key':key,'type':'blank','choices':[{'type':kind,'value':value}] if value else [],'correct_value':value,'evidence':'Correct value displayed in historical free-response textbox'})
            return '{{'+key+'}}'
        if extract_fields and 'selectList' in classes:
            selected=n.find(class_='selectListFrame')
            assert selected is not None and 'correctSelection' in selected.get('class',[]), 'Unverified historical dropdown'
            value=self.text(selected)
            value=value[1:-1] if value.startswith('$') and value.endswith('$') else value
            choices=[]
            for option in n.find_all(class_='selectListOption'):
                text=self.text(option)
                text=text[1:-1] if text.startswith('$') and text.endswith('$') else text
                if text not in [c['value'] for c in choices]:choices.append({'type':'math','value':text})
            key='field-'+str(len(self.fields)+1)
            self.fields.append({'key':key,'type':'select','choices':choices,'correct_value':value,
                'evidence':'Original historical dropdown options and correctSelection value'})
            return '{{'+key+'}}'
        if t in ('mjx-container','math'):
            math=n if t=='math' else n.find('math')
            if math is None:self.errors.append('Formula without MathML');return ''
            tex=self.m(math);self.formulas.append(tex)
            return '\n\n$$\n'+tex+'\n$$\n\n' if n.get('display')=='true' else '$'+tex+'$'
        if t=='img':return '![]('+self.asset(n.get('src',''))+')'
        if t=='svg':self.errors.append('Inline SVG needs saved asset');return ''
        if t=='br':return '\n'
        if t in ('ul','ol') and 'questionStatements' in classes:
            roman=['I','II','III','IV','V','VI']
            return '\n\n'+'\n'.join(roman[i]+'. '+self.text(c,extract_fields) for i,c in enumerate(n.find_all('li',recursive=False)))+'\n\n'
        if t=='table':
            rows=[]
            for row in n.find_all('tr'):
                cells=[self.text(c,extract_fields) for c in row.find_all(['td','th'],recursive=False)]
                if cells:rows.append(cells)
            width=max(map(len,rows),default=0)
            if width:
                lines=['| '+' | '.join(r+['']*(width-len(r)))+' |' for r in rows];lines.insert(1,'| '+' | '.join(['---']*width)+' |')
                return '\n\n'+'\n'.join(lines)+'\n\n'
        children=''.join(self.render(c,extract_fields) for c in n.children)
        if t=='li':return '- '+children.strip()+'\n'
        if t in ('b','strong'):return '**'+children+'**'
        if t in ('i','em'):return '*'+children+'*'
        if t in ('p','div','ul','ol'):return '\n\n'+children+'\n\n'
        return children
    def text(self,n,extract_fields=False):return re.sub('\n{3,}','\n\n',self.render(n,extract_fields)).strip()

def prepare():
    OUT.mkdir(parents=True,exist_ok=True)
    audit=json.loads(AUDIT.read_text());matches={q['question_id']:q['associations'] for q in audit['questions']}
    history=json.loads(HISTORY.read_text());records={};raw_cache={}
    for task in history['tasks']:
        for q in task['questions']:
            mid=q['id'].replace('question-','q-')
            if mid not in matches or mid in records:continue
            r=Renderer(q['topic_id']);p=BeautifulSoup(q['problem_html'],'html.parser');s=BeautifulSoup(q['worked_solution_html'],'html.parser')
            problem=r.text(p,True);prompt_formulas=r.formulas[:];r.formulas=[]
            solution=r.text(s);solution_formulas=r.formulas[:]
            paragraphs=[r.text(n) for n in s.find_all(['p','li'],recursive=True) if not n.find_parent(class_='studentAnswer')]
            paragraphs=[x for x in paragraphs if x and x!='Your Answer:']
            # The historical graphic frame sits outside questionText.
            source_file=ROOT/task['source_file']
            if source_file not in raw_cache:
                raw=json.loads(source_file.read_text());raw_cache[source_file]={x['id']:x for x in raw['questions']}
            raw=raw_cache[source_file][q['id']]
            graphic=BeautifulSoup(raw.get('raw_html',''),'html.parser').find(class_='questionGraphicFrame')
            if graphic:problem=r.text(graphic)+'\n\n'+problem
            body=BeautifulSoup(raw.get('raw_html',''),'html.parser').find(class_='questionBody')
            if body:problem+='\n\n'+r.text(body,True)
            assoc=matches[mid]
            assert len({a['database_kp_uuid'] for a in assoc})==1,(mid,assoc)
            records[mid]={'math_academy_id':mid,'topic_id':q['topic_id'],'knowledge_point_id':assoc[0]['database_kp_uuid'],
                'knowledge_point':assoc[0]['database_kp_title'],'problem':problem,'worked_solution':solution,
                'difficulty':{'E':'easy','M':'moderate','H':'hard'}[q['difficulty']],
                'answer_fields':r.fields,'extraction_errors':sorted(set(r.errors)),
                'solution_formulas':solution_formulas,'prompt_formulas':prompt_formulas,'solution_paragraphs':paragraphs,
                'assets':r.assets,'provenance':{'source_file':str(source_file.relative_to(ROOT)),'original_question_id':q['id'],
                    'source_kind':'completed historical activity','answer_derivation':'Displayed correct response or reconstructed from worked solution; no learner answer used'}}
        print('Prepared',len(records),'questions',flush=True) if len(records)%100<8 else None
    content=json.loads((ROOT/'reference/mathacademy/question-capture/13942892/content.json').read_text())
    for q in content['questions']:
        if q['math_academy_id'] in matches and q['math_academy_id'] not in records:records[q['math_academy_id']]={**q,'topic_id':3710,'extraction_errors':[],'source_kind':'automated lesson capture'}
    assert set(records)==set(matches)
    (OUT/'prepared.json').write_text(json.dumps({'questions':list(records.values())},indent=2)+'\n')
    print('Saved',len(records),'questions to',OUT/'prepared.json')
if __name__=='__main__':prepare()
