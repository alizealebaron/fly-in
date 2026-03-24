# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : main.py                                                          #
# @author : alebaron <alebaron@student.42.fr>                                #
#                                                                            #
# @creation : 2026/02/26 13:01:33 by alebaron                                #
# @update   : 2026/03/24 16:29:20 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


import os
import sys
from src.algorithm.dijkstra import calcule_path
from src.parsing.parsing import parsing_data
from src.utils.error import exit_error
from src.view.graph_view import show_graph


# +-------------------------------------------------------------------------+
# |                                  Main                                   |
# +-------------------------------------------------------------------------+

def main() -> None:

    # === Get Main arguments ===

    argc = len(sys.argv)
    argv = sys.argv

    if (argc != 2):
        exit_error(FileNotFoundError(), "Wrong arguments. Need one file.")

    # === Parsing Data ===

    flyinManager = parsing_data(argv[1])

    # print(flyinManager.to_string_detail())

    # === Use dijkstra algorithm ===

    path = calcule_path(flyinManager, flyinManager.get_startHub(), flyinManager.get_endHub())

    for node in path:
        print(f"{node.name} -> ", end="")

    print()

    # === Print graphic view ===

    show_graph(flyinManager, argv[1])



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        os.system("clear")
        file = open("src/utils/interrupt.txt", "r", encoding='utf-8')
        content = file.read()
        print(content)
    # except Exception as e:
    #     print(f"Error: {e}")
