# Contributing to HenryCat

Thank you for your interest in contributing to HenryCat! This document provides guidelines and instructions for contributing.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear, descriptive title
- Steps to reproduce the bug
- Expected vs actual behavior
- Screenshots (if applicable)
- Your environment (OS, Python version, etc.)

### Suggesting Features

We welcome feature suggestions! Please create an issue with:
- Clear description of the feature
- Use cases and benefits
- Possible implementation approach (optional)

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feat/your-feature-name
   ```

3. **Make your changes**
   - Follow the code style guidelines
   - Add tests if applicable
   - Update documentation

4. **Commit your changes**
   - Follow the commit convention (see below)
   ```bash
   git commit -m "feat: add amazing feature"
   ```

5. **Push to your fork**
   ```bash
   git push origin feat/your-feature-name
   ```

6. **Open a Pull Request**
   - Provide a clear description
   - Reference any related issues
   - Wait for review

## 📝 Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <description>

[optional body]

[optional footer]
```

### Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only changes
- `refactor`: Code refactoring (no feature change)
- `test`: Adding or updating tests
- `chore`: Maintenance tasks, dependencies

### Examples:
```
feat: add password strength indicator to Henry Vault
fix: resolve poster generation error for video files
docs: update installation instructions for Windows
refactor: optimize AI embedding generation
test: add unit tests for scanner categorization
chore: update dependencies to latest versions
```

## 🎨 Code Style

### Python
- Follow [PEP 8](https://pep8.org/)
- Use `black` for formatting
- Use `flake8` for linting
- Maximum line length: 88 characters

```bash
# Format code
black .

# Check linting
flake8 .
```

### Documentation
- Use clear, concise language
- Add docstrings to all functions/classes
- Update README.md if adding features

```python
def example_function(param: str) -> dict:
    """
    Brief description of what this function does.
    
    Args:
        param: Description of the parameter
        
    Returns:
        Description of return value
    """
    pass
```

## 🧪 Testing

- Add tests for new features
- Ensure existing tests pass
- Aim for good test coverage

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=.
```

## 📁 Project Structure

```
HenryCat/
├── ai_engine.py          # AI RAG system
├── app.py                # FastAPI application
├── database.py           # Database operations
├── main.py               # Core logic
├── scanner.py            # File scanner
├── tests/                # Test files
│   ├── test_scanner.py
│   ├── test_database.py
│   └── test_ai_engine.py
└── docs/                 # Additional documentation
```

## 🔍 Code Review Process

1. Maintainers will review your PR
2. Address any feedback or requested changes
3. Once approved, your PR will be merged
4. Your contribution will be credited

## 📋 Development Setup

1. **Clone your fork**
   ```bash
   git clone https://github.com/your-username/HenryCat.git
   cd HenryCat
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Dev dependencies
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

## 🌟 Recognition

All contributors will be:
- Listed in the README.md Contributors section
- Mentioned in release notes
- Credited in commit history

## 💬 Communication

- **Issues**: For bugs and feature requests
- **Discussions**: For questions and ideas
- **Pull Requests**: For code contributions

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to HenryCat! 🐱
