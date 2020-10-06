#!/bin/bash

function usage
{
    echo 'usage: mkpypi -v version [-u]'     
    echo 'where:'
    echo '-u: upload to pypi'
    exit 2
}

upload="n"
version="none"
while getopts v:u flag
do
    case "${flag}" in
        v) version=${OPTARG};;
        u) upload='y';;
    esac
done

if [ $version == "none" ] 
then
   usage
else
    echo "Creating release version: $version"
    cp setup_template.py setup.py 
    sed -i "s/{{VERSION}}/$version/g" setup.py 
    rm -rf test
    rm -rf dist
    rm -rf tschartslib
    cp ../../README.md .
    cp -r ../../tschartslib .
    find tschartslib -name "*.pyc" | xargs rm

    python setup.py sdist

    if [[ $upload == 'y' || $upload == 'Y' ]] 
    then
        twine upload dist/*
    fi
fi
