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
# @update   : 2026/03/24 17:59:35 by alebaron                                #
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

    nb_turn = 1

    while len(fly.get_endHub().lst_drones) != fly.get_nbDrones():

        str_print = ""
        mooved_drone = set()
        count = 0
        priority_queue = []

        heapq.heappush(priority_queue, (count, fly.get_endHub()))

        # Parcours des nodes pour bouger tous les drones
        while priority_queue:

            _, node = heapq.heappop(priority_queue)

            for drone in node.lst_drones.copy():

                if drone in mooved_drone:
                    continue

                path = calcule_path(fly, node, fly.get_endHub())
                # debug_print_path(path)

                # In case of there is no solution for this turn
                if len(path) == 1:
                    continue

                if path[1].add_drone(drone) is True:
                    mooved_drone.add(drone)
                    node.lst_drones.remove(drone)
                    str_print += f"{drone.name}-{path[1].name} "

            # Ajout des voisins de la node dans la queue

            for connexion in fly.get_listConnexion():
                if connexion.node1 == node:
                    count += 1
                    heapq.heappush(priority_queue, (count, connexion.node2))
                elif connexion.node2 == node:
                    count += 1
                    heapq.heappush(priority_queue, (count, connexion.node1))

        print(f"Turn n°{nb_turn}: {str_print}")
        nb_turn += 1



def debug_print_path(path: list[Node]) -> None:

    rendu = " -> ".join([obj.name for obj in path])
    print(rendu)
