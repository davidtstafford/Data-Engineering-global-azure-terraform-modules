# Branch Protection Setup Guide

## Overview
This guide walks through setting up branch protection rules for the `main` branch to ensure all changes go through pull requests and maintain code quality.

## GitHub Web Interface Setup

### 1. Navigate to Repository Settings
1. Go to: `https://github.com/davidtstafford/Data-Engineering-global-azure-terraform-modules`
2. Click the **Settings** tab
3. Click **Branches** in the left sidebar

### 2. Add Branch Protection Rule
1. Click **Add rule** button
2. Enter `main` as the branch name pattern

### 3. Configure Protection Settings

#### Pull Request Requirements
- ✅ **Require a pull request before merging**
  - ✅ **Require approvals**: Set to `1` (minimum)
  - ✅ **Dismiss stale pull request approvals when new commits are pushed**
  - ✅ **Require review from code owners** (if you create a CODEOWNERS file)

#### Status Check Requirements
- ✅ **Require status checks to pass before merging**
- ✅ **Require branches to be up to date before merging**
- Select these status checks (based on your GitHub Actions):
  - `test` (pytest runs)
  - `lint` (code quality checks)
  - `security` (security scans)

#### Additional Protection
- ✅ **Require conversation resolution before merging**
- ✅ **Require signed commits** (recommended for security)
- ✅ **Include administrators** (applies rules to repo admins too)
- ❌ **Allow force pushes** (keep unchecked)
- ❌ **Allow deletions** (keep unchecked)

### 4. Save the Rule
Click **Create** to save the branch protection rule.

## Recommended Additional Setup

### Create CODEOWNERS File
Create a `.github/CODEOWNERS` file to automatically assign reviewers:

```
# Global code owners
* @davidtstafford

# Terraform modules require infrastructure team review
terraform/ @davidtstafford

# Scripts and automation
scripts/ @davidtstafford

# CI/CD and GitHub Actions
.github/ @davidtstafford
```

### Update GitHub Actions for Status Checks
Ensure your `.github/workflows/*.yml` files run on pull requests:

```yaml
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
```

## Development Workflow After Protection

### 1. Create Feature Branch
```bash
git checkout -b feature/new-feature
# Make your changes
git add .
git commit -m "feat: add new feature"
git push origin feature/new-feature
```

### 2. Create Pull Request
1. Go to GitHub repository
2. Click "Compare & pull request"
3. Fill in PR description
4. Request reviewers
5. Wait for status checks to pass
6. Get approval from reviewer(s)
7. Merge via GitHub interface

### 3. Clean Up
```bash
git checkout main
git pull origin main
git branch -d feature/new-feature
```

## Testing the Protection

After setting up, try to push directly to main:
```bash
git checkout main
echo "test" >> README.md
git add README.md
git commit -m "test direct push"
git push origin main
```

This should be **rejected** with an error message about branch protection rules.

## Benefits

- ✅ **Code Review**: All changes reviewed before merging
- ✅ **Quality Gates**: Tests and linting must pass
- ✅ **Audit Trail**: Clear history of who approved what
- ✅ **Prevents Accidents**: No accidental direct pushes to main
- ✅ **CI/CD Integration**: Automated checks before merge

## Emergency Override

If you need to make an emergency change:
1. Temporarily disable branch protection (Settings > Branches)
2. Make the emergency change
3. Re-enable branch protection immediately
4. Create a follow-up PR to document the emergency change
