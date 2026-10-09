// Pure DOM extraction. No application state, answer keys, or network calls.
element => {
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
  const assets = [...element.querySelectorAll('img, canvas, svg')].filter(n => {
    if (emptyFormula(n)) return false;
    if (n.closest('.questionWidget-header, .questionWidget-result, .stepHeader, .spinnerFrame, .answer') ||
        n.parentElement?.closest('svg')) return false;
    const formula = n.closest('.mjpage, mjx-container, .MathJax');
    if (!formula) return true;
    if (n.localName === 'svg' && mixedTitle(n)) return true;
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
  let formulaFields = new Map();
  function m(n) {
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
    const cs = [...n.childNodes].map(m);
    // MathJax may attach a script to just the closing fence glyph. Wrapping
    // that glyph in braces obscures the fence boundary in extracted LaTeX.
    const scriptBase = [')',']','}'].includes(cs[0]) ? cs[0] : '{' + cs[0] + '}';
    switch(t) {
      case 'mfrac':
        // A zero-rule fraction is a stack, not division. Keep the source's rule.
        return /^0(?:\.0+)?(?:[a-z%]+)?$/i.test(n.getAttribute('linethickness') || '') ?
          '\\genfrac{}{}{0pt}{}{' + cs[0] + '}{' + cs[1] + '}' :
          '\\frac{' + cs[0] + '}{' + cs[1] + '}';
      case 'msup': return scriptBase + '^{' + cs[1] + '}';
      case 'msub': return scriptBase + '_{' + cs[1] + '}';
      case 'msubsup': return scriptBase + '_{' + cs[1] + '}^{' + cs[2] + '}';
      case 'munder': return '{' + cs[0] + '}_{' + cs[1] + '}';
      case 'mover': return '\\overset{' + cs[1] + '}{' + cs[0] + '}';
      case 'munderover': return '{' + cs[0] + '}_{' + cs[1] + '}^{' + cs[2] + '}';
      case 'msqrt': return '\\sqrt{' + cs.join('') + '}';
      case 'mroot': return '\\sqrt[' + cs[1] + ']{' + cs[0] + '}';
      case 'mspace': return '\\,';
      case 'mtext': return '\\text{' + n.textContent + '}';
      case 'mo': return ops[n.textContent] || greek[n.textContent] || n.textContent;
      case 'mi':
        // The local MathML application marker identifies this whole node as
        // a function name. Keep its boundary when adjacent factors share no space.
        if (/^[A-Za-z]+$/.test(n.textContent) &&
            n.nextElementSibling?.localName === 'mo' && n.nextElementSibling.textContent === '\u2061') {
          return '\\operatorname{' + n.textContent + '}';
        }
        return greek[n.textContent] || n.textContent;
      case 'mtable': return '\\begin{aligned}' + cs.join(' \\\\ ') + '\\end{aligned}';
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
      case 'mfenced': return (n.getAttribute('open') || '(') + cs.join(n.getAttribute('separators') || ',') + (n.getAttribute('close') || ')');
      case 'semantics': return cs[0] || '';
      case 'annotation': case 'annotation-xml': return '';
      case 'math': case 'mrow': case 'mn': case 'mtd': case 'mstyle': case 'mpadded': return cs.join('');
      default: errors.push('Unsupported MathML node: ' + t); return cs.join('');
    }
  }
  function render(n) {
    if (!n) return '';
    if (n.nodeType === 3) return n.textContent;
    if (n.nodeType !== 1) return '';
    const t = n.localName.toLowerCase();
    if (emptyFormula(n)) return '';
    if (['script','style','mjx-assistive-mml'].includes(t)) return '';
    if (n.matches('.studentAnswer, .studentAnswerHeader')) return '';
    if (fieldNodes.has(n)) return '{{' + fieldNodes.get(n) + '}}';
    if (assets.includes(n)) return '![](@asset-' + assets.indexOf(n) + '@)';
    if (t === 'svg' && n.closest('.mjpage, mjx-container, .MathJax')) {
      const title = n.querySelector('title');
      const math = title?.querySelector('mjx-assistive-mml math, math');
      const tex = math ? m(math) : title?.textContent?.trim();
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
    if (t === 'table') {
      const rows = [...n.querySelectorAll('tr')].map(row => [...row.children]
        .filter(c => ['td','th'].includes(c.localName)).map(c => text(c)));
      const width = Math.max(0,...rows.map(r => r.length));
      if (width) {
        const lines = rows.map(row => '| ' + row.concat(Array(width-row.length).fill('')).join(' | ') + ' |');
        lines.splice(1,0,'| ' + Array(width).fill('---').join(' | ') + ' |');
        return '\n\n' + lines.join('\n') + '\n\n';
      }
    }
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
