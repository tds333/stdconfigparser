#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Executor script providing commands to build, test, release, ...
Should be compatible to Python >= 3.4
"""

import sys
import os
import argparse
from subprocess import call
from pathlib import Path

CURRENTDIR = Path(__file__).parent
VENVDIR = CURRENTDIR / "venv"
PYTHON = VENVDIR / "py35" / "bin" / "python"


def invalid():
    print("Invalid action")


def docu():
    call([str(PYTHON), "-m", "sphinx", "-b", "html", "./docu", "./build/docu/html"])


def test():
    for dirname in (x for x in VENVDIR.iterdir() if x.is_dir()):
        py = dirname / "bin" / "python"
        call([str(py), "-m", "pytest", "test"])


def teststyle():
    call([str(PYTHON), "-m", "flake8", "stdconfigparser.py"])


def dist():
    call(["python3", "setup.py", "sdist", "bdist_wheel"])


commands = {
    "test": test,
    "docu": docu,
    "teststyle": teststyle,
    "dist": dist,
}

def main():
    parser = argparse.ArgumentParser(description='Executor script for project.')
    parser.add_argument('action', choices=list(commands.keys()))
    args = parser.parse_args(sys.argv[1:])
    action = args.action
    commands.get(action, invalid)()


if __name__ == '__main__':
    main()
