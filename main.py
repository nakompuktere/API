import requests
from urllib.parse import urlparse
import os
import argparse
from dotenv import load_dotenv
load_dotenv()


def shorten_link(bitly_token, long_url):
    url = "https://api-ssl.bitly.com/v4/shorten"
    payload = {"long_url": long_url}
    headers = {"Authorization": f"Bearer {bitly_token} " }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["link"]


def count_clicks(bitly_token, bitlink):
    bitlink = urlparse(bitlink)
    bitlink = f"{bitlink.netloc}{bitlink.path}"
    headers = {"Authorization": f"Bearer {bitly_token}"}
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["total_clicks"]


def is_bitlink(long_url, bitly_token):
    long_url = urlparse(long_url)
    long_url = f"{long_url.netloc}{long_url.path}"
    headers = {"Authorization": f"Bearer {bitly_token}"}
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{long_url}"
    response = requests.get(url, headers=headers)
    return response.ok


def main():
    parser = argparse.ArgumentParser(description='сокращает ссылки, считает количество кликов по ссылке')

    parser.add_argument('link', help="Ведите ссылку")
    args = parser.parse_args()
    bitly_token = os.environ['BITLY_TOKEN']
    try:
        if is_bitlink(args.link, bitly_token):
            print(count_clicks(bitly_token, args.link))
        else: 
            bitlink = shorten_link(bitly_token, args.link)
            print("битлинк:", bitlink)
    except requests.exceptions.HTTPError:
        print("Вы ввели неправильную ссылку или неверный токен.")


if __name__ == "__main__":
   main()