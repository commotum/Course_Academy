"""Small data-only EDN codec for the forms emitted by the EDB CLI."""
import json
import re
import uuid


class Keyword(str):
    pass


class Symbol(str):
    """An EDN symbol is data, distinct from a quoted string; never evaluated."""
    pass


class Tagged:
    def __init__(self, tag, value):
        self.tag, self.value = tag, value


def kw(name):
    return Keyword(':' + name.lstrip(':'))


def dumps(value):
    if isinstance(value, (Keyword, Symbol)):
        return str(value)
    if isinstance(value, uuid.UUID):
        return '#uuid ' + json.dumps(str(value))
    if isinstance(value, Tagged):
        return '#' + value.tag + ' ' + dumps(value.value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if value is None:
        return 'nil'
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if isinstance(value, (int, float)):
        return json.dumps(value, allow_nan=False)
    if isinstance(value, dict):
        return '{' + ' '.join(dumps(k) + ' ' + dumps(v) for k, v in value.items()) + '}'
    if isinstance(value, (list, tuple)):
        return '[' + ' '.join(map(dumps, value)) + ']'
    raise TypeError(type(value))


def loads(source):
    tokens = re.findall(r'"(?:\\.|[^"\\])*"|;[^\n]*|#\{|[\[\]{}]|[^\s,\[\]{}]+', source)
    tokens = [token for token in tokens if not token.startswith(';')]
    position = 0

    def read():
        nonlocal position
        if position >= len(tokens):
            raise ValueError('Unexpected end of EDN')
        token = tokens[position]
        position += 1
        if token in ('[', '{', '#{'):
            close = ']' if token == '[' else '}'
            items = []
            while position < len(tokens) and tokens[position] != close:
                items.append(read())
            if position >= len(tokens):
                raise ValueError('Unclosed EDN collection')
            position += 1
            if token == '{':
                if len(items) % 2:
                    raise ValueError('Odd EDN map')
                return dict(zip(items[::2], items[1::2]))
            return items
        if token == '#uuid':
            return uuid.UUID(read())
        if token in ('#inst', '#edb/ref'):
            return read()
        if token.startswith('"'):
            return json.loads(token)
        if token.startswith(':'):
            return Keyword(token)
        if token in ('true', 'false', 'nil'):
            return {'true': True, 'false': False, 'nil': None}[token]
        if re.fullmatch(r'-?\d+', token):
            return int(token)
        if re.fullmatch(r'[+-]?(?:\d+\.\d*(?:[Ee][+-]?\d+)?|\d+[Ee][+-]?\d+)', token):
            return float(token)
        if re.fullmatch(r'[A-Za-z_*+!?<>=][A-Za-z0-9_.*/+!?<>=-]*', token):
            return Symbol(token)
        raise ValueError('Unsupported EDN token: ' + token)

    result = read()
    if position != len(tokens):
        raise ValueError('Trailing EDN forms')
    return result
