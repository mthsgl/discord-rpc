# Application Discord RPC
Cette application permet d'effectuer des commandes simples : Mute/Unmute, Sourdine activé/désactivé, Changer le volume d'utilisateurs dans son channel vocal ou bien les mute.
## Prérequis
- Avoir installé python3
- Avoir l'application Discord
### 1. Créer une application sur le portail développeur de discord 
https://discord.com/developers/applications
- Créer une nouvelle application
- Renseigner un nom (peu importe)

### 2. Renseigner les informations de son application dans config.py
Dans le portail OAuth2 de votre application, copiez votre Client ID, Client Secret (reset si vous l'avez perdu) et renseignez une callback, par exemple : http://localhost:5000/callback 

Dans config.py :
CLIENT_ID = 'Votre client ID'
CLIENT_SECRET = 'Votre client secret'
REDIRECT_URI = 'Votre callback URL'

### 3. Renseigner ses informations redis 
Si vous ne souhaitez pas utiliser redis pour stocker votre token de connexion :
Changez les fonctions __init__ et _handle_authentication de discord_model.py par : 

```python
  def __init__(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.client = pypresence.Client(CLIENT_ID, loop=self.loop)
        
        self.current_guild = None
        self.current_channel = None
        self.current_member = None
        self.guilds_dict = {}
        self.channels_dict = {}
        self.members_dict = {}
```

```python
  def _handle_authentication(self):
        auth = self.client.authorize(str(CLIENT_ID), SCOPES)
        code_grant = auth['data']['code']
        token = exchange_code(code_grant)
        
        self.redis_client.setex('access_token', token['expires_in'], token['access_token'])
        self.redis_client.set('refresh_token', token['refresh_token'])
        
        return self.client.authenticate(token['access_token'])
```

A noter que sans redis, a chaque lancement de l'application, il faudra accepter les autorisations sur Discord

Sinon : 
Créer un compte redis, créer une base de données, en cliquant sur connecter, récupérez les informations necessaires et collez les dans config.py

## Lancement de l'application

- Récupérer le dossier :
  - Cloner le repos ou récupérer le fichier zip
- Ouvrir un terminal à la racine du projet et taper :
```cmd
pip install -r requirements.txt
```
