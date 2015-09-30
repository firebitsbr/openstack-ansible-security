#!/usr/bin/env python
import csv
from textwrap import fill
from jinja2 import Template
from pprint import pprint

stig_csv = 'rhel6stig.csv'

def reindent(string_to_indent, numSpaces):
    s = string_to_indent.splitlines()
    s = [(numSpaces * ' ') + line.lstrip() for line in s]
    return '\n'.join(s)

rst_template = """
{{ title }}
{{ '-' * title | length }}

{{ desc }}

Details: `{{ id }} in STIG Viewer`_.

.. _{{ id }} in STIG Viewer: https://www.stigviewer.com/stig/red_hat_enterprise_linux_6/2015-05-26/finding/{{ id }}

Developer Notes
~~~~~~~~~~~~~~~
This security hardening configuration is not yet implemented in
openstack-ansible-security.

"""

categories = {
    'Low': 1,
    'Medium': 2,
    'High': 3,
}

for category_name, category_level in categories.items():

    filename = "configurations-cat{0}.rst".format(category_level)
    file_handle = open(filename, 'w')

    header = (""".. include:: <xhtml1-lat1.txt>
`Home <index.html>`__ |raquo| Security hardening for openstack-ansible

Category {0} ({1}) configurations
================================

.. contents::
   :depth: 2

""".format(category_level, category_name))
    file_handle.write(header)

    with open(stig_csv, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[1] != category_name.lower():
                continue
            metadata = {
                'id':        row[0],
                'title':     "{0}: {1}".format(row[0], row[2]),
                'desc':      fill(row[3], width=78),
                'fixtext':   reindent(row[7], 4),
                'checktext': reindent(row[9], 4),
            }
            template = Template(rst_template)
            file_handle.write(template.render(metadata))

    file_handle.close()
