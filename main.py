import requests
import argparse
import os
from urllib.parse import urlparse
from requests.exceptions import HTTPError
from dotenv import load_dotenv

parser = argparse.ArgumentParser()
parser.add_argument("link")
args = parser.parse_args()

LINK = "https://api-ssl.bitly.com/v4"


def shorten_link(token, url: str):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    start_url = {"long_url": url}
    link = f'{LINK}/shorten'
    response = requests.post(link, headers=headers, json=start_url)
    response.raise_for_status()

    return response.json()['link']


def count_clicks(token, bitlink):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    bitlink = urlparse(bitlink)
    bitlink = f'{bitlink.netloc}{bitlink.path}'
    params = {
        'unit': 'month',
        'units': '-1' 
        }
    link = f"{LINK}/bitlinks/{bitlink}/clicks/summary"
    response = requests.get(link, headers=headers, params=params)
    response.raise_for_status()
    
    return response.json()['total_clicks']


def is_bitlink(token, url):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    url = urlparse(url)
    url = f'{url.netloc}{url.path}'
    link = f'{LINK}/bitlinks/{url}'
    response = requests.get(link, headers=headers)

    return response.ok
        

def main(link):
    load_dotenv()
    token = os.environ['BITLY_TOKEN']

    try:
        if is_bitlink(token, link):
            sum_click = count_clicks(token, link)
            print(f'По вашей ссылке прошли {sum_click} раз(а)')
            return 
        
        print(shorten_link(token, link))
        return 
    except HTTPError as ex:
        print(f"\n Ошибка \n\n {ex}")
        return 
    

if __name__ == '__main__':
    main(args.link)
    
    