#!/bin/bash
if [ -d htmlcov ]; then
	rm -rf htmlcov/
fi
python3.7 -m coverage run -m unittest
python3.7 -m coverage report
python3.7 -m coverage html
