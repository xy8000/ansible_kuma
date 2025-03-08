#!/bin/sh

rm -f ./*.tar.gz
ansible-galaxy collection build -v
ansible-galaxy collection install . -p  ~/.ansible/collections/ --force