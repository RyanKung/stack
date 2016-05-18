#!/bin/bash

wget "https://www.python.org/ftp/python/{version}/Python-{version}.tar.xz"
tar -xvf Python-3.5.1.tar.xz
cd Python-3.5.1
./configure&&make&&make install
cd ..
rm -r Python-3.5.1*
pip3.5 install python-stack
