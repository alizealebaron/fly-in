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
# @update   : 2026/03/24 16:55:02 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                                 Import                                  |
# +-------------------------------------------------------------------------+


from src.models.flyinManager import FlyinManager
from src.algorithm.dijkstra import calcule_path


# +-------------------------------------------------------------------------+
# |                                 Method                                  |
# +-------------------------------------------------------------------------+

def find_the_way(fly: FlyinManager) -> None:

    # Parcours des nodes pour bouger tous les drones
    for node in fly.get_listNode():

        # Initialisation des drones ayant déjà bougé
        mooved_drone = set()

        for drone in node.lst_drones:

            path = calcule_path(fly, node, fly.get_endHub())

            