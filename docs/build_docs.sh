#!/bin/bash

sphinx-apidoc -f -e -o ./ ../
make html

rm modules.rst
rm qtmud*rst
