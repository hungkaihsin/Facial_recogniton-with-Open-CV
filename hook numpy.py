
# -----------------------------------------------------------------------------
# Copyright (c) 2013-2021, PyInstaller Development Team.
#!/usr/bin/env python3

# --- Copyright Disclaimer ---
#
# In order to support PyInstaller with numpy<1.20.0 this file will be
# duplicated for a short period inside PyInstaller's repository [1]. However
# this file is the intellectual property of the NumPy team and is under the
# terms and conditions outlined their repository [2].
#
# Distributed under the terms of the GNU General Public License (version 2
# or later) with exception for distributing the bootloader.
# .. refs:
#
# The full license is in the file COPYING.txt, distributed with this software.
#   [1] PyInstaller: https://github.com/pyinstaller/pyinstaller/
#   [2] NumPy's license: https://github.com/numpy/numpy/blob/master/LICENSE.txt
#
# SPDX-License-Identifier: (GPL-2.0-or-later WITH Bootloader-exception)
# -----------------------------------------------------------------------------

import os
import glob
from PyInstaller.compat import is_win, is_venv, base_prefix
from PyInstaller.utils.hooks import get_module_file_attribute

# numpy.testing is unconditionally imported by numpy, thus we can not exclude
# .testing (which would be preferred). Anyway, this only saves about 7
# modules. See also https://github.com/numpy/numpy/issues/17183
#excludedimports = ["numpy.testing"]

# FIXME check if this workaround is still necessary!
if is_win:
    from PyInstaller.utils.win32.winutils import extend_system_path
    from distutils.sysconfig import get_python_lib
    # SciPy/Numpy Windows builds from http://www.lfd.uci.edu/~gohlke/pythonlibs
    # contain some dlls in directory like C:\Python27\Lib\site-packages\numpy\core\
    numpy_core_paths = [os.path.join(get_python_lib(), 'numpy', 'core')]
    # In virtualenv numpy might be installed directly in real prefix path.
    # Then include this path too.
    if is_venv:
        numpy_core_paths.append(
            os.path.join(base_prefix, 'Lib', 'site-packages', 'numpy', 'core')
        )
    extend_system_path(numpy_core_paths)
    del numpy_core_paths

# if we bundle the testing module, this will cause
# `scipy` to be pulled in unintentionally but numpy imports
# numpy.testing at the top level for historical reasons.
# excludedimports = collect_submodules('numpy.testing')

binaries = []

# package the DLL bundle that official numpy wheels for Windows ship
# The DLL bundle will either be in extra-dll on windows proper
# and in .libs if installed on a virtualenv created from MinGW (Git-Bash
# for example)
if is_win:
    extra_dll_locations = ['extra-dll', '.libs']
    for location in extra_dll_locations:
        dll_glob = os.path.join(os.path.dirname(
            get_module_file_attribute('numpy')), location, "*.dll")
        if glob.glob(dll_glob):
            binaries.append((dll_glob, "."))
"""
This hook should collect all binary files and any hidden modules that numpy
needs.
Our (some-what inadequate) docs for writing PyInstaller hooks are kept here:
https://pyinstaller.readthedocs.io/en/stable/hooks.html
PyInstaller has a lot of NumPy users so we'd consider maintaining this hook to
be high priority. Feel free to @mention either bwoodsend or Legorooj on Github
for help keeping it working.
"""

from PyInstaller.utils.hooks import collect_dynamic_libs
from PyInstaller.compat import is_conda, is_pure_conda

# Collect all DLLs inside numpy's installation folder, dump them into built
# app's root.
binaries = collect_dynamic_libs("numpy", ".")

# If using Conda without any non-conda virtual environment manager:
if is_pure_conda:
    # Assume running the NumPy from Conda-forge and collect it's DLLs from the
    # communal Conda bin directory. DLLs from NumPy's dependencies must also be
    # collected to capture MKL, OpenBlas, OpenMP, etc.
    from PyInstaller.utils.hooks import conda_support
    datas = conda_support.collect_dynamic_libs("numpy", dependencies=True)

# Submodules PyInstaller can't detect (probably because they're only imported
# by extension modules which PyInstaller can't read).
hiddenimports = ['numpy.core._dtype_ctypes']
if is_conda:
    hiddenimports.append("six")

# Remove testing and building code and packages which are referenced throughout
# NumPy but aren't really dependencies.
excludedimports = [
    "scipy",
    "pytest",
    "nose",
    "distutils",
    "f2py",
    "setuptools",
    "numpy.f2py",
    "numpy.distutils",
]