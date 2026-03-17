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
# @update   : 2026/03/17 13:41:35 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                                 Import                                  |
# +-------------------------------------------------------------------------+


from pydantic import BaseModel, Field, ValidationError
from src.models.drone import Drone
from typing import Optional
from typing_extensions import Self
import re


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

    # +---------------------------------------------------------------------+
    # |                            lst drones                               |
    # +---------------------------------------------------------------------+

    def add_drone(self, drone: Drone) -> bool:
        if len(self.lst_drones) < self.max_drones and self.zone != "blocked":
            self.lst_drones.append(drone)
            return True
        return False
