#!/bin/bash

sphinx-apidoc -f -e -o ./source/ ../qtmud
sphinx-apidoc -f -e -o ./source/ ../mudlib/starhopper/
sphinx-apidoc -f -e -o ./source/ ../mudlib/yeolderpg/
make html
make doctest
rm ./source/modules.rst
rm ./source/qtmud*.rst
rm ./source/starhopper*.rst
rm ./source/yeolderpg*.rst