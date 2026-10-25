// Pure DOM extraction. No application state, answer keys, or network calls.
element => {
function sourceHTMLTable(table, renderLeaf, reportError) {
  const esc=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]);
  const safeText=value=>{const math=[];let prefix='CATABLETEXT';while(String(value).includes(prefix))prefix+='X';let text=String(value).replace(/\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\[\s\S]|[^$\\])*?(?<!\\)\$/g,m=>{math.push(m);return prefix+(math.length-1)+'END'});return esc(text).replace(/(?<!\\)\$/g,'\\$').replace(new RegExp(prefix+'(\\d+)END','g'),(_,i)=>math[Number(i)])};
  const props=node=>Object.fromEntries((node.getAttribute('style')||'').split(';').filter(x=>x.includes(':')).map(x=>{const i=x.indexOf(':');return[x.slice(0,i).trim().toLowerCase(),x.slice(i+1).trim()]}));
  const align=value=>['left','right','center','justify'].includes(value)?value:null;
  const color=raw=>{let v=String(raw||'').trim();if(/^[\da-f]{6}$/i.test(v))v='#'+v;if(/^#[\da-f\s]+$/i.test(v))v=v.replace(/\s/g,'');return /^(?:#[\da-f]{3}(?:[\da-f]{3})?|[a-z]+|rgba?\([\d.,%\s]+\))$/i.test(v)&&!['transparent','inherit','initial','unset','currentcolor'].includes(v.toLowerCase())?v:null};
  const structural=new Set(['table','thead','tbody','tfoot','tr','td','th','caption','colgroup','col']);
  const lastRows=new Set();for(const t of [table,...table.querySelectorAll('table')]){const rows=[...t.querySelectorAll('tr')].filter(r=>r.closest('table')===t);if(rows.length)lastRows.add(rows.at(-1))}
  function attributes(node){
    const tag=node.localName,s=props(node),a=[];const put=(k,v)=>a.push(' '+k+'="'+esc(v)+'"');
    if(/^(?:grid|inline-grid|flex|inline-flex)$/.test(s.display)||['absolute','fixed'].includes(s.position))reportError('Unsupported table layout style');
    if(tag==='table'){
      put('class','source-table');put('data-rules',['all','rows','cols'].includes(node.getAttribute('rules'))?node.getAttribute('rules'):'none');
      const location=align(node.getAttribute('align'))||((s.margin==='auto'||s['margin-left']==='auto'&&s['margin-right']==='auto')?'center':null);if(location)put('data-table-align',location);
      if(!['','0'].includes(node.getAttribute('border')||'0')||s.border&&!/^(?:none|hidden|0(?:px)?)(?:\s|$)/.test(s.border))put('data-frame','true');
    }else if(tag==='tr'&&!lastRows.has(node))put('data-next-row','true');
    for(const k of ['rowspan','colspan','span'])if(node.hasAttribute(k)){const v=node.getAttribute(k);if(!/^\d{1,3}$/.test(v)||Number(v)===0&&k!=='rowspan')reportError('Unsupported table span: '+k+'='+v);else put(k,v)}
    if(tag==='th'&&['row','col','rowgroup','colgroup'].includes(node.getAttribute('scope')))put('scope',node.getAttribute('scope'));
    const ancestors=[node];if(['td','th'].includes(tag))for(let p=node.parentElement;p;p=p.parentElement){ancestors.push(p);if(p.localName==='table')break}
    for(const p of ancestors){const value=(p.localName==='table'?null:align(p.getAttribute('align')))||align(props(p)['text-align']);if(value){put('data-cell-align',value);break}}
    const fill=color(node.getAttribute('bgcolor')||s['background-color']||s.background);if(fill)put('data-fill',fill);
    if(/^(?:bold|[6-9]00)$/.test(s['font-weight']||''))put('data-cell-weight','bold');
    if(['top','middle','bottom'].includes(s['vertical-align']||node.getAttribute('valign')))put('data-cell-valign',s['vertical-align']||node.getAttribute('valign'));
    if(['td','th'].includes(tag))for(const side of ['top','right','bottom','left']){const value=s['border-'+side]??s.border;if(value!==undefined)put('data-border-'+side,/^(?:none|hidden|0(?:px)?)(?:\s|$)/.test(value)?'none':'solid')}
    return a.join('');
  }
  function walk(node){
    if(node.nodeType===3)return safeText(renderLeaf(node));if(node.nodeType!==1)return '';
    const tag=node.localName;if(node.matches('script,style,mjx-assistive-mml,.studentAnswer,.studentAnswerHeader,.stepHeader,.helpButton,[id^="continueButton-"],[id^="submitButton-"]'))return '';
    if(node.matches('math,mjx-container,svg,input,select,img,.freeResponseTextbox,.selectList,.mjpage,.MathJax')){
      const value=renderLeaf(node),image=/^!\[([^\]]*)\]\(([^)]+)\)$/.exec(value.trim());return image?'<img src="'+esc(image[2])+'" alt="'+esc(image[1])+'">':safeText(value);
    }
    const content=()=>[...node.childNodes].map(walk).join('');
    if(structural.has(tag)){const result='<'+tag+attributes(node)+'>'+content()+(tag==='col'?'':'</'+tag+'>');return tag==='table'?'<div class="source-table-scroll">'+result+'</div>':result}
    if(tag==='br')return '<br>';
    const normalized=({b:'strong',i:'em'})[tag]||tag;
    if(['strong','em','sup','sub','p','ul','ol','li'].includes(normalized)){
      let attrs='';for(const k of ['type','start','reversed','value'])if(node.hasAttribute(k))attrs+=' '+k+'="'+esc(node.getAttribute(k))+'"';
      return '<'+normalized+attrs+'>'+content()+'</'+normalized+'>';
    }
    if(tag==='a'&&node.hasAttribute('href'))return '<a href="'+esc(node.getAttribute('href'))+'">'+content()+'</a>';
    return content();
  }
  return '\n\n'+walk(table)+'\n\n';
}

  const errors = [];
  const emptyFormula = n => n?.localName === 'svg' && n.closest('.mjpage, mjx-container, .MathJax') &&
    n.getAttribute('width') === '0' && n.getAttribute('viewBox')?.trim().split(/\s+/)[2] === '0' &&
    !n.textContent.trim() && !n.querySelector('path,use,text,line,polyline,polygon,circle,ellipse,rect,image,foreignObject');
  // MathJax can render part of an SVG's TeX title again as nested MathML.
  // That MathML describes only the inner fragment (e.g. phantom spacing),
  // not the surrounding visible fbox. Preserve the whole rendered formula.
  const mixedTitle = n => {
    const title = n?.querySelector('title');
    return title?.querySelector('math') && [...title.childNodes].some(child =>
      child.nodeType === 3 && child.textContent.trim());
  };
  // Some old SVG titles wrap complete MathML in a redundant eqalign, or put
  // just the fences outside its MathML table. These known wrappers
  // can be recovered without turning the equations into screenshot assets.
  const recoverableTitle = n => {
    const title = n?.querySelector('title');
    if (!title || title.children.length !== 1) return null;
    const math = title.querySelector('math');
    if (!math || title.querySelectorAll('math').length !== 1) return null;
    const children = [...title.childNodes], index = children.indexOf(title.children[0]);
    const literal = nodes => nodes.filter(child => child.nodeType === 3).map(child => child.textContent).join('').replace(/\s+/g, '');
    const before = literal(children.slice(0, index)), after = literal(children.slice(index + 1));
    if (before === '\\eqalign{' && after === '}') return {math};
    if (before === '\\left\\{' && after === '\\right.' && math.children.length === 1 && math.children[0].localName === 'mtable') {
      return {math: math.children[0], environment: 'cases'};
    }
    if (before === '\\left[' && after === '\\right]' && math.children.length === 1 &&
        math.children[0].localName === 'mtable' &&
        (math.children[0].getAttribute('columnalign') || 'center').split(/\s+/).every(value => value === 'center')) {
      return {math: math.children[0], environment: 'bmatrix'};
    }
    return null;
  };
  function legacyMatrixTex(value) {
    let source = value, match;
    const command = /\\matrix\s*\{/g;
    while ((match = command.exec(source))) {
      const opening = command.lastIndex - 1;
      let depth = 1, end = opening + 1;
      for (; end < source.length && depth; end++) {
        if (source[end] === '\\' && ['\\', '{', '}'].includes(source[end + 1])) { end++; continue; }
        if (source[end] === '{') depth++;
        else if (source[end] === '}') depth--;
      }
      if (depth) { errors.push('Unclosed legacy TeX matrix'); break; }
      // Archived SVG titles can retain only one slash before a physical row
      // newline. A TeX backslash-space on the same line is not a row break.
      const body = source.slice(opening + 1, end - 1).replace(/\\cr\b/g, ' \\\\ ')
        .replace(/(?<!\\)\\[ \t]*\r?\n/g, ' \\\\\n')
        .replace(/\\\\\s*$/, '');
      const replacement = '\\begin{matrix}' + body + '\\end{matrix}';
      source = source.slice(0, match.index) + replacement + source.slice(end);
      command.lastIndex = match.index + '\\begin{matrix}'.length;
    }
    return source;
  }
  const assets = [...element.querySelectorAll('img, canvas, svg')].filter(n => {
    if (emptyFormula(n)) return false;
    if (n.closest('.questionWidget-header, .questionWidget-result, .stepHeader, .spinnerFrame, .answer') ||
        n.parentElement?.closest('svg')) return false;
    const formula = n.closest('.mjpage, mjx-container, .MathJax');
    if (!formula) return true;
    if (n.localName === 'svg' && mixedTitle(n) && !recoverableTitle(n)) return true;
    // Some server-rendered formulas have only SVG paths, with no local TeX or
    // assistive MathML. Preserve their visible rendering as a formula image.
    return n.localName === 'svg' && !formula.querySelector('mjx-assistive-mml math') &&
      !n.querySelector('title')?.textContent.trim();
  });
  const fields = [], fieldNodes = new Map();
  const rows = [...element.querySelectorAll('.questionWidget-choicesTable tr, tr:has(.choiceLetterCircle)')]
    .filter(row => row.closest('table')?.matches('.questionWidget-choicesTable') ||
      [...row.querySelectorAll('.choiceLetterCircle')].some(circle => circle.closest('tr') === row));
  if (rows.length) fields.push({key:'selection', type:'radio', choices:[]});
  const nodes = [...element.querySelectorAll('.matheditor-wrapper-answer, .selectList, input:not([type="hidden"]), textarea, select, [contenteditable="true"]' +
    (['Correct','Incorrect','Skipped Question'].includes(element.querySelector('.questionWidget-result')?.textContent.trim()) ? ', .freeResponseTextbox' : ''))]
    .filter(n => !n.closest('.questionWidget-explanation, .exampleExplanation') &&
      !n.parentElement?.closest('.matheditor-wrapper-answer, .selectList, [contenteditable="true"]'));
  for (const n of nodes) {
    const key = 'field-' + (fields.filter(f => f.key !== 'selection').length + 1);
    if (!n.id && !n.matches('.matheditor-wrapper-answer')) {
      errors.push('Answer control needs an observed DOM ID: ' + n.tagName);
      continue;
    }
    let type = n.matches('.selectList, select') ? 'select' : 'blank';
    const f = {key, type, dom_id:n.id, tag:n.tagName.toLowerCase(), choices:[]};
    if (n.matches('.matheditor-wrapper-answer')) {
      f.tag = 'mathquill';
      f.dom_index = [...element.querySelectorAll('.matheditor-wrapper-answer')].indexOf(n);
      f.input_html = n.outerHTML;
      f.rendered_text = n.querySelector('.mq-root-block')?.textContent || '';
      if (!n.querySelector('.mq-editable-field .mq-textarea textarea')) errors.push('Unsupported math editor: ' + n.id);
    } else if (n.matches('.selectList')) {
      f.tag = 'custom-select';
      const graded = ['Correct','Incorrect','Partial Credit','Skipped Question'].includes(element.querySelector('.questionWidget-result')?.textContent.trim());
      const frame = n.querySelector('.selectListFrame') || n.querySelector(
        graded ? '.selectListFrameDisabled' : '.selectListFrameDisabled.correctSelection, .selectListFrameDisabled.correctSelectionMultipleAttempts');
      f.frame_id = frame?.id;
      if (!f.frame_id) errors.push('Select frame has no ID: ' + n.id);
    } else if (n.matches('input') && !['text','number',''].includes(n.getAttribute('type') || '')) {
      errors.push('Unsupported input type: ' + n.getAttribute('type'));
    }
    fields.push(f); fieldNodes.set(n, key);
  }
  const greek = {'α':'\\alpha ','β':'\\beta ','γ':'\\gamma ','δ':'\\delta ','θ':'\\theta ','λ':'\\lambda ','μ':'\\mu ','π':'\\pi ','ρ':'\\rho ','σ':'\\sigma ','φ':'\\phi ','ω':'\\omega ','∞':'\\infty '};
  const ops = {'∫':'\\int ','∑':'\\sum ','∏':'\\prod ','⋅':'\\cdot ','×':'\\times ','−':'-', '±':'\\pm ','≤':'\\le ','≥':'\\ge ','≠':'\\ne ','→':'\\to ','∈':'\\in ','∉':'\\notin ','∪':'\\cup ','∩':'\\cap '};
  const literalMathGlyph = value => value.replace(/[$%#{}]/g, glyph => '\\' + glyph);
  let formulaFields = new Map();
  // A fenced, centered MathML table is a matrix. Equation layouts have explicit
  // right/left column alignment and must keep their aligned environment.
  function matrixTable(n) {
    if (!n || n.nodeType !== 1) return null;
    if (n.localName === 'mtable') {
      const alignment = n.getAttribute('columnalign') || 'center';
      return alignment.trim().split(/\s+/).every(value => value === 'center') ? n : null;
    }
    if (!['mrow', 'mstyle', 'mpadded', 'semantics'].includes(n.localName)) return null;
    const children = [...n.children].filter(child => !['annotation', 'annotation-xml'].includes(child.localName));
    return children.length === 1 ? matrixTable(children[0]) : null;
  }
  const matrixEnvironments = {'[]':'bmatrix', '()':'pmatrix', '{}':'Bmatrix', '||':'vmatrix', '‖‖':'Vmatrix'};
  // MathJax emits a brace as an ordinary munder/mover, often without an
  // accent attribute, and wraps it in an mrow before adding its label.
  const braceGlyph = (n, glyph) => n?.localName === 'mo' && n.textContent.trim() === glyph;
  function braceBase(n, direction, glyph) {
    if (!n) return 0;
    if (['mrow', 'mstyle', 'mpadded', 'semantics'].includes(n.localName)) {
      const children = [...n.children].filter(child => !['annotation', 'annotation-xml'].includes(child.localName));
      return children.length === 1 ? braceBase(children[0], direction, glyph) : 0;
    }
    if (n.localName !== direction) return 0;
    if (braceGlyph(n.children[1], glyph)) return 1;
    return braceBase(n.children[0], direction, glyph) ? 2 : 0;
  }
  function braceLabel(n, cs, direction, glyph, command, script, stack) {
    const base = braceBase(n.children[0], direction, glyph);
    if (!base) return null;
    // Grouping the brace before its script would put the label at the right.
    // Stack instead if a style wrapper or another label needs its own scope.
    return base === 1 && cs[0].startsWith(command + '{') ? cs[0] + script + '{' + cs[1] + '}' :
      stack + '{' + cs[1] + '}{' + cs[0] + '}';
  }
  function hatAccent(n, cs) {
    const accent = n.children[1];
    if (accent?.localName !== 'mo' || accent.textContent.trim() !== '^') return null;
    const unsupported = ['mathcolor', 'mathbackground', 'mathvariant', 'style', 'minsize', 'maxsize', 'lspace', 'rspace']
      .filter(attribute => accent.hasAttribute(attribute) && !['', 'inherit', 'none', 'transparent'].includes(accent.getAttribute(attribute)));
    if (n.getAttribute('accent') === 'false') unsupported.push('accent=false');
    const stretchy = accent.getAttribute('stretchy');
    if (stretchy !== null && !['true', 'false'].includes(stretchy)) unsupported.push('stretchy=' + stretchy);
    const base = n.children[0], variants = [base, ...base.querySelectorAll('[mathvariant]')].filter(node => node.hasAttribute('mathvariant'));
    const fullBase = new Set();
    for (let node = base; node; ) {
      fullBase.add(node);
      node = ['mrow', 'mstyle', 'mpadded', 'semantics'].includes(node.localName) && node.children.length === 1 ? node.children[0] : null;
    }
    const variantCommands = {'bold-italic':'\\mathbfit', 'bold':'\\mathbf', 'normal':'\\mathrm', 'italic':'\\mathit'};
    let body = cs[0];
    if (variants.length) {
      const variant = variants[0].getAttribute('mathvariant');
      if (variants.length !== 1 || !fullBase.has(variants[0]) || !variantCommands[variant]) unsupported.push('base mathvariant');
      else {
        // Greek command macros fix their own font in MathJax. Keep the source
        // glyph literal when applying its explicit bold/italic variant.
        const glyph = variants[0].textContent, macro = greek[glyph];
        body = variantCommands[variant] + '{' + (macro ? body.replace(macro, glyph) : body) + '}';
      }
    }
    if (unsupported.length) {
      // Styling the semantic hat would also style its base; retain the source
      // serialization and require review for unsupported operator-only cues.
      errors.push('Unsupported MathML hat: ' + unsupported.join(', '));
      return '\\overset{' + cs[1] + '}{' + cs[0] + '}';
    }
    // MathJax's hat sets stretchy=false; widehat uses the operator default.
    return (stretchy === 'false' ? '\\hat{' : '\\widehat{') + body + '}';
  }
  function fence(n) {
    if (n?.localName === 'mo') return n.textContent;
    if (['msup', 'msub', 'msubsup'].includes(n?.localName) && n.children[0]?.localName === 'mo') return n.children[0].textContent;
    return null;
  }
  function m(n, environment=null) {
    let value = mathNode(n, environment);
    if (n.nodeType !== 1 || !value) return value;
    // These attributes carry instructional cues, including highlighted entries.
    // Scope colors to their own node so later cells do not inherit them.
    for (const attribute of ['mathcolor', 'mathbackground']) {
      const color = n.getAttribute(attribute);
      if (!color || ['transparent', 'inherit', 'none'].includes(color)) continue;
      if (!/^(?:[a-zA-Z]+|#[\da-fA-F]{3}(?:[\da-fA-F]{3})?)$/.test(color)) {
        errors.push('Unsupported MathML ' + attribute + ': ' + color);
        continue;
      }
      if (attribute === 'mathbackground') value = '\\bbox[' + color + ', 2pt]{' + value + '}';
      else if (color.startsWith('#')) {
        const hex = color.length === 4 ? [...color.slice(1)].map(c => c + c).join('') : color.slice(1);
        value = '{\\color[HTML]{' + hex + '}' + value + '}';
      } else value = '{\\color{' + color + '}' + value + '}';
    }
    return value;
  }
  // A system often arrives as one MathML cell per equation. Split only a
  // top-level equals sign, keeping fractions, text and nested formulas intact.
  function equationColumns(value) {
    let depth = 0;
    for (let i = 0; i < value.length; i++) {
      if (value[i] === '\\') { i++; continue; }
      if (value[i] === '{') depth++;
      else if (value[i] === '}') depth--;
      else if (!depth && value[i] === '=') return value.slice(0, i).trim() + ' &=' + value.slice(i + 1).trim();
    }
    return null;
  }
  function mathNode(n, environment=null) {
    if (n.nodeType === 3) return greek[n.textContent] || n.textContent;
    if (n.nodeType !== 1) return '';
    const t = n.localName.toLowerCase();
    // The site's rendered math embeds select controls in place of local S-index
    // markers. The assistive MathML still contains the unselected sample value.
    // Bind only markers with a matching observed control in this formula.
    const marker = t === 'mrow' && n.children.length === 3 &&
      n.children[0].textContent === '{' && n.children[2].textContent === '}' &&
      n.children[1].localName === 'msub' && n.children[1].children[1]?.textContent.match(/^\(S(\d+)\)$/);
    if (marker && formulaFields.has(marker[1])) return '{{' + formulaFields.get(marker[1]) + '}}';
    // Phantom content only reserves space; none of its descendants are visible.
    if (t === 'mphantom') return '';
    const nodes = [...n.childNodes].filter(child => child.nodeType !== 3 || child.textContent.trim());
    const cs = [];
    for (let i = 0; i < nodes.length; i++) {
      const open = ['math', 'mrow', 'mtd', 'mstyle', 'mpadded'].includes(t) ? fence(nodes[i]) : null;
      const close = fence(nodes[i + 2]);
      const matrixEnvironment = open && close && matrixEnvironments[open + close];
      // Invisible right delimiters are sometimes omitted from archived MathML.
      const cases = open === '{' && (close === '' || !nodes[i + 2]) && nodes[i + 1]?.localName === 'mtable';
      if (nodes[i].localName === 'mo' && (matrixEnvironment && matrixTable(nodes[i + 1]) || cases)) {
        let matrix = m(nodes[i + 1], cases ? 'cases' : matrixEnvironment);
        const closing = nodes[i + 2];
        if (closing && closing.localName !== 'mo') {
          matrix = '{' + matrix + '}';
          if (closing.localName !== 'msup') matrix += '_{' + m(closing.children[1]) + '}';
          if (closing.localName !== 'msub') matrix += '^{' + m(closing.children[closing.localName === 'msubsup' ? 2 : 1]) + '}';
        }
        cs.push(matrix);
        i += 2;
      } else cs.push(m(nodes[i], environment && matrixTable(n) ? environment : null));
    }
    // MathJax may attach a script to just the closing fence glyph. Wrapping
    // that glyph in braces obscures the fence boundary in extracted LaTeX.
    const scriptBase = [')',']','}'].includes(cs[0]) ? cs[0] : '{' + cs[0] + '}';
    if (t === 'munder' && braceGlyph(n.children[1], '⏟') || t === 'mover' && braceGlyph(n.children[1], '⏞')) {
      const accent = n.children[1];
      const styling = ['mathcolor', 'mathbackground'].filter(attribute => {
        const value = accent.getAttribute(attribute);
        return value && !['transparent', 'inherit', 'none'].includes(value);
      });
      if (styling.length) {
        // Coloring the whole underbrace/overbrace would also recolor its base.
        // Keep the source cue, and require review instead of silently dropping
        // operator-only styling that the semantic brace macro cannot express.
        errors.push('Unsupported styled MathML brace: ' + styling.join(', '));
        return t === 'munder' ? '{' + cs[0] + '}_{' + cs[1] + '}' : '\\overset{' + cs[1] + '}{' + cs[0] + '}';
      }
    }
    switch(t) {
      case 'mfrac':
        // A zero-rule fraction is a stack, not division. Keep the source's rule.
        return /^0(?:\.0+)?(?:[a-z%]+)?$/i.test(n.getAttribute('linethickness') || '') ?
          '\\genfrac{}{}{0pt}{}{' + cs[0] + '}{' + cs[1] + '}' :
          '\\frac{' + cs[0] + '}{' + cs[1] + '}';
      case 'msup': return scriptBase + '^{' + cs[1] + '}';
      case 'msub': return scriptBase + '_{' + cs[1] + '}';
      case 'msubsup': return scriptBase + '_{' + cs[1] + '}^{' + cs[2] + '}';
      case 'munder': return braceGlyph(n.children[1], '⏟') ? '\\underbrace{' + cs[0] + '}' :
        braceLabel(n, cs, 'munder', '⏟', '\\underbrace', '_', '\\underset') ?? '{' + cs[0] + '}_{' + cs[1] + '}';
      case 'mover': return braceGlyph(n.children[1], '⏞') ? '\\overbrace{' + cs[0] + '}' :
        braceLabel(n, cs, 'mover', '⏞', '\\overbrace', '^', '\\overset') ?? hatAccent(n, cs) ?? (n.children[1]?.textContent === 'ˆ' ?
          '\\hat{' + cs[0] + '}' : '\\overset{' + cs[1] + '}{' + cs[0] + '}');
      case 'munderover': return '{' + cs[0] + '}_{' + cs[1] + '}^{' + cs[2] + '}';
      case 'msqrt': return '\\sqrt{' + cs.join('') + '}';
      case 'mroot': return '\\sqrt[' + cs[1] + ']{' + cs[0] + '}';
      case 'mspace': return '\\,';
      case 'mtext': return '\\text{' + literalMathGlyph(n.textContent) + '}';
      case 'mo': return ops[n.textContent] || greek[n.textContent] || literalMathGlyph(n.textContent);
      case 'mi':
        // The local MathML application marker identifies this whole node as
        // a function name. Keep its boundary when adjacent factors share no space.
        if (/^[A-Za-z]+$/.test(n.textContent) &&
            n.nextElementSibling?.localName === 'mo' && n.nextElementSibling.textContent === '\u2061') {
          return '\\operatorname{' + n.textContent + '}';
        }
        // A literal percent can be an identifier token in captured MathML.
        // Emit TeX content rather than a comment opener.
        return greek[n.textContent] || literalMathGlyph(n.textContent);
      case 'mtable': {
        if (!environment && nodes.length === 1 && nodes[0].children.length === 1 &&
            cs[0].startsWith('\\left\\{\\begin{aligned}')) return cs[0];
        if (environment === 'cases') {
          const equations = nodes.map(row => {
            const cells = [...row.children].map(cell => m(cell).trim());
            while (cells.length > 1 && !cells[0]) cells.shift();
            if (cells.length === 1) return equationColumns(cells[0]);
            if (cells.length === 2 && cells[1].startsWith('=')) return cells[0] + ' &' + cells[1];
            if (cells.length === 2 && cells[0].endsWith('=')) return cells[0].slice(0, -1).trim() + ' &=' + cells[1];
            if (cells.length === 3 && cells[1] === '=') return cells[0] + ' &=' + cells[2];
            if (cells.length === 2 && equationColumns(cells[0])) return equationColumns(cells[0]) + ' && ' + cells[1];
            return null;
          });
          if (equations.every(Boolean)) return '\\left\\{\\begin{aligned}' + equations.join(' \\\\ ') + '\\end{aligned}\\right.';
        }
        const centered = matrixTable(n) !== null;
        let columnCount = Math.max(...nodes.map(row => row.children.length));
        if (centered && (environment || n.getAttribute('columnalign')) &&
            !['columnlines', 'rowlines', 'frame'].some(attribute => (n.getAttribute(attribute) || 'none').split(/\s+/).some(value => value && value !== 'none'))) {
          const shortest = Math.min(...nodes.map(row => row.children.length));
          if (shortest !== columnCount) {
            // A saved rotation matrix has an accidental empty cell at the end
            // of its first row. Trim only empty extras; never drop an entry.
            if (nodes.every(row => [...row.children].slice(shortest).every(cell => m(cell) === ''))) {
              for (let i = 0; i < nodes.length; i++) cs[i] = [...nodes[i].children].slice(0, shortest).map(cell => m(cell)).join(' & ');
              columnCount = shortest;
            } else errors.push('Ragged MathML matrix');
          }
        }
        const values = attribute => (n.getAttribute(attribute) || 'none').trim().split(/\s+/);
        const columnlines = values('columnlines'), rowlines = values('rowlines'), frame = n.getAttribute('frame') || 'none';
        if ([...columnlines, ...rowlines, frame].some(value => value && value !== 'none')) {
          for (const attribute of ['columnlines', 'rowlines', 'frame']) {
            if (values(attribute).some(value => !['none', 'solid'].includes(value))) errors.push('Unsupported MathML table ' + attribute);
          }
          const width = columnCount;
          const at = (items, index) => items[Math.min(index, items.length - 1)];
          let columns = frame === 'solid' ? '|' : '';
          const alignment = (n.getAttribute('columnalign') || 'center').trim().split(/\s+/);
          if (alignment.some(value => !['left', 'center', 'right'].includes(value))) errors.push('Unsupported MathML table columnalign');
          for (let i = 0; i < width; i++) columns += ({left:'l', center:'c', right:'r'}[at(alignment, i)] || 'c') + (i < width - 1 && at(columnlines, i) === 'solid' || i === width - 1 && frame === 'solid' ? '|' : '');
          let body = frame === 'solid' ? '\\hline ' : '';
          for (let i = 0; i < cs.length; i++) {
            body += cs[i];
            if (i < cs.length - 1) body += ' \\\\ ' + (at(rowlines, i) === 'solid' ? '\\hline ' : '');
          }
          if (frame === 'solid') body += ' \\\\ \\hline';
          const array = '\\begin{array}{' + columns + '}' + body + '\\end{array}';
          const fences = {bmatrix:['[',']'], pmatrix:['(',')'], Bmatrix:['\\{','\\}'], vmatrix:['|','|'], Vmatrix:['\\Vert','\\Vert']}[environment];
          return fences ? '\\left' + fences[0] + array + '\\right' + fences[1] : array;
        }
        const layout = environment || (centered && n.getAttribute('columnalign') ? 'matrix' : 'aligned');
        return '\\begin{' + layout + '}' + cs.join(' \\\\ ') + '\\end{' + layout + '}';
      }
      case 'mtr': case 'mlabeledtr': return cs.join(' & ');
      case 'menclose':
        // The two borders group the synthetic-division root; retain both.
        if (n.getAttribute('notation') === 'bottom right') return '\\enclose{bottom right}{' + cs.join('') + '}';
        if (n.getAttribute('notation') === null || n.getAttribute('notation') === 'longdiv') return '\\enclose{longdiv}{' + cs.join('') + '}';
        if (n.getAttribute('notation') === 'left right') return '\\left|' + cs.join('') + '\\right|';
        if (n.getAttribute('notation') === 'right') return '\\left.' + cs.join('') + '\\right|';
        if (n.getAttribute('notation') === 'box') return '\\boxed{' + cs.join('') + '}';
        if (n.getAttribute('notation')?.includes('strike')) return '\\cancel{' + cs.join('') + '}';
        errors.push('Unsupported MathML enclosure'); return cs.join('');
      case 'mfenced': {
        const open = n.getAttribute('open') ?? '(', close = n.getAttribute('close') ?? ')';
        const layout = matrixEnvironments[open + close];
        if (layout && nodes.length === 1 && matrixTable(nodes[0])) return m(nodes[0], layout);
        return open + cs.join(n.getAttribute('separators') ?? ',') + close;
      }
      case 'semantics': return cs[0] || '';
      case 'annotation': case 'annotation-xml': return '';
      case 'math': case 'mrow': case 'mn': case 'mtd': case 'mstyle': case 'mpadded': return cs.join('');
      default: errors.push('Unsupported MathML node: ' + t); return cs.join('');
    }
  }
  function render(n) {
    if (!n) return '';
    if (n.nodeType === 3) return n.parentElement?.closest('pre,code,textarea') ? n.textContent :
      n.textContent.replace(/[ \t]*(?:\r?\n|\r)[ \t]*/g, '\n');
    if (n.nodeType !== 1) return '';
    const t = n.localName.toLowerCase();
    if (emptyFormula(n)) return '';
    if (['script','style','mjx-assistive-mml'].includes(t)) return '';
    if (n.matches('.studentAnswer, .studentAnswerHeader')) return '';
    if (fieldNodes.has(n)) return '{{' + fieldNodes.get(n) + '}}';
    if (assets.includes(n)) return '![](@asset-' + assets.indexOf(n) + '@)';
    if (t === 'svg' && n.closest('.mjpage, mjx-container, .MathJax')) {
      const title = n.querySelector('title');
      const recovered = recoverableTitle(n);
      const math = recovered?.math || title?.querySelector('mjx-assistive-mml math, math');
      const tex = math ? m(math, recovered?.environment) : legacyMatrixTex(title?.textContent?.trim() || '');
      if (!tex) errors.push('SVG formula has no local title or MathML');
      return n.closest('.mjpage__block') ? '\n\n$$\n' + (tex || '') + '\n$$\n\n' : '$' + (tex || '') + '$';
    }
    if (t === 'mjx-container' || t === 'math') {
      if (t === 'mjx-container' && mixedTitle(n.querySelector('svg')) &&
          assets.includes(n.querySelector('svg'))) return render(n.querySelector('svg'));
      const math = t === 'math' ? n : [...n.querySelectorAll('mjx-assistive-mml math')]
        .find(math => math.closest('.selectList') === n.closest('.selectList'));
      if (!math && emptyFormula(n.querySelector('svg'))) return '';
      if (!math && assets.includes(n.querySelector('svg'))) return render(n.querySelector('svg'));
      if (!math) { errors.push('MathJax formula has no assistive MathML'); return ''; }
      const previous = formulaFields;
      formulaFields = new Map([...fieldNodes].filter(([control]) => n.contains(control))
        .map(([control,key]) => [control.id.match(/-(\d+)$/)?.[1], key]));
      const tex = m(math);
      formulaFields = previous;
      return n.getAttribute('display') === 'true' ? '\n\n$$\n' + tex + '\n$$\n\n' : '$' + tex + '$';
    }
    if (t === 'table') return sourceHTMLTable(n, render, message => errors.push(message));
    const children = [...n.childNodes].map(render).join('');
    if (t === 'br') return '\n';
    if (t === 'li') return '- ' + children.trim() + '\n';
    if (t === 'b' || t === 'strong') return '**' + children + '**';
    if (t === 'i' || t === 'em') return '*' + children + '*';
    if (['p','div','ul','ol'].includes(t)) return '\n\n' + children + '\n\n';
    return children;
  }
  const text = n => render(n).replace(/\n{3,}/g,'\n\n').trim();
  function choice(n, option, dom_id=null) {
    const value = text(n);
    const mathOnly = /^\$[^$]+\$$/.test(value);
    const imageOnly = /^!\[\]\(@asset-\d+@\)$/.test(value);
    return {option, dom_id, type:mathOnly?'math':imageOnly?'image':'text',
      value:mathOnly?value.slice(1,-1):imageOnly?value.slice(4,-1):value, html:n.innerHTML};
  }
  if (rows.length) fields[0].choices = rows.map(row => {
    const circle = row.querySelector('.questionWidget-choiceLetterCircle, [id^="questionWidget-choiceLetterCircle-"], .choiceLetterCircle');
    if (!circle?.id) errors.push('Choice circle has no observed ID');
    return choice(row.querySelector('.questionWidget-choiceText, .choiceText'), circle?.textContent.trim(), circle?.id);
  });
  for (const [node,key] of fieldNodes) {
    const f = fields.find(f => f.key === key);
    if (f.type === 'select') f.choices = [...node.querySelectorAll('option, .selectListOptions > .selectListOption')]
      .filter(n => n.textContent.trim() && !(n.localName === 'option' && n.disabled))
      .map((n,i) => choice(n, n.localName === 'option' ? n.value : String(i), n.id || null));
  }
  for (const field of fields) {
    field.choices_complete = ['radio','select'].includes(field.type) && field.choices.length > 0 && errors.length === 0;
    if (field.tag === 'custom-select') {
      const frame = [...fieldNodes].find(([,key]) => key === field.key)?.[0]
        .querySelector('.selectListFrame, .selectListFrameDisabled');
      if (frame && !frame.querySelector('.selectListSelectedText')) {
        const selected = choice(frame, null);
        field.source_selected = {type:selected.type, value:selected.value};
      }
      if (frame?.matches('.correctSelection, .correctSelectionMultipleAttempts, .incorrectSelection')) {
        field.source_result = frame.matches('.incorrectSelection') ? 'Incorrect' : 'Correct';
        if (field.source_result === 'Correct') field.source_correct = field.source_selected;
      }
    }
  }
  const prompt = element.querySelector('.exampleQuestion, .questionWidget-text, .questionText') ||
    (element.matches('#steps > .step:not(:has(.question))') ? element : null);
  const graphic = element.querySelector('.questionWidget-graphic, #questionGraphic, .questionGraphicFrame');
  const instructions = element.querySelector('.questionWidget-calculatorInstructions, .calculatorInstructions');
  const solution = element.matches('.questionExplanation') ? element : element.querySelector('.exampleExplanation, .questionWidget-explanation, .questionExplanation');
  return {dom_id:element.id, name:element.querySelector('.stepName,.questionWidget-title')?.textContent.trim(),
    problem:[text(graphic),text(prompt)].filter(Boolean).join('\n\n'), worked_solution:text(solution),
    calculator_instructions:text(instructions), fields,
    result:element.querySelector('.questionWidget-result, .correctAnswerText, .incorrectAnswerText')?.textContent.trim(),
    proof_feedback:element.querySelector('.questionWidget-feedback')?.textContent.trim(),
    html:element.outerHTML, errors:[...new Set(errors)],
    assets:assets.map((n,index) => ({index, tag:n.localName, html:n.outerHTML,
      source_url:n.localName==='img' ? n.currentSrc || n.src : null}))};
}
