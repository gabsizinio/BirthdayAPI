import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re

def list_popular_animes():
    #Fazer a requisição para obter o HTML da página
    urls = ["https://myanimelist.net/topanime.php?type=bypopularity", "https://myanimelist.net/topanime.php?type=bypopularity&limit=50", "https://myanimelist.net/topanime.php?type=bypopularity&limit=100", "https://myanimelist.net/topanime.php?type=bypopularity&limit=150", "https://myanimelist.net/topanime.php?type=bypopularity&limit=200"]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
    }

    animes = []

    for url in urls:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            html = response.text

            soup = BeautifulSoup(html, "html.parser")
            
            tags = soup.find_all("a", class_="hoverinfo_trigger")

            for tag in tags:
                animes.append(tag.text)

        else:
            print(f"Erro: {response.status_code}")
    
    animes = [anime for anime in animes if anime.strip()]

    return animes

def list_popular_series():
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/110.0.0.0 Safari/537.36")


    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Abre a página do IMDB
    url = "https://www.imdb.com/chart/toptv/?sort=num_votes%2Cdesc"
    driver.get(url)

    # Espera um tempo para a página carregar completamente (caso precise)
    time.sleep(3)

    # Pega o HTML da página depois do carregamento completo do JavaScript
    soup = BeautifulSoup(driver.page_source, "html.parser")
    #print(soup.prettify())
    # Fecha o navegador
    driver.quit()

    # Encontra os títulos das séries
    tags = soup.find_all("h3", class_="ipc-title__text")

    series = [tag.text.strip() for tag in tags if tag.text.strip()]

    series = series[:-13]
    
    series = [re.sub(r"^\d+\.\s*", "", serie) for serie in series]
    
    return series

def list_popular_movies():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/110.0.0.0 Safari/537.36")


    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Abre a página do IMDB
    url = "https://www.imdb.com/chart/top/?sort=num_votes%2Cdesc"
    driver.get(url)

    # Espera um tempo para a página carregar completamente (caso precise)
    time.sleep(3)

    # Pega o HTML da página depois do carregamento completo do JavaScript
    soup = BeautifulSoup(driver.page_source, "html.parser")
    #print(soup.prettify())
    # Fecha o navegador
    driver.quit()

    # Encontra os títulos das séries
    tags = soup.find_all("h3", class_="ipc-title__text")

    movies = [tag.text.strip() for tag in tags if tag.text.strip()]

    movies = movies[:-13]
    
    movies = [re.sub(r"^\d+\.\s*", "", movie) for movie in movies]
    
    return movies

def list_popular_games():
    url = "https://vgsales.fandom.com/wiki/Best_selling_game_franchises"

    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
    }

    
    response = requests.get(url, headers=headers)

    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

    
    table = soup.find("table", {"class": "wikitable"})

    
    franchises = []

    
    for row in table.find_all("tr")[1:]: 
        columns = row.find_all("td")

        # Verifica se há pelo menos duas colunas (índice e nome da franquia)
        if len(columns) > 1:
            index = columns[0].text.strip()  
            franchise_name = columns[1].text.strip()  


            if index.isdigit():
                franchises.append(franchise_name)
    
    return franchises

def list_popular_books():
    urls = ["https://www.goodreads.com/list/show/50.The_Best_Epic_Fantasy_fiction_", "https://www.goodreads.com/list/show/3.Best_Science_Fiction_Fantasy_Books"]

    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
    }

    books = []

    for url in urls:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            html = response.text

            soup = BeautifulSoup(html, "html.parser")

            tags = soup.find_all("span", attrs={"role": "heading"})

            for tag in tags:
                books.append(tag.text)
        
        else:
            print(f"Erro: {response.status_code}")
    
    return books

l = list_popular_animes()  

for e in l:
    print(e)
#list_popular_movies()
#list_popular_series()
#list_popular_movies()
#list_popular_games()
#list_popular_books()