from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os
import random 

def delay(minimo=1.5, maximo=3.5):
    time.sleep(random.uniform(minimo, maximo))

def scroll_lista(navegador):
    scrollable_div = navegador.find_element(By.CSS_SELECTOR, 'div[role="feed"]')

    for i in range(10):
        navegador.execute_script( "arguments[0].scrollTop = arguments[0].scrollHeight",scrollable_div)
        delay(1, 2)

servico = Service(ChromeDriverManager().install())
navegador_options = webdriver.ChromeOptions()
# Mantém o navegador aberto mesmo após o fim da sessão do webdriver
navegador_options.add_experimental_option("detach", True)

navegador = webdriver.Chrome(service=servico, options=navegador_options)

navegador.get('https://www.google.com/maps')
time.sleep(10)

nicho = input("Digite o nicho (ex: Dentist): ")
cidade = input("Digite a cidade (ex: Miami): ")
quantidade = int(input("Quantas empresas deseja extrair? "))

busca = f"{nicho}, {cidade}"

from urllib.parse import quote

busca_codificada = quote(busca)
url = f"https://www.google.com/maps/search/{busca_codificada}"

navegador.get(url)
wait = WebDriverWait(navegador, 15)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.Nv2PK')))

scroll_lista(navegador) 
delay(2, 4)

todos_cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.Nv2PK')))

dados = []

for i in range(quantidade):

    # Recarrega lista sempre que volta
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.Nv2PK')))
    todos_cards = navegador.find_elements(By.CSS_SELECTOR, 'div.Nv2PK')

    lista_empresas = []

    for card in todos_cards:
        try:
            card.find_element(By.XPATH, ".//*[contains(text(), 'Sponsored') or contains(text(), 'Patrocinado')]")
            continue
        except:
            lista_empresas.append(card)

    if i >= len(lista_empresas):
        print("Não há mais empresas disponíveis.")
        break

    empresa = lista_empresas[i]
    navegador.execute_script("arguments[0].scrollIntoView(true);", empresa)
    delay(1, 2)

    empresa.click()

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.DUwDvf')))
    delay()

    nome = navegador.find_element(By.CSS_SELECTOR, 'h1.DUwDvf').text

    try:
        telefone_raw = navegador.find_element(By.CSS_SELECTOR,'button[data-item-id^="phone"]').text
        telefone = telefone_raw.split("\n")[-1]
    except:
        telefone = "Not available"

    try:
        site = navegador.find_element(By.CSS_SELECTOR,'a[data-item-id="authority"]').get_attribute("href")
    except:
        site = "Not available"

    try:
        endereco = navegador.find_element(By.CSS_SELECTOR,'button[data-item-id="address"]').text
        endereco = endereco.replace("\n", ", ")
        endereco = endereco.encode("utf-8", "ignore").decode("utf-8")
    except:
        endereco = "Not available"

    dados.append({
        "nome": nome,
        "telefone": telefone,
        "site": site,
        "endereco": endereco
    })

    print(f"{i+1} - {nome}")  

    # Fecha painel da empresa
    botao_fechar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Voltar"]')))
    botao_fechar.click()

    delay(1.5, 3)

    # Pequena espera para garantir que lista está ativa
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.Nv2PK')))

print(os.getcwd())
df = pd.DataFrame(dados, columns=["nome", "telefone", "site", "endereco"])
pasta_atual = os.path.dirname(os.path.abspath(__file__))
caminho_arquivo = os.path.join(pasta_atual, "leads.csv")

df.to_csv(caminho_arquivo, index=False, sep=";", encoding="utf-8-sig")

print("Arquivo salvo com sucesso!")
    