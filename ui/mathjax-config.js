window.MathJax = {
  startup: { typeset: false },
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
    processEscapes: true,
    packages: ['base', 'ams', 'newcommand', 'noundefined', 'configmacros'],
    maxBuffer: 50000,
  },
  svg: { fontCache: 'local' },
  options: { enableMenu: false },
};
