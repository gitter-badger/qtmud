#!/bin/bash

sphinx-apidoc -o ./source/ ../qtmud
sphinx-apidoc -o ./source/ ../mudlib/starhopper/
sphinx-apidoc -o ./source/ ../mudlib/yeolderpg/
make html
make doctest