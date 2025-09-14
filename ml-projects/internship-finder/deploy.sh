#!/bin/bash

# Create a new repository for the internship finder
echo "Setting up GitHub Pages deployment for Internship Finder..."

# Initialize git if not already done
if [ ! -d ".git" ]; then
    git init
    git remote add origin https://github.com/segnimekonnen7/internship-finder.git
fi

# Create gh-pages branch
git checkout -b gh-pages

# Remove all files except the HTML
git rm -rf . || true
git add index.html
git commit -m "Deploy Internship Finder to GitHub Pages"

# Push to GitHub
git push origin gh-pages --force

echo "Internship Finder deployed to GitHub Pages!"
echo "Your live demo will be available at: https://segnimekonnen7.github.io/internship-finder/" 