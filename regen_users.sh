#!/bin/bash

# List of users to delete (separated by space)
users_to_delete=("schoe" "steph" "pahll" "frisc" "zette" "klaku" "chris" "tongu" "haugs" "yesse" "stoec" "wittm" "grote>
# Iterate through the list of users to delete
for username in "${users_to_delete[@]}"; do
    # Check if the user exists
    if id "$username" &>/dev/null; then
        # Delete user (without removing home directory)
        sudo deluser --remove-all-files "$username"
        echo "Deleted user: $username"
    else
        echo "User not found: $username"
    fi
done


python3 add_users.py
