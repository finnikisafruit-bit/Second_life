import requests


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except (requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


if __name__ == '__main__':
    url = 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/obuv_muzhskaya/botinki_i_polubotinki-ASgBAgICAkTeArqp1gLOvQ6~nJQC'
    html = get_html(url)
    if html:
        with open('avito_ru_main.html', 'w', encoding='UTF-8') as f:
            f.write(html)
