# from .folder.file import func\class
#        or
# from .folder import file
# will make the func\class\file obj to be accessible as STARK.obj

from .field import FieldElement

print("loaded package STARK")

# to run the tests, enter
# (for a single test) pytest STARK/tests/test_field.py::test_eq()
#   or
# (for a single file) pytest STARK/tests/test_field.py
#   or
# (for all files) pytest STARK/tests/*.py
