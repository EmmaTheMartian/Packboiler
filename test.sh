#!/usr/bin/env sh
echo "THIS SCRIPT IS FOR DEVELOPERS!!!"
echo "If you are NOT developing Packboiler, don't run this!"

rm -rf dist output
python3 -m build && python3 -m pip install --force-reinstall ./dist/*.whl
python3 -m packboiler $@
