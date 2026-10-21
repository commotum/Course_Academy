"""Small source-preserving HTML to Markdown conversion."""
import re
from urllib.parse import urljoin


def markdown(source: str) -> str:
    if not re.search(r'<(?:p|div|span|table|img|h[1-6]|ul|ol|br|mjx-container|math)(?:\s[^<>]*|/?)>', source, re.I):
        return source.strip()
    # These are authored UI layouts, not source tables to flatten into Markdown.
    # Keep complete nested wrappers verbatim, including their answer controls.
    layouts, layout_prefix = [], 'CAMATRIXLAYOUTTOKEN'
    while layout_prefix in source:
        layout_prefix += 'X'
    pattern = re.compile(r'<div\b[^>]*\bclass=["\'](?:[^"\']*\s)?matrix-(?:answer|operands)(?=[\s"\'])[^"\']*["\'][^>]*>', re.I)
    offset = 0
    while match := pattern.search(source, offset):
        depth, end = 0, None
        for tag in re.finditer(r'</?div\b[^>]*>', source[match.start():], re.I):
            depth += -1 if tag[0].startswith('</') else 1
            if depth == 0:
                end = match.start() + tag.end()
                break
        if end is None:
            offset = match.end()
            continue
        layouts.append(source[match.start():end])
        token = layout_prefix + str(len(layouts) - 1) + 'END'
        source = source[:match.start()] + token + source[end:]
        offset = match.start() + len(token)
    table_math, table_math_prefix = [], 'CATABLEMATHTOKEN'
    complex_table = (re.search(r'<(?:td|th)\b[^>]*\b(?:rowspan|colspan)\s*=', source, re.I)
                     or re.search(r'<table\b(?:(?!</table\b)[\s\S])*<table\b', source, re.I))
    if complex_table:
        while table_math_prefix in source:
            table_math_prefix += 'X'
        def protect_table_math(match):
            table_math.append(match.group())
            return table_math_prefix + str(len(table_math) - 1) + 'END'
        # The UI protects these same complete spans before parsing HTML. Keep
        # exact TeX bytes through BeautifulSoup too, including < and & tokens.
        source = re.sub(r'\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\.|[^$\\])*?(?<!\\)\$', protect_table_math, source)
    from bs4 import BeautifulSoup, Comment, NavigableString
    soup = BeautifulSoup(source, 'html.parser')
    for node in soup.select('.mjpage, mjx-container, .MathJax, math'):
        if node.parent is None:
            continue
        if node.select_one('svg > title math') is not None:
            continue
        tex = node.select_one('annotation[encoding="application/x-tex"], svg > title')
        if tex and not tex.find('math') and tex.get_text(strip=True):
            marker = '$$' if node.get('display') in ('true', 'block') or 'mjpage__block' in node.get('class', []) else '$'
            # A source title's percent comments and legacy row delimiters need
            # their original line endings; resolve them before render() treats
            # HTML whitespace as spaces. Mixed titles remain whole graphics.
            from .math_content import formatter
            value = formatter().normalize_source_tex(tex.get_text())
            node.replace_with(NavigableString(marker + value + marker))
    for node in soup.select('script, style, head, .stepHeader, .helpButton, .explanationHeader'):
        node.decompose()
    def render(node):
        if isinstance(node, Comment):
            return ''
        if isinstance(node, NavigableString):
            # Extracted complex tables are mixed with already-authored Markdown
            # at document level. Its paragraphs and list lines are not HTML
            # whitespace; only text inside actual HTML elements is collapsed.
            if complex_table and node.parent is soup:
                return str(node)
            return re.sub(r'[\t\r\n ]+', ' ', str(node))
        body = ''.join(render(c) for c in node.children)
        name = node.name
        if name == 'img':
            return '![' + node.get('alt', '').replace(']', '') + '](' + node.get('src', '') + ')'
        if name in ('svg', 'canvas', 'math', 'mjx-container'):
            raise ValueError('Source contains an unresolved graphic or formula')
        if name == 'br':
            return '\n'
        if name in ('strong', 'b', 'em', 'i'):
            mark = '**' if name in ('strong', 'b') else '*'
            return mark + body.strip() + mark
        if name == 'a':
            href = node.get('href')
            return '[' + body.strip() + '](' + urljoin('https://mathacademy.com/', href) + ')' if href else body
        if name in ('ul', 'ol'):
            return '\n\n' + '\n'.join((f'{i}. ' if name == 'ol' else '- ') + render(c).strip()
                for i, c in enumerate(node.find_all('li', recursive=False), 1)) + '\n\n'
        if name == 'table':
            rows = [[render(c).strip().replace('|', '\\|').replace('\n', '<br>') for c in row.find_all(['td', 'th'], recursive=False)]
                    for row in node.find_all('tr') if row.find_parent('table') is node]
            rows = [r for r in rows if r]
            if not rows or len({len(r) for r in rows}) != 1 or node.select('[rowspan], [colspan]') or node.find('table'):
                return '\n\n' + str(node) + '\n\n'
            lines = ['| ' + ' | '.join(r) + ' |' for r in rows]
            lines.insert(1, '| ' + ' | '.join('---' for _ in rows[0]) + ' |')
            return '\n\n' + '\n'.join(lines) + '\n\n'
        if name and re.fullmatch('h[1-6]', name):
            return '\n\n' + '#' * int(name[1]) + ' ' + body.strip() + '\n\n'
        if name in ('p', 'div', 'blockquote', 'section'):
            return '\n\n' + body.strip() + '\n\n'
        if name in ('sup', 'sub'):
            return '<' + name + '>' + body + '</' + name + '>'
        return body
    result = re.sub(r'\n[ \t]*\n(?:[ \t]*\n)+', '\n\n', render(soup)).strip()
    if table_math:
        result = re.sub(table_math_prefix + r'(\d+)END', lambda match: table_math[int(match[1])], result)
    if layouts:
        result = re.sub(layout_prefix + r'(\d+)END', lambda match: layouts[int(match[1])], result)
    return result
