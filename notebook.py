import argparse
from html.parser import HTMLParser
import nbformat as nbf
import requests


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.ignore = True
        self.found = False
        self.problem = []

    def handle_starttag(self, tag, attrs):
        if tag == 'article' and not self.found:
            self.ignore = False

    def handle_data(self, data):
        if not self.ignore:
            self.problem.append(''.join(data))

    def handle_endtag(self, tag):
        if tag == 'article' and not self.found:
            self.ignore = True
            self.found = True


def problem_text(day):
    r = requests.get('http://adventofcode.com/2017/day/{}'.format(day))
    parser = MyHTMLParser()
    parser.feed(r.text)

    problem = ''.join(parser.problem[1:])
    return '\n\n'.join(['>' + text for text in problem.split('\n') if len(text) > 0])


def generate_template(day):
    nb = nbf.v4.new_notebook()
    title = '# Advent of Code 2017: Day {}'.format(day)
    problem_header = '## Problem statement'
    problem = problem_text(day)
    breakdown = '## Breaking down the problem\n- **Task**:\n- <font color=\'green\'>Input</font>:' \
                '\n- <font color=\'blue\'>Process the data</font>:\n- <font color=\'red\'>Compute</font>:'
    text = '\n\n'.join((title, problem_header, problem, breakdown))
    nb['cells'].append(nbf.v4.new_markdown_cell(text))
    nb['cells'].append(nbf.v4.new_markdown_cell('## Implementation'))
    nb['cells'].append(nbf.v4.new_markdown_cell('## Check against test cases'))
    nb['cells'].append(nbf.v4.new_markdown_cell('## Solve problem'))

    with open('Day{}.ipynb'.format(day), 'w+') as f:
        nbf.write(nb, f)


parser = argparse.ArgumentParser()
parser.add_argument('day', type=int)
args = parser.parse_args()
generate_template(day=args.day)
