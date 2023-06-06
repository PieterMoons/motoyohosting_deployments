#!/bin/bash

# Directory path to change permissions
directory="/mnt"
folder="html"

# Set the desired permissions
owner="sftp-user"

# Change permissions for the directory and its descending directories
find "$directory" -type d -name "$folder" -exec chown  "$owner"  {} +
find "$directory" -type d -name "$folder" -exec chgrp  "$owner"  {} +;