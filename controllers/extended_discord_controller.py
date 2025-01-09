from models.discord_model import DiscordModel
from controllers.discord_controller import DiscordController
from views.extended_discord_view import ExtendedDiscordView
import json

class ExtendedDiscordController(DiscordController):
    def __init__(self, model: DiscordModel, view: ExtendedDiscordView):
        super().__init__(model, view)

        self.view.new_view_button["command"] = self.show_my_channel_view

    def show_my_channel_view(self):
        try:
            vc = self.model.get_selected_voice_channel()
            print("Voice channel : ", json.dumps(vc, indent=4))
            
            if (vc['data'] == None):
                self.view.show_not_in_channel()
                return
            '''
            sub = self.model.subscribe_channel(channel_id=vc['data']['id'])
            print(json.dumps(sub, indent=4))
            '''
            members = vc['data']['voice_states'] 
            user_data = {
                member['nick']: {
                    'nick': member['nick'],
                    'volume': member['volume'],
                    'user_id': member['user']['id'],
                    #'apply_volume': lambda volume, member_id=member['user']['id']: self.model.set_member_volume(member_id, volume),
                    'apply_volume': lambda member_id, volume: self.model.set_member_volume(member_id, volume),
                    'mute_lambda': lambda mute, member_id=member['user']['id']: self.model.set_member_mute(member_id,mute),
                    'mute': member['mute']
                } for member in members if member['user']['id'] != self.current_user_id
            }

            self.view.create_my_channel_controls(user_data)
            self.view.show_my_channel_view()
            
        except Exception as e:
            self.view.show_error(str(e))

    '''
    def apply_user_volume(self, user_id, volume):
        try:
            print(f"Applying volume for user {user_id} with volume {volume}")
            self.model.set_member_volume(user_id, volume)
        except Exception as e:
            self.view.show_error(str(e))
    '''