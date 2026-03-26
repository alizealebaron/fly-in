# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : flyinManager.py                                                  #
# @author : alebaron <alebaron@student.42.fr>                                #
#                                                                            #
# @creation : 2026/02/27 13:53:46 by alebaron                                #
# @update   : 2026/03/26 12:21:26 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                                 Import                                  |
# +-------------------------------------------------------------------------+


from src.models.node import Node
from src.models.drone import Drone
from src.models.connexion import Connexion
import random
from typing import Optional


# +-------------------------------------------------------------------------+
# |                                  Class                                  |
# +-------------------------------------------------------------------------+

class FlyinManager():

    # +---------------------------------------------------------------------+
    # |                            Constructor                              |
    # +---------------------------------------------------------------------+

    def __init__(self, nb_drones: int) -> None:
        """
        Initialize the FlyinManager with the number of drones.

        Args:
            nb_drones (int): The number of drones to manage.
        """

        self.__nb_drones = nb_drones
        self.__start_hub: Optional[Node] = None
        self.__end_hub: Optional[Node] = None
        self.__list_node: list[Node] = []
        self.__list_drone: list[Drone] = []
        self.__lst_connexion: list[Connexion] = []
        self.__nb_coups = 0

        self.generate_drones()

    # +---------------------------------------------------------------------+
    # |                              Getter                                 |
    # +---------------------------------------------------------------------+

    def get_nbDrones(self) -> int:
        """Get the number of drones."""
        return self.__nb_drones

    def get_startHub(self) -> Optional[Node]:
        """Get the starting hub."""
        return self.__start_hub

    def get_endHub(self) -> Optional[Node]:
        """Get the ending hub."""
        return self.__end_hub

    def get_listNode(self) -> list[Node]:
        """Get the list of nodes."""
        return self.__list_node

    def get_listDrone(self) -> list[Drone]:
        """Get the list of drones."""
        return self.__list_drone

    def get_listConnexion(self) -> list[Connexion]:
        """Get the list of connexions."""
        return self.__lst_connexion

    def get_nbCoups(self) -> int:
        """Get the number of moves."""
        return self.__nb_coups

    # +---------------------------------------------------------------------+
    # |                              Setter                                 |
    # +---------------------------------------------------------------------+

    def set_startHub(self, node: Node) -> bool:
        """Set the starting hub."""
        if (type(node).__name__) == "Node":
            self.__start_hub = node
            return True
        return False

    def set_endHub(self, node: Node) -> bool:
        """Set the ending hub."""
        if (type(node).__name__) == "Node":
            self.__end_hub = node
            return True
        return False

    # +---------------------------------------------------------------------+
    # |                         list_node methods                           |
    # +---------------------------------------------------------------------+

    def add_node(self, node: Node) -> bool:
        """
        Add a node to the list of nodes.

        Args:
            node (Node): The node to add.

        Returns:
            bool: True if the node was added, False otherwise.
        """

        if (type(node).__name__) == "Node":
            self.__list_node.append(node)
            return True
        return False

    def check_dupplicated_name(self, name: str) -> bool:
        """
        Check if a node with the given name already exists.

        Args:
            name (str): The name to check.

        Returns:
            bool: True if a node with the name exists, False otherwise.
        """

        for node in self.__list_node:
            if node.name == name:
                return True
        return False

    def get_node_by_name(self, name: str) -> Node | None:
        """
        Get a node by its name.

        Args:
            name (str): The name of the node to get.

        Returns:
            Node | None: The node with the given name, or None if
                it doesn't exist.
        """

        for node in self.__list_node:
            if node.name == name:
                return node
        return None

    def get_node_max_coord(self) -> tuple[int, int] | None:
        """
        Get the maximum coordinates (x, y) among all nodes.

        Returns:
            tuple[int, int] | None: The maximum coordinates (x, y)
                among all nodes, or None if the list is empty.
        """

        if (len(self.__list_node) == 0):
            return None

        max_x = self.__list_node[0].x
        max_y = self.__list_node[0].y

        for node in self.__list_node:
            if node.x > max_x:
                max_x = node.x

            if node.y > max_y:
                max_y = node.y

        return (max_x, max_y)

    # +---------------------------------------------------------------------+
    # |                      list_connexions methods                        |
    # +---------------------------------------------------------------------+

    def add_connexion(self, connexion: Connexion) -> bool:
        """
        Add a connexion to the list of connexions.

        Args:
            connexion (Connexion): The connexion to add.

        Returns:
            bool: True if the connexion was added, False otherwise.
        """

        if (type(connexion).__name__) == "Connexion":
            self.__lst_connexion.append(connexion)
            return True
        return False

    def check_dupplicated_connexion(self, new_connexion: Connexion) -> bool:
        """
        Check if a connexion between the same nodes already exists.

        Args:
            new_connexion (Connexion): The connexion to check.

        Returns:
            bool: True if a connexion between nodes exists, False otherwise.
        """

        for connexion in self.__lst_connexion:

            same_direction = (
                connexion.node1 == new_connexion.node1
                and connexion.node2 == new_connexion.node2
            )
            opposite_direction = (
                connexion.node1 == new_connexion.node2
                and connexion.node2 == new_connexion.node1
            )

            if same_direction or opposite_direction:
                return True

        return False

    def get_connexion_between(
            self,
            node1: Node,
            node2: Node) -> Connexion | None:
        """
        Get the connexion between two nodes.

        Args:
            node1 (Node): The first node.
            node2 (Node): The second node.

        Returns:
            Connexion | None: The connexion between the two nodes, or None if
                it doesn't exist.
        """

        for connexion in self.__lst_connexion:
            if (connexion.node1 == node1 and connexion.node2 == node2) or \
               (connexion.node1 == node2 and connexion.node2 == node1):
                return connexion
        return None

    # +---------------------------------------------------------------------+
    # |                              Methods                                |
    # +---------------------------------------------------------------------+

    def generate_drones(self) -> None:
        """
        Generate the drones with random names and add
        them to the list of drones.
        """

        lst_title = ["TheDestroyer", "TheFunnyOne", "TheChoosenOne",
                     "TheGoofyOne", "TheDuckOne", "BATMAN", "TheHelminthOne",
                     "TheWorldEater", "TheSalty", "TheChaotic",
                     "TheTenno", "TheD4rkOne", "TheAnomaly", "TheVoidWalker",
                     "TheSmartest", "MasterKoala", "WidowMaker",
                     "TheMwetLover", "TheChaosAdorer", "TheTallestOne"]
        lst_name = ["Timmy", "George", "Bob", "Tommy", "Billy", "Bill",
                    "Sofie", "Shimada", "Kevin", "Mickeal", "Titouan", "Henry",
                    "James", "Edward", "Victoria", "Alice", "Aurora", "Luna",
                    "Brigitte", "Donald", "Timothé", "Taylor", "Mudkip",
                    "Boing", "Pouic", "Nono", "Sofia", "Allyn", "Nico",
                    "Victor", "Ana", "Romain", "Benoît", "Enzo", "Rémy",
                    "Thomas"]

        i = 0
        while (i < self.__nb_drones):

            random_title = random.choice(lst_title)
            random_name = random.choice(lst_name)

            drone_name = f"D{i}{random_name}{random_title}"
            new_drone = Drone(name=drone_name)

            self.__list_drone.append(new_drone)

            i += 1

    def to_string_detail(self) -> str:
        """
        This function was used for debugging purposes.

        Get a detailed string representation of the FlyinManager, including
        the list of nodes, connexions, and drones.

        Returns:
            str: A detailed string representation of the FlyinManager.
        """

        # === Section Nodes ===
        nodes_str = "  Nodes List:\n"
        if not self.__list_node:
            nodes_str += "    (Empty)\n"
        for node in self.__list_node:
            nodes_str += (
                f"    • {node.name:<20} "
                f"(x:{node.x:>2}, y:{node.y:>2}) | "
                f"Couleur: {node.color:<8} | "
                f"Zone: {node.zone:<10} | "
                f"Capacité: {len(node.lst_drones)}/{node.max_drones}\n"
            )

        # === Section Connexions ===
        conn_str = "  Connexions List:\n"
        if not self.__lst_connexion:
            conn_str += "    (Empty)\n"
        for conn in self.__lst_connexion:

            conn_str += (
                f"    • {conn.node1.name} <───> {conn.node2.name} "
                f"(Capacité: {len(conn.lst_drones)}/"
                f"{conn.max_link_capacity})\n"
            )

        # === Liste des drones ===

        drone_str = f"  Drone List ({self.__nb_drones}):\n"
        if not self.__list_drone:
            drone_str += "    (Empty)\n"
        for drone in self.__list_drone:

            drone_str += (
                f"    • {drone.name}\n"
            )

        header = f"╔{'═' * 80}╗\n║{'FLYIN MANAGER':^80}║\n╠{'═' * 80}╣"
        footer = f"╚{'═' * 80}╝"

        return f"{header}\n{nodes_str}\n{conn_str}\n{drone_str}{footer}"
