from models.discord_model import DiscordModel
from controllers.discord_controller import DiscordController
from views.extended_discord_view import ExtendedDiscordView
from utils import ui_to_client_vol, client_to_ui_vol
import json

class ExtendedDiscordController(DiscordController):
    def __init__(self, model: DiscordModel, view: ExtendedDiscordView):
        super().__init__(model, view)
        self.members_data = {}
        self.view.new_view_button["command"] = self.show_my_channel_view

    def show_my_channel_view(self):
        try:
            vc = self.model.get_selected_voice_channel()
            
            if (vc['data'] == None):
                self.view.show_not_in_channel()
                return

            members = vc['data']['voice_states'] 
            self.members_data = {
                member['nick']: {
                    'nick': member['nick'],
                    'volume': client_to_ui_vol(member['volume']),
                    'user_id': member['user']['id'],
                    'mute': member['mute']
                } for member in members if member['user']['id'] != self.current_user_id
            }

            self.view.create_my_channel_controls(self.members_data)
            self.view.show_my_channel_view()
            
        except Exception as e:
            self.view.show_error(str(e))

    def apply_user_volume(self, user_id, volume):
        try:
            # Convertir le volume de l'UI vers le format client
            client_volume = ui_to_client_vol(volume)
            
            # Appliquer le volume
            self.model.set_member_volume(user_id, client_volume)
            
            # Mettre à jour les données locales
            for member_data in self.members_data.values():
                if member_data['user_id'] == user_id:
                    member_data['volume'] = volume
                    break
                
        except Exception as e:
            self.view.show_error(str(e))
    
    def mute_user(self, user_id):
        try:
            # Trouver l'utilisateur dans les données
            for member_data in self.members_data.values():
                if member_data['user_id'] == user_id:
                    # Inverser l'état du mute
                    new_mute_state = not member_data['mute']
                    
                    # Appliquer le mute
                    self.model.set_member_mute(user_id, new_mute_state)
                    
                    # Mettre à jour les données locales
                    member_data['mute'] = new_mute_state
                    
                    # Recréer les contrôles pour mettre à jour l'interface
                    self.view.create_my_channel_controls(self.members_data)
                    break
            
        except Exception as e:
            self.view.show_error(str(e))