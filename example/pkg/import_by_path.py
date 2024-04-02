from mximport import import_by_path

pkg = import_by_path("../pkg")
print(pkg)

main2 = import_by_path("../pkg/main2.py")
print(main2)
