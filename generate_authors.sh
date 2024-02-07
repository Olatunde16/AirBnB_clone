#!/bin/bash

# Generate AUTHORS file
echo "Authors of the project:" > AUTHORS
git log --format='%aN <%aE>' | sort -u >> AUTHORS

