import requests
from data import *  # Импортируем username и password из файла data.py
import base64

def send_lead(phone, firstname):
    url_import_leads = 'https://crm-gw.sbermarket.ru/partner-candidate/v1/leads/import'
    leads_data = {
        "candidates": [
            {
                "phone": phone,
                "first_name": firstname,
                "vacancy_id": 3,
                "city_id": 112,
                "utm":{
                    "utm_source": utm_source
                }
            }
        ]
    }

    # Отправляем POST запрос с данными и заголовками
    response = requests.post(url_import_leads, json=leads_data, auth=(username, password))
    print(123)
    # Проверяем успешность запроса
    if response.status_code == 200:
        response_data = response.json()
        if 'deduplication' in response_data['details'][0]:
            if response_data['details'][0]['deduplication']['message']=='Правило дедубликации не применено, источник не закреплён за вами':
                print(response.text)
                return False
            else:

                print(f"Лиды успешно импортированы!{response.text}")
                return True
        else:
            print(f"Лиды успешно импортированы!{response.text}")
            return True

    else:
        print(f"Ошибка {response.status_code}: {response.text}")
