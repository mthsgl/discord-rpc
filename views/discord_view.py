import tkinter as tk
from tkinter import Button, messagebox, OptionMenu, Scale, StringVar, DoubleVar, Frame

class DiscordView(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Discord Controller")
        self._init_ui()

    def _init_ui(self):
        # Frame principal
        self.main_controls = Frame(self)
        self.main_controls.grid(row=0, column=0, padx=10, pady=5)

        # Titre
        self.label = tk.Label(self.main_controls, text="Test App Discord", font=("Helvetica", 12, "bold"))
        self.label.grid(column=0, row=0, columnspan=2, pady=(0, 10))

        # Frame pour les contrôles audio
        self.audio_frame = Frame(self.main_controls)
        self.audio_frame.grid(row=1, column=0, columnspan=2, pady=5)

        # Boutons Mute et Deaf
        self.mute_button = Button(self.audio_frame, text="🔊 Unmuted", width=15)
        self.mute_button.grid(column=0, row=0, padx=5)

        self.deaf_button = Button(self.audio_frame, text="🎧 Undeafened", width=15)
        self.deaf_button.grid(column=1, row=0, padx=5)

        # Bouton mode audio
        self.audio_mode_button = Button(self.audio_frame, text="🎙️ Voice Activity", width=15)
        self.audio_mode_button.grid(column=0, row=1, columnspan=2, pady=5)

        # Frame pour les sliders
        self.volume_frame = Frame(self.main_controls)
        self.volume_frame.grid(row=2, column=0, columnspan=2, pady=10)

        # Volume Micro
        self.mic_label = tk.Label(self.volume_frame, text="🎤 Micro")
        self.mic_label.grid(column=0, row=0, padx=5)
        
        self.mic_volume = DoubleVar(value=100)
        self.discord_mic_vol = Scale(self.volume_frame, from_=0, to=100, orient="horizontal", 
                                   variable=self.mic_volume, length=150)
        self.discord_mic_vol.grid(column=1, row=0, padx=5)

        # Volume Casque
        self.headphone_label = tk.Label(self.volume_frame, text="🎧 Casque")
        self.headphone_label.grid(column=0, row=1, padx=5)
        
        self.volume_slider_value = DoubleVar(value=100)
        self.volume_slider = Scale(self.volume_frame, from_=0, to=200, orient="horizontal", 
                                 variable=self.volume_slider_value, length=150)
        self.volume_slider.grid(column=1, row=1, padx=5)

        # Frame pour les menus de sélection
        self.selection_frame = Frame(self.main_controls)
        self.selection_frame.grid(row=3, column=0, columnspan=2, pady=10)

        # Variables pour les menus
        self.selected_guild = StringVar(self, "Selectionner un serveur")
        self.selected_channel = StringVar(self, "Sélectionner un canal")
        self.selected_member = StringVar(self, "Selectionner un membre")

    def create_guilds_menu(self, guild_names):
        self.guilds_menu = OptionMenu(self.selection_frame, self.selected_guild, *guild_names)
        self.guilds_menu.config(width=20)
        self.guilds_menu.grid(column=0, row=0, pady=2)

    def create_channels_menu(self, channel_names):
        if hasattr(self, 'channels_menu'):
            self.channels_menu.destroy()
        self.channels_menu = OptionMenu(self.selection_frame, self.selected_channel, *channel_names)
        self.channels_menu.config(width=20)
        self.channels_menu.grid(column=0, row=1, pady=2)

    def create_members_menu(self, member_names):
        if hasattr(self, 'members_menu'):
            self.members_menu.destroy()
        self.members_menu = OptionMenu(self.selection_frame, self.selected_member, *member_names)
        self.members_menu.config(width=20)
        self.members_menu.grid(column=0, row=2, pady=2)

    def update_mute_button(self, is_muted):
        self.mute_button["text"] = "🔇 Muted" if is_muted else "🔊 Unmuted"

    def update_deaf_button(self, is_deaf):
        self.deaf_button["text"] = "🔇 Deafened" if is_deaf else "🎧 Undeafened"

    def update_audio_mode(self, is_push_to_talk=False):
        self.audio_mode_button["text"] = "🎙️ Push to Talk" if is_push_to_talk else "🎙️ Voice Activity"

    def show_error(self, message):
        messagebox.showerror("Error", str(message))