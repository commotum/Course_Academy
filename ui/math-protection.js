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
    result += source.slice(offset, match.index) + replace(source.slice(match.index, end));
    offset = end;
  }
  return result + source.slice(offset);
}
