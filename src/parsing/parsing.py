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
# @update   : 2026/03/02 18:30:01 by alebaron                                #
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

    # === Initialisation of important variables ===

    flyinManager = None
    num_line = 1

    # === Reading lines one by one ===

    for line in lines:

        # == Pass the comments ==

        if line.startswith("#") or line == "":
            num_line += 1
            continue

        # == Rule 1 : First line must be the number of drones ==

        if (flyinManager is None):
            if (re.search("^nb_drones: [-0-9]+", line)):
                line_split = line.split(": ")
                nb_drone = int(line_split[1])
                if (nb_drone < 1):
                    exit_parsing_error("Number of drone must be greater "
                                       "than 0.",
                                       num_line)
                flyinManager = FlyinManager(nb_drone)
                num_line += 1
                continue
            else:
                exit_parsing_error("First line must be the number of "
                                   "drones (E.g : \"nb_drones: 5\")",
                                   num_line)

        # == Find new nodes to create ==

        line_split = line.split(" ")

        try:
            if ("hub" in line_split[0]):
                check_and_create_node(flyinManager, line_split)
            elif ("connection" in line_split[0]):
                print("2")
            else:
                exit_parsing_error("Undefined line structure.", num_line)
        except Exception as e:
            exit_parsing_error(str(e), num_line)

        # == Moving on the next line ==
        num_line += 1

    return flyinManager


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
# |                        Check & Create functions                         |
# +-------------------------------------------------------------------------+


def check_and_create_node(flyingManager: FlyinManager, line: list[str]) -> None:

    # === Checking for multiple start & end hub and incorrect hub ===

    if (line[0] == "start_hub:"):
        if (flyingManager.get_startHub() is not None):
            raise ParsingError("There must be exactly one start_hub zone.")
    elif (line[0] == "hub:"):
        pass
    elif (line[0] == "end_hub:"):
        if (flyingManager.get_endHub() is not None):
            raise ParsingError("There must be exactly one end_hub zone.")
    else:
        raise ParsingError("Undefined type of hub.")

    # === Checking node validity ===

    print(line)  # Debug

    if (len(line) != 5):
        raise ParsingError("Too many arguments for a zone "
                           "(Don't use space in zone name).")

    # == Verify that each zone have a unique name ==

    if (flyingManager.check_dupplicated_name(line[1]) is False):
        raise ParsingError("Each zone must have a unique name.")

    # == Check if there is a space or a dash in the name ==

    if (re.search("[ -]", line[1])):
        raise ParsingError("Zone names can use any valid characters "
                           "but dashes and spaces.")

    # == Initilisation of first validated data ==

    node_data = {
        "name": line[1],
        "x": line[2],
        "y": line[3],
        "lst_drones": []
    }

    # == Check if meta-data is valid ==


# +-------------------------------------------------------------------------+
# |                            Other functions                              |
# +-------------------------------------------------------------------------+


def exit_parsing_error(message: str, nb_ligne: int) -> None:
    exit_error(ParsingError(), message + f" [Line {nb_ligne}]")
