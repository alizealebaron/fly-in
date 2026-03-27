# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : connexion.py                                                     #
# @author : alebaron <alebaron@student.42.fr>                                #
#                                                                            #
# @creation : 2026/02/27 13:52:25 by alebaron                                #
# @update   : 2026/03/27 13:57:21 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                                 Import                                  |
# +-------------------------------------------------------------------------+


from typing import Any
import arcade
from pydantic import BaseModel, Field
from src.models.node import Node
from src.models.drone import Drone


# +-------------------------------------------------------------------------+
# |                                  Class                                  |
# +-------------------------------------------------------------------------+

class Connexion(BaseModel):

    # +---------------------------------------------------------------------+
    # |                             Attribute                               |
    # +---------------------------------------------------------------------+

    node1: Node
    node2: Node
    max_link_capacity: int = Field(default=1, ge=1)
    lst_drones: list[Drone]

    # +---------------------------------------------------------------------+
    # |                              Getter                                 |
    # +---------------------------------------------------------------------+

    def get_lst_drones(self) -> list[Drone]:
        """
        Get the list of drones on this connexion.

        Returns:
            list[Drone]: The list of drones on this connexion.
        """

        return self.lst_drones

    # +---------------------------------------------------------------------+
    # |                              Methods                                |
    # +---------------------------------------------------------------------+

    def add_drone(self, drone: Drone) -> bool:
        """
        Add a drone to this connexion if there is enough capacity.

        Args:
            drone (Drone): The drone to add.

        Returns:
            bool: True if the drone was added, False otherwise.
        """

        if len(self.lst_drones) < self.max_link_capacity:
            self.lst_drones.append(drone)
            return True
        return False

    # +---------------------------------------------------------------------+
    # |                             Graphic                                 |
    # +---------------------------------------------------------------------+

    def draw(self, start_x: int, start_y: int, end_x: int, end_y: int,
             color: Any) -> None:
        """
        Draw the node on the screen using arcade at
        the given screen coordinates.

        Args:
            screen_x (float): The x coordinate on the screen.
            screen_y (float): The y coordinate on the screen.
        """

        arcade.draw_line(start_x, start_y, end_x, end_y, color, 2)
