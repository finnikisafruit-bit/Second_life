from bs4 import BeautifulSoup



def get_product_info(html_file):
    with open(html_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, 'html.parser') 


    for a in soup.find_all('span', {'itemprop': 'price'}):
        price = a.get("content")
        print(price)

if __name__ == "__main__":
    get_product_info("product.html")

    


