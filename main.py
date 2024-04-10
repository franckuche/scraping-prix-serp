import pandas as pd
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import numpy as np  # For median calculation
import re

def interroger_api(mot_clef):
    print(f"Starting API interrogation for keyword: {mot_clef}")
    params = {
        'api_key': 'C25E576BDB1B461CA233A9905E909031',
        'q': mot_clef,
        'location': 'France',
        'google_domain': 'google.fr',
        'gl': 'fr',
        'hl': 'fr',
        'num': '10',
        'device': 'mobile',
        'output': 'json'
    }
    try:
        api_result = requests.get('https://api.valueserp.com/search', params=params)
        api_result.raise_for_status()
        json_response = api_result.json()
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred for {mot_clef}: {http_err}")
        return []
    except requests.RequestException as req_err:
        print(f"Request error occurred for {mot_clef}: {req_err}")
        return []
    except json.JSONDecodeError as json_err:
        print(f"JSON parsing error for {mot_clef}: {json_err}")
        return []

    results = [{'lien': result['link'], 'position': result['position']} for result in json_response.get('organic_results', [])]
    print(f"Extracted data for {mot_clef}: {results}")
    return results

def recuperer_prix(url):
    print(f"Loading page for URL: {url}")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")  # Ajouter cet argument pour simuler une demande provenant de Mozilla Firefox
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Validation de l'URL
        if not url or "http://" not in url and "https://" not in url:
            print(f"URL invalide ou manquante: {url}")
            return []
        
        driver.get(url)
        time.sleep(3)
        found_prices = []

        if "amazon." in url:
            whole_elements = driver.find_elements(By.CSS_SELECTOR, "span.a-price-whole")
            fraction_elements = driver.find_elements(By.CSS_SELECTOR, "span.a-price-fraction")
            for whole, fraction in zip(whole_elements, fraction_elements):
                whole_text = re.sub(r'[\s\xa0]+', '', whole.text.replace('.', '').replace(',', '.'))
                fraction_text = fraction.text.strip()
                full_price = f"{whole_text}.{fraction_text}"
                try:
                    price_value = float(full_price)
                    found_prices.append(price_value)
                    print(f"Found Amazon price: {full_price}")
                except ValueError:
                    print(f"Error converting Amazon price: {full_price}")
        else:
            selectors = [".price", ".Price", "[itemprop='price']", ".product-price", "span[class*='price']", ".diaVal", ".priceLine", ".KIH6jK", ".emptyLine", ".product-price", ".s-item__price", ".product-price-container pl-price"]
            for selector in selectors:
                price_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in price_elements:
                    price_text = element.text.strip()
                    cleaned_price = re.sub(r'[\s*]+', '', price_text.replace('EUR', '').replace('€', '').replace('$', '').replace(',', '.'))
                    if '–' in cleaned_price:
                        prices = cleaned_price.split('–')
                        try:
                            prices = [float(price.strip()) for price in prices]
                            avg_price = sum(prices) / len(prices)
                            found_prices.append(avg_price)
                            print(f"Average price found: {avg_price} for range {prices}")
                        except ValueError:
                            print(f"Error converting range price: {cleaned_price}")
                    else:
                        try:
                            price_value = float(cleaned_price)
                            found_prices.append(price_value)
                            print(f"Valid price found with {selector} on {url}: {price_value}")
                        except ValueError:
                            print(f"Error converting price: {cleaned_price}")
        return found_prices
    except Exception as e:
        print(f"Error loading URL: {url}")
        print(f"Detailed error: {e}")
        return []
    finally:
        driver.quit()

def charger_mots_clefs_de_csv(file_path):
    df = pd.read_csv(file_path)
    return df['keyword'].tolist() if 'keyword' in df.columns else []

def principal():
    mots_clefs = charger_mots_clefs_de_csv('keywords.csv')
    data_for_csv = []
    nombre_max_urls = 10  # Définir le nombre maximal d'URLs à traiter

    for mot_clef in mots_clefs:
        print(f"Traitement du mot-clé : {mot_clef}")
        resultats = interroger_api(mot_clef)
        if len(resultats) > nombre_max_urls:
            resultats = resultats[:nombre_max_urls]  # Limiter à 10 résultats
        elif len(resultats) < nombre_max_urls:
            # Ajouter des entrées vides si moins de 10 URLs sont retournées
            resultats += [{'lien': 'N/A résultat non donné API', 'position': i+1} for i in range(len(resultats), nombre_max_urls)]

        row = [mot_clef]  # Commencer la rangée avec le mot-clé
        urls_sans_prix = []  # Liste pour stocker les URLs sans prix
        saulaie_prices = []  # Collecter les prix spécifiquement des URLs de Saulaie
        serp_prices = []  # Collecter les prix de la SERP

        for resultat in resultats:
            prix = recuperer_prix(resultat['lien'])
            if "saulaie.com" in resultat['lien'] and prix:
                saulaie_prices.extend(prix)
            if prix:
                serp_prices.extend(prix)

            if prix:
                prix_median = np.median(prix) if prix else "N/A résultat non donné API"
                row.append(prix_median)
            else:
                row.append("N/A pas de prix")
                urls_sans_prix.append(resultat['lien'])

        # Calculer les prix médians de la Saulaie et de la SERP
        saulaie_median = np.median(saulaie_prices) if saulaie_prices else "Saulaie NP"
        serp_median = np.median(serp_prices) if serp_prices else "SERP NP"
        row.append(saulaie_median)
        row.append(serp_median)

        # Concaténer les URLs sans prix
        row.append("; ".join(urls_sans_prix))

        data_for_csv.append(row)

    # Sauvegarder dans un CSV après chaque mot-clé pour éviter la perte de données
    df = pd.DataFrame(data_for_csv, columns=['keyword'] + [f'prix moyen URL position {i+1}' for i in range(nombre_max_urls)] + ['Prix médian Saulaie', 'Prix médian SERP', 'URLs sans prix'])
    df.to_csv('output_progressive.csv', index=False)
    print("Les données ont été enregistrées dans le fichier CSV.")

if __name__ == "__main__":
    principal()
