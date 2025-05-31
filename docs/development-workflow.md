# Development Workflow Guide

This document explains the different levels of checks available and when to use them.

## Quick Reference

```bash
# One-time setup
make install

# While developing (fast checks)
make pre-commit

# Before committing (comprehensive checks)
make check

# Ready to commit
make commit-ready
```

## Understanding the Check Levels

### 1. Pre-commit Hooks (Fast - ~30 seconds)
**What runs:** Formatting, linting, basic security
**When:** Automatically on `git commit`, or manually with `make pre-commit`
**Purpose:** Catch obvious issues early

- Code formatting (black, isort)
- Linting (flake8)
- Type checking (mypy) - scripts only
- Basic security (bandit)
- File checks (trailing whitespace, etc.)
- Terraform security (checkov)

### 2. Comprehensive Checks (Slower - ~2-5 minutes)
**What runs:** Everything above + tests + more security
**When:** Before committing with `make check`
**Purpose:** Full validation

- All pre-commit hooks
- Dependency vulnerability scanning (safety)
- Full test suite with coverage
- Terraform validation
- Custom validation scripts

### 3. CI Checks (Complete validation)
**What runs:** Same as comprehensive + environment setup
**When:** GitHub Actions CI/CD
**Purpose:** Final gate before merge

## Recommended Workflow

1. **First time setup:**
   ```bash
   make install
   ```

2. **While developing:**
   ```bash
   # Quick feedback loop
   make pre-commit
   ```

3. **Before committing:**
   ```bash
   # Comprehensive validation
   make check
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: your feature description"
   # Pre-commit hooks run automatically here
   ```

## Why This Structure?

- **Fast feedback:** Pre-commit hooks catch 80% of issues in seconds
- **Comprehensive validation:** Full checks ensure quality before commit
- **Consistent tools:** Same tools in pre-commit, Makefile, and CI
- **No surprises:** What passes locally will pass in CI

## Troubleshooting

### "make pre-commit passes but make check fails"
This shouldn't happen anymore! We've synchronized the tools.

### "Pre-commit hooks are slow"
Pre-commit hooks should be fast (30 seconds). If they're slow:
- Check if you have uncommitted large files
- Try `make clean` to clear caches

### "I want to skip a hook temporarily"
```bash
git commit --no-verify -m "your message"
```
⚠️ **Use sparingly** - the hooks are there for good reasons!

## Available Commands

Run `make help` to see all available commands with descriptions.
