# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog],
and this project adheres to [Semantic Versioning].

## [0.3.0] - 2025-12-18

### Added

- service providers section
- CORIMP search engine support (beta version)
- load_providers function
- load_streets function with new logic
- load_buildings function with new logic

### Changed

- UI: service providers
- UI: spacing of buttons
- UI: buttons labels
- UI: buttons sizes
- some file names

### Deprecated

- dl_buildings - old download buildings function
- dl_pdf - old pdf download fuction

### Removed

- maximize button in main window

### Fixed

- bad url in PDF download ProNatura_api.save_pdf function
- bad default exception text for ProNatura_api.save_pdf - replaced "Nie można pobrać numerów budynków." to "Nie można pobrać pliku PDF."

## [0.2.0] - 2025-12-17

### Added

- error & info dialogs
- exceptions for different API scenarios

### Changed

- github url for raising issues with the app
- log filename

### Fixed

- issues with not selected streets and buildings

## [0.1.0] - 2025-12-17

- initial release

<!-- Links -->
[keep a changelog]: https://keepachangelog.com/en/1.0.0/
[semantic versioning]: https://semver.org/spec/v2.0.0.html

<!-- Versions -->
[unreleased]: https://github.com/Author/Repository/compare/v0.0.2...HEAD
[0.0.2]: https://github.com/Author/Repository/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/Author/Repository/releases/tag/v0.0.1