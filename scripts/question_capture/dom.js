// Pure DOM extraction. No application state, answer keys, or network calls.
element => {
  const errors = [];
  const assets = [...element.querySelectorAll('img, canvas, svg')].filter(n =>
    !n.closest('.mjpage, mjx-container, .MathJax, .questionWidget-header, .questionWidget-result, .stepHeader') &&
    !n.parentElement?.closest('svg'));
  const fields = [], fieldNodes = new Map();
  const rows = [...element.querySelectorAll('.questionWidget-choicesTable tr')];
  if (rows.length) fields.push({key:'selection', type:'radio', choices:[]});
  const nodes = [...element.querySelectorAll('.matheditor-wrapper-answer, .selectList, input:not([type="hidden"]), textarea, select, [contenteditable="true"]')]
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
      f.input_html = n.outerHTML;
      f.rendered_text = n.querySelector('.mq-root-block')?.textContent || '';
      if (!n.querySelector('.mq-editable-field .mq-textarea textarea')) errors.push('Unsupported math editor: ' + n.id);
    } else if (n.matches('.selectList')) {
      f.tag = 'custom-select';
      f.frame_id = n.querySelector('.selectListFrame')?.id;
      if (!f.frame_id) errors.push('Select frame has no ID: ' + n.id);
    } else if (n.matches('input') && !['text','number',''].includes(n.getAttribute('type') || '')) {
      errors.push('Unsupported input type: ' + n.getAttribute('type'));
    }
    fields.push(f); fieldNodes.set(n, key);
  }
  const greek = {'α':'\\alpha ','β':'\\beta ','γ':'\\gamma ','δ':'\\delta ','θ':'\\theta ','λ':'\\lambda ','μ':'\\mu ','π':'\\pi ','ρ':'\\rho ','σ':'\\sigma ','φ':'\\phi ','ω':'\\omega ','∞':'\\infty '};
  const ops = {'∫':'\\int ','∑':'\\sum ','∏':'\\prod ','⋅':'\\cdot ','×':'\\times ','−':'-', '±':'\\pm ','≤':'\\le ','≥':'\\ge ','≠':'\\ne ','→':'\\to ','∈':'\\in ','∉':'\\notin ','∪':'\\cup ','∩':'\\cap '};
  function m(n) {
    if (n.nodeType === 3) return greek[n.textContent] || n.textContent;
    if (n.nodeType !== 1) return '';
    const cs = [...n.childNodes].map(m), t = n.localName.toLowerCase();
    switch(t) {
      case 'mfrac': return '\\frac{' + cs[0] + '}{' + cs[1] + '}';
      case 'msup': return '{' + cs[0] + '}^{' + cs[1] + '}';
      case 'msub': return '{' + cs[0] + '}_{' + cs[1] + '}';
      case 'msubsup': return '{' + cs[0] + '}_{' + cs[1] + '}^{' + cs[2] + '}';
      case 'munder': return '{' + cs[0] + '}_{' + cs[1] + '}';
      case 'mover': return '\\overset{' + cs[1] + '}{' + cs[0] + '}';
      case 'munderover': return '{' + cs[0] + '}_{' + cs[1] + '}^{' + cs[2] + '}';
      case 'msqrt': return '\\sqrt{' + cs.join('') + '}';
      case 'mroot': return '\\sqrt[' + cs[1] + ']{' + cs[0] + '}';
      case 'mspace': return '\\,';
      case 'mtext': return '\\text{' + n.textContent + '}';
      case 'mo': return ops[n.textContent] || greek[n.textContent] || n.textContent;
      case 'mi': return greek[n.textContent] || n.textContent;
      case 'mtable': return '\\begin{aligned}' + cs.join(' \\\\ ') + '\\end{aligned}';
      case 'mtr': case 'mlabeledtr': return cs.join(' & ');
      case 'menclose':
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
      const math = t === 'math' ? n : n.querySelector('mjx-assistive-mml math');
      if (!math) { errors.push('MathJax formula has no assistive MathML'); return ''; }
      const tex = m(math);
      return n.getAttribute('display') === 'true' ? '\n\n$$\n' + tex + '\n$$\n\n' : '$' + tex + '$';
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
    const circle = row.querySelector('.questionWidget-choiceLetterCircle, [id^="questionWidget-choiceLetterCircle-"]');
    if (!circle?.id) errors.push('Choice circle has no observed ID');
    return choice(row.querySelector('.questionWidget-choiceText'), circle?.textContent.trim(), circle?.id);
  });
  for (const [node,key] of fieldNodes) {
    const f = fields.find(f => f.key === key);
    if (f.type === 'select') f.choices = [...node.querySelectorAll('option, .selectListOptions > .selectListOption')]
      .filter(n => n.textContent.trim() && !(n.localName === 'option' && n.disabled))
      .map((n,i) => choice(n, n.localName === 'option' ? n.value : String(i), n.id || null));
  }
  const prompt = element.querySelector('.exampleQuestion, .questionWidget-text, .questionText');
  const graphic = element.querySelector('.questionWidget-graphic');
  const instructions = element.querySelector('.questionWidget-calculatorInstructions');
  const solution = element.matches('.questionExplanation') ? element : element.querySelector('.exampleExplanation, .questionWidget-explanation');
  return {dom_id:element.id, name:element.querySelector('.stepName,.questionWidget-title')?.textContent.trim(),
    problem:[text(graphic),text(prompt)].filter(Boolean).join('\n\n'), worked_solution:text(solution),
    calculator_instructions:text(instructions), fields,
    result:element.querySelector('.questionWidget-result')?.textContent.trim(),
    html:element.outerHTML, errors:[...new Set(errors)],
    assets:assets.map((n,index) => ({index, tag:n.localName, html:n.outerHTML,
      source_url:n.localName==='img' ? n.currentSrc || n.src : null}))};
}
