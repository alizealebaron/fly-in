# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : parsing.py                                                       #
# @author : alebaron <alebaron@student.42lehavre.fr>                         #
#                                                                            #
# @creation : 2026/03/02 12:26:40 by alebaron                                #
# @update   : 2026/03/02 14:30:13 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                                 Import                                  |
# +-------------------------------------------------------------------------+

from src.utils.error import exit_error, ParsingError
from src.obj.connexion import Connexion
from src.obj.flyinManager import FlyinManager
from src.obj.drone import Drone
from src.obj.node import Node
import re

# +-------------------------------------------------------------------------+
# |                             Main Function                               |
# +-------------------------------------------------------------------------+


def parsing_data(filename: str) -> FlyinManager:

    # === Checking if the file can be read ===

    check_file(filename)

    # === Start the reading of the file ===

    fly = get_data(filename)

    # === Return the data with a flyinManager ===

    return fly


# +-------------------------------------------------------------------------+
# |                          Important functions                            |
# +-------------------------------------------------------------------------+

def get_data(filename) -> FlyinManager:

    # === Get the contents of the file ===

    with open(filename, "r") as file:
        lines = file.read().splitlines()

    # === Reading lines one by one ===

    num_line = 1

    for line in lines:

        fly = None

        # == Pass the comments ==

        if line.startswith("#") or line == "":
            continue


        # == Rule 1 : First line must be the number of drones ==

        if (fly is None):
            if (re.search("^nb_drones: [0-9]+", line)):
                # TODO: Initialiser lfy
            else:
                exit_parsing_error("First line must be the number of "
                                   "drones (E.g : \"nb_drones: 5\"")

        # == Moving on the next line ==
        num_line += 1

    return fly


def check_file(filename: str) -> None:
    """
    Checks if the file exists and is accessible.

    Args:
        filename (str): The path to the file to check.

    Raises:
        ParsingError: If the file is missing, inaccessible,
        or is a directory.
    """
    try:
        open(filename, "r")
    except FileNotFoundError:
        exit_parsing_error(f"File \"{filename}\" not found. "
                           "Check the path and try again.")
    except PermissionError:
        exit_parsing_error(f"No permission to access {filename}."
                           " Check your access rights.")
    except IsADirectoryError:
        exit_parsing_error(f"Expected a file, but got directory "
                           f"{filename}. Please provide a file.")
    except Exception as e:
        exit_parsing_error(f"Unexcepted exception ({e}).")

# +-------------------------------------------------------------------------+
# |                            Other functions                              |
# +-------------------------------------------------------------------------+

def exit_parsing_error(message: str) -> None:
    exit_error(ParsingError(), message)
