import requests
import os
from bs4 import BeautifulSoup

def url_to_soup(url):
    req = requests.get(url)
    return BeautifulSoup(req.content, 'html.parser')

def get_all_event_page_link(event_page_link_list, url):
    soup = url_to_soup(url)
    link_list = [x.get('href') for x in soup.find_all('a')]
    event_page_link_list.extend([os.environ['HOME_URL'] + x[1:] for x in link_list if x if x.startswith('./event/')])
    next_page_link = list(set([x for x in soup.find_all('a') if x if x.get('aria-label')]))
    for x in next_page_link:
        if x.get('aria-label') == '次のページへ':
            get_all_event_page_link(event_page_link_list, os.environ['HOME_URL'] + x.get('href')[1:])
    return event_page_link_list

def get_event_detail(url):
    soup = url_to_soup(url)
    table = soup.find_all('table', class_='table table-responsive')[0]
    td_list = [x for x in table.findAll("td") if x]
    event_name = td_list[0].text.strip()
    date = td_list[1].text.strip()
    place = td_list[2].text.strip()
    address = td_list[3].text.strip()
    print("----------------------------------------------------------------------")
    print('イベントタイトル: ' + event_name)
    print('イベント日時　　: ' + date)
    print('開催場所　　　　: ' + place)
    print('開催住所　　　　: ' + address)

def main():
    for x in get_all_event_page_link([], os.environ['SEARCH_URL']):
        get_event_detail(x)

if __name__ == '__main__':
    try:
        main()
    except:
        pass
