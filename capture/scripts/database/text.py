"""Small source-preserving HTML to Markdown conversion."""
import re
from urllib.parse import urljoin


def markdown(source: str) -> str:
    if not re.search(r'<(?:p|div|span|table|img|h[1-6]|ul|ol|br|mjx-container|math)\b', source, re.I):
        return source.strip()
    from bs4 import BeautifulSoup, Comment, NavigableString
    soup = BeautifulSoup(source, 'html.parser')
    for node in soup.select('.mjpage, mjx-container, .MathJax, math'):
        if node.parent is None:
            continue
        tex = node.select_one('annotation[encoding="application/x-tex"], svg > title')
        if tex and tex.get_text(strip=True):
            marker = '$$' if node.get('display') in ('true', 'block') or 'mjpage__block' in node.get('class', []) else '$'
            node.replace_with(NavigableString(marker + tex.get_text().strip() + marker))
    for node in soup.select('script, style, head, .stepHeader, .helpButton, .explanationHeader'):
        node.decompose()
    def render(node):
        if isinstance(node, Comment):
            return ''
        if isinstance(node, NavigableString):
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
            rows = [[render(c).strip().replace('|', '\\|').replace('\n', '<br>') for c in row.find_all(['td', 'th'], recursive=False)] for row in node.find_all('tr')]
            rows = [r for r in rows if r]
            if not rows or len({len(r) for r in rows}) != 1 or node.select('[rowspan], [colspan]'):
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
    return re.sub(r'\n[ \t]*\n(?:[ \t]*\n)+', '\n\n', render(soup)).strip()
