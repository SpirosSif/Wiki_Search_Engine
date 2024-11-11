#pip install requests
#pip install beautifulsoup4
#pip install requests
#pip install beautifulsoup4
import requests
from bs4 import BeautifulSoup
import json
import time
import re

url ='https://en.wikipedia.org/w/index.php?search=heroes+of+1821+greece&title=Special%3ASearch&ns0=1'
html = requests.get(url)
soup = BeautifulSoup(html.content, 'html.parser')
entries =soup.find_all('li', class_='mw-search-result mw-search-result-ns-0')
#print(entries)
data = []

for entry in entries:
    title_element = entry.find('div', class_='mw-search-result-heading')
    date_element = entry.find('div', class_='mw-search-result-data')

    if title_element and date_element:
        first_title = title_element.text.strip()
        date_parts = re.split(r'[-\n]', date_element.text.strip())
        infos = date_parts[0].strip() if len(date_parts) > 1 else "N/A"
        date = date_parts[1].strip() if len(date_parts) > 1 else "N/A"
        
       
        link_element = title_element.find('a')
        
        if link_element and 'href' in link_element.attrs:
            content_url = 'https://en.wikipedia.org' + link_element['href']
        else:
            print("No href attribute found")
            continue  

        content_html = requests.get(content_url)
        content_soup = BeautifulSoup(content_html.content, 'html.parser')
        content_element = content_soup.find('div', class_='mw-content-ltr mw-parser-output')
        
        content = content_element.text.strip() if content_element else "N/A"

        data.append([first_title, infos, date, content])
        print(f'First_Title: {first_title}\n\nInformations: {infos}\n\n Date: {date}\n\nContent: {content}\n{"-" * 50}')
    
    time.sleep(1)


json_filename = "results.json"
with open(json_filename, 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=2)

print(f"Τα δεδομένα αποθηκεύτηκαν στο αρχείο: {json_filename}")

