#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 01:23:22 2024

@author: yl
"""
import os
import sys
from multiprocessing import Lock


def filename(path):
    bname = os.path.basename(path)
    rindex = bname.rfind(".") if "." in bname else None
    return bname[:rindex]


class inpkg:
    """
    `inpkg` means "in package"

    Directly execute py file has relative import in a package.

    Usage：
        >>> with inpkg():
        >>>     from . import local_py

    Principle：
        Auto search and import "top level package". Then, temporary replace __name__ to "module name under top level package" during with statement
    """

    def __init__(self):
        frame = sys._getframe(1)
        self.frame = frame
        self._file_ = (
            frame.f_globals["__file__"]
            if "__file__" in frame.f_globals
            else frame.f_code.co_filename
        )
        self._name_ = frame.f_globals["__name__"]
        # NOTICE: second time %run will no '__package__' key
        self._package_ = self.frame.f_globals.get("__package__", None)
        self.importTopLevelPackage = (
            self._name_ == "__main__" or self._name_ == filename(self._file_)
        )

    def findPackageRoot(self):
        dirr = os.path.abspath(self._file_)
        files = []
        while len(dirr) > 1:
            files.append(filename(dirr))
            dirr = os.path.dirname(dirr)
            _init_p = os.path.join(dirr, "__init__.py")
            if not os.path.isfile(_init_p):
                return dirr, files
        raise Exception('Has __init__.py in root "/__init__.py"')

    def __enter__(self):
        if self.importTopLevelPackage:
            packageroot, files = self.findPackageRoot()
            if len(files) > 1:
                top_level_package_path = os.path.join(packageroot, files[-1])
                import_by_path(top_level_package_path)  # import top level package
            self.frame.f_globals["__name__"] = ".".join(files[::-1])
            self.frame.f_globals["__package__"] = ".".join(files[1:][::-1])

    def __exit__(self, *l):
        if self.importTopLevelPackage:
            self.frame.f_globals["__name__"] = self._name_
            if self._package_ is None:
                self.frame.f_globals.pop("__package__")
            else:
                self.frame.f_globals["__package__"] = self._package_


def import_by_path(pyPath):
    """
    import `.py` file or package by path, return a moudle object

    >>> module = import_by_path('far/away.py')
    """
    pyFile = pyPath
    assert os.path.isfile(pyFile) or os.path.isdir(pyFile), pyFile
    dirr = os.path.dirname(pyFile)
    import importlib

    try:
        sys.path.insert(0, dirr)
        module = importlib.import_module(os.path.basename(pyFile).replace(".py", ""))
        return module
    finally:
        assert sys.path.pop(0) == dirr


class syspath:
    """
    Temporary add the relative path to sys.path during with statement

    Usage：
        >>> with syspath(".."):
        >>>     import father_module

        >>> with syspath("/path/to/module/dir"):
        >>>     import module

    Parameters
    ----------
    relpath: str, List of str. default '.'
        The dir paths of the python file or package that you want to import
    """

    lock = Lock()  # ensure work fine in multi-threading

    def __init__(self, relpaths="."):
        frame = sys._getframe(1)
        _file_ = frame.f_globals.get("__file__", "python_shell.py")
        dirr = os.path.dirname(_file_)
        if isinstance(relpaths, str):
            relpaths = [relpaths]

        self.dirs = [
            os.path.abspath(os.path.join(dirr, os.path.expanduser(relpath)))
            for relpath in relpaths
        ]

    def __enter__(self):
        with self.lock:
            for d in self.dirs:
                sys.path.insert(0, d)

    def __exit__(self, *args):
        with self.lock:
            for d in self.dirs[::-1]:
                if sys.path[0] == d:
                    assert sys.path.pop(0) == d, "mximport.syspath error: " + d
                else:
                    ind = sys.path.index(d)
                    assert sys.path.pop(ind) == d, "mximport.syspath error: " + d
