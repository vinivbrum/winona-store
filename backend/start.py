from datasource.api import APICollector
from contracts.schema import ProdutoSchema, GenericSchema

schema = ProdutoSchema
sku = 'fields=id,name,handle,variants'
minha_classe = APICollector(schema).start(sku)
print (minha_classe)

