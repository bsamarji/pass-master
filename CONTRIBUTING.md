## 🤝 Contributing

Contributions are welcome — whether it's bug reports, new ideas, or pull requests.

If you're planning a substantial change, please open an issue first so we can discuss the approach.

### 👉 How to Contribute

1. **Fork** the repository  
2. **Create a branch** for your feature or fix  
3. **Commit** your changes with clear messages  
4. **Open a Pull Request**  
5. Wait for review and feedback

### 🧹 Code Style and Linting

Keepr uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting, and [pre-commit](https://pre-commit.com/) to ensure consistent code quality across all contributions.

Before contributing any code, please ensure you have the project’s development tooling set up.

#### 1. Install development tools

```bash
pip install ruff pre-commit
```

or if you're using uv:

```bash
uv pip install ruff pre-commit
```

#### 2. Install the pre-commit hook

This ensures all linting and formatting checks run automatically whenever you make a commit:

```bash
pre-commit install
```

After installing, every git commit will automatically:

* Run Ruff linting (ruff check)
* Run Ruff formatting (ruff format)
* Prevent commits that violate the project’s style rules

#### 3. Running checks manually

Run all the commands below in the **root** of the project directory.

To check the entire codebase at once:

```bash
ruff check .
```

To auto-fix everything ruff can fix:

```bash
ruff check --fix .
```

To format all files:

```bash
ruff format .
```

To run all pre-commit hooks without committing:

```bash
pre-commit run --all-files
```

#### 4. File types covered

**Covered:**

* Python (.py) files: fully linted and autoformatted
* TOML (pyproject.toml, ruff.toml): formatted by Ruff where applicable

**Not Covered:**

* YAML: Ruff doesn't have native support for yaml files - most of the yaml files are small, mainly for GitHub action workflows and can be formatted manually.
* Markdown: Needs specific manaul formatting for MkDocs, so is best left excluded from ruff.

---

## 👨‍🔧 Support

If you run into problems, the best way to get help is through the GitHub issue tracker.

- 🐛 **Bug Reports:**  
  Tag the issue with the `bug` label and include steps to reproduce.

- 💡 **Feature Requests:**  
  Use the `enhancement` label and describe what you’d like to see added or improved.

- ❓ **General Questions:**  
  Feel free to ask any question in the discussions page.
