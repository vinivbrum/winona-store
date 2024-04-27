from datasource.user.credenciais import USER_EMAIL, ACESS_TOKEN, CLIENT_ID
import requests

class APICollector:
    def __init__(self):
        self._schema = None
        self._render = None
        self._buffer = None
        return
    
    def start(self):
        pass
    
    def getData(self,param):
        url = f'https://api.tiendanube.com/v1/{CLIENT_ID}/products/sku/{param}'
        headers = {'Authentication': f'bearer {ACESS_TOKEN}',
                   'User-Agent': 'winona-api ({USER_EMAIL})'
                }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.HTTPError as err:
            print("Error making request", err)
            return None


   
    def extract_data(self):
        return
    
    def transform_data(self):
        return
    
    def load_data(self):
        return