# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : game_view.py                                                     #
# @author : alebaron <alebaron@student.42.fr>                                #
#                                                                            #
# @creation : 2026/03/27 10:21:57 by alebaron                                #
# @update   : 2026/03/27 13:50:18 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


import arcade
from src.models.flyinManager import FlyinManager
from src.view.graph_settings import WindowSettings
from typing import Any

# +-------------------------------------------------------------------------+
# |                                  Class                                  |
# +-------------------------------------------------------------------------+

class GameView(arcade.View):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, fly: FlyinManager):
        super().__init__()

        self.background_color = arcade.color.WHITE
        self.lst_node = fly.get_listNode()
        self.lst_connexion = fly.get_listConnexion()
        self.max_x, self.max_y = fly.get_node_max_coord()
        self.min_x, self.min_y = fly.get_node_min_coord()

    def graph_to_screen(self, x: float, y: float) -> tuple[float, float]:
        """
        Convert graph coordinates to screen coordinates.
        Centers the graph in the window with padding.

        Args:
            x, y: Coordinates from the graph

        Returns:
            tuple: (screen_x, screen_y) in pixels
        """
        PADDING = 50  # Margin from window edges

        # Calculate drawable area
        drawable_width = WindowSettings.WIDTH - 2 * PADDING
        drawable_height = WindowSettings.HEIGHT - 2 * PADDING

        # Normalize coordinates to [0, 1]
        if self.max_x != self.min_x:
            norm_x = (x - self.min_x) / (self.max_x - self.min_x)
        else:
            norm_x = 0.5

        if self.max_y != self.min_y:
            norm_y = (y - self.min_y) / (self.max_y - self.min_y)
        else:
            norm_y = 0.5

        # Convert to screen pixels
        screen_x = norm_x * drawable_width + PADDING
        screen_y = norm_y * drawable_height + PADDING

        return (screen_x, screen_y)

    def reset(self):
        """Reset the game to the initial state."""
        # Do changes needed to restart the game here if you want to support that
        pass

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        for connexion in self.lst_connexion:
            start_x, start_y = self.graph_to_screen(connexion.node1.x, connexion.node1.y)
            end_x, end_y = self.graph_to_screen(connexion.node2.x, connexion.node2.y)
            arcade.draw_line(start_x, start_y, end_x, end_y, arcade.color.GRAY)

        for node in self.lst_node:
            screen_x, screen_y = self.graph_to_screen(node.x, node.y)
            node.draw(screen_x, screen_y)

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        pass

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass
