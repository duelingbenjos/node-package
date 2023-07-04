#!/bin/bash

BLOCK_NUMBER=$1

# Check if block number is empty
if [ -z "$BLOCK_NUMBER" ]; then
    echo "Error: Block number is required"
    exit 1
fi

# Check if block number is an integer
if ! [[ $BLOCK_NUMBER =~ ^[0-9]+$ ]]; then
    echo "Error: Block number must be an integer"
    exit 1
fi

# Ask for user confirmation
read -p "Are you sure you want to rollback to block number ${BLOCK_NUMBER}? (yes/no) " confirm

if [[ "$confirm" != "yes" ]]; then
    echo "Rollback cancelled."
    exit 1
fi

echo "Block number is valid"
exit 0
