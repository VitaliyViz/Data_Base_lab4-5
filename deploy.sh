#!/bin/bash
cd /home/ubuntu/Data_Base_lab4-5        # шлях до твого проєкту
git pull origin main                   # тягнемо останні зміни з Git
source venv/bin/activate               # активуємо віртуальне середовище
pip install -r requirements.txt       # оновлюємо залежності
sudo systemctl restart myproject.service  # перезапускаємо сервіс
