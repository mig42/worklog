#!/bin/bash

PYTHON=/usr/bin/python3

if ! pandoc -v &>/dev/null; then
    echo "pandoc not found." >&2
    exit 1
fi

if ! ${PYTHON} -V &>/dev/null; then
    echo "python3 not found." >&2
    exit 1
fi

path=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
for source_file in "${path}"/data/*.md; do
    source_name=$( basename --suffix=.md "${source_file}" )
/usr/bin/python3 "${path}/src/input.py" "${source_file}" | pandoc -s -f markdown -t html -c /css/github-markdown.css --template="${path}/templates/markdown.tpl" -o "${path}/www/${source_name}.html"
done
