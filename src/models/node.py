# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : node.py                                                          #
# @author : alebaron <alebaron@student.42.fr>                                #
#                                                                            #
# @creation : 2026/02/26 14:36:30 by alebaron                                #
# @update   : 2026/03/26 11:18:57 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                                 Import                                  |
# +-------------------------------------------------------------------------+


from pydantic import BaseModel, Field
from src.models.drone import Drone
from src.utils.color import get_dict_color
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
    zone: Optional[str] = Field(default="normal", min_length=1)
    max_drones: Optional[int] = Field(default=1, ge=0)
    lst_drones: list[Drone]

    # +---------------------------------------------------------------------+
    # |                              Getter                                 |
    # +---------------------------------------------------------------------+

    def get_coord(self) -> tuple:
        return (self.x, self.y)

    def get_weight(self) -> float:
        if self.zone == "restricted":
            return 2
        if self.zone == "priority":
            return 0.5
        return 1

    def get_colored_name(self) -> str:
        dict_color = get_dict_color()

        if self.color is not None and self.color in dict_color:
            return f"{dict_color[self.color]}{self.name}{dict_color["reset"]}"
        else:
            return self.name

    # +---------------------------------------------------------------------+
    # |                            lst drones                               |
    # +---------------------------------------------------------------------+

    def add_drone(self, drone: Drone) -> bool:
        if len(self.lst_drones) < self.max_drones and self.zone != "blocked":
            self.lst_drones.append(drone)
            return True
        return False

    # +---------------------------------------------------------------------+
    # |                             Capacity                                |
    # +---------------------------------------------------------------------+

    def is_completed(self) -> bool:
        return (self.max_drones == len(self.lst_drones))

    # +---------------------------------------------------------------------+
    # |                             Hashable                                |
    # +---------------------------------------------------------------------+

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
