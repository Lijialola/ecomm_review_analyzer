# Python Module Template Usage Guide (Legacy)

This project is a template for creating an installable Python module, based on traditional packaging practices using `setup.py` and `setup.cfg`. Its goal is to serve as a starting guide, showcasing a robust project structure, good practices, and common processes in a package's lifecycle.

## Getting Started

Follow these steps to use this template and start your own module.

### 1. Clone the Repository

Clone this repository to your local machine with the desired name for your new project:

```bash
git clone https://github.com/user/python-template.git my-new-module
cd my-new-module
```

### 2. Rename the Module

The main source code is located in the `module_name` folder. You should rename it to match your Python package's name.

```bash
mv ecomm_review_analyzer my_package
```

### 3. Update Package Metadata

Open the `my_package/__init__.py` file and edit the following fields with your information:

```python
# my_package/__init__.py

__author__ = "Your Name"
__email__ = "your_email@domain.com"
__version__ = "0.0.1"  # Or your preferred initial version

PACKAGE_NAME = "my_package" # Make sure it matches the new folder name.
```

The `setup.py` file will automatically read this information.

### 4. Update Version Configuration

The `setup.cfg` file is used to automate versioning with `bumpversion`. Make sure the path points to your new package directory.

**If you renamed `module_name` to `my_package`**, update `setup.cfg` as follows:

```ini
[bumpversion:file:my_package/__init__.py]
search = __version__ = "{current_version}"
replace = __version__ = "{new_version}"
```

### 5. Choose a License

This project includes "The Unlicense" by default (see `LICENSE` file), which dedicates the software to the public domain.

**Best practice:** Research which license suits your needs. `choosealicense.com` is an excellent resource. Once chosen, replace the content of the `LICENSE` file.

### 6. Install Dependencies

**Best practice:** It is highly recommended to use a virtual environment to isolate your project's dependencies.

```bash
# Create a virtual environment
python -m venv .venv

# Activate the environment (on macOS/Linux)
source .venv/bin/activate

# Activate the environment (on Windows)
.\.venv\Scripts\activate
```

Install dependencies and your package in editable mode. This will allow you to test your changes locally immediately.

```bash
# Install dependencies
pip install -r requirements_dev.txt
pip install -r requirements.txt

# Install the package in editable mode
pip install -e .
```

### 7. Start Coding!

Done! You can now start developing your module. Add your code inside the `my_package` folder.

---

## Code Quality and Automated Tasks with `Makefile`

To facilitate common tasks and maintain clean, consistent code, this template includes code quality tools and a `Makefile`.

### Code Quality Tools

-   **Ruff (`ruff`)**: An extremely fast Python linter and formatter. It helps detect errors, bad practices, and style issues.
-   **Black (`black`)**: An "uncompromising" code formatter that ensures a uniform style throughout the project.

These tools are configured in the `pyproject.toml` file.

### `Makefile` Commands

The `Makefile` contains shortcuts for the most common commands. To see all available commands, run `make help`.

-   `make install`: Creates a virtual environment (if it doesn't exist) and installs all dependencies. **This should be the first command you run.**
-   `make test`: Runs the test suite.
-   `make lint`: Checks code for errors and style issues with `ruff`.
-   `make format`: Formats all project code with `ruff` and `black`.
-   `make build`: Builds the package for distribution.
-   `make clean`: Removes all generated files (virtual environment, build artifacts, etc.).

---

## Testing with `pytest`

`pytest` is the de facto standard for testing in Python due to its simplicity and power.

**Writing Tests:**
Simply create functions that start with `test_` and use `assert` to check the results.

```python
# tests/test_main.py
from ecomm_review_analyzer.main import greet


def test_greet_with_name():
    """Tests that the function greets by name."""
    assert greet("Javi") == "Hello, Javi"
```

**Running Tests:**
Use the `Makefile` shortcut:
```bash
make test
```
Or run `pytest` directly:
```bash
pytest
```

---

## Semantic Versioning and `bumpversion`

Versioning (`MAJOR.MINOR.PATCH`) is managed with `bumpversion`, which is configured to update the version in `VERSION.txt` and in your `__init__.py`.

**Best practice:** Before bumping the version, make sure all your changes are committed to `git`.

```bash
# Bump a patch (e.g., from 0.0.1 to 0.0.2)
bumpversion patch

# Bump a minor version (e.g., from 0.0.2 to 0.1.0)
bumpversion minor

# Bump a major version (e.g., from 0.1.0 to 1.0.0)
bumpversion major
```

These commands automatically update the version in `VERSION.txt` and `__init__.py`, and create a `git commit` and `tag`.

---

## Packaging and Distribution

When your module is ready to be shared, you need to package it.

### 1. Build the Package

The following command generates two distribution formats in a new `dist/` folder:

-   **Wheel (`.whl`)**: A pre-compiled (binary) format that speeds up installation.
-   **Source Archive (`.tar.gz`)**: An archive containing the source code (`sdist`).

```bash
python setup.py sdist bdist_wheel
```

**Best practice:** This template's `.gitignore` file is already configured to ignore the `dist/`, `build/`, and `*.egg-info/` folders, which are generated during this process.

### 2. Local Installation from the Artifact

If you want to install your package locally to test the final artifact before publishing, you can use the generated `.whl` file. This is useful for testing the actual package installation in a clean environment.

```bash
# Make sure to activate your virtual environment if you are using one.
pip install dist/your_package-0.0.1-py3-none-any.whl
```
**Note:** Replace `your_package-0.0.1-py3-none-any.whl` with the exact name of the `.whl` file generated in your `dist/` folder.

### 3. Publish to PyPI

[PyPI (Python Package Index)](https://pypi.org/) is the official repository for Python packages. To publish your module, you will need the `twine` tool.

```bash
# Install twine if you don't have it
pip install twine
```

**Best practice:** Before publishing to the actual PyPI, it is recommended to test on [TestPyPI](https://test.pypi.org/), a separate testing environment.

```bash
# Publish to TestPyPI
twine upload --repository testpypi dist/*
```

When you are sure everything is correct, publish to the official PyPI:

```bash
# Publish to PyPI (official)
twine upload dist/*
```

Twine will ask for your PyPI username and password. And that's it, your package will be available for anyone to install with `pip`!

---

## Next Steps: Making the Project Your Own

Once you've configured and tested the template, it's time to make it your own. Here are some steps to clean up the example content and start with your own code:

1.  **Remove example code (`module_name/main.py`):**
    *   The `greet()` function and the `main()` entry point are just examples. Delete them and start writing your module's real functionality.

2.  **Delete example tests (`tests/test_main.py`):**
    *   This file contains tests for the `greet()` function. Delete this file or clear its content to start writing your own tests.

3.  **Update your changelog (`CHANGELOG.md`):**
    *   The `CHANGELOG.md` file is empty, ready for you to add your first entry.
    *   You can start with something like: `0.0.1 - YYYY-MM-DD: Initial project setup from template.`

4.  **Review the license (`LICENSE`):**
    *   Although already mentioned, make sure the `LICENSE` file contains the final license you wish to use for your project.
