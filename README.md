mister
======

Mister is a Python library for parsing files in MIST format [1]. The
library creates an abstract syntax tree of the input and optionally
converts it to a Petri net coverability or reachability problem instance.

There's one limitation: it does not support inputs that define transfer
arcs.

Install it by running:

python setup.py build
python setup.py install

---

[1] https://github.com/pierreganty/mist

