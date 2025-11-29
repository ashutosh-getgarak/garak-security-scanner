# GitHub Starter Workflows Submission Guide

This document explains how to get the Garak Security Scanner workflow to appear in the "Choose a workflow" section when users click "Actions" → "New workflow" in their repositories.

## Overview

GitHub's starter workflows are maintained in the official repository: https://github.com/github/starter-workflows

To make our workflow appear automatically for users, we need to submit a Pull Request to this repository.

## Files Ready for Submission

We've prepared all required files in the `workflow-templates/` directory:

```
workflow-templates/
├── garak-security-scan.yml    # The workflow template
├── properties.json            # Metadata for the workflow
└── garak-security.svg         # Icon displayed in the UI
```

## Submission Process

### Step 1: Fork the starter-workflows repository

1. Go to https://github.com/github/starter-workflows
2. Click "Fork" in the top right
3. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/starter-workflows.git
   cd starter-workflows
   ```

### Step 2: Copy files to the correct location

Copy our workflow template files to the `code-scanning/` directory (since we're a security tool):

```bash
# From within the starter-workflows repo
cp /path/to/garak-security-scanner/workflow-templates/garak-security-scan.yml code-scanning/
cp /path/to/garak-security-scanner/workflow-templates/properties.json code-scanning/garak-security-scan.properties.json
cp /path/to/garak-security-scanner/workflow-templates/garak-security.svg code-scanning/garak-security.svg
```

**Important naming convention:**
- Workflow file: `garak-security-scan.yml`
- Properties file: `garak-security-scan.properties.json` (must match workflow name + `.properties.json`)
- Icon file: `garak-security.svg` (must match `iconName` in properties.json)

### Step 3: Create and submit PR

```bash
git checkout -b add-garak-security-scanner
git add code-scanning/garak-security-scan.yml
git add code-scanning/garak-security-scan.properties.json
git add code-scanning/garak-security.svg
git commit -m "Add Garak AI Security Scanner workflow

This workflow enables automated AI security scanning for LLM applications.

Features:
- Detects prompt injection and jailbreak attempts
- Scans for security vulnerabilities, privacy leaks, and toxicity
- Supports multiple LLM providers (Anthropic, OpenAI, Azure, etc.)
- Provides detailed security reports and PR comments
- Configurable security thresholds

Repository: https://github.com/garaksecurity/garak-security-scanner
Documentation: https://github.com/garaksecurity/garak-security-scanner#readme
"

git push origin add-garak-security-scanner
```

Then:
1. Go to https://github.com/github/starter-workflows
2. Click "Pull requests" → "New pull request"
3. Click "compare across forks"
4. Select your fork and branch
5. Create the PR with a clear description

### Step 4: PR Description Template

Use this template for your PR description:

```markdown
## Description

This PR adds a starter workflow for the Garak AI Security Scanner, which helps developers detect security vulnerabilities in LLM applications.

## What does this workflow do?

- Scans LLM endpoints for prompt injection, jailbreaks, and security vulnerabilities
- Runs automated security tests on AI/ML applications
- Provides detailed reports on security scores and vulnerabilities
- Integrates with CI/CD pipelines for continuous security testing

## Why should this be included?

- **Growing need**: AI security is critical as LLM adoption increases
- **Easy setup**: Users just add secrets and click "Configure"
- **Actionable results**: Clear pass/fail criteria with detailed reports
- **Multi-provider**: Works with Anthropic, OpenAI, Azure OpenAI, and custom endpoints

## Categories

- Security
- Python
- Automation

## Target audience

Developers building applications that use:
- Large Language Models (LLMs)
- AI/ML APIs (OpenAI, Anthropic, Azure OpenAI, etc.)
- Chatbots and conversational AI
- AI-powered features

## Documentation

- Repository: https://github.com/garaksecurity/garak-security-scanner
- Action in Marketplace: https://github.com/marketplace/actions/garak-security-scanner
- Full documentation: https://github.com/garaksecurity/garak-security-scanner#readme

## Checklist

- [x] Workflow file follows GitHub Actions best practices
- [x] Properties file includes all required metadata
- [x] Icon is included and referenced correctly
- [x] Workflow is tested and working
- [x] Documentation is clear and comprehensive
- [x] Secrets are properly documented in comments
```

## Alternative: Organization Starter Workflows

If you want the workflow to appear immediately for repositories in your organization without waiting for GitHub's approval:

### Create organization starter workflows

1. Create a special repository named `.github` in your organization
2. Add the workflow templates:
   ```
   your-org/.github/
   └── workflow-templates/
       ├── garak-security-scan.yml
       ├── garak-security-scan.properties.json
       └── garak-security.svg
   ```

3. The workflow will now appear in the "Actions" tab for all repositories in your organization!

**Benefits:**
- ✅ Immediate availability (no PR approval wait)
- ✅ Organization-specific customization
- ✅ Can include org-specific defaults

**Limitations:**
- ❌ Only available within your organization
- ❌ Not visible to external users

## Timeline

- **Organization workflows**: Immediate (once committed to `.github` repo)
- **Global starter workflows**: 1-4 weeks (depends on GitHub's review process)

## Testing

Before submitting, test that the workflow works correctly:

1. Create a test repository
2. Copy the workflow file to `.github/workflows/garak-security-scan.yml`
3. Set up required secrets (GARAK_API_KEY, X_API_KEY)
4. Trigger the workflow and verify it runs successfully

## Questions?

If you have questions about the submission process:
- GitHub Starter Workflows Guidelines: https://github.com/github/starter-workflows/blob/main/CONTRIBUTING.md
- GitHub Actions Documentation: https://docs.github.com/en/actions

---

**Once approved, users will see "Garak AI Security Scanner" in their workflow suggestions with a simple "Configure" button!**
