# Publish To GitHub

This folder is already structured like a standalone public repository.

## Before You Push

1. Review [docs/redaction-checklist.md](redaction-checklist.md).
2. Replace any placeholder text that should mention your own story or positioning.
3. Decide whether you want to keep the MIT License in [LICENSE](../LICENSE).

## Suggested Repository Name

- report-format-skill-kit
- agency-report-reconstruction-skill
- ai-report-format-playbook

## Suggested Commands

Run these commands from the repository root after you create a new GitHub repository:

```powershell
Set-Location report-format-skill-kit
git add .
git commit -m "Initial public skill kit"
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```

## If You Use GitHub CLI

If `gh` is installed and authenticated, you can do:

```powershell
Set-Location report-format-skill-kit
git add .
git commit -m "Initial public skill kit"
gh repo create report-format-skill-kit --public --source . --remote origin --push
```

## Suggested First Commit Message

`Initial public skill kit for strict report-format reconstruction`
