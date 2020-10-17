# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 18:20:38 2020

@author: nicol
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pandas as pd
from tqdm import tqdm
import time


url = 'https://www.larepublica.co/economia'
r = requests.get(url, timeout=30)
soup = BeautifulSoup(r.text, 'html.parser')

urls = []
articulos = soup.find('div', {'class': 'container section sect-economia'})
for a in articulos.find_all('a', href=True):
    urls.append(a['href'])

urls = list(set(urls))

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
        header = soup.find('div', {'class': 'col-8 order-2 d-flex flex-column'})
        article = soup.find('div', {'id': 'proportional-anchor-1'})
        
        autor = article.find('div', {'class': 'autorArticle'}).text.strip()
        subtitulo = article.find('div', {'class': 'lead'}).text.strip()
        articulo = article.find('div', {'class': 'html-content'}).text.strip()
        
        titulo = header.find('a', {'class': 'economiaSect'}).text.strip()
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
    
    time.sleep(5)
        
        
df = pd.DataFrame(list(zip(titulos, fechas, temas, autores, subtitulos, articulos, originals)),
                  columns =['titulos', 'fechas', 'temas', 'autores', 'subtitulos', 'articulos', 'url'])


df.to_excel('larepublica.xlsx', index=False)