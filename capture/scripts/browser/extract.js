// Pure DOM extraction. No application state, answer keys, or network calls.
(element, context = {}) => {
function sourceHTMLTable(table, renderLeaf, reportError) {
  const esc=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]);
  const safeText=value=>{const math=[];let prefix='CATABLETEXT';while(String(value).includes(prefix))prefix+='X';let text=String(value).replace(/\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\[\s\S]|[^$\\])*?(?<!\\)\$/g,m=>{math.push(m);return prefix+(math.length-1)+'END'});return esc(text).replace(new RegExp(prefix+'(\\d+)END','g'),(_,i)=>math[Number(i)])};
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
      if(!['','0'].includes(node.getAttribute('border')||'0')||s.border&&!/^(?:none|0(?:px)?)(?:\s|$)/.test(s.border))put('data-frame','true');
    }else if(tag==='tr'&&!lastRows.has(node))put('data-next-row','true');
    for(const k of ['rowspan','colspan','span'])if(node.hasAttribute(k)){const v=node.getAttribute(k);if(!/^\d{1,3}$/.test(v)||Number(v)===0&&k!=='rowspan')reportError('Unsupported table span: '+k+'='+v);else put(k,v)}
    if(tag==='th'&&['row','col','rowgroup','colgroup'].includes(node.getAttribute('scope')))put('scope',node.getAttribute('scope'));
    const ancestors=[node];if(['td','th'].includes(tag))for(let p=node.parentElement;p;p=p.parentElement){ancestors.push(p);if(p.localName==='table')break}
    for(const p of ancestors){const value=(p.localName==='table'?null:align(p.getAttribute('align')))||align(props(p)['text-align']);if(value){put('data-cell-align',value);break}}
    const fill=color(node.getAttribute('bgcolor')||s['background-color']||s.background);if(fill)put('data-fill',fill);
    if(['td','th'].includes(tag))for(const side of ['top','right','bottom','left']){const value=s['border-'+side]??s.border;if(value!==undefined)put('data-border-'+side,/^(?:none|0(?:px)?)(?:\s|$)/.test(value)?'none':'solid')}
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

  context ||= {};
  const errors = [], errorParts = {};
  let part = 'fields';
  const fail = message => {
    errors.push(message);
    errorParts[message] = [...new Set([...(errorParts[message] || []), part])];
  };
  const readPart = (name, read) => {
    const previous = part;
    part = name;
    try { return read(); } finally { part = previous; }
  };
  const emptyFormula = n => {
    if(n?.localName !== 'svg' || !n.closest('.mjpage, mjx-container, .MathJax') ||
       n.textContent.trim() || n.querySelector('path,use,text,line,polyline,polygon,circle,ellipse,rect,image,foreignObject')) return false;
    const box=n.getAttribute('viewBox')?.trim();
    if(n.getAttribute('width') === '0' && box?.split(/\s+/)[2] === '0') return true;
    // MathJax SVG also represents a completed empty formula with its minimum
    // 16-unit box. Require its exact dimensions and empty math root; an empty
    // arbitrary SVG or a formula still containing source nodes remains a gap.
    const root=n.querySelector('g[data-mml-node="math"]');
    return !!n.closest('mjx-container[jax="SVG"]') && box === '0 0 16 16' &&
      n.getAttribute('width') === '0.036ex' && n.getAttribute('height') === '0.036ex' &&
      !!root && !root.childNodes.length;
  };
  // MathJax can render part of an SVG's TeX title again as nested MathML.
  // That MathML describes only the inner fragment (e.g. phantom spacing),
  // not the surrounding visible fbox. Preserve the whole rendered formula.
  const mixedTitle = n => {
    const title = n?.querySelector('title');
    return title?.querySelector('math') && [...title.childNodes].some(child =>
      child.nodeType === 3 && child.textContent.trim());
  };
  // Some archived source titles contain MA's internal currency placeholder,
  // while the SVG visibly renders the dollar glyph correctly. Retain that
  // original graphic rather than treating its broken title as usable TeX.
  const currencyTitle = n => /\\\[\/?math\]/.test(n?.querySelector('title')?.textContent || '');
  const assets = [...element.querySelectorAll('img, canvas, svg')].filter(n => {
    if (emptyFormula(n)) return false;
    if (n.closest('.questionWidget-header, .questionWidget-result, .stepHeader, .spinnerFrame, .answer') ||
        n.parentElement?.closest('svg')) return false;
    const formula = n.closest('.mjpage, mjx-container, .MathJax');
    if (!formula) return true;
    if (n.localName === 'svg' && (mixedTitle(n) || currencyTitle(n))) return true;
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
  // History renders blank responses as static boxes, with the overall grade
  // outside this question node. Keep the observed answer position as a field
  // instead of folding its displayed value into the source problem.
  const historyQuestion = element.matches('.question[id^="question-"]');
  const terminalGrades = ['Correct','Incorrect','Full Credit','Partial Credit','No Credit','Skipped Question'];
  const finalResult = element.querySelector('.questionWidget-result,.correctAnswerText,.incorrectAnswerText')?.textContent.trim()
    || (historyQuestion ? context.history_grade : null);
  const nodes = [...element.querySelectorAll('.matheditor-wrapper-answer, .selectList, input:not([type="hidden"]), textarea, select, [contenteditable="true"]' +
    (historyQuestion || ['Correct','Incorrect','Skipped Question'].includes(element.querySelector('.questionWidget-result')?.textContent.trim()) ? ', .freeResponseTextbox' : ''))]
    .filter(n => !n.closest('.questionWidget-explanation, .exampleExplanation, .questionExplanation, .studentAnswer, .studentAnswerHeader') &&
      !n.parentElement?.closest('.matheditor-wrapper-answer, .selectList, .freeResponseTextbox, [contenteditable="true"]'));
  for (const n of nodes) {
    const key = 'field-' + (fields.filter(f => f.key !== 'selection').length + 1);
    let type = n.matches('.selectList, select') ? 'select' : 'blank';
    const f = {key, type, dom_id:n.id, tag:n.tagName.toLowerCase(), choices:[],
      dom_index:nodes.indexOf(n), disabled:!!n.disabled};
    if (n.matches('.matheditor-wrapper-answer')) {
      f.tag = 'mathquill';
      f.dom_index = [...element.querySelectorAll('.matheditor-wrapper-answer')].indexOf(n);
      f.input_html = n.outerHTML;
      f.rendered_text = n.querySelector('.mq-root-block')?.textContent || '';
      if (!n.querySelector('.mq-editable-field .mq-textarea textarea')) fail('Unsupported math editor: ' + n.id);
    } else if (n.matches('.selectList')) {
      f.tag = 'custom-select';
      const graded = terminalGrades.includes(finalResult);
      const frame = n.querySelector('.selectListFrame') || n.querySelector(
        graded ? '.selectListFrameDisabled' : '.selectListFrameDisabled.correctSelection, .selectListFrameDisabled.correctSelectionMultipleAttempts');
      f.frame_id = frame?.id;
      if (historyQuestion && frame?.matches('.selectListFrameDisabled')) f.disabled = true;
      if (!f.frame_id) fail('Select frame has no ID: ' + n.id);
    } else if (n.matches('.freeResponseTextbox')) {
      f.disabled = true;
      f.input_html = n.outerHTML;
      f.rendered_text = n.textContent.trim();
      f.readonly_history = historyQuestion;
    } else if (n.matches('input') && !['text','number',''].includes(n.getAttribute('type') || '')) {
      fail('Unsupported input type: ' + n.getAttribute('type'));
    }
    fields.push(f); fieldNodes.set(n, key);
  }
  const greek = {'α':'\\alpha ','β':'\\beta ','γ':'\\gamma ','δ':'\\delta ','θ':'\\theta ','λ':'\\lambda ','μ':'\\mu ','π':'\\pi ','ρ':'\\rho ','σ':'\\sigma ','φ':'\\phi ','ω':'\\omega ','∞':'\\infty '};
  const ops = {'∫':'\\int ','∑':'\\sum ','∏':'\\prod ','⋅':'\\cdot ','×':'\\times ','−':'-', '±':'\\pm ','≤':'\\le ','≥':'\\ge ','≠':'\\ne ','→':'\\to ','∈':'\\in ','∉':'\\notin ','∪':'\\cup ','∩':'\\cap '};
  // Literal MathML brace glyphs are delimiters, not TeX grouping syntax.
  const literalFence = value => value === '{' ? '\\{' : value === '}' ? '\\}' : value;
  // A currency glyph inside MathML is content, not a TeX math delimiter.
  const literalDollar = value => value.replace(/[$%#]/g, glyph => '\\' + glyph);
  let formulaFields = new Map();
  const mathColor = value => /^(?:[a-z]+|#[0-9a-f]{3}|#[0-9a-f]{6})$/i.test(value || '') &&
    !/^(?:inherit|initial|unset|revert|revertlayer|currentcolor)$/i.test(value) && CSS.supports('color', value);
  const metadataAttribute = name => name.startsWith('data-mjx-');
  function decoratedPhantom(n) {
    // Only explicit source decoration makes an otherwise invisible phantom
    // relevant. Do not turn unstyled spacing samples into visible answers.
    if (!n.querySelector('mphantom') || !['mstyle','mpadded'].includes(n.localName)) return null;
    const background = n.getAttribute('mathbackground');
    const style = n.getAttribute('style');
    if (background === null && style === null) return null;
    const reject = reason => { fail('Unsupported decorated MathML phantom: ' + reason); return ''; };
    if (n.localName !== 'mstyle' || [...n.attributes].some(a => !['mathbackground','style'].includes(a.name) && !metadataAttribute(a.name)))
      return reject('container attributes');
    let border = style?.trim().replace(/;$/, '').trim();
    if (background !== null && !mathColor(background)) return reject('background');
    if (style !== null) {
      // MathJax emits both "1pt solid black" and "solid black 1pt".
      // CSS shorthand order changes no geometry; reject any extra declaration.
      const match = /^border:\s*([^:;]+)$/i.exec(border);
      const tokens = match?.[1].trim().split(/\s+/) || [];
      const widths = tokens.filter(t => /^\d+(?:pt|px|em|ex|in|cm|mm)$/i.test(t));
      const colors = tokens.filter(t => mathColor(t));
      if (![2,3].includes(tokens.length) || widths.length !== 1 || colors.length !== tokens.length-2 ||
          tokens.filter(t => t.toLowerCase()==='solid').length !== 1) return reject('border style');
      border = 'border:' + widths[0] + ' solid' + (colors.length ? ' ' + colors[0] : '');
    }
    const padded = n.children.length === 1 && n.children[0];
    // A bbox with only a background has no padding node. Preserve its exact
    // hidden width rather than requiring the separate padded-bbox form.
    if (background !== null && style === null && padded?.localName === 'mrow' &&
        [...padded.attributes].every(a => metadataAttribute(a.name)))
      return '\\bbox[' + background + ']{' + [...padded.childNodes].map(child => m(child, true)).join('') + '}';
    if (!padded || padded.localName !== 'mpadded' || [...padded.attributes].some(a => !['height','depth','lspace','width'].includes(a.name) && !metadataAttribute(a.name)))
      return reject('padding container');
    // MathJax 3.2.2 bbox doubles padding with parseInt. Decimal padding would
    // silently alter the source width, so only exact integer dimensions bind.
    const pad = /^(\d+)(pt|px|em|ex|in|cm|mm)$/.exec(padded.getAttribute('lspace') || '');
    if (!pad || Number(pad[1]) <= 0 || padded.getAttribute('height') !== '+' + pad[0] || padded.getAttribute('depth') !== '+' + pad[0] ||
        padded.getAttribute('width') !== '+' + (2 * Number(pad[1])) + pad[2]) return reject('asymmetric or unsupported padding');
    const options = [pad[0]];
    if (background !== null) options.push(background);
    if (style !== null) options.push(border);
    return '\\bbox[' + options.join(',') + ']{' + [...padded.childNodes].map(child => m(child, true)).join('') + '}';
  }
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
      fail('Unsupported MathML hat: ' + unsupported.join(', '));
      return '\\overset{' + cs[1] + '}{' + cs[0] + '}';
    }
    // MathJax's hat sets stretchy=false; widehat uses the operator default.
    return (stretchy === 'false' ? '\\hat{' : '\\widehat{') + body + '}';
  }
  function m(n, preservePhantom = false) {
    if (n.nodeType === 3) return greek[n.textContent] || literalDollar(n.textContent);
    if (n.nodeType !== 1) return '';
    const t = n.localName.toLowerCase();
    // The site's rendered math embeds select controls in place of local S-index
    // markers. The assistive MathML still contains the unselected sample value.
    // Bind only markers with a matching observed control in this formula.
    const marker = t === 'mrow' && n.children.length === 3 &&
      n.children[0].textContent === '{' && n.children[2].textContent === '}' &&
      n.children[1].localName === 'msub' && n.children[1].children[1]?.textContent.match(/^\(S(\d+)\)$/);
    if (marker && formulaFields.has(marker[1])) return '{{' + formulaFields.get(marker[1]) + '}}';
    const decorated = decoratedPhantom(n);
    if (decorated !== null) return decorated;
    // A verified visible enclosure also depends on this hidden width. Bare
    // phantom samples elsewhere retain the previous source extraction behavior.
    const enclosure = t === 'menclose' && n.querySelector('mphantom') &&
      (n.getAttribute('notation') === null || n.getAttribute('notation') === 'longdiv');
    if (t === 'mphantom' && !preservePhantom) return '';
    const cs = [...n.childNodes].map(child => m(child, preservePhantom || enclosure));
    if (preservePhantom && (n.closest('mphantom') || n.querySelector('mphantom'))) {
      if (!['mphantom','mi','mstyle','mrow','mn','mo','msup','msub','msqrt'].includes(t))
        fail('Unsupported decorated MathML phantom: hidden node ' + t);
      const styled = ['mi','mstyle'].includes(t);
      // MathJax emits stretchy="false" for a fixed glyph inside \phantom.
      // TeX's ordinary glyph has that same fixed size. A stretchy operator
      // or any other geometry attribute still requires explicit support.
      const fixedOperator = a => t === 'mo' && a.name === 'stretchy' && a.value === 'false';
      if ([...n.attributes].some(a => !(styled && ['mathcolor','mathvariant'].includes(a.name)) && !fixedOperator(a) && !metadataAttribute(a.name)))
        fail('Unsupported decorated MathML phantom: hidden geometry attributes');
      let content = cs.join('');
      if (n.hasAttribute('mathvariant')) {
        if (n.getAttribute('mathvariant') !== 'bold') fail('Unsupported decorated MathML phantom: hidden mathvariant');
        else content = '\\mathbf{' + content + '}';
      }
      if (n.hasAttribute('mathcolor')) {
        if (!mathColor(n.getAttribute('mathcolor'))) fail('Unsupported decorated MathML phantom: hidden color');
        else content = '\\color{' + n.getAttribute('mathcolor') + '}{' + content + '}';
      }
      if (styled) return content;
    }
    if (t === 'mphantom') return '\\phantom{' + cs.join('') + '}';
    // MathJax may attach a script to just the closing fence glyph. Wrapping
    // that glyph in braces obscures the fence boundary in extracted LaTeX.
    const scriptBase = [')',']','}','\\}'].includes(cs[0]) ? cs[0] : '{' + cs[0] + '}';
    switch(t) {
      case 'mfrac': {
        // A zero-rule fraction is a stack, not division. Keep the source's rule.
        const thickness = n.getAttribute('linethickness')?.trim();
        const length = /^(\+?(?:\d+(?:\.\d*)?|\.\d+))(em|ex|px|in|cm|mm|pt|pc|%)?$/i.exec(thickness || '');
        if (length && Number(length[1]) === 0)
          return '\\genfrac{}{}{0pt}{}{' + cs[0] + '}{' + cs[1] + '}';
        if (thickness && !length && !/^(thin|medium|thick)$/.test(thickness))
          fail('Unsupported MathML fraction line thickness: ' + thickness);
        return '\\frac{' + cs[0] + '}{' + cs[1] + '}';
      }
      case 'msup': return scriptBase + '^{' + cs[1] + '}';
      case 'msub': return scriptBase + '_{' + cs[1] + '}';
      case 'msubsup': return scriptBase + '_{' + cs[1] + '}^{' + cs[2] + '}';
      case 'munder': return braceGlyph(n.children[1], '⏟') ? '\\underbrace{' + cs[0] + '}' :
        braceLabel(n, cs, 'munder', '⏟', '\\underbrace', '_', '\\underset') ?? '{' + cs[0] + '}_{' + cs[1] + '}';
      case 'mover': return braceGlyph(n.children[1], '⏞') ? '\\overbrace{' + cs[0] + '}' :
        braceLabel(n, cs, 'mover', '⏞', '\\overbrace', '^', '\\overset') ?? hatAccent(n, cs) ?? '\\overset{' + cs[1] + '}{' + cs[0] + '}';
      case 'munderover': return '{' + cs[0] + '}_{' + cs[1] + '}^{' + cs[2] + '}';
      case 'msqrt': return '\\sqrt{' + cs.join('') + '}';
      case 'mroot': return '\\sqrt[' + cs[1] + ']{' + cs[0] + '}';
      case 'mspace': return '\\,';
      case 'mtext': return '\\text{' + literalDollar(n.textContent) + '}';
      case 'mo': return ops[n.textContent] || greek[n.textContent] || literalFence(literalDollar(n.textContent));
      case 'mi':
        // The local MathML application marker identifies this whole node as
        // a function name. Keep its boundary when adjacent factors share no space.
        if (/^[A-Za-z]+$/.test(n.textContent) &&
            n.nextElementSibling?.localName === 'mo' && n.nextElementSibling.textContent === '\u2061') {
          return '\\operatorname{' + n.textContent + '}';
        }
        return greek[n.textContent] || literalDollar(n.textContent);
      case 'mtable': {
        const values = attribute => (n.getAttribute(attribute) || 'none').trim().split(/\s+/);
        const columnlines = values('columnlines'), rowlines = values('rowlines'), frame = n.getAttribute('frame') || 'none';
        if ([...columnlines, ...rowlines, frame].some(value => value && value !== 'none')) {
          for (const attribute of ['columnlines', 'rowlines', 'frame']) {
            if (values(attribute).some(value => !['none', 'solid'].includes(value))) fail('Unsupported MathML table ' + attribute);
          }
          const rows = [...n.children].filter(row => row.localName === 'mtr').map(row => [...row.children].map(cell => m(cell)));
          const width = Math.max(0, ...rows.map(row => row.length));
          if (!width) { fail('Empty ruled MathML table'); return ''; }
          const at = (items, index) => items[Math.min(index, items.length - 1)];
          const alignment = (n.getAttribute('columnalign') || 'center').trim().split(/\s+/);
          if (alignment.some(value => !['left', 'center', 'right'].includes(value))) fail('Unsupported MathML table columnalign');
          let columns = frame === 'solid' ? '|' : '';
          for (let i = 0; i < width; i++) columns += ({left:'l', center:'c', right:'r'}[at(alignment, i)] || 'c') +
            (i < width - 1 && at(columnlines, i) === 'solid' || i === width - 1 && frame === 'solid' ? '|' : '');
          let body = frame === 'solid' ? '\\hline ' : '';
          for (let i = 0; i < rows.length; i++) {
            body += [...rows[i], ...Array(width - rows[i].length).fill('')].join(' & ');
            if (i < rows.length - 1) body += ' \\\\ ' + (at(rowlines, i) === 'solid' ? '\\hline ' : '');
          }
          if (frame === 'solid') body += ' \\\\ \\hline';
          return '\\begin{array}{' + columns + '}' + body + '\\end{array}';
        }
        return '\\begin{aligned}' + cs.join(' \\\\ ') + '\\end{aligned}';
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
        fail('Unsupported MathML enclosure'); return cs.join('');
      case 'mfenced': return literalFence(n.getAttribute('open') || '(') + cs.join(n.getAttribute('separators') || ',') + literalFence(n.getAttribute('close') || ')');
      case 'semantics': return cs[0] || '';
      case 'annotation': case 'annotation-xml': return '';
      case 'math': case 'mrow': case 'mn': case 'mtd': case 'mstyle': case 'mpadded': return cs.join('');
      default: fail('Unsupported MathML node: ' + t); return cs.join('');
    }
  }
  function render(n) {
    if (!n) return '';
    // Live proof widgets sometimes concatenate the next prose sentence with
    // the prompt ("below.From"); history separates the same sentences into
    // sections. Normalize that prose boundary; MathML is rendered by m().
    if (n.nodeType === 3) return n.textContent.replace(/([a-z][.!?])(?=[A-Z][a-z]{2,}\b)/g, '$1 ');
    if (n.nodeType !== 1) return '';
    const t = n.localName.toLowerCase();
    if (emptyFormula(n)) return '';
    if (['script','style','mjx-assistive-mml'].includes(t)) return '';
    if (n.matches('.stepHeader,.helpButton,[id^="continueButton-"],[id^="submitButton-"]')) return '';
    if (n.matches('.studentAnswer, .studentAnswerHeader')) return '';
    if (part === 'problem' && n.matches('.questionWidget-explanation,.exampleExplanation,.questionExplanation,.questionWidget-feedback,.questionWidget-result,.questionWidget-header,.questionHeader,.answerDetails,.questionWidget-choicesTable')) return '';
    if (fieldNodes.has(n)) return '{{' + fieldNodes.get(n) + '}}';
    if (assets.includes(n)) return '![](@asset-' + assets.indexOf(n) + '@)';
    if (t === 'svg' && n.closest('.mjpage, mjx-container, .MathJax')) {
      const title = n.querySelector('title');
      const math = title?.querySelector('mjx-assistive-mml math, math');
      const tex = math ? m(math) : title?.textContent?.trim();
      if (!tex) fail('SVG formula has no local title or MathML');
      return n.closest('.mjpage__block') ? '\n\n$$\n' + (tex || '') + '\n$$\n\n' : '$' + (tex || '') + '$';
    }
    if (t === 'mjx-container' || t === 'math') {
      if (t === 'mjx-container' && mixedTitle(n.querySelector('svg')) &&
          assets.includes(n.querySelector('svg'))) return render(n.querySelector('svg'));
      const math = t === 'math' ? n : [...n.querySelectorAll('mjx-assistive-mml math')]
        .find(math => math.closest('.selectList') === n.closest('.selectList'));
      if (!math && emptyFormula(n.querySelector('svg'))) return '';
      if (!math && assets.includes(n.querySelector('svg'))) return render(n.querySelector('svg'));
      if (!math) { fail('MathJax formula has no assistive MathML'); return ''; }
      const previous = formulaFields;
      formulaFields = new Map([...fieldNodes].filter(([control]) => n.contains(control))
        .map(([control,key]) => [control.id.match(/-(\d+)$/)?.[1], key]));
      const tex = m(math);
      formulaFields = previous;
      // Bare phantom spacing has no visible content. Empty inline delimiters
      // would become an unmatched display opener in the saved Markdown.
      if (!tex.trim()) return '';
      return n.getAttribute('display') === 'true' ? '\n\n$$\n' + tex + '\n$$\n\n' : '$' + tex + '$';
    }
    if (t === 'table') return sourceHTMLTable(n, render, fail);
    if (t === 'ol') {
      const items = [...n.children].filter(child => child.localName === 'li');
      const styles = {'1':'decimal', 'I':'upper-roman', 'i':'lower-roman', 'A':'upper-alpha', 'a':'lower-alpha'};
      let style = getComputedStyle(n).listStyleType;
      // Saved question fragments omit app.css. Its authored rule is
      // ol.questionStatements { list-style-type: upper-roman; } (app.css?v=2).
      // Preserve that verified class meaning, not an inferred choice label.
      if (style === 'decimal' && n.matches('ol.questionStatements') && !n.hasAttribute('type') && !n.style.listStyleType) style = 'upper-roman';
      if (!style) style = styles[n.getAttribute('type')] || 'decimal';
      const label = value => {
        if (style === 'none') return '';
        if (['upper-roman','lower-roman'].includes(style) && value > 0 && value < 4000) {
          let roman = '', remaining = value;
          for (const [number, glyph] of [[1000,'M'],[900,'CM'],[500,'D'],[400,'CD'],[100,'C'],[90,'XC'],[50,'L'],[40,'XL'],[10,'X'],[9,'IX'],[5,'V'],[4,'IV'],[1,'I']]) {
            while (remaining >= number) { roman += glyph; remaining -= number; }
          }
          return style === 'lower-roman' ? roman.toLowerCase() : roman;
        }
        if (['upper-alpha','lower-alpha','upper-latin','lower-latin'].includes(style) && value > 0) {
          let alpha = '', remaining = value;
          while (remaining > 0) { remaining--; alpha = String.fromCharCode(65 + remaining % 26) + alpha; remaining = Math.floor(remaining / 26); }
          return style.startsWith('lower') ? alpha.toLowerCase() : alpha;
        }
        if (style === 'decimal-leading-zero') return value >= 0 && value < 10 ? '0' + value : String(value);
        if (['decimal','upper-roman','lower-roman','upper-alpha','lower-alpha','upper-latin','lower-latin'].includes(style)) return String(value);
        fail('Unsupported ordered list style: ' + style);
        return '';
      };
      const step = n.hasAttribute('reversed') ? -1 : 1;
      let ordinal = n.hasAttribute('start') ? n.start : step === -1 ? items.length : 1;
      const lines = [...n.childNodes].map(item => {
        if (item.nodeType !== 1 || item.localName !== 'li') return render(item).trim();
        if (item.hasAttribute('value')) ordinal = item.value;
        const marker = label(ordinal);
        ordinal += step;
        const body = [...item.childNodes].map(render).join('').trim();
        // Escape decimal dots so Markdown cannot silently renumber explicit
        // li[value] resets. Roman/alpha labels are already literal prose.
        const prefix = marker ? marker + (/^-?\d+$/.test(marker) ? '\\.' : '.') + ' ' : '';
        return prefix + body.split('\n').map((line, index) => index && line ? '  ' + line : line).join('\n');
      }).filter(Boolean);
      return '\n\n' + lines.join('\n\n') + '\n\n';
    }
    const children = [...n.childNodes].map(render).join('');
    if (t === 'br') return '\n';
    if (t === 'li') return '- ' + children.trim() + '\n';
    if (t === 'b' || t === 'strong') return '**' + children + '**';
    if (t === 'i' || t === 'em') return '*' + children + '*';
    if (['p','div','ul','ol'].includes(t) || n.matches('.proofSection')) return '\n\n' + children + '\n\n';
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
    if (!circle?.id) fail('Choice circle has no observed ID');
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
    (element.matches('.step:not(:has(.question)):not(:has(.questionWidget-text))') ? element : null);
  const graphic = element.querySelector('.questionWidget-graphic, #questionGraphic, .questionGraphicFrame');
  const instructions = element.querySelector('.questionWidget-calculatorInstructions, .calculatorInstructions');
  const solution = element.matches('.questionExplanation') ? element : element.querySelector('.exampleExplanation, .questionWidget-explanation, .questionExplanation');
  const staged = !!element.querySelector('.proofSection,.questionWidget-healthFrame');
  const fieldErrors = errors.length;
  const candidates = [...new Set([graphic, ...element.querySelectorAll('.exampleQuestion,.questionWidget-text,.questionText,.questionWidget-body,.questionBody'),
    ...(prompt === element ? [element] : [])].filter(Boolean))];
  const sections = candidates.filter(n => !candidates.some(other => other !== n && other.contains(n)));
  const problem = readPart('problem', () => sections.map(text).filter(Boolean).join('\n\n'));
  const problemFieldKeys = [...fieldNodes].filter(([n]) => sections.some(section => section.contains(n))).map(([,key]) => key);
  const proofSectionsComplete = [...element.querySelectorAll('.proofSection')].every(section => {
    // A section may inherit a hidden stage wrapper. Inspect only this question,
    // not the surrounding history accordion whose expansion is handled by UI.
    for (let node = section; node && element.contains(node); node = node.parentElement) {
      const style = getComputedStyle(node);
      if (node.hidden || style.display === 'none' || ['hidden','collapse'].includes(style.visibility)) return false;
      if (node === element) break;
    }
    return true;
  });
  const historyProofComplete = !historyQuestion || (proofSectionsComplete && fields.every(f =>
    f.tag !== 'custom-select' || ['Correct','Incorrect'].includes(f.source_result) ||
      (finalResult === 'No Credit' && f.disabled && f.frame_id && f.choices.length > 1)));
  const workedSolution = readPart('solution', () => text(solution));
  const calculatorInstructions = readPart('problem', () => text(instructions));
  const parts = [];
  if (sections.length || instructions) parts.push('problem');
  if (fields.length) parts.push('fields');
  if (solution) parts.push('solution');
  return {dom_id:element.id, name:element.querySelector('.stepName,.questionWidget-title')?.textContent.trim(),
    problem, worked_solution:workedSolution, calculator_instructions:calculatorInstructions, fields,
    problem_field_keys:problemFieldKeys,
    answer_fields_complete:fields.length ? fieldErrors === 0 && (!staged || (terminalGrades.includes(finalResult) && historyProofComplete)) : null,
    result:element.querySelector('.questionWidget-result, .correctAnswerText, .incorrectAnswerText')?.textContent.trim(),
    proof_feedback:element.querySelector('.questionWidget-feedback')?.textContent.trim(),
    html:element.outerHTML, errors:[...new Set(errors)],
    extraction_parts:parts, extraction_error_parts:errorParts,
    assets:assets.map((n,index) => ({index, tag:n.localName, html:n.outerHTML,
      extraction_part:n.closest('.exampleExplanation,.questionWidget-explanation,.questionExplanation') ? 'solution' :
        n.closest('.questionWidget-choicesTable,.choiceText,.questionWidget-choiceText,.selectList,select') ? 'fields' : 'problem',
      dom_index:[...element.querySelectorAll(n.localName)].indexOf(n),
      source_url:n.localName==='img' ? n.currentSrc || n.src : null}))};
}
