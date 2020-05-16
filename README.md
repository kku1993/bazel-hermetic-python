# Introduction

This repo demonstrates how to build a python interpreter from source and use it
in bazel as a toolchain.

The repo also showcases how this setup can work with `pip_import` from
[rules_python](https://github.com/bazelbuild/rules_python).

Advantages of this approach:
- No need to depend on the local python version.
- Don't need to check in pre-compiled python interpreter binaries.

# Explanation

1. Download and build python 3.8.3 interpreter from source using
  `http_archive` in `WORKSPACE`.
1. Create `py_runtime` and `toolchain` in `BUILD.bazel` to use the python
   3.8.3 interpreter we've just built.
1. Register the toolchain in `WORKSPACE` such that all python targets
   automatically use our custom interpreter.
1. Configure `pip_import` to use our custom interpreter to ensure the
   imported packages are compatible.

# Note for macOS

In order to build python with SSL support, this demo assumes that you have
installed `openssl` via `homebrew`. If not, you'll likely get this error from
`pip_import`:

```
pip Can't connect to HTTPS URL because the SSL module is not available.
```

For more information, see
[https://devguide.python.org/setup/#macos-and-os-x](https://devguide.python.org/setup/#macos-and-os-x).

# Demo

Environment:
- Ubuntu 18.04.4
- Host python3 version: 3.6.9
- Bazel version: 2.2.0

```shell
$ bazel run //:main
Bazel python executable is /home/kku/.cache/bazel/_bazel_kku/d727175bc5d0ccda8e0f97f510a8a329/execroot/py_test/bazel-out/k8-fastbuild/bin/main.runfiles/python_interpreter/python_bin
Bazel python version is 3.8.3
Host python executable is /usr/bin/python3
Host python version is 3.6.9
Successfully imported psycopg2-binary!
```
