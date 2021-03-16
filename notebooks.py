#%%
links = tuple(f'https://www.pichau.com.br/computadores/pichau-home?p={page}&product_list_limit=48' for page in range(1, 4))
# %%
import bs4
import cloudscraper
import pandas as pd
import re
#%%
scraper = cloudscraper.create_scraper().get

#%%
responses = tuple(scraper(url).text for url in links)

#%%
def get_urls(response):
    page = bs4.BeautifulSoup(response, 'html.parser')
    css = 'div.products.wrapper.grid.products-grid > ol > li > div > a'
    computers = page.select(css)
    urls = [data['href'] for data in computers]
    return urls

#%%

urls = sum(map(get_urls, responses), [])
#%%
#
import time

def read_html(index, url):
    print(f'página {index}')
    try:
        return bs4.BeautifulSoup(scraper(url).text, 'html.parser')
    except:
        time.sleep(5)
        return read_html(url)

#%%
def regex_find(regex, data):
    try:
        return re.findall(regex, data)[0]
    except:
        return ''

#%%
def process_data(index, url):
    page = read_html(index, url)

    data = '\n'.join([val.text for val in page.select('div > h2.product-name')])
  
    processador = regex_find('Processador .*', data)
  
    RAM = regex_find('.*RAM.*', data)
  
    SSD = regex_find('.*SSD.*', data)
    
    try:
        price = page.select('#maincontent > div.columns > div > div.product-info-main > div.product-info-price > div.price-box.price-final_price > p > span.price-container.price-final_price.tax')[0].text
    except:
        price = ''
        
    return (processador, RAM, SSD, ' '.join(price.split()).replace('As low ', ''), url)

#%%
def generate_DataFrame(urls):
    DataFrame = pd.DataFrame(process_data(*url) for url in enumerate(urls))

    DataFrame.columns = ['processador', 'ram', 'ssd', 'preco', 'link']

    return DataFrame
# %%

frame = generate_DataFrame(urls)

#%%
frame.to_csv('computadores.csv', index = False)
# %%
