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
# @update   : 2026/04/01 11:52:36 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


import arcade
from src.models.flyinManager import FlyinManager
from src.models.node import Node
from src.models.connexion import Connexion
from src.view.graph_settings import WindowSettings


# +-------------------------------------------------------------------------+
# |                                  Class                                  |
# +-------------------------------------------------------------------------+

class GameView(arcade.View):
    """
    Class representing the game view, which is responsible for rendering
    the graph.

    Attributes:
        fly (FlyinManager): The FlyinManager instance containing the
            graph data.

    Methods:
        __init__(self, fly: FlyinManager): Initializes the GameView
            with the given FlyinManager instance.
        graph_to_screen(self, x: float, y: float) -> tuple[float, float]:
            Converts graph coordinates to screen coordinates, centering
            the graph in the window with padding.
        on_draw(self): Renders the graph on the screen.
    """

    lst_node: list[Node]
    lst_connexion: list[Connexion]
    max_x: float
    max_y: float
    min_x: float
    min_y: float

    def __init__(self, fly: FlyinManager):
        super().__init__()

        self.background_color = arcade.color.WHITE
        self.lst_node = fly.get_listNode() or []
        self.lst_connexion = fly.get_listConnexion() or []
        max_coord = fly.get_node_max_coord()
        min_coord = fly.get_node_min_coord()
        self.max_x, self.max_y = max_coord if max_coord is not None else (0, 0)
        self.min_x, self.min_y = min_coord if min_coord is not None else (0, 0)

    def graph_to_screen(self, x: float, y: float) -> tuple[float, float]:
        """
        Convert graph coordinates to screen coordinates.
        Centers the graph in the window with padding.

        Args:
            x, y: Coordinates from the graph

        Returns:
            tuple: (screen_x, screen_y) in pixels
        """
        PADDING = 50

        # Calculate drawable area
        drawable_width = WindowSettings.WIDTH - 2 * PADDING
        drawable_height = WindowSettings.HEIGHT - 2 * PADDING

        # Calculate coordinates
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

    def on_draw(self) -> None:
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color
        # and erase what we drew last frame.
        self.clear()

        for connexion in self.lst_connexion:
            start_x, start_y = self.graph_to_screen(connexion.node1.x,
                                                    connexion.node1.y)
            end_x, end_y = self.graph_to_screen(connexion.node2.x,
                                                connexion.node2.y)
            arcade.draw_line(start_x, start_y, end_x, end_y, arcade.color.GRAY)

        for node in self.lst_node:
            screen_x, screen_y = self.graph_to_screen(node.x, node.y)
            node.draw(screen_x, screen_y)
