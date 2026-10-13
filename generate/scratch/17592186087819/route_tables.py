"""Shared route-table HTML, plus lossless readers for captured table formats."""
from dataclasses import dataclass
from html import escape
from html.parser import HTMLParser
import re

TABLE_FORMAT = 'route-matrix-html-v1'


@dataclass(frozen=True)
class RouteTable:
    rows: tuple[str, ...]
    columns: tuple[str, ...]
    cells: tuple[tuple[str, ...], ...]


def render_route_table(table: RouteTable) -> str:
    """Render one format for every station count, order, and response shape."""
    rows, columns, cells = table.rows, table.columns, table.cells
    if len(rows) not in (3, 4) or len(columns) != len(rows):
        raise ValueError('route tables need three or four station rows and columns')
    if len(set(rows)) != len(rows) or set(rows) != set(columns):
        raise ValueError('station headings must be unique and cover the same stations')
    if len(cells) != len(rows) or any(len(row) != len(columns) for row in cells):
        raise ValueError('cell dimensions must match the headings')
    if any(label not in 'ABCD' or len(label) != 1 for label in (*rows, *columns)):
        raise ValueError('unsupported station label')
    lines = ['<div class="route-matrix">',
             '  <span class="matrix-to">To</span>',
             '  <span class="matrix-from">From</span>',
             '  <table aria-label="Route matrix: rows are From stations; columns are To stations">',
             '    <thead>',
             '      <tr><td class="matrix-corner"></td>' + ''.join(
                 f'<th scope="col">{escape(label)}</th>' for label in columns) + '</tr>',
             '    </thead>', '    <tbody>']
    for label, values in zip(rows, cells):
        lines.append(f'      <tr><th scope="row">{escape(label)}</th>' + ''.join(
            f'<td>{escape(value)}</td>' for value in values) + '</tr>')
    lines.extend(['    </tbody>', '  </table>', '</div>'])
    return '\n'.join(lines)


class _Cells(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.cell = None

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.rows.append([])
        elif tag in ('td', 'th'):
            self.cell = ''

    def handle_data(self, data):
        if self.cell is not None:
            self.cell += data

    def handle_endtag(self, tag):
        if tag in ('td', 'th') and self.cell is not None:
            self.rows[-1].append(self.cell.strip())
            self.cell = None


def parse_route_table(block: str) -> RouteTable:
    if '<table' in block:
        parser = _Cells()
        parser.feed(block)
        lines = parser.rows
    else:
        lines = [[cell.strip() for cell in line.strip().strip('|').split('|')]
                 for line in block.splitlines() if line.startswith('|')]
    def label(value):
        plain = value.strip('*')
        return plain if len(plain) == 1 and plain in 'ABCD' else None
    header = next((i for i, row in enumerate(lines)
                   if sum(label(value) is not None for value in row) >= 3), None)
    if header is None:
        raise ValueError('not a station route table')
    columns = tuple(label(value) for value in lines[header] if label(value))
    rows, cells = [], []
    for line in lines[header + 1:]:
        positions = [i for i, value in enumerate(line) if label(value)]
        if len(positions) != 1:
            continue
        index = positions[0]
        values = tuple(line[index + 1:index + 1 + len(columns)])
        if len(values) != len(columns):
            raise ValueError('route row has missing cells')
        rows.append(label(line[index]))
        cells.append(values)
    result = RouteTable(tuple(rows), columns, tuple(cells))
    # The formatter validates structure, but does not interpret or change cells.
    render_route_table(result)
    return result


_TABLES = re.compile(
    r'<div class="route-matrix">.*?</div>|<table\b[^>]*>.*?</table>|'
    r'(?:^\|[^\n]*\|[ \t]*(?:\n|$))+', re.S | re.M)


def route_table_spans(text: str):
    for match in _TABLES.finditer(text):
        try:
            parsed = parse_route_table(match.group())
        except ValueError as error:
            if str(error) == 'not a station route table':
                continue
            raise
        yield match.start(), match.end(), parsed


def replace_route_tables(text: str, replacement: str | None = None) -> str:
    """Normalize existing tables, or replace a source table with sampled cells."""
    for start, end, table in reversed(list(route_table_spans(text))):
        rendered = render_route_table(table) if replacement is None else replacement
        if text[start:end].endswith('\n'):
            rendered += '\n'
        text = text[:start] + rendered + text[end:]
    return text
