#!/bin/bash

# Your LeetCode repo path
REPO_PATH="/home/chakib/Desktop/vs_code/Leet_Code"
BRANCH="main"

# Navigate to repo
cd "$REPO_PATH" || exit 1

# Pull latest changes
git pull origin "$BRANCH" --quiet

# Get current date
CURRENT_DATE=$(date '+%B %d, %Y at %H:%M')

# Update README
cat > README.md << EOF
# LeetCode Solutions

This is my full solution of diverse problems from LeetCode with full documentation in each folder.

**Last Updated:** $CURRENT_DATE

---

*This repository is automatically updated daily to keep my GitHub activity consistent 🟩*
EOF

# Commit and push
git add README.md
git commit -m "📅 Daily update: $CURRENT_DATE" --quiet
git push origin "$BRANCH" --quiet

# Log success
echo "$(date '+%Y-%m-%d %H:%M:%S'): ✅ Successfully updated Leet_Code repo" >> ~/leetcode-update.log
