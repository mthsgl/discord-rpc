from views.discord_view import DiscordView
import tkinter as tk

class ExtendedDiscordView(DiscordView):
    def __init__(self):
        super().__init__()  

        self.new_view_button = tk.Button(self, text="Utilisateurs de mon channel", command=self.show_my_channel_view)
        self.new_view_button.grid(column=0, row=5, columnspan=2)

        self.main_frame = tk.Frame(self)
        self.my_channel_frame = tk.Frame(self)

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

        row = 0
        for user, data in user_data.items():
            nickname = tk.Label(self.my_channel_frame, text=user)
            nickname.grid(column=0, row=row)

            volume_slider = tk.Scale(self.my_channel_frame, from_=0, to=200, orient="horizontal")
            volume_slider.set(data['volume'])
            volume_slider.grid(column=1, row=row)

            apply_button = tk.Button(self.my_channel_frame, text="Apply", command=lambda u=data: self._apply_user_volume(u, volume_slider))
            apply_button.grid(column=2, row=row)

            mute_button = tk.Button(self.my_channel_frame, text="Mute", command=lambda u=data: self._mute_user(u))
            mute_button.grid(column=3, row=row)

            row += 1

        back_button = tk.Button(self.my_channel_frame, text="Back", command=self.show_main_view)
        back_button.grid(column=0, row=row, columnspan=3)

    def _apply_user_volume(self, user, slider):
        print("user to apply volume : ", user)
        volume = slider.get()
        user['apply_volume'](user['user_id'], volume)

    def _mute_user(self, user):
        user['mute_lambda'](mute= not user['mute'])
        user['mute'] = not user['mute']
    
    '''
    def create_my_channel_controls(self, user_data):
        # Clear previous controls
        for widget in self.my_channel_frame.winfo_children():
            widget.destroy()

        row = 0
        for user, data in user_data.items():
            nickname = tk.Label(self.my_channel_frame, text=user)
            nickname.grid(column=0, row=row)

            volume_slider = tk.Scale(self.my_channel_frame, from_=0, to=200, orient="horizontal")
            volume_slider.set(data['volume'])
            volume_slider.grid(column=1, row=row)

            # Corrected lambda to capture data['user_id'] and other values
            apply_button = tk.Button(
                self.my_channel_frame,
                text="Apply",
                command=lambda u_id=data['user_id'], slider=volume_slider: self._apply_user_volume(u_id, slider)
            )
            apply_button.grid(column=2, row=row)

            mute_button = tk.Button(
                self.my_channel_frame,
                text="Mute",
                command=lambda u_id=data['user_id'], is_muted=data['mute']: self._mute_user(u_id, is_muted)
            )
            mute_button.grid(column=3, row=row)

            row += 1

        back_button = tk.Button(self.my_channel_frame, text="Back", command=self.show_main_view)
        back_button.grid(column=0, row=row, columnspan=3)

    def _apply_user_volume(self, user_id, slider):
        volume = slider.get()
        # Informer le contrôleur de l'action
        self.controller.apply_user_volume(user_id, volume)


    def _mute_user(self, user_id, is_muted):
        print(f"Toggling mute for user {user_id}")
        self.model.set_member_mute(user_id, mute=not is_muted)
    '''