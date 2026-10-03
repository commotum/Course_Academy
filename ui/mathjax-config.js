window.MathJax = {
  loader: { load: ['[tex]/color'] },
  startup: { typeset: false },
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
    processEscapes: true,
    packages: ['base', 'ams', 'newcommand', 'noundefined', 'configmacros', 'color'],
    maxBuffer: 50000,
  },
  svg: { fontCache: 'local' },
  options: { enableMenu: false },
};
