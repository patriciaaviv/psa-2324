#!/bin/bash

# introduces the variable "users"
source ./psa_users.sh

# delete users
for username in "${users_to_delete[@]}"; do
    # Check if the user exists
    if id "$username" &>/dev/null; then
        # Delete user (including home dir)
        sudo deluser --remove-all-files "$username"
        echo "Deleted user: $username"
    else
        echo "User not found: $username"
    fi
done


python3 add_users.py
