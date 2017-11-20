#!/usr/bin/env python3

import requests
import csv
import sys
from datetime import datetime

def unpad_ip(ip):
    return '.'.join([i.lstrip('0') or '0' for i in ip.split('.')])

# Headers assumed to be similar to: https://isc.sans.edu/api/#topips
def format_ip(ip, reports, targets, first_seen, last_seen):
    return {
        'source_ip': unpad_ip(ip),
        'reports': reports,
        'targets': targets,
        'first_seen': first_seen,
        'last_seen': last_seen,
        # I debated about putting the time of the report in here,
        # but that seemed to clutter things up and duplicate the
        # same value for every row. The idea behind putting the
        # date of the report in here would be for whatever system
        # this data is being loaded into, so you can keep track of
        # where this data came from.
        # I opted for adding the report date to the file name instead
        # as that was less clutter and the user of the file can do
        # whatever with it.
    }

def get_report():
    # note: this request is slow
    resp = requests.get('https://isc.sans.edu/ipsascii.html')
    return resp.text

def is_valid_line(line):
    if len(line) == 0:
        return False
    if line.startswith('#'):
        return False
    return True

def get_created_at(data):
    # Ugh, this is gross. Iterating through the list another time...
    for line in data:
        if line.startswith('# created: '):
            date_str = line.split('created: ')[1]
            break
    date = datetime.strptime(date_str, '%a, %d %b %Y %X %z')
    return date

def format_report(text):
    data = text.split('\n')
    created_at_date = get_created_at(data)

    data = [ line for line in data if is_valid_line(line) ]
    data = [ x.split('\t') for x in data ]

    hostile_ips = [ format_ip(*args) for args in data ]

    return (hostile_ips, created_at_date)

def output_csv(hostile_ips, output_file):
        field_names = [ 'source_ip', 'reports', 'targets', 'first_seen', 'last_seen' ]
        writer = csv.DictWriter(output_file, field_names)
        writer.writeheader()
        writer.writerows(hostile_ips)

def main():
    raw_report = get_report()
    hostile_ips, created_at_date = format_report(raw_report)

    # this can easily be changed to print to stdout to be more chain-able with
    # other tools:
    #   if print_to_stdout:
    #     csvfile = sys.stdout
    #     output_csv(hostile_ips, csvfile)

    # I opted for controlling the filename based on when the report was created.
    # The report contains that info, so we don't have to worry about losing data
    # if we end up overwriting a file.
    output_filepath = 'hostile-ips-top-100.{}.csv'.format(created_at_date.strftime('%Y%m%dT%H%M%S'))
    with open(output_filepath, 'w', newline='') as csvfile:
        output_csv(hostile_ips, csvfile)


if __name__ == '__main__':
    main()
