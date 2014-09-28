#!/usr/bin/env python2.7

"""Creates a tag cloud from the local user's bash history file.
Outputs a HTML5 document to stdout.
Note this requires jinja2.
"""

from itertools import starmap
import math
import os.path
import re
import sys

from jinja2 import Template

HISTORY_FILE = os.path.expanduser('~/.bash_history')

MIN_FONT_SIZE = 0.1
MAX_FONT_SIZE = 5.0
MIN_OCCURANCES = 2

def compute_counts():
    """Reads the specified history file and computes a list of all commands
    run, returning a list sorted alphabetically."""

    cmd_counts = {}
    with open(HISTORY_FILE, 'r') as fp:
        for l in fp:
            m = re.match(r'^([-/.\w]+)', l)
            if m:
                cmd = m.groups()[0]
                if cmd not in cmd_counts:
                    cmd_counts[cmd] = 1
                else:
                    cmd_counts[cmd] += 1
    return sorted([(k, v) for k, v in cmd_counts.items() if v >= MIN_OCCURANCES], key=lambda x: x[0])

def make_weights(tag_list):
    """Takes a list of (tag, count) and returns a new list with (tag, count, font_size, font_weight)."""

    max_value = float(max(map(lambda x: x[1], tag_list)))

    def font_size(value):
        size = math.log(value) / math.log(max_value) * (MAX_FONT_SIZE - MIN_FONT_SIZE) + MIN_FONT_SIZE
        return '%0.1fem' % size

    def font_weight(value):
        weight = int(math.ceil(value / 100.0)) * 100
        return '%d' % weight

    return starmap(lambda tag, count: 
            (tag, count, font_size(count), font_weight(count)), tag_list)

tag_list = compute_counts()
with open('template.html', 'r') as fp:
    t = Template(fp.read())
    print t.render(
            tags=make_weights(tag_list),
            history_file=HISTORY_FILE,
    )
