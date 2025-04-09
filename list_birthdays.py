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
import os
import re
import base64
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import threading
import requests
from bs4 import BeautifulSoup


def setup_driver():
    options = Options()
    options.set_preference("dom.webdriver.enabled", False)  # Evita detecção de Selenium
    options.set_preference("useAutomationExtension", False)
    options.set_preference("general.useragent.override", 
                           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/123.0")
    
    # Ignorar erros SSL e de segurança
    options.set_preference("network.stricttransportsecurity.preloadlist", False)
    options.set_preference("security.enterprise_roots.enabled", True)
    options.set_preference("browser.privatebrowsing.autostart", True)  # Modo anônimo
    options.set_preference("dom.security.https_only_mode", False)

    # Configuração para evitar bloqueios
    options.set_preference("dom.webdriver.enabled", False)  
    options.set_preference("useAutomationExtension", False)

    # Criação do driver
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    driver.set_page_load_timeout(720)
    return driver


# Aceitar cookies, se o pop-up existir
def accept_cookies(driver):
    try:
        accept_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@data-tracking-opt-in-accept='true']"))
        )
        accept_button.click()
        print("✔ Aviso de cookies fechado com sucesso.")
        time.sleep(2)
    except:
        print("⚠ Nenhum aviso de cookies encontrado.")

# Obter links das letras na seção "All Items"
def get_alphabet_links(driver):
    letter_links = []
    try:
        alphabet_section = driver.find_element(By.CLASS_NAME, "category-page__alphabet-shortcuts")
        letter_elements = alphabet_section.find_elements(By.TAG_NAME, "a")

        for letter in letter_elements:
            if "href" in letter.get_attribute("outerHTML"):
                letter_links.append(letter.get_attribute("href"))
            elif letter.get_attribute("data-uncrawlable-url"):
                encoded_url = letter.get_attribute("data-uncrawlable-url")
                decoded_url = base64.b64decode(encoded_url).decode('utf-8')
                letter_links.append(decoded_url)
    except Exception as e:
        print(f"❌ Erro ao buscar as letras: {e}")
    
    for link in letter_links:
        print(link)
    
    return letter_links[1:]

# Contar palavras em uma página de personagem
def count_words_on_page(driver):
    try:
        text = driver.find_element(By.TAG_NAME, "body").text
        return len(text.split())
    except:
        return 0

# Processar cada link do arquivo
def process_fandom_links(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        lines = file.readlines()

    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December",
              "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Separar nome da obra e link corretamente
        parts = line.split(" ")
        for part in parts:
            if part.startswith("https://"):
                fandom_link = part
                work_name = line.replace(fandom_link, "").strip()
                break
        else:
            print(f"❌ Nenhum link encontrado na linha: {line}")
            continue

        print(f"\n🔍 Processando: {work_name} -> {fandom_link}")

        driver = setup_driver()
        driver.get(fandom_link)
        accept_cookies(driver)

        

        # Coletar os links de cada letra na seção "All Items"
        letter_links = get_alphabet_links(driver)

        character_word_counts = {}  # Dicionário para armazenar os personagens e contagem de palavras

        # Percorrer cada letra
        for letter_link in letter_links:
            time.sleep(2)
            print(letter_link)
            driver.get(letter_link)

            

            # Obter links de personagens na página da letra
            try:
                character_elements = driver.find_elements(By.CSS_SELECTOR, "a.category-page__member-link")
                character_links = [char.get_attribute("href") for char in character_elements]
            except:
                continue

            # Visitar cada personagem e contar palavras
            for char_link in character_links:
                driver.get(char_link)

                time.sleep(2)

                char_name = char_link.split("/")[-1].replace("_", " ")  # Nome do personagem
                word_count = count_words_on_page(driver)

                character_word_counts[char_name] = (word_count, char_link)
                print(f"📌 {char_name}: {word_count} palavras")


        # Ordenar os personagens pelo número de palavras
        sorted_characters = sorted(character_word_counts.items(), key=lambda x: x[1][0], reverse=True)
        print(sorted_characters)
        # Criar diretório para salvar os arquivos
        os.makedirs("characters_lists", exist_ok=True)

        # Salvar a lista em um arquivo txt
        work_name = re.sub(r'[<>:"/\\|?*]', '', work_name)
        output_file = f"characters_lists/{work_name.replace(' ', '_')}.txt"
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(f"{work_name}\n\n")
            counter = 0
            limit = len(sorted_characters) * 0.3
            for char_name, tup in sorted_characters:
                #pesquisar no Google <char_name + work_name + fandom> e clicar no primeiro link
                headers = {
                    "User-Agent": "Mozilla/5.0"
                }
                html = requests.get(tup[1], headers=headers)

                soup = BeautifulSoup(html.text, "html.parser")

                caixa = soup.find("aside", class_="portable-infobox")

                if caixa == None:
                    caixa = soup.find("table", class_="infobox")

                print(caixa)

                birthday = None
                ind = False

                if caixa:
                    textos = caixa.find_all(text=True)  # pega TODO o texto dentro da caixa

                for texto in textos:
                    if any(month in texto for month in months):
                        birthday = texto.strip()
                        print(f"{char_name} {birthday}")
                        break
                
                priority = 0

                if counter > len(sorted_characters) * 0.1 and counter <= len(sorted_characters) * 0.2:
                    priority = 1
                elif  counter > len(sorted_characters) * 0.2 and counter <= len(sorted_characters) * 0.3:
                    priority = 2

                file.write(f"[{char_name}, {work_name}, {priority}, {birthday}]\n")
                
                counter+=1
                if counter > limit:
                    break
            
        driver.quit()
        print(f"✅ Lista salva em {output_file}")



if __name__ == '__main__':
    process_fandom_links("Bloco.txt")

    


