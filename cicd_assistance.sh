#!/bin/bash

# Check for required arguments
if [ $# -lt 3 ] || [ $# -gt 4 ]; then
  echo "Error: Invalid number of arguments!"
  echo "Usage: $0 <branch_to_pull> <jira_ticket> <source_branch> [<num_commits>]"
  exit 1
fi

BRANCH_TO_PULL="$1"
JIRA_TICKET="$2"
SOURCE_BRANCH="$3"
NUM_COMMITS=${4:-1}  # Default to last commit if not provided
TIMESTAMP=$(date +%Y%m%d%H%M%S)
NEW_BRANCH="${JIRA_TICKET}_${BRANCH_TO_PULL}_${TIMESTAMP}"
COMMIT_MESSAGE="${JIRA_TICKET}: $(date +%Y-%m-%d) - Added required files for implementation"
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Fetch latest updates
echo "Step 1: Fetching latest updates from origin..."
git fetch origin

# Checkout the specified branch
echo "Step 2: Checking out branch '$BRANCH_TO_PULL'..."
git checkout "$BRANCH_TO_PULL" || { echo "Branch '$BRANCH_TO_PULL' not found! Exiting."; exit 1; }

echo "Step 3: Pulling latest changes from '$BRANCH_TO_PULL'..."
git pull origin "$BRANCH_TO_PULL"

# Create new branch
echo "Step 4: Creating new branch '$NEW_BRANCH'..."
git checkout -b "$NEW_BRANCH"

# Get changed files from the last N commits of the source branch
CHANGED_FILES=$(git log -n "$NUM_COMMITS" --pretty=format: --name-only "$SOURCE_BRANCH" | sort -u)

# If no files changed, exit
if [ -z "$CHANGED_FILES" ]; then
  echo "No files changed in the last $NUM_COMMITS commit(s) of '$SOURCE_BRANCH'. Exiting."
  exit 1
fi

# Copy files based on the last N commits
for FILE_PATH in $CHANGED_FILES; do
  source_file="$SOURCE_BRANCH:$FILE_PATH"
  target_path="$FILE_PATH"
  target_dir=$(dirname "$target_path")

  if [ ! -d "$target_dir" ]; then
    mkdir -p "$target_dir"
  fi

  if git show "$source_file" &> /dev/null; then
    git show "$source_file" > "$target_path"
    git add "$target_path"
    git commit -m "Copy file $FILE_PATH from last $NUM_COMMITS commit(s) of $SOURCE_BRANCH"
  else
    echo "Warning: Source file not found in last $NUM_COMMITS commit(s) of '$SOURCE_BRANCH': $FILE_PATH"
  fi
done

# Add changes to git
echo "Step 6: Adding changes to git..."
git add .

echo "Step 7: Committing changes... $COMMIT_MESSAGE"
if ! git diff --staged --quiet; then
  git commit -m "$COMMIT_MESSAGE"
else
  echo "No changes detected. Skipping commit."
fi

# Push the new branch
echo "Step 8: Pushing branch '$NEW_BRANCH' to origin..."
git push origin "$NEW_BRANCH"

echo "Done! New branch '$NEW_BRANCH' created and pushed successfully."
echo "Please create a merge or pull request for branch '$NEW_BRANCH' to '$BRANCH_TO_PULL' and assign it for review."
