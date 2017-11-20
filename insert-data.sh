#!/bin/bash -ex

curl -s https://gist.githubusercontent.com/ickymettle/b9087ca0bcc4dfee1ba2/raw/7f4a22538e0b02c10f4aa4e63cb45955ef82cc55/image-access.log 2>&1 | nc localhost 5555
