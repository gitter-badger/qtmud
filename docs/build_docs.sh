#!/bin/bash

sphinx-apidoc -f -e -o ./ ../
make html

rm qtmud*rst
