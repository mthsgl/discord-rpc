from models.discord_model import DiscordModel
from utils import client_to_ui_vol
from views.discord_view import DiscordView
import threading
import nest_asyncio
import json

class DiscordController:
    def __init__(self, model: DiscordModel, view: DiscordView):
        self.model = model
        self.view = view

        self.current_user_id = None
        # Corrige l'erreur RuntimeError('This event loop is already running')
        nest_asyncio.apply()
        
        self._bind_events()
        self._start_discord_thread()

    def _bind_events(self):
        self.view.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Contrôles audio
        self.view.mute_button["command"] = self.toggle_mute
        self.view.deaf_button["command"] = self.toggle_deaf
        self.view.audio_mode_button["command"] = self.toggle_audio_mode
        
        # Binding des sliders
        self.view.discord_mic_vol.config(command=lambda _: self.update_mic_volume())
        self.view.volume_slider.config(command=lambda _: self.update_output_volume())
        
        # Menus de sélection
        self.view.selected_guild.trace_add('write', self._on_guild_selected)
        self.view.selected_channel.trace_add('write', self._on_channel_selected)
        self.view.selected_member.trace_add('write', self._on_member_selected)

    def _start_discord_thread(self):
        self.discord_thread = threading.Thread(target=self._init_discord)
        self.discord_thread.start()

    def _init_discord(self):
        try:
            auth = self.model.start_client()
            self.current_user_id = auth['data']['user']['id']
            voice_settings = self.model.get_voice_settings()
            # print(json.dumps(voice_settings, indent=4))
            self._update_audio_states(voice_settings)
            self._populate_guilds()
            sb = self.model.get_soundboard_sounds()
            print(json.dumps(sb, indent=4))
            
        except Exception as e:
            self.view.show_error(str(e))

    def _update_audio_states(self, voice_settings):
        is_deaf = voice_settings['data']["deaf"] is True
        is_muted = (voice_settings['data']["mute"] is True) or is_deaf
        
        self.view.update_mute_button(is_muted)
        self.view.update_deaf_button(is_deaf)
        
        # Mise à jour des volumes sans appliquer les changements
        input_volume = voice_settings['data']['input']['volume']
        output_volume = voice_settings['data']['output']['volume']
        
        self.view.mic_volume.set(client_to_ui_vol(input_volume))
        self.view.volume_slider_value.set(client_to_ui_vol(output_volume))
        
        # Mise à jour du mode audio
        is_ptt = voice_settings['data']['mode']['type'] == 'PUSH_TO_TALK'
        self.view.update_audio_mode(is_ptt)

    def toggle_mute(self):
        try:
            current_state = "Muted" in self.view.mute_button["text"]
            self.model.set_voice_settings(mute=not current_state)
            self.view.update_mute_button(not current_state)
            
            # Si on démute et qu'on était en sourdine, on désactive aussi la sourdine
            if not current_state and "Deafened" in self.view.deaf_button["text"]:
                self.model.set_voice_settings(deaf=False)
                self.view.update_deaf_button(False)
                
        except Exception as e:
            self.view.show_error(str(e))

    def toggle_deaf(self):
        try:
            current_state = "Deafened" in self.view.deaf_button["text"]
            self.model.set_voice_settings(deaf=not current_state)
            self.view.update_deaf_button(not current_state)
            
            # La sourdine active aussi le mute
            self.view.update_mute_button(not current_state)
                
        except Exception as e:
            self.view.show_error(str(e))

    def toggle_audio_mode(self):
        try:
            current_text = self.view.audio_mode_button["text"]
            
            if "Push to Talk" in current_text:
                self.model.set_voice_activity()
                self.view.update_audio_mode(False)
            else:
                self.model.set_push_to_talk()
                self.view.update_audio_mode(True)
                
        except Exception as e:
            self.view.show_error(str(e))

    def update_mic_volume(self):
        try:
            volume = self.view.mic_volume.get()
            self.model.set_mic_volume(volume)
        except Exception as e:
            self.view.show_error(str(e))

    def update_output_volume(self):
        try:
            volume = self.view.volume_slider_value.get()
            self.model.set_headphone_volume(volume)
        except Exception as e:
            self.view.show_error(str(e))

    def _populate_guilds(self):
        try:
            guilds = self.model.get_guilds()
            self.view.create_guilds_menu(guilds.keys())
        except Exception as e:
            self.view.show_error(str(e))

    def _on_guild_selected(self, *args):
        guild_name = self.view.selected_guild.get()
        selected_guild = self.model.guilds_dict.get(guild_name)
        if selected_guild:
            self.model.current_guild = selected_guild
            self._populate_channels(selected_guild['id'])

    def _populate_channels(self, guild_id):
        try:
            channels = self.model.get_channels(guild_id)
            print(json.dumps(channels, indent=4))
            self.view.create_channels_menu(channels.keys())
        except Exception as e:
            self.view.show_error(str(e))

    def _on_channel_selected(self, *args):
        channel_name = self.view.selected_channel.get()
        selected_channel = self.model.channels_dict.get(channel_name)
        if selected_channel:
            self.model.current_channel = selected_channel
            self._populate_members(selected_channel['id'])

    def _populate_members(self, channel_id):
        try:
            members = self.model.get_channel_members(channel_id)
            my_channel = self.model.get_selected_voice_channel()
            if ((my_channel['data'] is None) or (my_channel['data']['id'] != channel_id)):
                self.view.create_btn_join()
                self.view.join_btn.config(command=lambda: self._join_channel(channel_id))
            elif (my_channel['data']['id'] == channel_id):
                #self.view.create_members_menu(members.keys())
                self.view.create_btn_leave()
                self.view.leave_btn.config(command=lambda: self._leave_channel())
        except Exception as e:
            self.view.show_error(str(e))
    
    def _join_channel(self, channel_id):
        try:
            self.model.select_voice_channel(channel_id)
            self.view.create_btn_leave()
        except Exception as e:
            self.view.show_error(str(e))
    
    def _leave_channel(self):
        try:
            self.model.leave_voice_channel()
            self.view.create_btn_join()
        except Exception as e:
            self.view.show_error(str(e))

    def _on_member_selected(self, *args):
        member_name = self.view.selected_member.get()
        selected_member = self.model.members_dict.get(member_name)
        if selected_member:
            self.model.current_member = selected_member
            self._create_volume_controls(selected_member['volume'])

    def _create_volume_controls(self, volume):
        self.view.create_volume_slider(volume)
        self.view.volume_apply_button["command"] = self._apply_volume

    def _apply_volume(self):
        try:
            volume = self.view.volume_slider.get()
            self.model.set_member_volume(self.model.current_member['user']['id'], volume)
        except Exception as e:
            self.view.show_error(str(e))

    def _on_closing(self):
        self.model.loop.stop()
        self.view.destroy()