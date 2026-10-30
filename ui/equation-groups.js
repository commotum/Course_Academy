// Display lists of independent equations can reflow between complete items.
// Leave arrays, derivations, inline math and ambiguous comma lists to MathJax.
const spacing = /^(?:\s|\\(?:[,;:!]|quad\b|qquad\b|enspace\b|thinspace\b))+/;
const variable = '(?:[A-Za-z]|\\\\[A-Za-z]+|\\{[A-Za-z]\\})';
const assignment = new RegExp('^(' + variable + '(?:_\\{[^{}]+\\}|_[A-Za-z0-9])?(?:\\s*\\([^()]*\\))?)\\s*=\\s*([^=]+)$');

export function equationGroup(tex) {
  let body = tex.startsWith('$$') && tex.endsWith('$$') ? tex.slice(2, -2)
    : tex.startsWith('\\[') && tex.endsWith('\\]') ? tex.slice(2, -2) : null;
  if (body === null || /\\(?:begin|end|tag|label|def|gdef|newcommand|color|underbrace|overbrace)\b|\\\\|&|\{\{(?:answer-field:)?(?:field-\d+|selection)\}\}|\|/.test(body)) return null;
  body = body.trim().replace(/^\\displaystyle\s*/, '');
  const trailing = /[,;]\s*$/.exec(body);
  if (trailing) body = body.slice(0, trailing.index);
  const stack = [], parts = [], separators = [];
  let start = 0;
  for (let i = 0; i < body.length; i++) {
    let token = body[i];
    if (token === '\\') {
      const command = /^\\(?:[A-Za-z]+|.)/.exec(body.slice(i));
      if (!command) return null;
      token = command[0]; i += token.length - 1;
    }
    const open = { '{': '}', '(': 'bracket', '[': 'bracket', '\\{': '\\}', '\\lbrace': '\\rbrace', '\\langle': '\\rangle' }[token];
    if (open) stack.push(open);
    else if (['}', ')', ']', '\\}', '\\rbrace', '\\rangle'].includes(token)) {
      if (stack.pop() !== (token === ')' || token === ']' ? 'bracket' : token)) return null;
    } else if (!stack.length && [',', ';', '\\quad', '\\qquad'].includes(token)) {
      const part = body.slice(start, i + 1 - token.length).replace(spacing, '').trim();
      // A spacing command after a comma belongs to that same boundary.
      if (part) { parts.push(part); separators.push(token.length === 1 ? token : ''); }
      else if (token.length === 1) return null;
      start = i + 1;
    }
  }
  if (stack.length || !parts.length) return null;
  parts.push(body.slice(start).replace(spacing, '').trim());
  const equations = parts.map(part => assignment.exec(part));
  // At least two distinct explicit assignments, optionally followed by a domain.
  // This excludes tuples, value lists, chained equalities and lone equations.
  const count = equations.at(-1) ? parts.length : parts.length - 1;
  if (count < 2 || count > 6 || equations.slice(0, count).some(part => !part)) return null;
  const names = equations.slice(0, count).map(part => part[1].replace(/[{}\s]/g, ''));
  if (new Set(names).size !== names.length) return null;
  if (count !== parts.length && !/^(?!.*=)[\s\S]*(?:\\(?:leq?|geq?|in)\b|[<>≤≥∈])[\s\S]+$/.test(parts.at(-1))) return null;
  return parts.map((part, i) => part + (separators[i] || (i === parts.length - 1 && trailing ? trailing[0].trim() : '')));
}

export function decorateEquationGroups(root) {
  const doc = root.ownerDocument;
  const walker = doc.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  const nodes = [];
  while (walker.nextNode()) {
    const node = walker.currentNode;
    if (!node.parentElement?.closest('pre, code, script, style, textarea, math-field, mjx-container, .equation-group') && /\$\$|\\\[/.test(node.data)) nodes.push(node);
  }
  for (const node of nodes) {
    const displays = /(?<!\\)\$\$[\s\S]*?(?<!\\)\$\$|(?<!\\)\\\[[\s\S]*?(?<!\\)\\\]/g;
    const fragment = doc.createDocumentFragment();
    let offset = 0, match, changed = false;
    while ((match = displays.exec(node.data))) {
      const parts = equationGroup(match[0]);
      if (!parts) continue;
      fragment.append(doc.createTextNode(node.data.slice(offset, match.index)));
      const group = doc.createElement('span');
      group.className = 'equation-group';
      group.setAttribute('role', 'group');
      group.setAttribute('aria-label', 'Related equations');
      for (const part of parts) {
        const item = doc.createElement('span');
        item.className = 'equation-group-item';
        item.textContent = '\\(\\displaystyle ' + part + '\\)';
        group.append(item);
      }
      fragment.append(group); offset = displays.lastIndex; changed = true;
    }
    if (changed) {
      fragment.append(doc.createTextNode(node.data.slice(offset)));
      node.replaceWith(fragment);
    }
  }
}
