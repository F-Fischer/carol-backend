from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import requests
import pandas as pd

def get_products(predictions):
    url = "https://appfarmacitymicroservice-prod.azurewebsites.net/api/Medicine/search?filter="
    for word in predictions:
        url = url + word + "%20"

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    response = session.get(url)

    prices= []
    ids = []
    description = []
    labs = []
    formula = []

    for drug in response.json():
        prices.append(drug['publicPrice'])
        #ids.append(drug['id'])
        description.append(drug['description'])
        labs.append(drug['medicalLaboratory']['abbreviation'])
        formula.append(drug['formula']['description'])

    df = pd.DataFrame(list(zip(description, labs, prices, formula)), columns =['description', 'lab', 'prices', 'formula'])

    return df
