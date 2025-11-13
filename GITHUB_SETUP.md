# 🚀 GitHub Setup Guide

This guide will help you connect your Interactive Story Generator project to GitHub.

## 📋 Prerequisites

- Git installed on your system
- GitHub account
- Project files ready

## 🔧 Step-by-Step Setup

### Step 1: Initialize Git Repository

Open terminal/command prompt in the project directory and run:

```bash
cd storytelling_ai
git init
```

### Step 2: Add All Files

```bash
git add .
```

### Step 3: Create Initial Commit

```bash
git commit -m "Initial commit: Interactive Story Generator with AI"
```

### Step 4: Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the **"+"** icon in the top right corner
3. Select **"New repository"**
4. Fill in the repository details:
   - **Repository name**: `interactive-story-generator` (or your preferred name)
   - **Description**: "Interactive Story Generator using Google Gemini AI with automatic image generation"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click **"Create repository"**

### Step 5: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
# Add remote repository (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

### Step 6: Verify

Go to your GitHub repository page and verify all files are uploaded.

## 📝 Common Git Commands

### Daily Workflow

```bash
# Check status
git status

# Add changes
git add .

# Commit changes
git commit -m "Description of changes"

# Push to GitHub
git push
```

### Update from GitHub

```bash
# Pull latest changes
git pull
```

### Create New Branch

```bash
# Create and switch to new branch
git checkout -b feature/new-feature

# Push new branch
git push -u origin feature/new-feature
```

## 🔒 Important Notes

### Files NOT Uploaded to GitHub

The following files are excluded (via `.gitignore`):
- `.env` - Contains your API keys (NEVER commit this!)
- `__pycache__/` - Python cache files
- `venv/` - Virtual environment
- `outputs/*` - Generated story images
- `.streamlit/` - Streamlit config

### Security Best Practices

1. **Never commit `.env` file** - It contains sensitive API keys
2. **Use `env_template.txt`** - This is safe to commit as it has no real keys
3. **Review changes before committing** - Use `git status` and `git diff`

## 🎯 Repository Structure on GitHub

Your repository should have:
```
interactive-story-generator/
├── frontend/
│   └── app.py
├── services/
│   ├── __init__.py
│   ├── gemini_service.py
│   └── image_service.py
├── outputs/
│   └── .gitkeep
├── .gitignore
├── env_template.txt
├── requirements.txt
├── setup.bat
├── run.bat
├── README.md
├── QUICK_START.md
├── TROUBLESHOOTING.md
└── GITHUB_SETUP.md
```

## 🔄 Updating Repository

When you make changes:

```bash
# 1. Check what changed
git status

# 2. Add changes
git add .

# 3. Commit with descriptive message
git commit -m "Add new feature: [description]"

# 4. Push to GitHub
git push
```

## 🌿 Branching Strategy

For larger features, consider using branches:

```bash
# Create feature branch
git checkout -b feature/story-types

# Make changes, commit
git add .
git commit -m "Add new story types"

# Push branch
git push -u origin feature/story-types

# Create Pull Request on GitHub
# After merge, switch back to main
git checkout main
git pull
```

## 📚 Additional Resources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

## ❓ Troubleshooting

### "Remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
```

### "Permission denied"
- Check your GitHub credentials
- Use SSH keys or Personal Access Token

### "Large file warning"
- Make sure large files are in `.gitignore`
- Use Git LFS for large files if needed

---

**Your project is now on GitHub! 🎉**

