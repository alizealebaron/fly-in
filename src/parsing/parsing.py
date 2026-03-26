# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : parsing.py                                                       #
# @author : alebaron <alebaron@student.42.fr>                                #
#                                                                            #
# @creation : 2026/03/02 12:26:40 by alebaron                                #
# @update   : 2026/03/26 12:12:31 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                                 Import                                  |
# +-------------------------------------------------------------------------+

from pydantic import ValidationError
from src.algorithm.dijkstra import calcule_path
from src.utils.error import exit_error, ParsingError
from src.models.connexion import Connexion
from src.models.flyinManager import FlyinManager
from src.models.node import Node
import re
from typing import Any, Optional

# +-------------------------------------------------------------------------+
# |                             Main Function                               |
# +-------------------------------------------------------------------------+


def parsing_data(filename: str) -> FlyinManager:
    """
    Parse the data from the file and return a flyinManager.

    Args:
        filename (str): The path to the file to parse.

    Returns:
        FlyinManager: The flyinManager containing the data from the file.
    """

    # === Checking if the file can be read ===

    check_file(filename)

    # === Start the reading of the file ===

    fly = get_data(filename)

    # === Check that there is a start and end hub ===

    if (fly.get_startHub() is None or fly.get_endHub() is None):
        exit_parsing_error("The start hub or end hub is missing.", 0)

    # === Get the hubs with type safety ===
    start_hub = fly.get_startHub()
    end_hub = fly.get_endHub()
    assert start_hub is not None, "Start hub must exist"
    assert end_hub is not None, "End hub must exist"

    # === Check that there is a path between the start and the end ===

    path = calcule_path(fly, start_hub, end_hub)

    if (start_hub not in path):
        exit_parsing_error("There is no path between the start and the "
                           "end.", 0)

    # === Put the drone on the start hub ===

    for drone in fly.get_listDrone():
        start_hub.add_drone(drone)

    # === Return the data with a flyinManager ===

    return fly


# +-------------------------------------------------------------------------+
# |                          Important functions                            |
# +-------------------------------------------------------------------------+

def get_data(filename: str) -> FlyinManager:
    """
    Get the data from the file and return a flyinManager.

    Args:
        filename (str): The path to the file to parse.

    Returns:
        FlyinManager: The flyinManager containing the data from the file.

    Raises:
        ParsingError: If there is an error in the parsing of the file.
    """

    # === Get the contents of the file ===

    with open(filename, "r") as file:
        lines = file.read().splitlines()

    # === Initialisation of important variables ===

    flyinManager: Optional[FlyinManager] = None
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

        if ("[" in line):
            meta_data = line.split("[")
            line_split = meta_data[0].split(" ")[:-1]
            meta_data = (meta_data[1][:-1]).split(" ")
        else:
            meta_data = []
            line_split = line.split(" ")

        # == Verify the number of arguments ==

        if (len(line_split) < 1):
            exit_parsing_error(f"Incorrect number of arguments "
                               f"({len(line_split)}).", num_line)

        if ((len(line_split) != 4 and "hub" in line_split[0]) or
           (len(line_split) != 2 and "connection" in line_split[0])):
            exit_parsing_error(f"Incorrect number of arguments "
                               f"({len(line_split)}).",
                               num_line)

        # == Try to create a node or a connexion ==

        try:
            assert flyinManager is not None, "FlyinManager not initialized"
            if ("hub" in line_split[0]):
                check_and_create_node(flyinManager, line_split, meta_data)
            elif ("connection" in line_split[0]):
                check_and_create_connexion(flyinManager, line_split, meta_data)
            else:
                exit_parsing_error("Undefined line structure.", num_line)
        except Exception as e:
            exit_parsing_error(str(e), num_line)

        # == Moving on the next line ==
        num_line += 1

    assert flyinManager is not None, "FlyinManager not initialized"
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
        with open(filename, "r") as file:
            lines = file.read().splitlines()
        if (len(lines) == 0):
            raise ParsingError("Empty files are not allowed.")
    except FileNotFoundError:
        exit_parsing_error(f"File \"{filename}\" not found. "
                           "Check the path and try again.", 0)
    except PermissionError:
        exit_parsing_error(f"No permission to access {filename}."
                           " Check your access rights.", 0)
    except IsADirectoryError:
        exit_parsing_error(f"Expected a file, but got directory "
                           f"{filename}. Please provide a file.", 0)
    except ParsingError as e:
        exit_parsing_error(str(e), 0)
    except Exception as e:
        exit_parsing_error(f"Unexcepted exception ({e}).", 0)


# +-------------------------------------------------------------------------+
# |                        Check & Create functions                         |
# +-------------------------------------------------------------------------+


