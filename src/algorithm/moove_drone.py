# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : moove_drone.py                                                   #
# @author : alebaron <alebaron@student.42.fr>                                #
#                                                                            #
# @creation : 2026/03/24 16:49:54 by alebaron                                #
# @update   : 2026/03/26 12:25:36 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                                 Import                                  |
# +-------------------------------------------------------------------------+


import heapq
from src.models.flyinManager import FlyinManager
from src.models.node import Node
from src.algorithm.dijkstra import calcule_path


# +-------------------------------------------------------------------------+
# |                                 Method                                  |
# +-------------------------------------------------------------------------+

def find_the_way(fly: FlyinManager) -> None:
    """
    Move the drones from their starting position to the end hub using
    Dijkstra's algorithm to find the shortest path for each drone.

    It will print the movements of the drones at each turn until all drones
    are on the end hub.

    The path is calculated for each drone at each turn to take into
    account the dynamic changes of the graph (drones moving, connections
    being used, etc.).

    Args:
        fly (FlyinManager): The flyin manager containing the graph and drones.
    """

    nb_turn = 1

    end_hub = fly.get_endHub()
    assert end_hub is not None, "End hub must be defined"

    while len(end_hub.lst_drones) != fly.get_nbDrones():

        str_print = ""
        mooved_drone = set()

        # +-----------------------------------------------------------------+
        # | Step 1: Check all connections                                   |
        # +-----------------------------------------------------------------+

        for connexion in fly.get_listConnexion():
            for drone in connexion.lst_drones.copy():
                if drone in mooved_drone:
                    continue

                if drone.next_restricted_node is None:
                    continue

                restricted_node = fly.get_node_by_name(
                    drone.next_restricted_node)

                # Try adding the drone to the restricted zone

                if (restricted_node is not None and
                   restricted_node.add_drone(drone) is True):

                    mooved_drone.add(drone)
                    connexion.lst_drones.remove(drone)
                    str_print += f"{drone.name}-"
                    str_print += f"{restricted_node.get_colored_name()} "
                    # Réinitialiser les flags
                    drone.is_on_connection = False
                    drone.waiting_connection_nodes = None

        # +-----------------------------------------------------------------+
        # | Step 1: Check all nodes                                         |
        # +-----------------------------------------------------------------+

        checked_node = set()
        count = 0
        priority_queue: list[tuple[int, Node]] = []

        heapq.heappush(priority_queue, (count, end_hub))

        # Pathing through nodes to move all the drones
        while priority_queue:

            _, node = heapq.heappop(priority_queue)

            for drone in node.lst_drones.copy():

                if drone in mooved_drone:
                    continue

                path = calcule_path(fly, node, end_hub)

                # In case of there is no solution for this turn
                if len(path) == 1:
                    continue

                next_node = path[1]

                # Case 1: The next node is a restricted area
                if next_node.zone == "restricted":
                    connexion_opt = fly.get_connexion_between(node, next_node)

                    if (connexion_opt is not None and
                       connexion_opt.add_drone(drone) is True):
                        connexion = connexion_opt

                        mooved_drone.add(drone)
                        node.lst_drones.remove(drone)

                        drone.is_on_connection = True
                        drone.waiting_connection_nodes = (
                            node.name, next_node.name)
                        drone.next_restricted_node = next_node.name
                        str_print += (f"{drone.name}-"
                                      f"({connexion_opt.node1.name}-")
                        str_print += f"{connexion_opt.node2.name}) "
                    continue

                # Case 2: Normal movement
                if next_node.add_drone(drone) is True:
                    mooved_drone.add(drone)
                    node.lst_drones.remove(drone)
                    str_print += f"{drone.name}-"
                    str_print += f"{next_node.get_colored_name()} "

            # Add the node's neighbours to the queue

            for connexion in fly.get_listConnexion():
                new_node = None

                if (connexion.node1 == node and
                   connexion.node2 not in checked_node):
                    new_node = connexion.node2

                elif (connexion.node2 == node and
                      connexion.node1 not in checked_node):
                    new_node = connexion.node1

                if new_node is not None:
                    count += 1
                    heapq.heappush(priority_queue, (count, new_node))
                    checked_node.add(new_node)

        print(f"Turn n°{nb_turn}: {str_print}")
        nb_turn += 1


def debug_print_path(path: list[Node]) -> None:
    """
    Debug function to print the path of nodes.
    """

    rendu = " -> ".join([obj.name for obj in path])
    print(rendu)
