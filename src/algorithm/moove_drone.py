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
# @update   : 2026/03/25 14:03:23 by alebaron                                #
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

        # +---------------------------------------------------------------------+
        # | PASSE 1: Traiter les drones en attente sur les connexions           |
        # +---------------------------------------------------------------------+

        for connexion in fly.get_listConnexion():
            for drone in connexion.lst_drones.copy():
                if drone in mooved_drone:
                    continue

                restricted_node = fly.get_node_by_name(drone.next_restricted_node)
                
                # Essayer d'ajouter le drone à la zone restricted
                if restricted_node is not None and restricted_node.add_drone(drone) is True:
                    mooved_drone.add(drone)
                    connexion.lst_drones.remove(drone)
                    str_print += f"{drone.name}-{restricted_node.name} "
                    # Réinitialiser les flags
                    drone.is_on_connection = False
                    drone.waiting_connection_nodes = None

        # +---------------------------------------------------------------------+
        # | PASSE 2: Traiter les drones dans les nœuds                          |
        # +---------------------------------------------------------------------+

        checked_node = set()
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

                next_node = path[1]

                # Cas 1: Le prochain nœud est une zone restricted
                if next_node.zone == "restricted":
                    connexion = fly.get_connexion_between(node, next_node)

                    # Vérifier si la connexion existe et a de la capacité
                    if connexion is not None and connexion.add_drone(drone) is True:
                        mooved_drone.add(drone)
                        node.lst_drones.remove(drone)

                        # Marquer le drone comme étant en attente sur la connexion
                        drone.is_on_connection = True
                        drone.waiting_connection_nodes = (node.name, next_node.name)
                        drone.next_restricted_node = next_node.name
                    continue

                # Cas 2: Déplacement normal
                if next_node.add_drone(drone) is True:
                    mooved_drone.add(drone)
                    node.lst_drones.remove(drone)
                    str_print += f"{drone.name}-{next_node.name} "

            # Ajout des voisins de la node dans la queue

            for connexion in fly.get_listConnexion():
                new_node = None

                if connexion.node1 == node and connexion.node2 not in checked_node:
                    new_node = connexion.node2

                elif connexion.node2 == node and connexion.node1 not in checked_node:
                    new_node = connexion.node1

                if new_node is not None:
                    count += 1
                    heapq.heappush(priority_queue, (count, new_node))
                    checked_node.add(new_node)

        print(f"Turn n°{nb_turn}: {str_print}")
        nb_turn += 1



def debug_print_path(path: list[Node]) -> None:

    rendu = " -> ".join([obj.name for obj in path])
    print(rendu)
