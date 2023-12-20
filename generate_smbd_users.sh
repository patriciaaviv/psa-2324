#!/bin/bash

# introduces users variable
source ./psa_users.sh

for username in "${users[@]}"; do
    # Check if the user exists
    if sudo pdbedit -L | grep -q "$username"  &>/dev/null; then
        echo "already exists: $username"
    else
	echo "ADDING $username..."
	# yes, the EOF block has to be (un)indented this way
	# will throw error if it fails
        sudo smbpasswd -a "$username"<<EOF > /dev/null
psa
psa
EOF

    fi
done
