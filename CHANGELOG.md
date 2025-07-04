## CHANGELOG: karpyncho-stdout-context

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

### [Unreleased]

#### Features

#### Bug Fixes

#### Changes

### [0.2.0] - 2025-06-04

#### Changes
 + type hints
 + drop python 3.9 support

### [0.1.2] - 2025-06-02

#### Bug Fixes
 + changed version number in pyproject.toml
 + changed dependencies section

### [0.1.1] - 2025-06-02

#### Features
 + added DateNumberSerializerMixin class

#### Bug Fixes
 + Optional[date] in DateSerializerMixin was not working
 + serialize "" as None in DateDMYSerializerMixin
 + serialize 0 as None in DateNumberSerializerMixin
 + typo in README.md

#### Changes
 + 

### [0.1.0] - 2025-05-10

* first version with
  + DateSerializerMixin and DateDMYSerializerMixin classes
  + all tests with 100% coverage

