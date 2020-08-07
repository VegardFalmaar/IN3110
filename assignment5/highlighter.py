import re, os
from argparse import ArgumentParser

parser = ArgumentParser(description='Print the contents of a file with syntax highlighting.')
parser.add_argument('syntax', type=str,
                help='the syntax file to use')
parser.add_argument('theme', type=str,
                help='the higlighting theme to use')
parser.add_argument('source', type=str,
                help='the file to whose content should be printed')

args = parser.parse_args()

for arg in vars(args):
    fname = getattr(args, arg)
    assert os.path.isfile(fname), f'Hey! {fname} is not a file...'

theme = {}
with open(args.theme, 'r') as infile:
    for line in infile:
        name, color = line.split()
        name = name.strip(':')
        theme[name] = color

syntax = {}
with open(args.syntax, 'r') as infile:
    for line in infile:
        *pattern, name = line.split()
        pattern = ' '.join(pattern)
        pattern = pattern.strip(':')[1:-1]
        pattern = re.compile('(' + pattern + ')')
        syntax[pattern] = theme[name]

with open(args.source, 'r') as infile:
    content = infile.readlines()
content = ''.join(content)

# Let us go
# This is a print test
start_code = "\033[{}m"
end_code = "\033[0m"

"""
colored = {}

for line in content:
    for pattern, color in syntax.items():
        matches = pattern.finditer(line)
        for match in matches:
            colored[match.span()] = color
        start = start_code.format(color)
        line = pattern.sub(start + r'\1' + end_code, line)
    print(line, end='')
print()
"""

color_code = "\033[{}m"
to_color = {}

for pattern, color in syntax.items():
    shift = 0
    matches = pattern.finditer(content)
    for match in matches:
        idx = match.span()
        start, stop = idx
        end = 0
        for (prev_start, prev_stop), (prev_color, _) in to_color.items():
            if (start > prev_start) and (stop < prev_stop):
                end = prev_color
        to_color[idx] = (color, end)

single_to_color = {}
for idx, colors in to_color.items():
    for i in range(2):
        single_to_color[idx[i]] = colors[i]

add = 0
for idx in sorted(single_to_color):
    color = single_to_color[idx]
    color = color_code.format(color)
    content = content[:idx+add] + color + content[idx+add:]
    add += len(color)
print(content)
