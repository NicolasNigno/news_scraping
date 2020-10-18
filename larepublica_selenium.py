from selenium import webdriver
import pandas as pd
import time
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm


browser = webdriver.Chrome(executable_path=r'C:\Users\nicol\Downloads\chromedriver.exe') ## path quemado

url = 'https://www.larepublica.co/buscar?term=banco+de+la+republica'
# url = 'https://www.larepublica.co/buscar?term=banco+de+la+republica&from={}T00%3A00%3A00-05%3A00&to={}T00%3A00%3A00-05%3A00'.format('2020-08-01', '2020-11-01')

browser.get(url)
time.sleep(5)

try:
    path_search = r"//*[@id='vue-container']/div[2]/div[2]/div[2]/div/div/button"
    elem = browser.find_element_by_xpath(path_search)
    more = True
except:
    more = False

while more:
    elem.click()
    try:
        elem = browser.find_element_by_xpath(path_search)
        more = True
    except:
        more = False


container = browser.find_element_by_xpath('//*[@id="sticky-anchor-1"]')
articulos = container.find_elements_by_xpath(".//a")
urls = [articulo.get_attribute('href') for articulo in articulos]

browser.quit()

titulos = []
articulos = []
fechas = []
temas = []
autores = []
subtitulos = []
originals = []

for url in tqdm(urls):
    r = requests.get(url, timeout=30)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    try:
        header = soup.find('div', {'class': 'col-8 order-2 d-flex flex-column'}) ## classic header 
        article = soup.find('div', {'id': 'proportional-anchor-1'})
        
        autor = article.find('div', {'class': 'autorArticle'}).text.strip()
        subtitulo = article.find('div', {'class': 'lead'}).text.strip()
        articulo = article.find('div', {'class': 'html-content'}).text.strip()
        
        titulo = header.find('a').text.strip() #{'class': 'economiaSect'}
        tema = header.find('span').text.strip()
        fecha = header.find('div', {'class': 'd-flex align-items-end'}).text.strip()

        titulos.append(titulo)
        fechas.append(fecha)
        temas.append(tema)
        articulos.append(articulo)
        autores.append(autor)
        subtitulos.append(subtitulo)
        originals.append(url)
    except:
        titulos.append(None)
        fechas.append(None)
        temas.append(None)
        articulos.append(None)
        autores.append(None)
        subtitulos.append(None)
        originals.append(url)
    
    #time.sleep(5)
        
        
df = pd.DataFrame(list(zip(titulos, fechas, temas, autores, subtitulos, articulos, originals)),
                  columns=['titulos', 'fechas', 'temas', 'autores', 'subtitulos', 'articulos', 'url'])


df.to_excel(r'data\larepublica.xlsx', index=False)