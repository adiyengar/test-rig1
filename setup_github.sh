#!/bin/bash
# GitHub Setup Script for Data Quality Analyzer

echo "🚀 Setting up GitHub repository..."

# Check if we have a remote
if git remote -v | grep -q "origin"; then
    echo "✅ Remote 'origin' already exists"
    REMOTE_URL=$(git remote get-url origin)
    echo "Current remote: $REMOTE_URL"
else
    echo "Please go to https://github.com/new and create a repository named 'data-quality-analyzer'"
    echo "Then come back and run:"
    echo ""
    echo "git remote add origin https://github.com/YOUR_USERNAME/data-quality-analyzer.git"
    echo "git push -u origin main"
    echo ""
fi

echo ""
echo "📝 Current commits ready to push:"
git log --oneline
echo ""
echo "✨ Ready to deploy!"
