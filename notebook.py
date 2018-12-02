import argparse
import nbformat as nbf
import requests
from datetime import datetime


def problem_text(day, year):
    r = requests.get(f'http://adventofcode.com/{year}/day/{day}')
    day_text = r.text.split('<article')[1].split('</article>')[0]

    title = day_text[(day_text.find('<h2>') + 4):day_text.find('</h2>')]
    name = title.strip(f'--- Day {day}:').strip()
    problem = day_text[day_text.find('<p>'):]
    return name, problem


def generate_template(day, year):
    nb = nbf.v4.new_notebook()
    title = f'# Advent of Code {year}: [Day {day}](http://adventofcode.com/{year}/day/{day})'
    problem_header = '## Problem statement'
    name, problem = problem_text(day, year)
    breakdown = '## Breaking down the problem\n- **Task**:\n- <font color=\'green\'>Input</font>:' \
                '\n- <font color=\'blue\'>Process the data</font>:\n- <font color=\'red\'>Compute</font>:'
    text = '\n\n'.join((title, problem_header, problem, breakdown))
    nb['cells'].append(nbf.v4.new_markdown_cell(text))
    nb['cells'].append(nbf.v4.new_markdown_cell('## Implementation'))
    nb['cells'].append(nbf.v4.new_markdown_cell('## Check against test cases'))
    nb['cells'].append(nbf.v4.new_markdown_cell('## Solve problem'))

    with open(f'{year}/README.md', 'a') as f:
        f.write(f'- [Day {day}: {name}](http://nbviewer.jupyter.org/github/jrdurrant/adventofcode/blob/master/{year}/Day{day}.ipynb)\n')

    with open(f'{year}/Day{day}.ipynb', 'w+') as f:
        nbf.write(nb, f)


parser = argparse.ArgumentParser()
parser.add_argument('--day', type=int, default=datetime.now().day)
parser.add_argument('--year', type=int, default=datetime.now().year)
args = parser.parse_args()
generate_template(day=args.day, year=args.year)
