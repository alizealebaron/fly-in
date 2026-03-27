# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : color.py                                                         #
# @author : alebaron <alebaron@student.42.fr>                                #
#                                                                            #
# @creation : 0026/03/06 13:12:14 by lebaron                                 #
# @update   : 2026/03/27 11:56:33 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                                 Import                                  |
# +-------------------------------------------------------------------------+


import arcade
from typing import Any


# +-------------------------------------------------------------------------+
# |                                 Method                                  |
# +-------------------------------------------------------------------------+


def get_dict_color() -> dict[str, str]:
    """
    Get a dictionary of colors.

    Returns:
        dict[str, str]: A dictionary of colors.
    """

    return {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "light_gray": "\033[37m",
        "black": "\033[30m",
        "dark_gray": "\033[90m",
        "bright_red": "\033[91m",
        "bright_green": "\033[92m",
        "gold": "\033[93m",
        "sky_blue": "\033[94m",
        "pink": "\033[95m",
        "turquoise": "\033[96m",
        "white": "\033[97m",
        "orange": "\033[38;5;208m",
        "coral": "\033[38;5;203m",
        "lime": "\033[38;5;118m",
        "brown": "\033[38;5;130m",
        "reset": "\033[0m"
    }


def get_arcade_defined_color(value: str) -> Any | None:
    """
    Check if the color is defined in arcade.

    Args:
        value (str): The color to check.

    Returns:
        arcade.color | None: The color if defined, None otherwise.
    """

    if hasattr(arcade.color, value.upper()):
        return getattr(arcade.color, value.upper())
    else:
        return None
