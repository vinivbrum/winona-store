from typing import Union, Dict, List, Any
from datetime import datetime

GenericSchema = Dict[str, Union[int, str, bool, None]]

ProdutoSchema = {
    'id': int,
    'name': Dict[str, str],
    'handle': Dict[str, str],
    'variants': {
        'id': int,
        'value': str,
        'sku': str,
        'price': str
    }
}