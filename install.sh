#!/bin/sh

rm -f ./*.tar.gz
ansible-galaxy collection build -v
ansible-galaxy collection install xy8000-uptime_kuma-1.2.1.tar.gz -p  ~/.ansible/collections/ --force