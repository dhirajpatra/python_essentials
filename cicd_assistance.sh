#!/bin/bash

# Check for required arguments
if [ $# -ne 4 ]; then
  echo "Error: Invalid number of arguments!"
  echo "Usage: $0 <branch_to_pull> <jira_ticket> <source_branch> <file_list>"
  echo "  <branch_to_pull>: Branch to pull from origin (e.g., develop)"
  echo "  <jira_ticket>: Jira ticket number (e.g., JIRA-1234)"
  echo "  <source_branch>: Directory containing folders and files to copy. It should be same way as in file_list and should be relative to the repository root."
  echo "  <file_list>: Text file containing paths to copy to"
  exit 1
fi

BRANCH_TO_PULL="$1"
JIRA_TICKET="$2"
SOURCE_BRANCH="$3"
FILE_LIST="$4"
TIMESTAMP=$(date +%Y%m%d%H%M%S)
NEW_BRANCH="${JIRA_TICKET}_${BRANCH_TO_PULL}_${TIMESTAMP}"
COMMIT_MESSAGE="${JIRA_TICKET}: $(date +%Y-%m-%d) - Added required files for implementation"
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

# 1. Pull the specified branch
# Display execution steps
echo "Step 1: Fetching latest updates from origin..."
git fetch origin

# 2. Checkout the specified branch
echo "Step 2: Checking out branch '$BRANCH_TO_PULL'..."
git checkout "$BRANCH_TO_PULL" || { echo "Branch '$BRANCH_TO_PULL' not found! Exiting."; exit 1; }

# 3. Pull the latest changes
echo "Step 3: Pulling latest changes from '$BRANCH_TO_PULL'..."
git pull origin "$BRANCH_TO_PULL"

# 4. Create a new branch
echo "Step 4: Creating new branch '$NEW_BRANCH'..."
git checkout -b "$NEW_BRANCH"

# Flag to track if any file not found
FILE_NOT_FOUND=false

# 5. Copy files based on file list
echo "Step 5: Copying files from '$SOURCE_BRANCH' as per '$FILE_LIST'..."
while IFS= read -r FILE_PATH; do
  if [ -n "$FILE_PATH" ]; then # Skip empty lines.
    source_file="${SOURCE_BRANCH}/${FILE_PATH##*/}" # get only filename, remove path.
    target_path="$FILE_PATH"
    target_dir="$(dirname "$target_path")"

    if [ ! -d "$target_dir" ]; then
      mkdir -p "$target_dir"
    fi

 # Create the target directory if it doesn't exist
    if git show "$TARGET_BRANCH:$target_dir" &> /dev/null; then
      echo "Target directory '$target_dir' already exists in branch '$TARGET_BRANCH'"
    else
      git checkout "$TARGET_BRANCH"
      mkdir -p "$target_dir"
      git add "$target_dir"
      git commit -m "Create directory $target_dir"
    fi

 # Copy the file from the source branch to the target branch
    if git show "$BRANCH_TO_PULL:$FILE_PATH" &> /dev/null; then
      git checkout "$TARGET_BRANCH"
      git show "$BRANCH_TO_PULL:$FILE_PATH" > "$target_path"
      git add "$target_path"
      git commit -m "Copy file $FILE_PATH from branch $BRANCH_TO_PULL"
    else
      echo "Warning: Source file not found in branch '$BRANCH_TO_PULL': $FILE_PATH"
    fi
  fi
done < "$FILE_LIST"

# If any file is not found, remove the new branch
if $FILE_NOT_FOUND; then
  echo "Removing new branch '$NEW_BRANCH' due to file not found."
  git switch $CURRENT_BRANCH # or the previous branch
  git branch -D "$NEW_BRANCH"

  echo "Unsuccessful due to file not found. Check source folder and files."
else
  echo "All files found and copied successfully."

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
  echo "Please create a merge or pull request for branch '$NEW_BRANCH' to 'BRANCH_TO_PULL' and assign it for review."
fi
