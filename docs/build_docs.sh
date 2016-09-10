#!/bin/bash

sphinx-apidoc -f -e -o ./source/ ../
make html

rm ./source/modules.rst
rm ./source/qtmud*rst
