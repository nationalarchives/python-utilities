# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased](https://github.com/nationalarchives/python-utilities/compare/v1.9.0...HEAD)

### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security

## [1.9.0](https://github.com/nationalarchives/python-utilities/compare/v1.8.0...v1.9.0) - 2026-08-26

### Changed

- `CspGenerator.sandbox()` now accepts multiple parameters

### Fixed

- Fixed issue adding `sandbox` CSP directive through Flask Talisman

## [1.8.0](https://github.com/nationalarchives/python-utilities/compare/v1.7.0...v1.8.0) - 2026-08-19

### Added

- Added `tna_frontend_pagination()` to `tna_utilities.component` to generate the entire content block required for [TNA Frontend pagination components](https://design-system.nationalarchives.gov.uk/components/pagination/)

### Changed

- `QueryStringTransformer` is now read-only - to modify query strings, create a new editable object with `new()`

## [1.7.0](https://github.com/nationalarchives/python-utilities/compare/v1.6.0...v1.7.0) - 2026-08-19

### Added

- `QueryStringTransformer` now has a `tolerant` option which doesn't raise exceptions for missing keys

## [1.6.0](https://github.com/nationalarchives/python-utilities/compare/v1.5.0...v1.6.0) - 2026-08-04

### Added

- Added `vary_by_cookies()` and `vary_by_headers()` decorators for Flask
- Added `cacheable_duration_cloudfront()` decorator for adding `Cache-Control` headers that are Cloudfront compatible

### Changed

- Removed the trailing semicolon from CSP strings
- Added some missing `int` into function parameter types

## [1.5.0](https://github.com/nationalarchives/python-utilities/compare/v1.4.0...v1.5.0) - 2026-05-14

### Added

- Added option in Flask Talisman to add Adobe Typekit CSP rules with `allow_typekit_content_security_policy=True`
- Added `extra_headers` parameter in `Talisman` to update or add any global response headers
- New pagination functions for populating pagination components
- New Flask decorators for specifying `Cache-Control` headers in response

### Changed

- Updated Google CSP domains
- Switched to checking response codes from `requests` in `SimpleJsonApiClient`
- Renamed `ResourceForbidden`, `ResourceNotFound` and `ResourceUnauthorized` to `ResourceForbiddenError`, `ResourceNotFoundError` and `ResourceUnauthorizedError` in `tna_utilities.api`
- `SimpleJsonApiClient` raises `ApiError` exceptions rather than generic `Exception`
- Renamed the `bytes` parameter of `pretty_file_size()` to `filesize_bytes`

### Removed

- Removed `security_headers` parameter in `Talisman`

### Fixed

- Fixed logic inversion for `default_headers` in `SimpleJsonApiClient`
- Incorrect `ValueError` exceptions changed to `TypeError`

## [1.4.0](https://github.com/nationalarchives/python-utilities/compare/v1.3.0...v1.4.0) - 2026-04-14

### Added

- CSP directives are appended by default with the option to be overwritten
- Flask Talisman module added `tna_utilities.flask.talisman`
- Added ability to show seconds in `pretty_datetime` and `pretty_datetime_range`
- Added a new basic API client

### Changed

- Added a default of `object-src 'none'` to the `CspGenerator`
- Renamed `security_headers` function to `common_security_headers`
- Updated `CspGenerator.get_csp()` method to `CspGenerator.to_string()`
- Moved the simplification step of generating a CSP string to the `to_string()` method
- By default, disallow `frame-ancestors` and `child-src` in CSP
- `datetime.group_by_year_and_month` now accepts a list of items rather than a dict that requires an `items` key

### Removed

- Removed support for deprecated `X-Frame-Options` header in `common_security_headers`

### Fixed

- Handle empty lists for initialisation of `CspGenerator`
- Don't add `report-to` or `report-uri` for blank strings in `CspGenerator`
- Time comparisons fixed for datetimes with timezones other than UTC in `pretty_age()`

## [1.3.0](https://github.com/nationalarchives/python-utilities/compare/v1.2.0...v1.3.0) - 2026-01-02

### Added

- Added a `security` module with `CspGenerator` and `security_headers` functionality
- Added `pretty_file_size` function to `numbers` module

### Fixed

- Date functions fixed to work with Windows' C runtime

## [1.2.0](https://github.com/nationalarchives/python-utilities/compare/v1.1.0...v1.2.0) - 2026-01-02

### Added

- Allow `QueryStringTransformer` to be instantiated with a list of tuples or an empty query object
- Add `pretty_age` to show human-readable deltas (e.g. `3 days ago`)
- Add `numbers` module with `numberish` function to provide human-readable approximate numbers (e.g. `About 120 million`)

### Changed

- Transformations to non-existent keys in `QueryStringTransformer` now throw `KeyError` rather than `AttributeError`
- If there is an empty query string, `QueryStringTransformer` returns a blank string rather than an empty `?`

## [1.1.0](https://github.com/nationalarchives/python-utilities/compare/v1.0.0...v1.1.0) - 2025-12-15

### Changed

- Allow functions in `QueryStringTransformer` to be chained

## [1.0.0](https://github.com/nationalarchives/python-utilities/releases/tag/v1.0.0) - 2025-12-05

Initial release
