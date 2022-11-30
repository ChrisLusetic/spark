#!/bin/bash

eval "$(ssh-agent -s)"
if [ ! -d "$HOME/.ssh/" ]; then
    # This is added by docker-compose.yml `secrets` keyword
    ssh-add -k /run/secrets/git_key
    mkdir $HOME/.ssh
    ssh-keyscan git.byte-lab.com > /root/.ssh/known_hosts
fi
# now execute command which require authentication via ssh (example, git clone from a private repo)
echo "Running blanalyzer"
python3 /home/blanalyzer/blanalyzer.py

