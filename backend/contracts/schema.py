from typing import Union, Dict, List
from datetime import datetime

GenericSchema = Dict[str, Union[int, str, bool, None]]

VariantSchema: GenericSchema = {
    'id': int,
    'sku': str,
    'price': str,
    'created_at': datetime,
    'updated_at': datetime,
}

CategorySchema: GenericSchema = {
    'id': int,
    'name': str,
    'description': str,
    'handle': str,
    'parent': Union[int, None],
    'subcategories': List[int],
    'seo_title': str,
    'seo_description': str,
    'google_shopping_category': str,
    'created_at': datetime,
    'updated_at': datetime,
}

ProdutoSchema: GenericSchema = {
    'id': int,
    'name': Dict[str, str],
    'variants': List[VariantSchema],
    'categories': List[CategorySchema],
}