# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : dijkstra.py                                                      #
# @author : alebaron <alebaron@student.42.fr>                                #
#                                                                            #
# @creation : 2026/03/24 12:33:58 by alebaron                                #
# @update   : 2026/03/26 12:24:10 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                                 Import                                  |
# +-------------------------------------------------------------------------+


import heapq
from src.models.node import Node
from src.models.connexion import Connexion
from src.models.flyinManager import FlyinManager


# +-------------------------------------------------------------------------+
# |                                 Method                                  |
# +-------------------------------------------------------------------------+

def calcule_path(flyin: FlyinManager, start: Node, end: Node) -> list[Node]:
    """
    Calculate the shortest path from start to end using Dijkstra's algorithm.

    Args:
        flyin (FlyinManager): The flyin manager containing the graph.
        start (Node): The starting node.
        end (Node): The ending node.

    Returns:
        list[Node]: The shortest path from start to end.
    """

    # Initialize a new queue
    priority_queue: list[tuple[float, int, Node]] = []

    # Initialize the nodes with infinite distance
    dict_distances = {node.name: float('inf') for node in flyin.get_listNode()}
    dict_parent: dict[str, Node | None] = {
        node.name: None for node in flyin.get_listNode()
    }

    # Set the distance of the starting node to 0
    dict_distances[start.name] = 0

    count = 0
    heapq.heappush(priority_queue, (0, count, start))

    while len(priority_queue) != 0:

        # Get the nearest node
        act_dist, _, act_node = heapq.heappop(priority_queue)

        # End if we reach the end
        if act_node.name == end.name:
            break

        # Update the distance dictionary
        for neighbor in get_neighbours(act_node, flyin.get_listConnexion()):

            new_dist = act_dist + neighbor.get_weight()

            # Checking flow and distance constraints
            if (new_dist < dict_distances[neighbor.name] and
               neighbor.is_completed() is False and
               neighbor.zone != "blocked"):

                count += 1
                dict_distances[neighbor.name] = new_dist
                dict_parent[neighbor.name] = act_node
                heapq.heappush(priority_queue, (new_dist, count, neighbor))

    # Get the path from start to the end
    path: list[Node] = []
    curr: Node | None = end
    while curr is not None:
        path.append(curr)
        curr = dict_parent.get(curr.name)
    return path[::-1]


def get_neighbours(node: Node, lst_connections: list[Connexion]) -> set[Node]:
    """
    Get the neighbors of a node based on the connections.

    Args:
        node (Node): The node to get the neighbors of.
        lst_connections (list[Connexion]): The list of connections to use.

    Returns:
        set[Node]: The set of neighboring nodes.
    """

    lst_neighbours = set()

    for connexion in lst_connections:

        if connexion.node1 == node:
            lst_neighbours.add(connexion.node2)
        elif connexion.node2 == node:
            lst_neighbours.add(connexion.node1)

    return lst_neighbours
