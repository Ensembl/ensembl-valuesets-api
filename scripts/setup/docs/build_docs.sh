#!/bin/bash

sphinx-apidoc -Mf --implicit-namespaces -o source ../src/ensembl

SPHINX_MAKEFILE="../setup/docs/Makefile"

make -f $SPHINX_MAKEFILE clean && make -f $SPHINX_MAKEFILE html text
