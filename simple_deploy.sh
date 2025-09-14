#!/bin/bash

echo "🚀 Simple Deployment to GitHub Pages..."

# Function to deploy a project
deploy_project() {
    local project_name=$1
    local project_path=$2
    local repo_name=$3
    
    echo "📦 Deploying $project_name..."
    
    cd "$project_path"
    
    # Remove existing git
    rm -rf .git
    
    # Initialize new git
    git init
    git remote add origin "https://github.com/segnimekonnen7/$repo_name.git"
    
    # Add only the HTML file
    git add index.html
    git commit -m "Deploy $project_name to GitHub Pages"
    
    # Create and push gh-pages branch
    git branch -M gh-pages
    git push origin gh-pages --force
    
    echo "✅ $project_name deployed to: https://segnimekonnen7.github.io/$repo_name/"
    echo ""
    
    cd - > /dev/null
}

# Deploy each project
deploy_project "Internship Finder" "ml-projects/internship-finder" "internship-finder"
deploy_project "Sentiment Analyzer" "ml-projects/sentiment-analyzer" "sentiment-analyzer"
deploy_project "Plant Disease Classifier" "ml-projects/image-classifier" "plant-classifier"
deploy_project "Interview Prep" "ml-projects/interview-prep" "interview-prep"

echo "🎉 All projects deployed successfully!"
echo ""
echo "📋 Live Demo URLs:"
echo "• Internship Finder: https://segnimekonnen7.github.io/internship-finder/"
echo "• Sentiment Analyzer: https://segnimekonnen7.github.io/sentiment-analyzer/"
echo "• Plant Disease Classifier: https://segnimekonnen7.github.io/plant-classifier/"
echo "• Interview Prep: https://segnimekonnen7.github.io/interview-prep/"
echo ""
echo "🔗 Add these URLs to your portfolio for live demos!" 