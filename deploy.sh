#!/bin/bash
cd /home/ubuntu/Data_Base_lab4-5 || exit
git fetch origin main
git reset --hard origin/main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart myproject.service
