# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : node.py                                                          #
# @author : alebaron <alebaron@student.42lehavre.fr>                         #
#                                                                            #
# @creation : 2026/02/26 14:36:30 by alebaron                                #
# @update   : 2026/03/29 17:10:01 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                                 Import                                  |
# +-------------------------------------------------------------------------+


import arcade
from pydantic import BaseModel, Field
from src.models.drone import Drone
from src.utils.color import get_dict_color, get_arcade_defined_color
from typing import Optional


# +-------------------------------------------------------------------------+
# |                                  Class                                  |
# +-------------------------------------------------------------------------+

class Node(BaseModel):

    # +---------------------------------------------------------------------+
    # |                             Attribute                               |
    # +---------------------------------------------------------------------+

    name: str = Field(min_length=1)
    x: int
    y: int
    color: Optional[str] = Field(None, min_length=1)
    zone: str = Field(default="normal", min_length=1)
    max_drones: int = Field(default=1, ge=0)
    lst_drones: list[Drone]

    # +---------------------------------------------------------------------+
    # |                              Getter                                 |
    # +---------------------------------------------------------------------+

    def get_coord(self) -> tuple[int, int]:
        """Get the coordinates of the node."""
        return (self.x, self.y)

    def get_weight(self) -> float:
        """Get the weight of the node based on its zone type."""
        if self.zone == "restricted":
            return 2
        if self.zone == "priority":
            return 0.5
        return 1

    def get_colored_name(self) -> str:
        """Get the colored name of the node based on its color attribute."""
        dict_color = get_dict_color()

        if self.color is not None and self.color in dict_color:
            return f"{dict_color[self.color]}{self.name}{dict_color['reset']}"
        else:
            return self.name

    # +---------------------------------------------------------------------+
    # |                            lst drones                               |
    # +---------------------------------------------------------------------+

    def add_drone(self, drone: Drone) -> bool:
        """
        Add a drone to this node if there is enough capacity
        and the zone is not blocked.

        Args:
            drone (Drone): The drone to add.

        Returns:
            bool: True if the drone was added, False otherwise.
        """
        if len(self.lst_drones) < self.max_drones and self.zone != "blocked":
            self.lst_drones.append(drone)
            return True
        return False

    # +---------------------------------------------------------------------+
    # |                             Capacity                                |
    # +---------------------------------------------------------------------+

    def is_completed(self) -> bool:
        """Check if the node has reached its maximum drone capacity."""
        return (self.max_drones == len(self.lst_drones))

    # +---------------------------------------------------------------------+
    # |                             Hashable                                |
    # +---------------------------------------------------------------------+

    def __eq__(self, other: object) -> bool:
        """Override the default equality method to compare nodes
        by their name."""

        if not isinstance(other, Node):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        """Override the default hash method to make nodes hashable"""

        return hash(self.name)

    # +---------------------------------------------------------------------+
    # |                             Graphic                                 |
    # +---------------------------------------------------------------------+

    def draw(self, screen_x: float, screen_y: float) -> None:
        """
        Draw the node on the screen using arcade at
        the given screen coordinates.

        Args:
            screen_x (float): The x coordinate on the screen.
            screen_y (float): The y coordinate on the screen.
        """

        color = get_arcade_defined_color(self.color)

        if color is not None:
            arcade.draw_ellipse_filled(screen_x, screen_y, 30, 30, color)
        else:
            arcade.draw_ellipse_filled(screen_x, screen_y, 30, 30,
                                       arcade.color.AMARANTH_PINK)
