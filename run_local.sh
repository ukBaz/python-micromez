#!/usr/bin/env bash
coverage run -m unittest -v tests.test_outputs
test1001=$?
coverage run --append -m unittest -v tests.test_inputs
test1002=$?
coverage run --append -m unittest -v tests.test_examples
test1003=$?

pycodestyle -v micromez/*.py
lint_micromez=$?
pycodestyle -v examples
lint_examples=$?
pycodestyle -v micromez/fonts/font_builder.py
lint_fonts=$?

coverage report
coverage html
group100=$((test1001 + test1002 + test1003))
group_lint=$((lint_micromez + lint_examples + lint_fonts))
if [ $((group100 + group_lint)) -ne 0 ]; then
   echo -e "\n\n###  A test has failed!!  ###\n"
else
    echo -e "\n\nSuccess!!!\n"
fi

