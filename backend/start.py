from datasource.api import APICollector
from contracts.schema import ProdutoSchema, GenericSchema

schema = ProdutoSchema
sku = 1001
minha_classe = APICollector().start(sku)
print (minha_classe)

