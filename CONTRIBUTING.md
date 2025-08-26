# Contributing to Email Sender

Thank you for your interest in contributing to the Email Sender project! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

### Our Standards

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## How Can I Contribute?

### Reporting Bugs

- Use the GitHub issue tracker
- Include detailed steps to reproduce the bug
- Provide your operating system and Python version
- Include error messages and stack traces
- Describe the expected behavior vs actual behavior

### Suggesting Enhancements

- Use the GitHub issue tracker
- Clearly describe the enhancement
- Explain why this enhancement would be useful
- Include mockups or examples if applicable

### Pull Requests

- Fork the repository
- Create a feature branch
- Make your changes
- Add tests if applicable
- Update documentation
- Submit a pull request

## Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/email_sender.git
   cd email_sender
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Development Dependencies**
   ```bash
   pip install pytest black flake8 mypy
   ```

5. **Set up Environment Variables**
   ```bash
   cp env_example.txt .env
   # Edit .env with your test Gmail credentials
   ```

## Coding Standards

### Python Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use 4 spaces for indentation
- Maximum line length of 88 characters (Black formatter)
- Use meaningful variable and function names

### Code Formatting

We use [Black](https://black.readthedocs.io/) for code formatting:

```bash
black email_sender.py test_setup.py
```

### Linting

We use [flake8](https://flake8.pycqa.org/) for linting:

```bash
flake8 email_sender.py test_setup.py
```

### Type Checking

We use [mypy](http://mypy-lang.org/) for type checking:

```bash
mypy email_sender.py test_setup.py
```

### Documentation

- Add docstrings to all functions and classes
- Use Google-style docstrings
- Include type hints for function parameters and return values
- Update README.md for new features

Example docstring:
```python
def send_email(self, recipient_data: dict) -> bool:
    """Send a single email to a recipient.
    
    Args:
        recipient_data: Dictionary containing recipient information
                       with keys 'email', 'name', 'company'
    
    Returns:
        bool: True if email sent successfully, False otherwise
    
    Raises:
        SMTPException: If email sending fails
    """
```

## Testing

### Running Tests

```bash
# Run the setup test
python test_setup.py

# Run with pytest (if you add pytest tests)
pytest tests/
```

### Writing Tests

- Create tests for new features
- Ensure good test coverage
- Use descriptive test names
- Mock external dependencies (like SMTP)

Example test:
```python
def test_send_email_success():
    """Test successful email sending."""
    sender = BulkEmailSender()
    recipient = {
        'email': 'test@example.com',
        'name': 'Test User',
        'company': 'Test Company'
    }
    result = sender.send_email(recipient)
    assert result is True
```

## Pull Request Process

1. **Update Documentation**
   - Update README.md if needed
   - Add docstrings to new functions
   - Update any relevant documentation

2. **Test Your Changes**
   - Run the test suite
   - Test manually with your Gmail account
   - Ensure no new linting errors

3. **Submit Pull Request**
   - Use a descriptive title
   - Include a detailed description
   - Reference any related issues
   - Include screenshots if UI changes

4. **Review Process**
   - Address any review comments
   - Make requested changes
   - Ensure CI checks pass

## Security Considerations

When contributing, please be mindful of security:

- Never commit sensitive information (passwords, API keys)
- Use environment variables for configuration
- Validate all user inputs
- Follow secure coding practices
- Report security vulnerabilities privately

## Email Best Practices

When contributing email-related features:

- Respect email regulations (CAN-SPAM, GDPR, etc.)
- Include unsubscribe mechanisms
- Use proper email headers
- Implement rate limiting
- Add error handling for email failures

## Getting Help

If you need help with contributing:

1. Check existing issues and pull requests
2. Read the documentation
3. Ask questions in issues
4. Join our community discussions

## Recognition

Contributors will be recognized in:
- The project README
- Release notes
- GitHub contributors page

Thank you for contributing to Email Sender! 🚀
