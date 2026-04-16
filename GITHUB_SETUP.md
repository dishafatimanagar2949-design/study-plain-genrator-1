# GitHub CLI Reference

Commands to quickly set up GitHub:

## 1. Initial Setup
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## 2. Create Repository
```bash
# Initialize if not done
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit: AI Study Planner Generator"
```

## 3. Push to GitHub
```bash
# Add remote (replace with your repo URL)
git remote add origin https://github.com/yourusername/study-planner-generator.git

# Rename branch to main (GitHub default)
git branch -M main

# Push all commits
git push -u origin main
```

## 4. Verify
```bash
# Check remote
git remote -v

# View history
git log --oneline
```

## Useful Git Commands

```bash
# Check status
git status

# Commit changes
git add .
git commit -m "Describe changes here"

# Push changes
git push

# Pull changes
git pull

# Create new branch
git checkout -b feature-name

# Switch branches
git checkout main

# Merge branches
git merge feature-name

# View branches
git branch -a
```

## GitHub Actions (CI/CD)

Optional: Add automated testing on every push.  
Create `.github/workflows/test.yml`:

```yaml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest
```
