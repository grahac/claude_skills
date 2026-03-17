# Changelog Format Reference

## File Structure

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New feature description

## [1.2.0] - 2026-02-22

### Fixed
- Bug description

[Unreleased]: https://github.com/owner/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/owner/repo/compare/v1.1.0...v1.2.0
```

## Version Comparison Links

When cutting a release, update the links at the bottom:

```markdown
[Unreleased]: https://github.com/owner/repo/compare/vX.Y.Z...HEAD
[X.Y.Z]: https://github.com/owner/repo/compare/vPREVIOUS...vX.Y.Z
```

Get the remote URL from `git remote get-url origin` — never guess it.
