from models.discord_model import DiscordModel
from views.extended_discord_view import ExtendedDiscordView
from controllers.extended_discord_controller import ExtendedDiscordController

def main():
    model = DiscordModel()
    view = ExtendedDiscordView(None)
    controller = ExtendedDiscordController(model, view)
    view.controller = controller
    view.mainloop()

if __name__ == "__main__":
    main()