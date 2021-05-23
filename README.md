# Hermetic Python in Bazel

This repo demonstrates how to build a python interpreter from source and use it
in bazel as a toolchain.

# Features

- Use the same python version across all devs working on the same workspace.
- No need to depend on the local python version.
- Don't need to check in pre-compiled python interpreter binaries.
- Support `pip_import` from [rules_python](https://github.com/bazelbuild/rules_python).
- Support for building a docker image using
  [`py3_image`](https://github.com/bazelbuild/rules_docker#py3_image).

# Local Binary Demo

Environment:
- Ubuntu 18.04.4
- Bazel version: 2.2.0
- Host python3 version: 3.6.9
- Custom python3 version (from WORKSPACE): 3.8.3

```shell
$ bazel run //:main
=== Bazel Python ===
/home/kku/.cache/bazel/_bazel_kku/8646bea57e4c755fe6c60a8ab13b2451/execroot/py_test/bazel-out/k8-fastbuild/bin/main.runfiles/python_interpreter/python_bin
3.8.3 (default, Jan  1 1970, 00:00:00)
[GCC 9.3.0]
=== Host Python ===
/usr/bin/python3
3.8.5 (default, Jan 27 2021, 15:41:15)
[GCC 9.3.0]
=== Pip Package ===
Successfully imported psycopg2-binary!
```

# py_test demo

```
bazel test //:main_test
```

# Docker Image Demo

The image we're using is `python3:3.8.3-slim-buster`, which matches the python
version of our custom-built python interpreter. Our `main.py` running inside the
container should use the image's python interpreter.

```shell
$ bazel run //:main_image
Loaded image ID: sha256:3d082aa60d5e241c868a354a90515ad11350b624b39f11f2806728dbc1e65a6e
Tagging 3d082aa60d5e241c868a354a90515ad11350b624b39f11f2806728dbc1e65a6e as bazel:main_image
Bazel python executable is /usr/bin/python3
Bazel python version is 3.8.3
Host python executable is /usr/local/bin/python3
Host python version is 3.8.3
Successfully imported psycopg2-binary!
```

# Explanation

1. Download and build python 3.8.3 interpreter from source using
  `http_archive` in `WORKSPACE`.
1. Create `py_runtime` and `toolchain` in `BUILD.bazel` to use the python
   3.8.3 interpreter we've just built.
1. Register the toolchain in `WORKSPACE` such that all python targets
   automatically use our custom interpreter.
1. Configure `pip_import` to use our custom interpreter to ensure the
   imported packages are compatible.
1. To build a docker image:
    - Fetch an official python image verion that matches the version we've built
      (e.g. `python3:3.8.3-slim-buster` for `python3.8.3`).
    - Modify the official image to create symlink to `/usr/local/bin/python`
      from `/usr/bin/python3`. This is for compatibility with "host" python
      toolchain (see below).
    - Install external dependencies using `pip` (or any other tool) inside the
      container image to ensure python version matches.
    - Use the fetched image as base for
      [`py3_image`](https://github.com/bazelbuild/rules_docker#py3_image) rule
      since `py3_image` defaults to something like `python3.5` from
      [distroless](https://github.com/googlecloudplatform/distroless).
    - We must register our custom python tool chain LAST in order for the
      container image to pick the "host" toolchain (e.g. `/usr/bin/python3`) and
      use it in the image instead of our local copy (e.g.
      `/home/kku/.cache/bazel/_bazel_kku/.../main.runfiles/python_interpreter/python_bin`).

# Note for macOS

In order to build python with SSL support, this demo assumes that you have
installed `openssl` via `homebrew`. If not, you'll likely get this error from
`pip_import`:

```
pip Can't connect to HTTPS URL because the SSL module is not available.
```

For more information, see
[https://devguide.python.org/setup/#macos-and-os-x](https://devguide.python.org/setup/#macos-and-os-x).
