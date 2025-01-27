from views.discord_view import DiscordView
import tkinter as tk
from tkinter import Scale, Frame, Button, Label

class ExtendedDiscordView(DiscordView):
    def __init__(self, controller):
        super().__init__()  
        self.controller = controller
        self.user_volume_sliders = {}  # Pour stocker les références aux sliders

        self.new_view_button = tk.Button(self, text="Utilisateurs de mon channel", command=self.show_my_channel_view)
        self.new_view_button.grid(column=0, row=5, columnspan=2)

        self.main_frame = Frame(self)
        self.my_channel_frame = Frame(self)

        self.main_frame.grid(row=6, column=0, columnspan=3)
        self.my_channel_frame.grid(row=6, column=0, columnspan=3)
        self.my_channel_frame.grid_remove()

    def show_main_view(self):
        self.my_channel_frame.grid_remove()
        self.main_frame.grid()

    def show_my_channel_view(self):
        self.main_frame.grid_remove()
        self.my_channel_frame.grid()
        self.new_view_button['text'] = "Utilisateurs de mon channel"

    def show_not_in_channel(self):
        self.new_view_button['text'] = "!! Vous n'êtes pas dans un channel !!"
   
    def create_my_channel_controls(self, user_data):
        # Clear previous controls
        for widget in self.my_channel_frame.winfo_children():
            widget.destroy()
        self.user_volume_sliders.clear()

        # Frame pour les en-têtes
        header_frame = Frame(self.my_channel_frame)
        header_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=(0, 5))
        header_frame.grid_columnconfigure(1, weight=1)

        Label(header_frame, text="Utilisateur", width=15, anchor='w').grid(row=0, column=0)
        Label(header_frame, text="Volume", width=20, anchor='w').grid(row=0, column=1)
        Label(header_frame, text="Mute", width=10).grid(row=0, column=2)

        row = 1
        for user, data in user_data.items():
            # Frame pour chaque utilisateur
            user_frame = Frame(self.my_channel_frame)
            user_frame.grid(row=row, column=0, sticky='ew', padx=5, pady=2)
            user_frame.grid_columnconfigure(1, weight=1)

            # Nom d'utilisateur
            nickname = Label(user_frame, text=user, width=15, anchor='w')
            nickname.grid(column=0, row=0)

            # Slider de volume
            volume_slider = Scale(user_frame, from_=0, to=200, orient="horizontal", length=150)
            volume_slider.set(data['volume'])
            volume_slider.grid(column=1, row=0, padx=5, sticky='ew')
            
            # Stocker la référence au slider
            self.user_volume_sliders[data['user_id']] = volume_slider

            # Configurer le callback du slider
            volume_slider.config(command=lambda value, u_id=data['user_id']: 
                               self.controller.apply_user_volume(u_id, float(value)))

            # Bouton Mute
            mute_button = Button(
                user_frame,
                text="🔇 Muted" if data['mute'] else "🔊 Unmuted",
                width=10,
                command=lambda u_id=data['user_id']: self._mute_user(u_id)
            )
            mute_button.grid(column=2, row=0)

            row += 1

        # Bouton retour
        back_button = Button(self.my_channel_frame, text="← Back", command=self.show_main_view)
        back_button.grid(column=0, row=row, columnspan=3, pady=10)

    def update_user_volume(self, user_id, volume):
        """Met à jour le slider de volume pour un utilisateur spécifique"""
        if user_id in self.user_volume_sliders:
            self.user_volume_sliders[user_id].set(volume)

    def _mute_user(self, user_id):
        self.controller.mute_user(user_id)