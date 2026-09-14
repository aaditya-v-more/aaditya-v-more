"""Compact generated SVG syntax without rounding coordinates or changing artwork."""
from decimal import Decimal, localcontext
import re

NUMBER = r'-?(?:\d+(?:\.\d*)?|\.\d+)'
POLYLINE = re.compile(rf'M({NUMBER}) ({NUMBER})(?:L{NUMBER} {NUMBER})+')


def number(value):
    """Shorten decimal notation while preserving its exact value."""
    value = format(Decimal(value), 'f')
    if '.' in value:
        value = value.rstrip('0').rstrip('.')
    if Decimal(value) == 0:
        return '0'
    return value.replace('0.', '.', 1) if value.startswith(('0.', '-0.')) else value


def coordinates(values):
    return re.sub(r' (?=-)', '', ' '.join(number(v) for v in values))


def compact_path(value):
    # Only rewrite the generator's simple M/L polylines. Curves stay untouched.
    if not POLYLINE.fullmatch(value):
        return value
    values = re.findall(NUMBER, value)
    absolute = 'M' + coordinates(values)
    with localcontext() as context:
        context.prec = 50
        points = list(zip(map(Decimal, values[::2]), map(Decimal, values[1::2])))
        deltas = [str(v) for previous, current in zip(points, points[1:])
                  for v in (current[0] - previous[0], current[1] - previous[1])]
    relative = 'M' + coordinates(values[:2]) + 'l' + coordinates(deltas)
    return min((absolute, relative), key=len)


def optimize_svg(svg):
    def attribute(match):
        key, value = match.groups()
        if key == 'd':
            value = compact_path(value)
        elif key in ('x', 'y', 'x1', 'x2', 'y1', 'y2', 'cx', 'cy', 'r', 'rx', 'ry',
                     'width', 'height', 'opacity', 'fill-opacity', 'stroke-opacity',
                     'stroke-width', 'font-size', 'font-weight', 'letter-spacing',
                     'offset', 'stop-opacity') and re.fullmatch(NUMBER, value):
            value = number(value)
        elif key in ('points', 'viewBox'):
            value = ' '.join(number(v) for v in re.findall(NUMBER, value))
        return f'{key}="{value}"'
    svg = re.sub(r'([\w:-]+)="([^"]*)"', attribute, svg)
    # Remove whitespace between elements and before tag endings, never text nodes.
    svg = re.sub(r'>\s+<', '><', svg)
    svg = re.sub(r'\s+(/?>)', r'\1', svg)
    return svg.rstrip() + '\n'
