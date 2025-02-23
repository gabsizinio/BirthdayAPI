from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import random  # Para tempo de espera aleatório
import list_popular

def list_all_works():
    works = []

    animes = list_popular.list_popular_animes()
    books = list_popular.list_popular_books()
    games = list_popular.list_popular_games()
    movies = list_popular.list_popular_movies()
    series = list_popular.list_popular_series()

    works = animes + books + games + movies + series

    return works

def list_fandom_links():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    works = list_all_works()
    links = {}

    for work in works:
        query = f"{work} fandom category:characters"
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

        driver.get(search_url)
        time.sleep(random.uniform(2, 4))  # Pequeno tempo para evitar bloqueio do Google

        try:
            # Aguarda até que os resultados apareçam
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h3"))
            )

            # Agora encontramos o <h3> primeiro
            first_result = driver.find_element(By.CSS_SELECTOR, "h3")

            # Depois subimos para o <a> que o contém e pegamos o href
            parent_link = first_result.find_element(By.XPATH, "./ancestor::a").get_attribute("href")

            links[work] = parent_link
            print(f"{work}: {parent_link}")

        except Exception as e:
            print(f"Erro ao buscar {work}: {e}")
            links[work] = None

        # Aguarda entre 3 e 6 segundos para evitar bloqueios do Google
        time.sleep(random.uniform(3, 6))

    driver.quit()
    return links

def save_links_to_file(links, filename="links.txt"):
    with open(filename, "w", encoding="utf-8") as file:
        for work, link in links.items():
            if link:  
                file.write(f"{work}: {link}\n")
            else:
                file.write(f"{work}: Nenhum link encontrado\n")
    print(f"\n✅ Links salvos em {filename}")

def find_non_category_lines(filename="links.txt"):
    """Percorre o arquivo e guarda o índice das linhas que não contêm 'Category:Characters'"""
    non_category_indices = []

    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()  # Lê todas as linhas do arquivo

        for index, line in enumerate(lines):
            if "Category:" not in line:
                non_category_indices.append(index)  # Guarda o índice da linha

    return non_category_indices


def remove_duplicate_links(filename="links.txt", output_filename="links_cleaned.txt"):
    """Remove linhas duplicadas do arquivo, mantendo apenas a primeira ocorrência de cada link."""
    unique_links = {}
    
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    with open(output_filename, "w", encoding="utf-8") as file:
        for line in lines:
            parts = line.strip().split(": ", 1)  # Divide no primeiro ": "
            if len(parts) == 2:
                work, link = parts
                if link not in unique_links:  # Se o link ainda não foi adicionado
                    unique_links[link] = work
                    file.write(f"{work}: {link}\n")
    



# Próximos passos:

# 1) Acessar os Links, extrair os personagens mais populares (critério: número de palavras em cada uma das páginas dos mesmos)
# 2) Com a lista de personagens, abrir a página de cada um e extrair os aniversários

#list_fandom_links()