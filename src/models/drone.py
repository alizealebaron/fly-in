# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : drone.py                                                         #
# @author : alebaron <alebaron@student.42.fr>                                #
#                                                                            #
# @creation : 2026/03/02 12:20:11 by alebaron                                #
# @update   : 2026/03/26 12:14:15 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                                 Import                                  |
# +-------------------------------------------------------------------------+


from pydantic import BaseModel, Field
from typing import Optional


# +-------------------------------------------------------------------------+
# |                                  Class                                  |
# +-------------------------------------------------------------------------+

class Drone(BaseModel):

    # +---------------------------------------------------------------------+
    # |                             Attribute                               |
    # +---------------------------------------------------------------------+

    name: str = Field(min_length=1)
    is_on_connection: bool = Field(default=False)
    waiting_connection_nodes: Optional[tuple[str, str]] = Field(default=None)
    next_restricted_node: Optional[str] = Field(default=None)

    # +---------------------------------------------------------------------+
    # |                             Hashable                                |
    # +---------------------------------------------------------------------+

    def __eq__(self, other: object) -> bool:
        """Override the default equality method to compare drones
        by their name."""

        if not isinstance(other, Drone):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        """Override the default hash method to make drones hashable"""
        return hash(self.name)
