# Introduction

This repo demonstrates how to build a python interpreter from source and use it
in bazel as a toolchain.

The repo also showcases how this setup can work with `pip_import` from
[rules_python](https://github.com/bazelbuild/rules_python).

Advantages of this approach:
- No need to depend on the local python version.
- Don't need to check in pre-compiled python interpreter binaries.

# Explanation

1. We download and build python 3.8.3 interpreter from source using
  `http_archive` in `WORKSPACE`.
1. We create `py_runtime` and `toolchain` in `BUILD.bazel` to use the python
   3.8.3 interpreter we've just built.
1. We register the toolchain in `WORKSPACE` such that all python targets
   automatically use our custom interpreter.
1. We configure `pip_import` to use our custom interpreter to ensure the
   imported packages are compatible.

# Demo

Running on Ubuntu 18.04.4 with default python3 version being 3.6.9:

```shell
$ bazel run //:main
My python executable is /home/kku/.cache/bazel/_bazel_kku/d727175bc5d0ccda8e0f97f510a8a329/execroot/py_test/bazel-out/k8-fastbuild/bin/main.runfiles/python_interpreter/python
My python version is 3.8.3
The host's python executable is b'/usr/bin/python3\n'
The host's python version is b'Python 3.6.9\n'
```
