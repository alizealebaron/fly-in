# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : graph_view.py                                                    #
# @author : alebaron <alebaron@student.42.fr>                                #
#                                                                            #
# @creation : 2026/03/06 13:02:33 by alebaron                                #
# @update   : 2026/03/26 11:15:46 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


from src.models.flyinManager import FlyinManager
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import networkx as nx


# +-------------------------------------------------------------------------+
# |                             Main Function                               |
# +-------------------------------------------------------------------------+

def show_graph(flyinManager: FlyinManager, filename: str) -> None:

    # === Recovery of flyinManager data ===

    lst_node = flyinManager.get_listNode()
    lst_connexion = flyinManager.get_listConnexion()

    # === Initialisation of the graph ===

    G = nx.Graph()

    pos = {}
    node_colors = []

    for node in lst_node:
        G.add_node(node.name)

        pos[node.name] = (node.x, node.y)

        try:
            mcolors.to_rgba(node.color)
            node_colors.append(node.color)
        except (ValueError, TypeError):
            node_colors.append("skyblue")

    for connexion in lst_connexion:
        G.add_edge(connexion.node1.name, connexion.node2.name)

    plt.figure(figsize=(20, 10), dpi=100)

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=node_colors,
        node_size=450,
        edge_color='gray',
        font_size=8,
        font_weight='light'
    )

    plt.title(filename)

    plt.show()
