from bs4 import BeautifulSoup

html = "avito_ru_main.html"

def get_links_from_page(html_file):
    base_url = "https://www.avito.ru"
    links = []

    with open(html_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, 'html.parser') 
    
    for a in soup.find_all('a', {'itemprop': 'url'}):
        href = a.get("href")
        full_url = base_url + href
        links.append(full_url)
    return links


if __name__ == '__main__':
    links = get_links_from_page(html)
    with open('links.txt', 'w', encoding='utf-8') as f:
        for link in links:
            f.write(link + '\n')
