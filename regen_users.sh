#!/bin/bash

# introduces the variable "users"
source ./psa_users.sh

# List of users to delete (separated by space)
# chris and yesse are gone now, but still in here in case you run this on old machine that still has them
users_to_delete=users
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
