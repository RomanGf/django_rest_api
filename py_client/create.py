import requests

headers = {'Authentication': 'Bearer 929c1c442d65159f122e9266a7412f528eab49a7'}

endpoint = 'http://127.0.0.1:8000/api/products/'

data = {
    'title': 'This field is done',
    'price': 32.99
}

get_response = requests.post(endpoint, json=data)

print(get_response.json())