def check_and_create_connexion(flyingManager: FlyinManager, line: list[str],
                               meta_data: list[str]) -> None:
    """
    Check the validity of the connexion and create it if it's valid.

    Args:
        flyingManager (FlyinManager): The flyinManager to add the connexion to.
        line (list[str]): The line containing the connexion data.
        meta_data (list[str]): The list of meta_data for the connexion.

    Raises:
        ParsingError: If the connexion is invalid.
    """

    lst_node = line[1].split("-")

    # === Verifying the validity of the connection ===

    # == A connexion must connect two zone ==

    if (len(lst_node) != 2):
        raise ParsingError("A connexion must connect two zone.")

    # == Both zones must already exist. ==

    for node in lst_node:
        if (flyingManager.get_node_by_name(node) is None):
            raise ParsingError(f"Zone {node} does not exist and "
                               f"cannot be connected.")

    # == Recovery of both nodes ==

    node1 = flyingManager.get_node_by_name(lst_node[0])
    node2 = flyingManager.get_node_by_name(lst_node[1])

    assert node1 is not None, f"Zone {lst_node[0]} should exist"
    assert node2 is not None, f"Zone {lst_node[1]} should exist"

    connexion_data: dict[str, Any] = {
        "node1": node1,
        "node2": node2,
        "lst_drones": []
    }

    # == Checking meta_data ==

    for data in meta_data:
        match = re.search("^[A-Za-z_]+=[0-9A-Za-z_]+$", data)
        if (match):
            data_split = data.split("=")
            if (data.startswith("max_link_capacity")):
                connexion_data["max_link_capacity"] = int(data_split[1])
            else:
                raise ParsingError(f"Invalid meta_data name ({data}).")
        else:
            raise ParsingError(f"Invalid meta_data format ({data}).")

    # == Initialisation of the connexion ==

    try:
        new_connexion = Connexion(**connexion_data)
    except ValidationError as e:
        for error in e.errors():
            raise ParsingError(f"{error['msg']} ({error['loc']}="
                               f"{error['input']})")

    # == Checking whether the connection already exists ==

    if (flyingManager.check_dupplicated_connexion(new_connexion)):
        raise ParsingError(f"Connexion {new_connexion.node1.name}-"
                           f"{new_connexion.node2.name} already exist.")

    flyingManager.add_connexion(new_connexion)


def check_and_create_node(flyingManager: FlyinManager, line: list[str],
                          meta_data: list[str]) -> None:
    """
    Check the validity of the node and create it if it's valid.

    Args:
        flyingManager (FlyinManager): The flyinManager to add the node to.
        line (list[str]): The line containing the node data.
        meta_data (list[str]): The list of meta_data for the node.

    Raises:
        ParsingError: If the node is invalid.
    """

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

    # == Checking space in node name ==

    if (len(line) != 4):
        raise ParsingError("Too many arguments for a zone "
                           "(Don't use space in zone name).")

    # == Verify that each zone have a unique name ==

    if (flyingManager.check_dupplicated_name(line[1])):
        raise ParsingError("Each zone must have a unique name.")

    # == Check if there is a space or a dash in the name ==

    if (re.search("[ -]", line[1])):
        raise ParsingError("Zone names can use any valid characters "
                           "but dashes and spaces.")

    # == Initilisation of first validated data ==

    node_data: dict[str, Any] = {
        "name": line[1],
        "x": int(line[2]),
        "y": int(line[3]),
        "lst_drones": []
    }

    # == Check if meta-data is valid ==

    valid_zone = ["normal", "blocked", "restricted", "priority"]

    for data in meta_data:
        match = re.search("^[A-Za-z_]+=[0-9A-Za-z_]+$", data)
        if (match):
            data_split = data.split("=")
            if (data.startswith("color")):
                node_data["color"] = data_split[1]
            elif (data.startswith("zone")):
                if (data_split[1] in valid_zone):
                    node_data["zone"] = data_split[1]
                else:
                    raise ParsingError(f"Invalid type of zone ({data}).")
            elif (data.startswith("max_drones")):
                node_data["max_drones"] = int(data_split[1])
            else:
                raise ParsingError(f"Invalid meta_data name ({data}).")
        else:
            raise ParsingError(f"Invalid meta_data format ({data}).")

    if (line[0] == "start_hub:" or line[0] == "end_hub:"):
        node_data["max_drones"] = flyingManager.get_nbDrones()

    try:
        new_node = Node(**node_data)
    except ValidationError as e:
        for error in e.errors():
            raise ParsingError(f"{error['msg']} ({error['loc']}="
                               f"{error['input']})")

    flyingManager.add_node(new_node)

    if (line[0] == "start_hub:"):
        flyingManager.set_startHub(new_node)
    elif (line[0] == "end_hub:"):
        flyingManager.set_endHub(new_node)


# +-------------------------------------------------------------------------+
# |                            Other functions                              |
# +-------------------------------------------------------------------------+


def exit_parsing_error(message: str, nb_ligne: int) -> None:
    """
    Exit the program with a parsing error message.

    Args:
        message (str): The error message to display.
        nb_ligne (int): The line number where the error occurred.
    """

    exit_error(ParsingError(), message + f" [Line {nb_ligne}]")
