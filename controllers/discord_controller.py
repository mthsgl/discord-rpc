from models.discord_model import DiscordModel
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
        
        self.view.mute_button["command"] = self.toggle_mute
        self.view.deaf_button["command"] = self.toggle_deaf
        
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
            self._update_button_states(voice_settings)
            self._populate_guilds()
            
        except Exception as e:
            self.view.show_error(str(e))

    def _update_button_states(self, voice_settings):
        is_muted = voice_settings.get('mute', True) or voice_settings.get('deaf', True)
        is_deaf = voice_settings.get('deaf', True)
        
        self.view.update_mute_button(is_muted)
        self.view.update_deaf_button(is_deaf)

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
            self.view.create_members_menu(members.keys())
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
            print(volume)
            self.model.set_member_volume(self.model.current_member['user']['id'], volume)
        except Exception as e:
            self.view.show_error(str(e))

    def toggle_mute(self):
        try:
            current_state = self.view.mute_button["text"] == "Unmute"
            self.model.set_voice_settings(mute=not current_state)
            self.view.update_mute_button(not current_state)
            if not current_state and self.view.deaf_button["text"] == "Undeaf":
                self.view.update_deaf_button(False)
        except Exception as e:
            self.view.show_error(str(e))

    def toggle_deaf(self):
        try:
            current_state = self.view.deaf_button["text"] == "Undeaf"
            self.model.set_voice_settings(deaf=not current_state)
            self.view.update_deaf_button(not current_state)
            if not current_state and self.view.mute_button["text"] == "Unmute":
                self.view.update_mute_button(False)
        except Exception as e:
            self.view.show_error(str(e))

    def _on_closing(self):
        self.model.loop.stop()
        self.view.destroy()