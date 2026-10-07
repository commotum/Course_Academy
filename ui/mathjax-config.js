window.MathJax = {
  loader: { load: ['[tex]/color'] },
  startup: {
    typeset: false,
    ready() {
      MathJax.startup.defaultReady();
      const tex = MathJax.startup.document.inputJax.find(jax => jax.name === 'TeX');
      const { length2em } = MathJax._.util.lengths;
      // Older MathML captures kept the function-application marker but lost
      // the TeX operator command. Restore marked operators for display only;
      // existing commands and literal text remain intact.
      tex.preFilters.add(({ math }) => {
        math.math = math.math.replace(
          /\\(?:operatorname|mathrm|text|textrm|mathit)\*?\s*\{[^{}]*\}|\\[A-Za-z]+|(arcsin|arccos|arctan|sinh|cosh|tanh|sin|cos|tan|sec|csc|cot|ln|log|exp|arg|lim|min|max)(?=\}?(?:[_^]\{[^{}]*\})*\u2061)/g,
          (match, operator) => operator ? `\\${operator} ` : match,
        ).replaceAll('\u2061', ' ');
      });
      // Space the parsed rows before SVG layout so fractions and enclosing
      // brackets still size correctly. The authored TeX is never rewritten.
      tex.postFilters.add(({ data }) => {
        data.root.walkTree(node => {
          if (node.kind !== 'mtable' || node.childNodes.length < 2) return;
          const spacing = String(node.attributes.get('rowspacing')).trim().split(/\s+/);
          node.attributes.set('rowspacing', spacing.map(value =>
            `${Number((length2em(value) + 0.2).toFixed(4))}em`).join(' '));
        });
      }, 10);
    },
  },
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
    processEscapes: true,
    packages: ['base', 'ams', 'newcommand', 'noundefined', 'configmacros', 'color'],
    maxBuffer: 50000,
  },
  svg: { fontCache: 'local' },
  options: { enableMenu: false, skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code', 'annotation', 'annotation-xml', 'math-field'] },
};
