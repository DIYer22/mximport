# `mximport`: Remove all limits on Python package imports 🚀

```bash
pip install mximport
```
## ▮ Painless Relative Import

Relative imports in Python can become annoying because they prevent the current code from being run directly.  
For example:
```python
# pkg/main.py
from .utils import *

if __name__ == "__main__":
    print("This is the main file")
```
Run bash
```bash
~/pkg$ tree .
pkg/
├── __init__.py
├── main.py
└── utils.py

~/pkg$ python main.py
Traceback (most recent call last):
  File "~/pkg/main.py", line 1, in <module>
    from .utils import *
ImportError: attempted relative import with no known parent package
```

`mximport.inpkg()` can remove this limitation:

```python
# pkg/main.py
from mximport import inpkg
with inpkg():
    from .utils import *

if __name__ == "__main__":
    print("This is the main file")
```
Then every thing is OK! Say goodbye to `python -m pkg.main`


## ▮ Temporary add relative path in sys.path

Temporary add the relative path to sys.path during with statement

Usage：
```python
from mximport import syspath
with syspath(".."):  # relative path
    import father_module

with syspath("/abspath/to/module/dir"):
    import module
```

## ▮ Import by Path

import `.py` file or package by path, return a moudle object
```python
from mximport import import_by_path

module = import_by_path('/path/to/module.py')
pkg = import_by_path('/path/to/pkg')
```
