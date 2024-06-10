import requests
from bs4 import BeautifulSoup

def get_currency_data():
    url = "https://bank.uz/uz/currency/dollar-ssha"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    organization_contacts = soup.find('div', class_='organization-contacts')

    left_blocks = organization_contacts.find('div', class_='bc-inner-blocks-left').find("div", class_="bc-inner-block-left")
    right_blocks = organization_contacts.find('div', class_='bc-inner-blocks-right')

    if not organization_contacts:
        return None

    data = {}

    for left_block in left_blocks.find_all('div', class_='bc-inner-block-left-texts'):
        currency_name = left_block.find('span', class_='medium-text').get_text(strip=True)
        currency_value = left_block.find('span', class_='green-date').get_text(strip=True)
        data[currency_name] = {"buy": currency_value}

    for right_block in right_blocks.find_all('div', class_='bc-inner-block-left-texts'):
        currency_name = right_block.find('span', class_='medium-text').get_text(strip=True)
        currency_value = right_block.find('span', class_='green-date').get_text(strip=True)

        if currency_name in data:
            data[currency_name]["sell"] = currency_value

    return data

currency_data = get_currency_data()