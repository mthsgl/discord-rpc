import requests
from config import REDIRECT_URI, API_ENDPOINT, CLIENT_ID, CLIENT_SECRET

'''https://discord.com/developers/docs/topics/oauth2#authorization-code-grant-access-token-exchange-example'''

def exchange_code(code):
    # Données à envoyer dans la requête POST
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Effectuer la requête POST pour obtenir le token
    response = requests.post(f'{API_ENDPOINT}/oauth2/token', data=data, headers=headers)
    
    if response.status_code != 200:
        print("Erreur lors de l'échange du code pour un token")
        response.raise_for_status()
    
    return response.json()

def exchange_refresh_token(refresh_token):
  # TODO : Ne fonctionne pas -> 400 Client Error: Bad Request for url: https://discord.com/api/v10/oauth2/token
  data = {
    'grant_type': 'refresh_token',
    'refresh_token': refresh_token
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers, auth=(CLIENT_ID, CLIENT_SECRET))

  if (r.status_code != 200):
     print("erreur de rafraichissement du token")
     r.raise_for_status()

  return r.json()