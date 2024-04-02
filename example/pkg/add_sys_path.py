from mximport import syspath

with syspath(".."):  # relative path
    import pkg


print(pkg)
