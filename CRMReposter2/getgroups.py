import requests
import json
from data import *
# Ваш долгосрочный токен


headers = {
    'Authorization': f'Bearer {long_term_token}',
    'Content-Type': 'application/json'
}

# Функция для получения информации об аккаунте
def get_account_info():
    response = requests.get('https://kriloks303.amocrm.ru/api/v4/leads/pipelines', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Ошибка получения информации об аккаунте: {response.status_code}')
        return None

# Вызов функции и получение информации об аккаунте
account_info = get_account_info()
if account_info:
    print(json.dumps(account_info, indent=4, ensure_ascii=False))

