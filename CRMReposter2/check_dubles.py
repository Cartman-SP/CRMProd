import requests
import json
from data import *
from leads_sender import *
import time
headers = {
    'Authorization': f'Bearer {long_term_token}',
    'Content-Type': 'application/json'
}

def get_contacts_info(id):

    url = f'https://kriloks303.amocrm.ru/api/v4/contacts/{id}'

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data['name']
    else:
        print(f'Ошибка {response.status_code}: {response.json()}')
        return []

def get_leads_info(id):

    url = f'https://kriloks303.amocrm.ru/api/v4/leads/{id}'
    print(id)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        phone_number = None
        data = data['custom_fields_values']
        try:
            for field in data:
                if field['field_name'] == 'А5: телефон':
                    phone_number = field['values'][0]['value']
                    return phone_number
            return None
        except:
            return None
    else:
        print(f'Ошибка {response.status_code}: {response.json()}')
        return []

# Функция для получения лидов по статусу
def get_latest_leads_by_status(limit,page):
    status = {
        "id": 64790430,
        "name": "Дубли",
        "sort": 70,
        "is_editable": True,
        "pipeline_id": 7877450,
        "color": "#f3beff",
        "type": 0,
        "account_id": 31453934,
        "_links": {
            "self": {
                "href": "https://kriloks303.amocrm.ru/api/v4/leads/pipelines/7877450/statuses/64790430"
            }
        }
    },

    url = 'https://kriloks303.amocrm.ru/api/v4/leads'
    params = {
        'limit': limit,
        'order[created_at]': 'desc',
        'filter[pipeline_id]': 7877450,
        'filter[statuses]': [status],
        'with': 'contacts',
        'page': page
    }
    response = requests.get(url, headers=headers,params=params)
    if response.status_code == 200:
        data = response.json()
        return data['_embedded']['leads']


def move_to_status(lead,status_ids):
    id = lead['id']
    url = f'https://kriloks303.amocrm.ru/api/v4/leads/{id}'
    params = {
        'status_id' : status_ids
    }
    response = requests.patch(url, headers=headers, json=params)

def newlead(file, id):
    file.seek(0)  # Перемещаем указатель в начало файла
    for line in file:
        if str(id) in line:
            return False
    return True
leads = [1,]
page = 0
while(len(leads)):
    leads = get_latest_leads_by_status(40000,page)
    page+=1
    print(page,len(leads))
    if leads:
        for i in leads:
            if i['status_id'] != 64790430:
                continue
            lead_id = i['id']
            contact_id = i['_embedded']['contacts'][0]['id']
            name = get_contacts_info(contact_id)
            phone = get_leads_info(lead_id)
            isincrm = send_lead(phone, name)
            if phone:
                if isincrm:
                    move_to_status(i, 64790290)
                    print(name, phone, "занесён в Кенди")
