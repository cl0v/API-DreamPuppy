from fastapi import FastAPI
import requests
from env import MERCHANT_ID

app = FastAPI(
    debug=False,
    docs_url=None,
    redoc_url=None,
)


@app.post("/upload")
def add_pet_to_merchant(pet: dict):
    offer_id = 'pet#%s' % pet['uuid']
    title = 'Filhote de %s' % pet['breed']
    description = f"Filhote de {pet['breed']} vacinado e vermifugado. Consulte o app para mais informações" 

    product = {
        'offerId': offer_id,
        'title': title,
        'description': description,
        'link': 'https://www.dreampuppy.com.br/filhotes/%s' % pet['uuid'],
        'imageLink': pet['images'][0],
        'contentLanguage': 'pt',
        'targetCountry': 'BR',
        'channel': 'online',
        'availability': 'in stock',
        'condition': 'new',
        'googleProductCategory': # TODO: Adicionar Live Animals.
            'Media > Books',
        'price': {
            'value': pet['price'],
            'currency': 'BRL'
        },
        'shipping': [{
            'country': 'BR',
            'service': 'Standard shipping',
            'price': {
                'value': '100',
                'currency': 'BRL'
            }
        }],
        'shippingWeight': {
            'value': '200',
            'unit': 'grams'
        }
    }
    print(product)
    pass


@app.put("/delete/{id}")
def delete_pet_from_merchant():
    print('Deletar sai no log?')
    pass


@app.get("/list-pets")
def list_all_pets():
    r = requests.get(f'https://shoppingcontent.googleapis.com/content/v2.1/{MERCHANT_ID}/products')
    # Default url
    # https://shoppingcontent.googleapis.com/content/v2.1/{merchantId}/products
    return r.json()
    
    