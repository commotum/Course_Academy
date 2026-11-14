#!/usr/bin/env python3
"""Read-only, formula-scoped comparison of EDB math against archived source.

No database access or mutations. Match semantic token sequences inside one MA
identity before comparing fonts, color, and significant authored spacing.
Conflicting source presentations are reported as ambiguous rather than losses.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import csv
from dataclasses import dataclass, field
import hashlib
import gzip
import sqlite3
import time
import resource
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / 'reference/edb-math/audits/2026-11-13-source-math-style-loss'
GREEK = dict(zip(
    'alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron pi rho sigma tau upsilon phi chi psi omega Gamma Delta Theta Lambda Xi Pi Sigma Upsilon Phi Psi Omega varepsilon vartheta varpi varrho varsigma varphi'.split(),
    'αβγδεζηθικλμνξοπρστυφχψωΓΔΘΛΞΠΣΥΦΨΩϵϑϖϱςϕ'))
ALIASES = {'neq':'ne', 'leq':'le', 'geq':'ge', 'rightarrow':'to', 'lnot':'neg',
           'land':'wedge', 'lor':'vee', 'dfrac':'frac', 'tfrac':'frac',
           'dbinom':'binom', 'tbinom':'binom', 'lbrack':'[', 'rbrack':']',
           'lbrace':r'\{', 'rbrace':r'\}', 'checkmark':'✓'}
UNICODE = {'−':'-', '×':r'\times', '⋅':r'\cdot', '≠':r'\ne', '≤':r'\le',
           '≥':r'\ge', '∈':r'\in', '∉':r'\notin', '→':r'\to', '∞':r'\infty',
           '∅':r'\emptyset', '±':r'\pm', '∪':r'\cup', '∩':r'\cap', '∑':r'\sum',
           '∏':r'\prod', '∫':r'\int', '\u2061':'', '\u2062':''}
FONTS = {'mathrm':'normal', 'mathnormal':'default', 'mathbf':'bold', 'boldsymbol':'bold',
         'bm':'bold', 'mathit':'italic', 'mathbfit':'bold-italic', 'mathbb':'double-struck',
         'mathcal':'script', 'mathscr':'script', 'mathfrak':'fraktur',
         'mathsf':'sans-serif', 'mathtt':'monospace'}
DECLARATIONS = {'rm':'normal', 'bf':'bold', 'it':'italic', 'sf':'sans-serif', 'tt':'monospace'}
SPACING = {',':1/6, ':':2/9, ';':5/18, '!':-1/6, 'quad':1., 'qquad':2.,
           'enspace':.5, 'enskip':.5, 'thinspace':1/6, 'medspace':2/9, 'thickspace':5/18,
           'negthinspace':-1/6, 'negmedspace':-2/9, 'negthickspace':-5/18, ' ':1/3}
SIZING = {'left','right','middle','big','Big','bigg','Bigg','bigl','bigr','Bigl','Bigr',
          'biggl','biggr','Biggl','Biggr'}
LAYOUT = {'displaystyle','textstyle','scriptstyle','scriptscriptstyle','limits','nolimits'}
ARGUMENTS = {'frac':2,'binom':2,'sqrt':1,'overline':1,'underline':1,'hat':1,'widehat':1,
             'bar':1,'vec':1,'dot':1,'ddot':1,'tilde':1,'widetilde':1,'overbrace':1,
             'underbrace':1,'overset':2,'underset':2,'stackrel':2,'cancel':1,'bcancel':1,
             'xcancel':1,'phantom':1,'hphantom':1,'vphantom':1,'smash':1,'boxed':1}
TOKEN = re.compile(r'\\[A-Za-z]+\*?|\\.|.', re.S)
MATH = re.compile(r'(?<!\\)\$\$(.*?)\$\$|(?<![\\$])\$(?!\$)(.*?)(?<!\\)\$|\\\[(.*?)\\\]|\\\((.*?)\\\)', re.S)

@dataclass
class Parsed:
    tokens: list[str] = field(default_factory=list)
    atoms: dict[int, dict] = field(default_factory=dict)
    spaces: dict[int, float] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)


def color_name(value: str) -> str:
    value = value.strip().lower().replace(' ', '')
    names = {'red':'#ff0000','darkgreen':'#006400','green':'#008000','black':'#000000',
             'white':'#ffffff','blue':'#0000ff','yellow':'#ffff00','gray':'#808080',
             'grey':'#808080','orange':'#ffa500','purple':'#800080'}
    if re.fullmatch(r'#[0-9a-f]{3}', value): value = '#' + ''.join(x*2 for x in value[1:])
    return names.get(value, value)


class Parser:
    def __init__(self, text: str):
        # Comments and alignment padding do not change the expression.
        text = re.sub(r'(?<!\\)%[^\n]*', '', text)
        self.parts = TOKEN.findall(text)
        self.i = 0
        self.out = Parsed()

    def peek(self):
        while self.i < len(self.parts) and self.parts[self.i].isspace(): self.i += 1
        return self.parts[self.i] if self.i < len(self.parts) else None

    def take(self):
        value = self.peek()
        if value is not None: self.i += 1
        return value

    def group_text(self, optional=False):
        opening = '[' if optional else '{'; closing = ']' if optional else '}'
        if self.peek() != opening:
            if optional:return None
            value = self.take()
            if value is None:self.out.errors.append('missing argument');return ''
            return value
        self.i += 1; depth = 1; result=[]
        while self.i < len(self.parts):
            value=self.parts[self.i];self.i+=1
            if value==opening:depth+=1
            elif value==closing:
                depth-=1
                if not depth:return ''.join(result)
            result.append(value)
        self.out.errors.append('unclosed argument')
        return ''.join(result)

    def atom(self, token, state, origin=None, visible=True):
        index=len(self.out.tokens);self.out.tokens.append(token)
        if not visible:return
        identifier = len(token)==1 and (token.isalpha() or token.isdigit())
        default = 'italic' if identifier and not token.isdigit() else 'normal'
        if origin in GREEK and GREEK[origin].isupper():default='normal'
        font=state.get('font')
        if font in (None,'default'):font=default
        self.out.atoms[index]={'token':token, 'font':font, 'identifier':identifier,
                               'color':state.get('color'), 'background':state.get('background'),
                               'required_font':state.get('font') not in (None,'default') or (origin in GREEK and GREEK[origin].isupper())}

    def argument(self,state,semantic=False):
        if semantic:self.atom('ARG(',state,visible=False)
        if self.peek()=='{':self.i+=1;self.sequence(dict(state),'}')
        else:self.one(dict(state))
        if semantic:self.atom(')ARG',state,visible=False)

    def sequence(self,state,end=None):
        while (token:=self.peek()) is not None:
            if token==end:self.i+=1;return
            if token=='}':self.out.errors.append('unexpected closing brace');self.i+=1;continue
            self.one(state)
        if end:self.out.errors.append('unclosed group')

    def one(self,state):
        token=self.take()
        if token is None:return
        if token=='{':self.sequence(dict(state),'}');return
        if token in ('^','_'):
            self.atom(token,state,visible=False);self.argument(state,semantic=True);return
        if token=='&':self.atom('CELL',state,visible=False);return
        if not token.startswith('\\'):
            normalized=UNICODE.get(token,token)
            if normalized:self.atom(normalized,state)
            return
        name=token[1:]
        if name in FONTS:
            sub=dict(state);sub['font']=FONTS[name];self.argument(sub);return
        if name in DECLARATIONS:state['font']=DECLARATIONS[name];return
        if name in ('color','textcolor'):
            model=self.group_text(True);value=self.group_text()
            if model and model.lower()=='html':value='#'+value
            elif model:self.out.errors.append('unsupported color model '+model)
            if name=='color':state['color']=color_name(value)
            else:sub=dict(state);sub['color']=color_name(value);self.argument(sub)
            return
        if name in ('bbox','colorbox','fcolorbox'):
            if name=='bbox':
                opts=self.group_text(True)
                values=(opts or '').split(',');colors=[x.strip() for x in values if re.fullmatch(r'#[0-9A-Fa-f]+|[A-Za-z]+',x.strip())]
                if len(colors)!=1:self.out.errors.append('unsupported bbox options');self.argument(state);return
                value=colors[0]
            else:
                if name=='fcolorbox':self.group_text()
                value=self.group_text()
            sub=dict(state);sub['background']=color_name(value);self.argument(sub);return
        if name in SPACING:
            pos=len(self.out.tokens);self.out.spaces[pos]=self.out.spaces.get(pos,0)+SPACING[name];return
        if name in ('hspace','hspace*','kern','mkern','mskip'):
            if name.startswith('hspace'):value=self.group_text()
            else:
                pieces=[]
                while self.peek() and re.fullmatch(r'[\d.+\-a-z]',self.peek()):pieces.append(self.take())
                value=''.join(pieces)
            match=re.fullmatch(r'([+-]?(?:\d+(?:\.\d*)?|\.\d+))\s*(em|mu)',value)
            if match:
                size=float(match[1])/(18 if match[2]=='mu' else 1);pos=len(self.out.tokens)
                self.out.spaces[pos]=self.out.spaces.get(pos,0)+size
            else:self.out.errors.append('unsupported spacing '+value)
            return
        if name in LAYOUT:return
        if name in SIZING:
            if self.peek()=='.':self.i+=1
            return
        if name in ('begin','end'):
            env=self.group_text()
            self.atom(name+':'+env,state,visible=False)
            if name=='begin' and env in ('array','alignedat'):self.group_text()
            if name=='begin' and env in ('aligned','gathered','array'):self.group_text(True)
            return
        if name=='\\':
            self.atom('ROW',state,visible=False);self.group_text(True);return
        if name in ('text','operatorname','operatorname*','mbox','textrm'):
            self.atom('TEXT(',state,visible=False)
            self.argument(dict(state,font='normal'))
            self.atom(')TEXT',state,visible=False);return
        name=ALIASES.get(name,name)
        if name in ARGUMENTS:
            self.atom('\\'+name,state,visible=False)
            if name=='sqrt' and self.peek()=='[':
                index=self.group_text(True);nested=Parser(index);parsed=nested.parse()
                self.atom('INDEX:'+','.join(parsed.tokens),state,visible=False)
            for _ in range(ARGUMENTS[name]):self.argument(state,semantic=True)
            return
        if name in GREEK:self.atom(GREEK[name],state,origin=name);return
        if name in ('✓','[',']') or name.startswith('\\'):self.atom(name,state);return
        if name=='not' and self.peek()=='\\in':self.i+=1;self.atom('\\notin',state);return
        self.atom('\\'+name,state)

    def parse(self):
        self.sequence({})
        return self.out


def parse(text):
    try:return Parser(text).parse()
    except (RecursionError,ValueError,TypeError) as exc:return Parsed(errors=[type(exc).__name__+': '+str(exc)])


def identity(value):return re.sub(r'^(?:tutorial|t)-','t-',str(value))

def formulas(field):
    value=field.get('value','')
    if not isinstance(value,str):return []
    # Remove fenced code examples, which are not rendered mathematical content.
    if field.get('bare_math') or field.get('math_type') in ('math',':answer.type/math','answer.type/math'):
        return [{'tex':value,'start':0,'end':len(value)}]
    return [{'tex':next(g for g in m.groups() if g is not None),'start':m.start(),'end':m.end()} for m in MATH.finditer(value)]


def preferred(records,role):
    roles={'prompt':['problem'],'solution':['worked-solution'],'label':['problem','answer'],
           'answer':['answer'],'feedback':['worked-solution','answer'],'tutorial':['content']}.get(role,[])
    for preferred_role in roles:
        matches=[r for r in records if r['record'].get('role')==preferred_role]
        if matches:return matches,True
    # Migrated statement labels can appear in solutions. Unknown roles are
    # useful evidence but never sufficient to confirm a presentation loss.
    known=[r for r in records if r['record'].get('role') not in (None,'unknown')]
    return (known,False) if known else (records,False)


def feature_losses(source,current):
    losses=[]
    for pos,atom in source.atoms.items():
        target=current.atoms.get(pos)
        if not target:continue
        for kind in ('font','color','background'):
            expected=atom.get(kind);observed=target.get(kind)
            if kind=='font':
                if not atom['identifier'] or not atom.get('required_font'):continue
            elif expected is None:continue
            if expected!=observed:
                losses.append((kind,pos,expected,observed))
    for boundary,size in source.spaces.items():
        observed=current.spaces.get(boundary,0.)
        if abs(observed-size)>1e-6:
            kind='space' if size>=.75 and observed<size else 'space_minor'
            losses.append((kind,boundary,round(size,6),round(observed,6)))
    return losses


def source_evidence(items):
    result=[];seen=set()
    for item in items:
        record=item['record']
        evidence=record.get('evidence') or [{'path':record.get('source_path'),'locator':record.get('locator'),'role':record.get('role')}]
        for e in evidence:
            key=(e.get('path'),e.get('locator'),e.get('role'))
            if key not in seen:seen.add(key);result.append(e)
    return result


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current',type=Path,default=DEFAULT/'current.json')
    parser.add_argument('--sources',type=Path,default=DEFAULT/'source-formulas.jsonl')
    parser.add_argument('--output-dir',type=Path,default=DEFAULT)
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args(argv)
    if args.self_test:self_test();return
    current=json.loads(args.current.read_text())
    started=time.monotonic()
    args.output_dir.mkdir(parents=True,exist_ok=True)
    source_count=0;source_errors=0
    db_path=args.output_dir/'comparison-index.sqlite'
    db=sqlite3.connect(db_path)
    db.execute('PRAGMA journal_mode=OFF');db.execute('PRAGMA synchronous=OFF')
    db.execute('DROP TABLE IF EXISTS source_formulas')
    db.execute('CREATE TABLE source_formulas (identity TEXT, signature TEXT, item TEXT)')
    with args.sources.open() as handle:
        for line in handle:
            if not line.strip():continue
            record=json.loads(line);source_count+=1;result=parse(record.get('source_tex',''))
            record_errors=record.get('errors') or []
            record={k:v for k,v in record.items() if k not in ('raw_mathml','features')}
            item={'record':record,'parsed':result.__dict__,'errors':[*record_errors,*result.errors]}
            if item['errors']:source_errors+=1
            if result.tokens or result.spaces:
                signature=hashlib.sha256('\x1f'.join(result.tokens).encode()).hexdigest()
                db.execute('INSERT INTO source_formulas VALUES (?,?,?)',(identity(record.get('math_academy_id',record.get('ma_id'))),signature,json.dumps(item,ensure_ascii=False)))
            if source_count%10000==0:db.commit()
    db.execute('CREATE INDEX identity_signature ON source_formulas(identity,signature)');db.commit()
    def owner_sources(mid):
        result=defaultdict(list)
        for signature,serialized in db.execute('SELECT signature,item FROM source_formulas WHERE identity=?',(mid,)):
            item=json.loads(serialized);parsed=item['parsed']
            parsed['atoms']={int(k):v for k,v in parsed['atoms'].items()}
            parsed['spaces']={int(k):v for k,v in parsed['spaces'].items()}
            item['parsed']=Parsed(**parsed);result[signature].append(item)
        return result
    unmatched_handle=gzip.open(args.output_dir/'unmatched-formulas.jsonl.gz','wt')
    gaps=[]
    findings=[];counters=Counter();seen={};coverage=Counter()
    owners=[*current.get('questions',[]),*current.get('tutorials',[])]
    def emit(row):
        key=(row['entity'],row['attribute'],row.get('formula_hash'),row['status'],row.get('feature'),str(row.get('expected')),str(row.get('observed')),tuple(row.get('positions',[])))
        if key in seen:
            existing=seen[key];existing['occurrences'].extend(row['occurrences'])
            return
        seen[key]=row;findings.append(row)
    for owner in owners:
        mid=identity(owner.get('ma_id'));candidates=owner_sources(mid)
        owner_unmatched=Counter()
        coverage['owners']+=1
        if not candidates:coverage['owners_without_source']+=1
        for f in owner.get('fields',[]):
            coverage['fields']+=1
            for occurrence,formula in enumerate(formulas(f)):
                counters['current_formulas']+=1;parsed=parse(formula['tex'])
                digest=hashlib.sha256('\x1f'.join(parsed.tokens).encode()).hexdigest()
                base={'entity':f.get('entity',owner['entity']),'question_entity':owner['entity'],'ma_id':owner.get('ma_id'),
                      'attribute':f.get('attribute'),'role':f.get('role'),'retired':owner.get('retired',False),
                      'topics':owner.get('topics',[]),'knowledge_points':owner.get('knowledge_points',[]),
                      'formula_hash':digest,'current_tex':formula['tex'],'occurrences':[{'index':occurrence,'start':formula['start'],'end':formula['end']}]}
                if parsed.errors:
                    unmatched_handle.write(json.dumps({'entity':base['entity'],'question_entity':owner['entity'],'ma_id':owner.get('ma_id'),'attribute':f.get('attribute'),'tex':formula['tex'],'reason':'current_parse_error','errors':parsed.errors},ensure_ascii=False)+'\n');counters['current_parse_error']+=1;owner_unmatched['current_parse_error']+=1;continue
                matches=[m for m in candidates.get(digest,[]) if m['parsed'].tokens==parsed.tokens]
                if not matches:
                    reason='no_matching_source_formula' if candidates else 'no_source_identity'
                    if candidates:unmatched_handle.write(json.dumps({'entity':base['entity'],'question_entity':owner['entity'],'ma_id':owner.get('ma_id'),'attribute':f.get('attribute'),'tex':formula['tex'],'reason':reason},ensure_ascii=False)+'\n')
                    counters['unmatched_formulas']+=1;owner_unmatched[reason]+=1;continue
                matches,role_known=preferred(matches,f.get('role'))
                usable=[m for m in matches if not m['errors']]
                if not usable:
                    emit(dict(base,status='ambiguous',reason='source_parse_error',sources=source_evidence(matches),errors=sorted({e for m in matches for e in m['errors']})))
                    counters['source_parse_error_matches']+=1;continue
                counters['matched_formulas']+=1
                loss_sets=[set(feature_losses(m['parsed'],parsed)) for m in usable]
                union=set.union(*loss_sets) if loss_sets else set()
                common=set.intersection(*loss_sets) if loss_sets else set()
                if not union:counters['matching_presentations']+=1;continue
                grouped=defaultdict(list)
                for kind,pos,expected,observed in union:
                    confirmed=(kind,pos,expected,observed) in common and role_known and len(usable)==len(matches)
                    status=('confirmed_spacing_difference' if kind=='space_minor' else 'confirmed_loss') if confirmed else 'ambiguous'
                    grouped[(status,kind,expected,observed)].append(pos)
                for (status,kind,expected,observed),positions in grouped.items():
                    row=dict(base,status=status,feature=kind,expected=expected,observed=observed,positions=sorted(positions),
                             source_tex=list(dict.fromkeys(m['record']['source_tex'] for m in usable)),sources=source_evidence(usable))
                    row['reason']=('authored_spacing_differs' if status=='confirmed_spacing_difference' else 'source_style_absent_or_weaker') if status.startswith('confirmed') else 'conflicting_or_incomplete_source_presentation'
                    emit(row)
        if owner_unmatched:gaps.append({'entity':owner['entity'],'ma_id':owner.get('ma_id'),'topics':owner.get('topics',[]),'counts':dict(owner_unmatched)})
    unmatched_handle.close();db.close()
    (args.output_dir/'source-gaps.json').write_text(json.dumps(gaps,ensure_ascii=False,indent=2)+'\n')
    findings.sort(key=lambda f:(f['status'],str(f.get('ma_id')),f['entity'],f['attribute'],f['formula_hash'],f.get('feature','')))
    (args.output_dir/'findings.json').write_text(json.dumps(findings,ensure_ascii=False,indent=2)+'\n')
    columns=['status','entity','question_entity','ma_id','attribute','role','retired','topic_titles','feature','expected','observed','positions','current_tex','source_tex','source_paths','reason']
    with (args.output_dir/'findings.csv').open('w',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=columns);writer.writeheader()
        for row in findings:
            simple={k:row.get(k,'') for k in columns};simple['topic_titles']=' | '.join(t.get('title','') for t in row['topics'])
            simple['source_paths']=' | '.join(dict.fromkeys(s.get('path','') or '' for s in row.get('sources',[])))
            for key in ('positions','source_tex'):simple[key]=json.dumps(row.get(key,[]),ensure_ascii=False)
            writer.writerow(simple)
    summary={'basis':current.get('basis'),'source_formulas':source_count,'source_formula_parse_errors':source_errors,
             'coverage':dict(coverage),'formula_counts':dict(counters),'findings_by_status':dict(Counter(f['status'] for f in findings)),
             'confirmed_by_feature':dict(Counter(f['feature'] for f in findings if f['status']=='confirmed_loss')),
             'affected_questions':len({f['question_entity'] for f in findings if f['status']=='confirmed_loss'}),
             'affected_attributes':len({(f['entity'],f['attribute']) for f in findings if f['status']=='confirmed_loss'}),
             'runtime_seconds':round(time.monotonic()-started,2),'peak_memory_mib':round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,1),
             'unmatched_details':'unmatched-formulas.jsonl.gz; owners without any source are listed once in source-gaps.json',
             'read_only':True,'matching':'Exact presentation-stripped semantic tokens inside MA identity; scoped effective font/color/spacing comparison; conflicts quarantined.',
             'limitations':['Unmatched formulas are not evidence of loss.','Authored spacing >=0.75em reduced in current content is prioritized as confirmed_loss; smaller, zero, negative, or increased spacing is reported separately as confirmed_spacing_difference.','Conflicting source presentations and parse errors cannot confirm a loss.','No source correction or EDB mutation is performed.']}
    (args.output_dir/'comparison-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False))


def self_test():
    def pair(a,b):
        aa,bb=parse(a),parse(b);assert not aa.errors,(a,aa.errors);assert not bb.errors,(b,bb.errors);assert aa.tokens==bb.tokens,(a,b,aa.tokens,bb.tokens);return aa,bb
    a,b=pair(r'0\cdot\mathbf{v}=\mathbf{0}',r'0\cdot v=0')
    assert [(x[1],x[2]) for x in feature_losses(a,b)]==[(2,'bold'),(4,'bold')]
    a,b=pair(r'\mathrm{Π}',r'\Pi');assert not feature_losses(a,b)
    a,b=pair(r'\mathrm{Π}','Π');assert feature_losses(a,b)==[('font',0,'normal','italic')]
    a,b=pair(r'x=0\quad{\color{red}\times}',r'x=0\,\times')
    assert ('color',3,'#ff0000',None) in feature_losses(a,b)
    assert ('space',3,1.,round(1/6,6)) in feature_losses(a,b)
    a,b=pair(r'x\qquad y',r'x\hspace{2em}y');assert not feature_losses(a,b)
    a,b=pair(r'{\mathbb{R}}^{2}',r'{R}^2');assert feature_losses(a,b)==[('font',0,'double-struck','italic')]
    a,b=pair(r'x\hspace{0em}y',r'x\,y');assert feature_losses(a,b)==[('space_minor',1,0.,round(1/6,6))]
    a,b=pair(r'x\hspace{-0.167em}y',r'x\,y');assert feature_losses(a,b)==[('space_minor',1,-.167,round(1/6,6))]
    a,b=pair(r'\mathit{Π}',r'\Pi');assert feature_losses(a,b)==[('font',0,'italic','normal')]
    assert parse(r'\frac{a}{bc}').tokens!=parse(r'\frac{ab}{c}').tokens
    a,b=pair(r'\mathbf{a}+b',r'a+\mathbf{b}');assert feature_losses(a,b)[0][1]==0
    a,b=pair(r'{\color{red}x}+y',r'x+{\color{red}y}');assert feature_losses(a,b)==[('color',0,'#ff0000',None)]
    print('Self-test passed: scoped fonts/colors, default Greek, spacing equivalence, and fraction structure.')

if __name__=='__main__':main()
