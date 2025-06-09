# 🤝 Contributing to File Organizer

Thank you for your interest in contributing to File Organizer! This document provides guidelines and instructions for contributing to this project.

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guide](#style-guide)
- [Testing](#testing)
- [Documentation](#documentation)

## 📜 Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone. Please be kind and courteous to other contributors.

## 💡 How Can I Contribute?

### Reporting Bugs
- Check if the bug has already been reported in the Issues section
- Use the bug report template when creating a new issue
- Include detailed steps to reproduce the bug
- Provide screenshots if applicable
- Specify your operating system and Python version

### Suggesting Features
- Check if the feature has already been suggested
- Use the feature request template
- Provide a clear description of the feature
- Explain why this feature would be useful
- Include any relevant examples or mockups

### Pull Requests
- Fork the repository
- Create a new branch for your feature/fix
- Follow the style guide
- Add tests for new features
- Update documentation
- Submit a pull request

## 🛠️ Development Setup

1. Fork and clone the repository:
```bash
git clone https://github.com/yourusername/file-organizer.git
cd file-organizer
```

2. Create a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install development dependencies:
```bash
pip install pytest pytest-cov black flake8
```

## 🔄 Pull Request Process

1. Update the README.md with details of changes if needed
2. Update the documentation if you're changing functionality
3. The PR will be merged once you have the sign-off of at least one other developer
4. Make sure all tests pass before submitting

## 📝 Style Guide

### Python Code Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused
- Use type hints where appropriate

Example:
```python
def organize_files(source_path: str, date_based: bool = False) -> None:
    """
    Organize files in the specified directory.

    Args:
        source_path (str): Path to the directory containing files
        date_based (bool): Whether to organize by date

    Returns:
        None
    """
    # Implementation
```

### Commit Messages
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally

Example:
```
feat: Add dark mode support

- Implement dark theme toggle
- Add theme persistence
- Update documentation

Closes #123
```

## 🧪 Testing

1. Run the test suite:
```bash
pytest
```

2. Check test coverage:
```bash
pytest --cov=file_organizer
```

3. Write tests for new features:
- Create test files in the `tests` directory
- Name test files with `test_` prefix
- Use descriptive test names
- Test both success and failure cases

## 📚 Documentation

### Code Documentation
- Add docstrings to all functions and classes
- Use Google style docstrings
- Include type hints
- Document complex algorithms

### User Documentation
- Update README.md for user-facing changes
- Add comments for complex UI elements
- Document new features in the appropriate sections
- Keep the documentation up to date

## 🎯 Project Structure

```
file-organizer/
├── file_organizer.py      # Main application file
├── requirements.txt       # Project dependencies
├── README.md             # Project documentation
├── CONTRIBUTING.md       # Contributing guidelines
├── tests/                # Test directory
│   └── test_*.py        # Test files
└── docs/                 # Additional documentation
```

## 🔍 Code Review Process

1. All submissions require review
2. Reviewers will look for:
   - Code quality and style
   - Test coverage
   - Documentation
   - Performance considerations
   - Security implications

## 🚀 Getting Help

- Open an issue for bugs or feature requests
- Join our community chat (if available)
- Check existing documentation
- Review closed issues and pull requests

## 📄 License

By contributing to File Organizer, you agree that your contributions will be licensed under the project's MIT License.

---

Thank you for contributing to File Organizer! 🎉

Made with ❤️ by Aakash Sharma 