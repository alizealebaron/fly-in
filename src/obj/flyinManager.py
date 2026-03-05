# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : flyinManager.py                                                  #
# @author : alebaron <alebaron@student.42lehavre.fr>                         #
#                                                                            #
# @creation : 2026/02/27 13:53:46 by alebaron                                #
# @update   : 2026/03/05 15:36:08 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                                 Import                                  |
# +-------------------------------------------------------------------------+


from src.obj.node import Node
from src.obj.drone import Drone
from src.obj.connexion import Connexion
import random


# +-------------------------------------------------------------------------+
# |                                  Class                                  |
# +-------------------------------------------------------------------------+

class FlyinManager():

    # +---------------------------------------------------------------------+
    # |                            Constructor                              |
    # +---------------------------------------------------------------------+

    def __init__(self, nb_drones: int):

        self.__nb_drones = nb_drones
        self.__start_hub = None
        self.__end_hub = None
        self.__list_node: list[Node] = []
        self.__list_drone: list[Drone] = []
        self.__lst_connexion: list[Connexion] = []

        self.generate_drones()

    # +---------------------------------------------------------------------+
    # |                              Getter                                 |
    # +---------------------------------------------------------------------+

    def get_nbDrones(self) -> int:
        return self.__nb_drones

    def get_startHub(self) -> Node:
        return self.__start_hub

    def get_endHub(self) -> Node:
        return self.__end_hub

    def get_listNode(self) -> list[Node]:
        return self.__list_node

    def get_listDrone(self) -> list[Drone]:
        return self.__list_drone

    def get_listConnexion(self) -> list[Connexion]:
        return self.__lst_connexion

    # +---------------------------------------------------------------------+
    # |                              Setter                                 |
    # +---------------------------------------------------------------------+

    def set_startHub(self, node: Node) -> bool:
        if (type(node).__name__) == "Node":
            self.__start_hub = node
            return True
        return False

    def set_endHub(self, node: Node) -> bool:
        if (type(node).__name__) == "Node":
            self.__end_hub = node
            return True
        return False

    # +---------------------------------------------------------------------+
    # |                         list_node methods                           |
    # +---------------------------------------------------------------------+

    def add_node(self, node: Node) -> bool:
        if (type(node).__name__) == "Node":
            self.__list_node.append(node)
            return True
        return False

    def check_dupplicated_name(self, name: str) -> bool:

        for node in self.__list_node:
            if node.name == name:
                return True
        return False

    def get_node_by_name(self, name: str) -> Node | None:

        for node in self.__list_node:
            if node.name == name:
                return node
        return None

    # +---------------------------------------------------------------------+
    # |                      list_connexions methods                        |
    # +---------------------------------------------------------------------+

    def add_connexion(self, connexion: Connexion) -> bool:
        if (type(connexion).__name__) == "Connexion":
            self.__lst_connexion.append(connexion)
            return True
        return False

    def check_dupplicated_connexion(self, new_connexion: Connexion) -> bool:

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

    # +---------------------------------------------------------------------+
    # |                              Methods                                |
    # +---------------------------------------------------------------------+

    def generate_drones(self) -> None:

        lst_title = ["TheDestroyer", "TheFunnyOne", "TheChoosenOne",
                     "TheGoofyOne", "TheDuckOne", "BATMAN", "TheHelminthOne",
                     "TheWorldEater", "TheSalty", "TheChaotic",
                     "TheTenno", "TheD4rkOne", "TheAnomaly", "TheVoidWalker",
                     "TheSmartest", "MasterKoala", "WidowMaker",
                     "TheMwetLover", "TheChaosAdorer"]
        lst_name = ["Timmy", "George", "Bob", "Tommy", "Billy", "Bill",
                    "Sofie", "Shimada", "Kevin", "Mickeal", "Titouan", "Henry",
                    "James", "Edward", "Victoria", "Alice", "Aurora", "Luna",
                    "Brigitte", "Donald", "Timothé", "Taylor", "Mudkip",
                    "Boing", "Pouic", "Nono", "Sofia", "Allyn", "Nico",
                    "Victor", "Ana", "Romain", "Benoît", "Enzo", "Rémy"]

        i = 0
        while (i < self.__nb_drones):

            random_title = random.choice(lst_title)
            random_name = random.choice(lst_name)

            drone_name = f"D{i}{random_name}{random_title}"
            new_drone = Drone(name=drone_name)

            self.__list_drone.append(new_drone)

            i += 1

    def to_string_detail(self) -> str:
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
                f"(Capacité: {len(conn.lst_drones)}/{conn.max_link_capacity})\n"
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
