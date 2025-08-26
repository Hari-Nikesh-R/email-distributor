# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup
- Bulk email sending functionality
- HTML template support with Jinja2
- Embedded image support
- File attachment support
- Gmail SMTP integration
- Rate limiting and progress tracking
- Comprehensive documentation
- MIT License
- Contributing guidelines
- Code of Conduct
- Python packaging support

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- N/A

## [1.0.0] - 2024-01-01

### Added
- Initial release of Email Sender
- Core bulk email functionality
- Template system with Jinja2
- Asset and attachment management
- Gmail SMTP integration
- Comprehensive documentation
- Open source licensing (MIT)
- Contributing guidelines and Code of Conduct

---

## Version History

### Version 1.0.0
- **Release Date**: 2024-01-01
- **Status**: Initial Release
- **Features**:
  - Bulk email sending via Gmail SMTP
  - HTML template support with dynamic content
  - Embedded images from assets folder
  - File attachments from attachments folder
  - Rate limiting to avoid spam filters
  - Progress tracking and error handling
  - Comprehensive documentation and examples
  - Open source licensing and contribution guidelines

---

## Contributing to Changelog

When adding entries to the changelog, please follow these guidelines:

1. **Use the present tense** ("Add feature" not "Added feature")
2. **Use the imperative mood** ("Move cursor to..." not "Moves cursor to...")
3. **Reference issues and pull requests** liberally after the applicable entry
4. **Consider including credit to external contributors** in the changelog

### Categories

- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** in case of vulnerabilities

### Example Entry

```markdown
## [1.1.0] - 2024-02-01

### Added
- Support for multiple email templates (#123)
- Custom SMTP server configuration (#124)

### Fixed
- Template rendering with special characters (#125)
- Memory leak in bulk sending (#126)

### Security
- Updated dependencies to fix CVE-2024-XXXX (#127)
```
