workspace(name="py_test")

load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

# Special logic for building python interpreter with OpenSSL from homebrew.
# See https://devguide.python.org/setup/#macos-and-os-x
_py_configure = """
if [[ "$OSTYPE" == "darwin"* ]]; then
    ./configure --prefix=$(pwd)/bazel_install --with-openssl=$(brew --prefix openssl)
else
    ./configure --prefix=$(pwd)/bazel_install
fi
"""

http_archive(
    name = "python_interpreter",
    urls = ["https://www.python.org/ftp/python/3.8.3/Python-3.8.3.tar.xz"],
    sha256 = "dfab5ec723c218082fe3d5d7ae17ecbdebffa9a1aea4d64aa3a2ecdd2e795864",
    strip_prefix = "Python-3.8.3",
    patch_cmds = [
        "mkdir $(pwd)/bazel_install",
        _py_configure,
        # Produce deterministic binary by using a fixed build timestamp and
        # running `ar` in deterministic mode. See #7
        "SOURCE_DATE_EPOCH=0 make -j $(nproc) ARFLAGS='rvD'",
        "make install",
        "ln -s bazel_install/bin/python3 python_bin",
    ],
    build_file_content = """
exports_files(["python_bin"])

filegroup(
    name = "files",
    srcs = glob(["bazel_install/**"], exclude = ["**/* *"]),
    visibility = ["//visibility:public"],
)
""",
)

git_repository(
    name = "rules_python",
    remote = "https://github.com/bazelbuild/rules_python.git",
    commit = "06672cd470ce513a256c7ef2dbb8497a0f5502f3",
)

load("@rules_python//python:repositories.bzl", "py_repositories")

py_repositories()

load("@rules_python//python:pip.bzl", "pip_repositories")

pip_repositories()

load("@rules_python//python:pip.bzl", "pip_import")

pip_import(
    name = "py_deps",
    requirements = "//:requirements.txt",
    python_interpreter_target = "@python_interpreter//:python_bin",
)

load("@py_deps//:requirements.bzl", "pip_install")

pip_install()

####################
# rules_docker
####################

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "io_bazel_rules_docker",
    sha256 = "3efbd23e195727a67f87b2a04fb4388cc7a11a0c0c2cf33eec225fb8ffbb27ea",
    strip_prefix = "rules_docker-0.14.2",
    urls = ["https://github.com/bazelbuild/rules_docker/releases/download/v0.14.2/rules_docker-v0.14.2.tar.gz"],
)

load(
    "@io_bazel_rules_docker//repositories:repositories.bzl",
    container_repositories = "repositories",
)
container_repositories()

load("@io_bazel_rules_docker//repositories:deps.bzl", container_deps = "deps")

container_deps()

load(
    "@io_bazel_rules_docker//container:container.bzl",
    "container_pull",
)

# Python image version must match the python interpreter version in
# @python_interpreter http_archive in order for dependencies imported by
# pip_import to have the right version.
container_pull(
    name = "python3.8.3_slim_buster",
    registry = "docker.io",
    repository = "library/python",
    digest = "sha256:bad43dc620ed7f3bc085782b63c6cc0f307819af41b0ebfecb8457c82abc7f99",  # 3.8.3-slim-buster
)

load("@io_bazel_rules_docker//python3:image.bzl", _py3_image_repos = "repositories")

_py3_image_repos()

####################
# rules_pkg
####################

http_archive(
    name = "rules_pkg",
    urls = [
        "https://github.com/bazelbuild/rules_pkg/releases/download/0.2.5/rules_pkg-0.2.5.tar.gz",
        "https://mirror.bazel.build/github.com/bazelbuild/rules_pkg/releases/download/0.2.5/rules_pkg-0.2.5.tar.gz",
    ],
    sha256 = "352c090cc3d3f9a6b4e676cf42a6047c16824959b438895a76c2989c6d7c246a",
)
load("@rules_pkg//:deps.bzl", "rules_pkg_dependencies")
rules_pkg_dependencies()

# Our custom python toolchain must be registered at the end in order for python
# container images built with @python3.8.3_slim_buster as the base to use the
# "host" toolchain rather than the one with our locally compiled interpreter.
# See:
# https://docs.bazel.build/versions/master/toolchains.html#toolchain-resolution
register_toolchains("//:my_py_toolchain")
