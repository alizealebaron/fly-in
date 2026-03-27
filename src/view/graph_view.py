# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : graph_view.py                                                    #
# @author : alebaron <alebaron@student.42.fr>                                #
#                                                                            #
# @creation : 2026/03/06 13:02:33 by alebaron                                #
# @update   : 2026/03/27 11:21:17 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


import arcade
from src.models.flyinManager import FlyinManager
from src.view.game_view import GameView
from src.view.graph_settings import WindowSettings


# +-------------------------------------------------------------------------+
# |                             Main Function                               |
# +-------------------------------------------------------------------------+

def show_graph(flyinManager: FlyinManager, filename: str) -> None:
    """
    Show the graph of the flyinManager.

    Args:
        flyinManager (FlyinManager): The flyinManager to show.
        filename (str): The name of the file to show in the title.
    """

    # === Initialisation of the game ===

    # Create a window class.
    window = arcade.Window(WindowSettings.WIDTH, WindowSettings.HEIGHT,
                           WindowSettings.TITLE)

    # Create and setup the GameView
    game = GameView(flyinManager)

    # Show GameView on screen
    window.show_view(game)


    # Start the arcade game loop
    arcade.run()
