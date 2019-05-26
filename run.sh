#!/bin/bash

set -u

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd "${DIR}"
venv/bin/python main.py -c credentials.txt -d data
