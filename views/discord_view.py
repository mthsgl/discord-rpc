import tkinter as tk
from tkinter import Button, messagebox, OptionMenu, Scale, StringVar, DoubleVar

class DiscordView(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Discord Controller")
        self._init_ui()

    def _init_ui(self):
        # Main label
        self.label = tk.Label(self, text="Discord Control Panel")
        self.label.grid(column=0, row=0, columnspan=2)

        # Mute and Deaf buttons
        self.mute_button = Button(self, text="Mute")
        self.mute_button.grid(column=0, row=1)

        self.deaf_button = Button(self, text="Deaf")
        self.deaf_button.grid(column=1, row=1)

        # Dropdown menus (will be populated later)
        self.selected_guild = StringVar(self, "Selectionner un serveur")
        self.selected_channel = StringVar(self, "Sélectionner un canal")
        self.selected_member = StringVar(self, "Selectionner un membre")
        
        # Volume slider
        self.volume_slider_value = DoubleVar()
        self.volume_slider = None
        self.volume_apply_button = None

    def create_guilds_menu(self, guild_names):
        self.guilds_menu = OptionMenu(self, self.selected_guild, *guild_names)
        self.guilds_menu.grid(column=0, row=2, columnspan=2)

    def create_channels_menu(self, channel_names):
        if hasattr(self, 'channels_menu'):
            self.channels_menu.destroy()
        self.channels_menu = OptionMenu(self, self.selected_channel, *channel_names)
        self.channels_menu.grid(column=0, row=3, columnspan=2)

    def create_members_menu(self, member_names):
        if hasattr(self, 'members_menu'):
            self.members_menu.destroy()
        self.members_menu = OptionMenu(self, self.selected_member, *member_names)
        self.members_menu.grid(column=0, row=4, columnspan=2)

    def create_volume_slider(self, initial_volume):
        self.volume_slider_value.set(initial_volume)
        self.volume_slider = Scale(self, from_=0, to=200, orient="vertical", 
                                 variable=self.volume_slider_value)
        self.volume_slider.grid(column=2, row=0, rowspan=4)

        self.volume_apply_button = Button(self, text="Apply")
        self.volume_apply_button.grid(column=2, row=4)

    def update_mute_button(self, is_muted):
        self.mute_button["text"] = "Unmute" if is_muted else "Mute" 

    def update_deaf_button(self, is_deaf):
        self.deaf_button["text"] = "Undeaf" if is_deaf else "Deaf"

    def show_error(self, message):
        messagebox.showerror("Error", str(message))