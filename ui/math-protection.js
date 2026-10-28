// Preserve complete TeX spans before Markdown can consume their backslashes,
// split paragraphs, or interpret alignment cells as tables.
export function protectMath(source, replace) {
  const tokens = /\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\[\s\S]|[^$\\])*?(?<!\\)\$|\\begin\{([^{}]+)\}/g;
  let result = '', offset = 0, match;
  while ((match = tokens.exec(source))) {
    let end = tokens.lastIndex;
    if (match[1]) {
      const environments = /\\(begin|end)\{([^{}]+)\}/g;
      environments.lastIndex = end;
      const stack = [match[1]];
      let token, complete = false;
      while ((token = environments.exec(source))) {
        if (token[1] === 'begin') stack.push(token[2]);
        else if (stack.pop() !== token[2]) break;
        if (!stack.length) { end = environments.lastIndex; complete = true; break; }
      }
      // Incomplete environments are validation failures, not guessed closures.
      if (!complete) continue;
      tokens.lastIndex = end;
    }
    let tex = source.slice(match.index, end);
    const line = source.slice(source.lastIndexOf('\n', match.index - 1) + 1, match.index);
    const quote = line.match(/^(?: {0,3}>[\t ]?)+/);
    if (quote && tex.includes('\n')) {
      const depth = (quote[0].match(/>/g) || []).length;
      // Container markers belong to Markdown. Strip exactly this quote depth
      // from continuation lines; an additional > remains a TeX comparison.
      const marker = new RegExp('^(?: {0,3}>[\\t ]?){' + depth + '}');
      tex = tex.replace(/\n([^\n]*)/g, (_, line) => '\n' + line.replace(marker, ''));
    }
    // MathJax treats an initial [A|I] as aligned's optional placement and
    // silently discards it. Only [t], [b], [c] are placement instructions.
    tex = tex.replace(/(\\begin\{aligned\}\s*)\[(?!\s*[tbc]\s*\])/g, '$1{}[');
    result += source.slice(offset, match.index) + replace(tex);
    offset = end;
  }
  return result + source.slice(offset);
}
