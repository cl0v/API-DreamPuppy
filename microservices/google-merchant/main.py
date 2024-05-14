from fastapi import FastAPI
from fastapi.responses import JSONResponse
import requests
from env import MERCHANT_ID
from auth import get_token

app = FastAPI(
    debug=False,
    docs_url=None,
    redoc_url=None,
)


@app.post("/upload")
def add_pet_to_merchant(pet: dict):
    offer_id = pet['uuid']
    title = 'Filhote de %s' % pet['breed']
    description = f"Filhote de {pet['breed']} vacinado e vermifugado. Consulte o app para mais informações" 

    product = {
        'id': offer_id,
        'offerId': offer_id,
        'title': title,
        'description': description,
        'link': 'https://www.dreampuppy.com.br/filhotes/%s' % pet['uuid'],
        'imageLink': pet['images'][0],
        "contentLanguage": "pt",
        "targetCountry": "BR",
        "channel": "online",
        "availability": "in stock",
        "condition": "new",
        "googleProductCategory": "Animals & Pet Supplies > Live Animals",
        "price": {
            "value": pet["price"],
            "currency": "BRL"
        },
        "shipping": [{
            "country": "BR",
            "service": "Standard shipping",
            "price": {
                "value": "100",
                "currency": "BRL"
            }
        }],
        "shippingWeight": {
            "value": "200",
            "unit": "grams"
        }
    }
    
    
    r = requests.post(f'https://shoppingcontent.googleapis.com/content/v2.1/{MERCHANT_ID}/products', headers={'Authorization': f'Bearer {get_token()}'}, json=product)
   
    return JSONResponse(status_code=r.status_code, content=r.json())


@app.put("/delete/{id}")
def delete_pet_from_merchant():
    productId= f'online:pt:BR:{id}'
   
    r = requests.post(f'https://shoppingcontent.googleapis.com/content/v2.1/{MERCHANT_ID}/products/{productId}', headers={'Authorization': f'Bearer {get_token()}'},)
    
    return JSONResponse(status_code=r.status_code, content=r.json())


@app.get("/list-pets")
def list_all_pets():
    r = requests.get(f'https://shoppingcontent.googleapis.com/content/v2.1/{MERCHANT_ID}/products')
    # Default url
    # https://shoppingcontent.googleapis.com/content/v2.1/{merchantId}/products
    return r.json()
    
    