import asyncio
import pypresence
from pypresence import DiscordNotFound
import redis
import json
from controllers.discord_bridge import exchange_code, exchange_refresh_token
from config import CLIENT_ID, SCOPES, REDIS_PORT, REDIS_HOST, REDIS_USERNAME, REDIS_PASSWORD

class DiscordModel:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.client = pypresence.Client(CLIENT_ID, loop=self.loop)
        
        # Init Redis
        self.redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            decode_responses=True,
            username=REDIS_USERNAME,
            password=REDIS_PASSWORD,
        )
        
        self.current_guild = None
        self.current_channel = None
        self.current_member = None
        self.guilds_dict = {}
        self.channels_dict = {}
        self.members_dict = {}

    def start_client(self):
        try:
            self.client.start()
            return self._handle_authentication()
        except DiscordNotFound as e:
            raise e

    def _handle_authentication(self):
        access_token = self.redis_client.get('access_token')
        refresh_token = self.redis_client.get('refresh_token')
    
        if access_token:
            return self.client.authenticate(access_token)
        else:
            auth = self.client.authorize(str(CLIENT_ID), SCOPES)
            code_grant = auth['data']['code']
            token = exchange_code(code_grant)
            
            self.redis_client.setex('access_token', token['expires_in'], token['access_token'])
            self.redis_client.set('refresh_token', token['refresh_token'])
            
            return self.client.authenticate(token['access_token'])
        # TODO : pour le moment le rafraichissement de token ne fonctionne pas
        '''
        elif refresh_token:
            print("refreshing token..")
            token = exchange_refresh_token(refresh_token)
            return self.client.authenticate(token['access_token'])
        '''
        

    def get_voice_settings(self):
        return self.client.get_voice_settings()

    def set_voice_settings(self, mute=None, deaf=None):
        return self.client.set_voice_settings(mute=mute, deaf=deaf)

    def get_guilds(self):
        response = self.client.get_guilds()
        self.guilds_dict = {guild['name']: guild for guild in response['data']['guilds']}
        return self.guilds_dict

    def get_channels(self, guild_id):
        response = self.client.get_channels(guild_id)
        channels = [channel for channel in response['data']['channels'] if channel['type'] == 2]
        self.channels_dict = {channel['name']: channel for channel in channels}
        return self.channels_dict

    def get_channel_members(self, channel_id):
        response = self.client.get_channel(channel_id)
        members = response['data']['voice_states']
        self.members_dict = {member['nick']: member for member in members}
        return self.members_dict

    def set_member_volume(self, member_id, volume):
        return self.client.set_user_voice_settings(member_id, volume=volume)
    
    def set_member_mute(self, member_id, mute: bool):
        print("mute :", mute, "member :", member_id)
        return self.client.set_user_voice_settings(member_id, mute=mute)
    
    def get_selected_voice_channel(self):
        return self.client.get_selected_voice_channel()
    
    def subscribe_channel(self, channel_id):
        return self.client.subscribe("VOICE_STATE_CREATE", {"channel_id": channel_id})