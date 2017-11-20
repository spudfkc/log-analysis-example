#!/usr/bin/env python3

import json
from statistics import median, mean, mode

response_file = 'success.json'

def get_response_size(message):
    return int(message['message']['response_size'])

def main():
    with open(response_file, 'r') as f:
        data = json.loads(f.read())

    response_sizes = [ get_response_size(msg) for msg in data['messages'] ]

    print('mean={}'.format(mean(response_sizes)))
    print('median={}'.format(median(response_sizes)))
    print('mode={}'.format(mode(response_sizes)))

if __name__ == '__main__':
    main()
