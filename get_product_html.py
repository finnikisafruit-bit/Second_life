from get_main_html import get_html


if __name__ == "__main__":
    with open("links.txt", encoding="utf-8") as f:
        url = f.readline()     
          
    html = get_html(url)
    if html:
        with open("product.html", "w", encoding="utf-8") as f:
            f.write(html)