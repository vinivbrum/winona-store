from datasource.user.credenciais import USER_EMAIL, ACESS_TOKEN, CLIENT_ID
from contracts.schema import ProdutoSchema, VariantSchema, CategorySchema
import requests
import json
import pydantic
from typing import List, Any, Dict, Union
from datetime import datetime

class APICollector:
    def __init__(self):
        self._schema = None
        self._render = None
        self._buffer = None
        return
    
    def start(self, param):
        response = self.getData(param)
        resp = self.extractData(response)
        return (resp)
    
    def getData(self,param):
        url = f'https://api.tiendanube.com/v1/{CLIENT_ID}/products/sku/{param}'
        headers = {'Authentication': f'bearer {ACESS_TOKEN}',
                   'User-Agent': 'winona-api ({USER_EMAIL})'
                }
        try:
            response = requests.get(url, headers=headers).json()
            return response
        except requests.exceptions.HTTPError as err:
            print("Error making request", err)
            return None
    @staticmethod
    def extractData(response: Dict[str, Any]) -> Dict[str, Any]:
        extracted_data: Dict[str, Any] = {}
        # Função para extrair dados de acordo com o schema
        def extract_with_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
            extracted: Dict[str, Any] = {}
            for key, value_type in schema.items():
                if key in data:
                    if isinstance(value_type, dict):
                        extracted[key] = extract_with_schema(data[key], value_type)
                    elif value_type == datetime:
                        extracted[key] = datetime.strptime(data[key], "%Y-%m-%dT%H:%M:%S%z")
                    else:
                        extracted[key] = data[key]
            return extracted

        # Extrair informações usando o schema do produto
        extracted_data = extract_with_schema(response, ProdutoSchema)

        # Extrair variantes
        extracted_data['variants'] = [extract_with_schema(variant_data, VariantSchema) for variant_data in response['variants']]

        # Extrair categorias
        extracted_data['categories'] = [extract_with_schema(category_data, CategorySchema) for category_data in response['categories']]

        return extracted_data
    
    
    def transform_data(self):
        return
    
    def load_data(self):
        return