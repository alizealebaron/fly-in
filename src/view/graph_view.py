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
# @update   : 2026/03/06 13:28:05 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


from src.models.flyinManager import FlyinManager
import pyqtgraph as pg


# +-------------------------------------------------------------------------+
# |                             Main Function                               |
# +-------------------------------------------------------------------------+

def show_graph(flyinManager: FlyinManager) -> None:

    # === Recovery of flyinManager data ===

    lst_node = flyinManager.get_listNode()

    # === Initialisation of the graph ===

    # app = pg.mkQApp("Flyin_View")
    # win = pg.GraphicsLayoutWidget(show=True, title="Flyin_View")

    # app = pg.mkQApp("Graphe de Points Reliés")

    # 1. Créer la fenêtre et le widget de plot
    win = pg.GraphicsLayoutWidget(show=True)
    view = win.addPlot()

    # 2. Masquer les axes pour n'avoir que les points
    view.hideAxis('left')
    view.hideAxis('bottom')

    # 3. Définir les coordonnées des points (X, Y)
    points_x = [1, 3, 5, 2, 4]
    points_y = [2, 5, 2, 8, 7]

    # 4. Afficher les points (ScatterPlotItem)
    # symbol='o' pour des cercles, size=15 pour la taille
    scatter = pg.ScatterPlotItem(
        x=points_x, 
        y=points_y, 
        size=15, 
        pen=pg.mkPen('w'), 
        brush=pg.mkBrush(100, 100, 255)
    )
    view.addItem(scatter)

    # 5. Relier certains points (ex: le point 0 avec le point 2, et le 1 avec le 4)
    # On crée une courbe pour chaque segment ou une liste de segments
    connections = [(0, 2), (1, 4), (3, 4)]

    for start_idx, end_idx in connections:
        x_coords = [points_x[start_idx], points_x[end_idx]]
        y_coords = [points_y[start_idx], points_y[end_idx]]
        
        line = pg.PlotCurveItem(x_coords, y_coords, pen=pg.mkPen('w', width=1, style=pg.QtCore.Qt.DashLine))
        view.addItem(line)

    # Optionnel : Forcer un ratio d'aspect 1:1 pour ne pas déformer les distances
    view.setAspectLocked(True)