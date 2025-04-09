import os
import urllib.parse
import re

def transform_date(date_string):
    """Transforma uma data do tipo 'December 1st, 1998' para 'December 1'."""
    # Regex para detectar a data com mês e dia (por exemplo, 'December 1st')
    match = re.match(r"([A-Za-z]+)\s(\d{1,2})(st|nd|rd|th)?,?\s*(\d{4})?", date_string)
    if match:
        # Extrai o mês e o dia
        month = match.group(1)
        day = match.group(2)
        return f"{month} {day}"
    return None  # Retorna None se não for uma data válida

def decode_url_encoded(character_list):
    """Decodifica nomes codificados e formata a data do terceiro membro."""
    decoded_list = []
    
    for character in character_list:
        # Decodificar o primeiro item (nome do personagem) se for codificado
        decoded_name = urllib.parse.unquote(character[0]) if isinstance(character[0], str) else character[0]
        
        # Verificar e formatar o terceiro item (data)
        if len(character) > 2:
            new_date = transform_date(character[2])  # Modificar o terceiro item se houver
            if new_date:  # Se a data for válida
                character[2] = new_date
                decoded_list.append([decoded_name] + character[1:])
        else:
            # Se não houver data válida no terceiro item, a linha é ignorada
            continue
    
    return decoded_list

def process_characters_files(directory):
    """Processa todos os arquivos dentro do diretório 'characters_list'."""
    # Verifica se o diretório existe
    if not os.path.exists(directory):
        print(f"Diretório {directory} não encontrado.")
        return
    
    # Percorrer todos os arquivos na pasta 'characters_list'
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):  # Garantir que estamos lidando com arquivos .txt
            file_path = os.path.join(directory, filename)
            print(f"Processando arquivo: {filename}")
            
            # Abrir o arquivo e ler as linhas
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
            
            character_list = []
            # Processar as linhas e decodificar os nomes
            for line in lines:
                line = line.strip()
                if line:  # Ignorar linhas vazias
                    # Supondo que os dados sejam separados por vírgula (ou outro separador)
                    character_data = line.split(", ")
                    
                    # Verificar se o nome está codificado
                    if character_data and character_data[0]:
                        character_list.append(character_data)
            
            # Decodificar todos os nomes de personagens e formatar as datas
            decoded_character_list = decode_url_encoded(character_list)
            
            # Salvar os dados decodificados de volta no arquivo
            with open(file_path, "w", encoding="utf-8") as file:
                for character in decoded_character_list:
                    file.write(", ".join(str(item) for item in character) + "\n")
            
            print(f"✅ Arquivo {filename} processado com sucesso.")
            
directory = "characters_lists"  # Caminho para a pasta de arquivos

# Processar todos os arquivos dentro do diretório
process_characters_files(directory)
