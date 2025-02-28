#!/bin/bash

# Check for required arguments
if [ $# -ne 4 ]; then
  echo "Error: Invalid number of arguments!"
  echo "Usage: $0 <branch_to_pull> <jira_ticket> <source_dir> <file_list>"
  echo "  <branch_to_pull>: Branch to pull from origin (e.g., develop)"
  echo "  <jira_ticket>: Jira ticket number (e.g., JIRA-1234)"
  echo "  <source_dir>: Directory containing folders and files to copy. It should be same way as in file_list and should be relative to the repository root."
  echo "  <file_list>: Text file containing paths to copy to"
  exit 1
fi

SOURCE_BRANCH="$1"
JIRA_TICKET="$2"
SOURCE_FOLDER="$3"
FILE_LIST="$4"
TIMESTAMP=$(date +%Y%m%d%H%M%S)
NEW_BRANCH="${JIRA_TICKET}_${SOURCE_BRANCH}_${TIMESTAMP}"
COMMIT_MESSAGE="${JIRA_TICKET}: $(date +%Y-%m-%d) - Added required files for implementation"

# 1. Pull the specified branch
# Display execution steps
echo "Step 1: Fetching latest updates from origin..."
git fetch origin

# 2. Checkout the specified branch
echo "Step 2: Checking out branch '$SOURCE_BRANCH'..."
git checkout "$SOURCE_BRANCH" || { echo "Branch '$SOURCE_BRANCH' not found! Exiting."; exit 1; }

# 3. Pull the latest changes    
echo "Step 3: Pulling latest changes from '$SOURCE_BRANCH'..."
git pull origin "$SOURCE_BRANCH"

# 4. Create a new branch
echo "Step 4: Creating new branch '$NEW_BRANCH'..."
git checkout -b "$NEW_BRANCH"

# 5. Copy files based on file list
echo "Step 5: Copying files from '$SOURCE_FOLDER' as per '$FILE_LIST'..."
while IFS= read -r FILE_PATH; do
  if [ -n "$FILE_PATH" ]; then # Skip empty lines.
    source_file="${SOURCE_FOLDER}/${FILE_PATH##*/}" # get only filename, remove path.
    target_path="$FILE_PATH"
    target_dir="$(dirname "$target_path")"

    if [ ! -d "$target_dir" ]; then
      mkdir -p "$target_dir"
    fi

    if [ -f "$SOURCE_FOLDER/$FILE_PATH" ]; then
        cp "$SOURCE_FOLDER/$FILE_PATH" "$target_path"
    elif [ -d "$SOURCE_FOLDER/$FILE_PATH" ]; then
        cp -r "$SOURCE_FOLDER/$FILE_PATH" "$target_path"
    else
      echo "Warning: Source file or directory not found: $SOURCE_FOLDER/$FILE_PATH"
    fi
  fi
done < "$FILE_LIST"

# 6. Add changes to git
echo "Step 6: Adding changes to git..."
git add .

# 7. Commit changes
echo "Step 7: Committing changes... $COMMIT_MESSAGE"
if ! git diff --staged --quiet; then
    git commit -m "$COMMIT_MESSAGE"
else
    echo "No changes detected. Skipping commit."
fi

# 8. Push the new branch
echo "Step 8: Pushing branch '$NEW_BRANCH' to origin..."
git push origin "$NEW_BRANCH"

echo "Done! New branch '$NEW_BRANCH' created and pushed successfully."
echo "Please create a merge or pull request for branch '$NEW_BRANCH' to 'SOURCE_BRANCH' and assign it for review."
