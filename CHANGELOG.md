# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased](https://github.com/nationalarchives/python-utilities/compare/v1.1.0...HEAD)

### Added

- Allow `QueryStringTransformer` to be instantiated with a list of tuples or an empty query object
- Add `pretty_age` to show human-readable deltas (e.g. `3 days ago`)
- Add `numbers` module with `numberish` function to provide human-readable approximate numbers (e.g. `About 120 million`)

### Changed

- Transformations to non-existent keys in `QueryStringTransformer` now throw `KeyError` rather than `AttributeError`

### Deprecated

### Removed

### Fixed

### Security

## [1.1.0](https://github.com/nationalarchives/python-utilities/compare/v1.0.0...v1.1.0) - 2025-12-15

### Changed

- Allow functions in `QueryStringTransformer` to be chained

## [1.0.0](https://github.com/nationalarchives/python-utilities/releases/tag/v1.0.0) - 2025-12-05

Initial release
