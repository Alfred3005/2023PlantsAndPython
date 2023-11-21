import requests
import pandas as pd

# Configuración inicial
api_key = '64de424f445d2edba43a030fe459761e'
query = 'TITLE-ABS-KEY(metabolite profile) AND TITLE-ABS-KEY(plants)'
base_url = "https://api.elsevier.com/content/search/scopus"
headers = {
    "X-ELS-APIKey": api_key,
    "Accept": "application/json"
}

# Función para realizar la búsqueda
def search_scopus(query, count=25, start=0):
    """ Realiza una búsqueda en la API de Scopus """
    params = {
        "query": query,
        "count": count,
        "start": start,
        "view": "STANDARD"
    }
    response = requests.get(base_url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error en la solicitud:", response.status_code)
        return None

# Función para extraer abstracts
def extract_abstracts(search_results):
    """ Extrae los abstracts de los resultados de búsqueda """
    abstracts = []
    for item in search_results.get('search-results', {}).get('entry', []):
        abstract_data = {
            "title": item.get("dc:title"),
            "doi": item.get("prism:doi"),
            "abstract": item.get("dc:description")
        }
        abstracts.append(abstract_data)
    return abstracts

# Realizar la búsqueda y extraer abstracts
results = search_scopus(query)
if results:
    abstracts = extract_abstracts(results)
    df_abstracts = pd.DataFrame(abstracts)
    print(df_abstracts.head())  # Mostrar los primeros resultados

    # Guardar los resultados en un archivo CSV
    df_abstracts.to_csv("abstracts.csv", index=False)
else:
    print("No se encontraron resultados o hubo un error en la solicitud.")
