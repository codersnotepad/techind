# Packaging `techind` for PyPI — Step-by-Step Guide

This guide takes the repo from its current state (a `setup.py`-based project) to a fully automated CI/CD pipeline that publishes to **PyPI Test** and **PyPI Production** via GitHub Actions.

---

## Table of Contents

1. [Overview of the target structure](#1-overview-of-the-target-structure)
2. [Migrate to `pyproject.toml`](#2-migrate-to-pyprojecttoml)
3. [Add a `tests/` directory](#3-add-a-tests-directory)
4. [Set up PyPI accounts and API tokens](#4-set-up-pypi-accounts-and-api-tokens)
5. [Add GitHub repository secrets](#5-add-github-repository-secrets)
6. [Create GitHub Actions workflows](#6-create-github-actions-workflows)
7. [Versioning strategy](#7-versioning-strategy)
8. [Local release workflow (your day-to-day process)](#8-local-release-workflow-your-day-to-day-process)
9. [Verifying a release](#9-verifying-a-release)

---

## 1. Overview of the target structure

After following this guide your repo will look like:

```
techind/
├── .github/
│   └── workflows/
│       ├── ci.yml          # runs tests on every push / PR
│       └── publish.yml     # publishes to PyPI Test or Prod on tag
├── techind/
│   ├── __init__.py
│   └── *.py                # your indicator modules
├── tests/
│   ├── __init__.py
│   └── test_indicators.py  # your tests
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml          # replaces setup.py
└── requirements.txt        # kept for dev environment only
```

> `setup.py` will be deleted once `pyproject.toml` is in place.

---

## 2. Migrate to `pyproject.toml`

Modern Python packaging uses `pyproject.toml` instead of `setup.py`. It is the current standard and is required by the latest PyPI tooling.

### 2a. Create `pyproject.toml`

Create a file called `pyproject.toml` in the repo root with the following content. Update the values marked with `# <-- update this` to match your details:

```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "techind"
version = "0.1.0"                          # <-- update this (see versioning section)
description = "Collection of technical indicators for financial time series analysis."
readme = "README.md"
license = { file = "LICENSE" }
authors = [
    { name = "Timote WB", email = "timote.wb@gmail.com" }   # <-- update this
]
keywords = ["finance", "technical analysis", "trading", "indicators"]
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
    "Topic :: Office/Business :: Financial",
]
requires-python = ">=3.8"
dependencies = [
    "numpy>=1.18.1",
]

[project.urls]
Homepage = "https://github.com/codersnotepad/techind"   # <-- update this
Issues   = "https://github.com/codersnotepad/techind/issues"

[tool.setuptools.packages.find]
where = ["."]
include = ["techind*"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

### 2b. Delete `setup.py`

Once `pyproject.toml` is in place and you have verified tests pass (step 3), delete `setup.py`:

```bash
git rm setup.py
```

---

## 3. Add a `tests/` directory

Tests are required for CI to be meaningful. Create a minimal test file to start with; add more tests as you build new indicators.

### 3a. Create `tests/__init__.py`

```bash
mkdir tests
touch tests/__init__.py
```

### 3b. Create `tests/test_indicators.py`

Write at least one test per indicator. Below is a starter template — add cases for each function as you write them:

```python
import numpy as np
import pytest
import techind as ti


# ── Helpers ──────────────────────────────────────────────────────────────────

def _close(n=100, seed=42):
    """Reproducible synthetic close-price series."""
    rng = np.random.default_rng(seed)
    return np.cumsum(rng.normal(0, 1, n)) + 100.0


# ── EMA ───────────────────────────────────────────────────────────────────────

def test_ema_output_length():
    data = _close()
    result = ti.exponentialMovingAverage(14, data)
    assert len(result) == len(data)

def test_ema_leading_values_are_nan():
    data = _close()
    result = ti.exponentialMovingAverage(14, data)
    # first (period-1) values should be NaN
    assert all(np.isnan(result[:13]))

def test_ema_no_nan_after_warmup():
    data = _close()
    result = ti.exponentialMovingAverage(14, data)
    assert not any(np.isnan(result[13:]))


# ── SMA ───────────────────────────────────────────────────────────────────────

def test_sma_output_length():
    data = _close()
    result = ti.simpleMovingAverage(14, data)
    assert len(result) == len(data)


# Add similar smoke-test blocks for every indicator you add.
```

### 3c. Add test dependencies to `requirements.txt`

Append the following lines:

```
pytest>=7.0
build>=1.0
twine>=5.0
```

---

## 4. Set up PyPI accounts and API tokens

You need accounts on both TestPyPI and PyPI, and an API token for each.

### 4a. Create accounts

- **TestPyPI**: https://test.pypi.org/account/register/
- **PyPI (production)**: https://pypi.org/account/register/

Use the **same email/username** for both to keep things simple.

### 4b. Generate API tokens

1. Log in to **TestPyPI** → Account Settings → API tokens → Add API token.
   - Token name: `github-actions-techind`
   - Scope: Entire account (or restrict to the `techind` project once it exists)
   - Copy the token value — you will only see it once.

2. Repeat the same steps on **PyPI (production)**.

> Store these tokens somewhere safe (e.g., a password manager) before adding them to GitHub.

---

## 5. Add GitHub repository secrets

GitHub Actions reads secrets you define at the repository level. Never commit tokens to the repo.

1. Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**.

2. Add **two** secrets:

   | Secret name             | Value                          |
   |-------------------------|--------------------------------|
   | `PYPI_TEST_API_TOKEN`   | The token from TestPyPI        |
   | `PYPI_API_TOKEN`        | The token from PyPI production |

---

## 6. Create GitHub Actions workflows

Create the `.github/workflows/` directory and add the two workflow files below.

```bash
mkdir -p .github/workflows
```

### 6a. CI workflow — runs tests on every push and pull request

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: ["**"]
  pull_request:
    branches: ["**"]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install numpy pytest
          pip install -e .

      - name: Run tests
        run: pytest
```

### 6b. Publish workflow — publishes on version tags

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  push:
    tags:
      - "v*.*.*"           # triggers on tags like v0.1.0, v1.2.3

jobs:
  # ── 1. Run tests first ────────────────────────────────────────────────────
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install numpy pytest && pip install -e .
      - run: pytest

  # ── 2. Build the distribution ─────────────────────────────────────────────
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Build wheel and sdist
        run: |
          pip install build
          python -m build
      - name: Upload dist artifacts
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  # ── 3. Publish to TestPyPI ────────────────────────────────────────────────
  publish-test:
    needs: build
    runs-on: ubuntu-latest
    environment: testpypi           # optional: add environment protection rules
    steps:
      - name: Download dist artifacts
        uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/
      - name: Publish to TestPyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          repository-url: https://test.pypi.org/legacy/
          password: ${{ secrets.PYPI_TEST_API_TOKEN }}

  # ── 4. Publish to PyPI Production ────────────────────────────────────────
  publish-prod:
    needs: publish-test
    runs-on: ubuntu-latest
    environment: pypi               # add a required reviewer here for safety
    steps:
      - name: Download dist artifacts
        uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/
      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}
```

> **Tip — require a manual approval before prod**: In GitHub repo Settings → Environments, create environments named `testpypi` and `pypi`. On the `pypi` environment, enable "Required reviewers" and add yourself. This means the production publish step waits for you to click "Approve" in the GitHub Actions UI before it runs.

---

## 7. Versioning strategy

Use [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`

| Change type                          | Bump      | Example       |
|--------------------------------------|-----------|---------------|
| Breaking API change                  | MAJOR     | `1.0.0→2.0.0` |
| New indicator added (backwards compat) | MINOR   | `0.1.0→0.2.0` |
| Bug fix, documentation only          | PATCH     | `0.1.0→0.1.1` |

**The version lives in exactly one place**: the `version` field in `pyproject.toml`. The git tag must match it exactly (e.g. tag `v0.2.0` → `version = "0.2.0"`).

---

## 8. Local release workflow (your day-to-day process)

Follow these steps every time you want to cut a new release:

```bash
# 1. Make sure all your changes are committed and tests pass locally
pip install -e .
pytest

# 2. Update the version in pyproject.toml
#    Edit the `version = "x.y.z"` line manually.

# 3. Commit the version bump
git add pyproject.toml
git commit -m "chore: bump version to x.y.z"

# 4. Create and push the git tag — this triggers the publish workflow
git tag v x.y.z          # e.g. git tag v0.2.0
git push origin main
git push origin vx.y.z   # e.g. git push origin v0.2.0
```

After pushing the tag:
- GitHub Actions runs **CI** (tests) → **build** → **TestPyPI** → (optional approval) → **PyPI production**.
- Monitor progress in the **Actions** tab of your GitHub repo.

---

## 9. Verifying a release

### Check TestPyPI first

```bash
pip install --index-url https://test.pypi.org/simple/ \
            --extra-index-url https://pypi.org/simple/ \
            techind==x.y.z
python -c "import techind as ti; print(dir(ti))"
```

### Check PyPI production

```bash
pip install techind==x.y.z
python -c "import techind as ti; print(dir(ti))"
```

### Quick smoke test

```python
import numpy as np
import techind as ti

close = np.array([float(x) for x in range(1, 101)])
ema = ti.exponentialMovingAverage(14, close)
print(ema[-5:])  # should print the last 5 EMA values
```

---

## Summary checklist

- [ ] Create `pyproject.toml` (step 2)
- [ ] Delete `setup.py` (step 2b)
- [ ] Create `tests/__init__.py` and `tests/test_indicators.py` (step 3)
- [ ] Update `requirements.txt` with test deps (step 3c)
- [ ] Create TestPyPI and PyPI accounts + API tokens (step 4)
- [ ] Add `PYPI_TEST_API_TOKEN` and `PYPI_API_TOKEN` to GitHub secrets (step 5)
- [ ] Create `.github/workflows/ci.yml` (step 6a)
- [ ] Create `.github/workflows/publish.yml` (step 6b)
- [ ] (Optional) Configure GitHub environment protection for `pypi` (step 6b tip)
- [ ] Push everything to GitHub and verify the CI workflow passes
- [ ] Cut your first release tag and watch the publish pipeline run end-to-end
