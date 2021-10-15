import csv
import sys
from typing import List
import tkinter as tk
from tkinter import *

import requests
from bs4 import BeautifulSoup
urls = []
root = tk.Tk()
FILE = ''
sum_lab = tk.Entry(fg="yellow", bg="blue", width=50)
fora_lab = tk.Entry(fg="yellow", bg="blue", width=50)


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"
}


def get_html(url, params=None) -> str:
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    return r.text


def get_specifications_parameter(url: str) -> dict:
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    param = soup.find_all("dd", class_="range-revamp-product-dimensions__list-item-measure")
    titles = soup.find_all("dt", class_="range-revamp-product-dimensions__list-item-name")
    content = {}

    for title, value in zip(titles, param):
        content[title.text.strip("\xA0:")] = value.text
    return content
def get_price(url):
    html = get_html(url)
    soup = BeautifulSoup(html,'html.parser')
    price = soup.find('span',class_='range-revamp-price__integer').text
    return price

def get_name(url):
    html = get_html(url)
    soup = BeautifulSoup(html,'html.parser')
    name = soup.find('div',class_='range-revamp-header-section__title--big notranslate').text
    return name

def get_descropthion(url):
    html = get_html(url)
    soup = BeautifulSoup(html,'html.parser')
    descropthion = soup.find('span',class_='range-revamp-product-details__paragraph').text
    return descropthion

def get_identifier(url):
    html = get_html(url)
    soup = BeautifulSoup(html,'html.parser')
    identifier = soup.find('span',class_='range-revamp-product-identifier__value').text
    return "I" + identifier
    
def get_photo(url):
    html = get_html(url)
    soup = BeautifulSoup(html,'html.parser')
    photo = soup.find('span',class_='range-revamp-aspect-ratio-image range-revamp-aspect-ratio-image--square range-revamp-media-grid__media-image').find('img').get('src')
    return photo

def scrape_urls(urls: List[str]) -> List[dict]:
    contents = []
    for url in urls:
        name = get_name(url)
        price = get_price(url)
        descropthion = get_descropthion(url)
        photo = get_photo(url)
        content = get_specifications_parameter(url)
        identifier = get_identifier(url)
        content["url"] = url
        content["Название"] = name
        content["Описание"] = price
        content["Характеристики"] = descropthion
        content["Фотография"] = photo
        content["Артикул"] = identifier



        print(content, file=sys.stderr)  # progress printing
        contents.append(content)
    return contents


def write_output(contents: List[dict]):
    all_keys = set()
    for content in contents:
        all_keys |= set(content)
    w = csv.DictWriter(open(FILE + ".csv", "w",encoding='utf-8'), all_keys)
    w.writeheader()
    for content in contents:
        w.writerow(content)

def get_url(html):
    soup = BeautifulSoup(html,'html.parser')
    url = soup.find_all('div',class_='range-revamp-product-compact')
    for URL in url:
        urls.append(URL.find('a').get('href'))
   
    contents = scrape_urls(urls)
    write_output(contents)

def start():
    global FILE
    url_text = name_entry.get()
    FILE = pswd_entry.get()
    URL = (url_text + '?page=100')
    html = get_html(URL)
    get_url(html)
   


name_label = Label(text="URL:")
pswd_label = Label(text="Введите название файла(без .csv):")


name_entry = tk.Entry()
pswd_entry = tk.Entry()


name_entry.grid(row=0,column=1, padx=5, pady=5, sticky="e")
pswd_entry.grid(row=1,column=1, padx=5, pady=5, sticky="e")

name_label.grid(row=0,column=0, padx=5, pady=5)
pswd_label.grid(row=1,column=0, padx=5, pady=5)


message_button = Button(text="Старт",command=start)


root.mainloop()
