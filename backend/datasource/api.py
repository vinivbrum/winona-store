from datasource.user.credenciais import USER_EMAIL, ACESS_TOKEN, CLIENT_ID
import requests
from typing import List, Any, Dict, Union
import pandas as pd
from io import BytesIO 
import pyarrow.parquet as pq

class APICollector:
    def __init__(self,schema):
        self._schema = schema
        self._render = None
        self._buffer = None
        return
    
    def start(self, param):
        response = self.getData(param)
        response = self.extractData(response)
        response = self.transform_data(response)
        response = self.to_parquet(response)

        if self._buffer is not None:
            file_name = "Name"
            print(file_name)
            
        return (response)
    
    def getData(self,param):
        url = f'https://api.tiendanube.com/v1/{CLIENT_ID}/products?{param}'
        headers = {'Authentication': f'bearer {ACESS_TOKEN}',
                   'User-Agent': 'winona-api ({USER_EMAIL})'
                }
        try:
            response = requests.get(url, headers=headers).json()
            return response
        except requests.exceptions.HTTPError as err:
            print("Error making request", err)
            return None
        
    def extractData(self, response: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        extracted_data = []
        for product in response:
            product_data = self.extract_product_data(product)
            extracted_data.append(product_data)
        return extracted_data

    def extract_product_data(self, product: Dict[str, Any]) -> Dict[str, Any]:
        extracted_product_data = self.extract_with_schema(product, self._schema)
        extracted_product_data['variants'] = [self.extract_with_schema(variant, self._schema['variants']) for variant in product['variants']]
        return extracted_product_data

    def extract_with_schema(self, data: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
        extracted = {}
        for key, value_type in schema.items():
            if key in data:
                if isinstance(value_type, dict):
                    extracted[key] = self.extract_with_schema(data[key], value_type)
                else:
                    extracted[key] = data[key]
        return extracted

    
    
    def transform_data(self, extracted):
        result = pd.json_normalize(extracted)
        result = result.explode('variants').reset_index(drop=True)
        result_normalized = pd.json_normalize(result['variants'])
        print(result_normalized)
        result_normalized['values'] = result_normalized['values'].apply(lambda x: x[0]['pt'].split()[0] if isinstance(x, list) and len(x) > 0 else None)
        print(result_normalized)
        result = pd.concat([result.drop(columns=['variants']), result_normalized], axis=1)
        result['sku'] = result.apply(lambda row: row.name + 1000, axis=1)
        response = result
        return response
    
    def to_parquet(self, response):
        self._buffer = BytesIO()
        try:
            response.to_parquet(self._buffer)
        except:
            print('Error ao transformar em parquet')
            self._buffer = None