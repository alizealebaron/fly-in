# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : main.py                                                          #
# @author : alebaron <alebaron@student.42lehavre.fr>                         #
#                                                                            #
# @creation : 2026/02/26 13:01:33 by alebaron                                #
# @update   : 2026/03/03 13:10:46 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+

import os
import sys
from src.obj.flyinManager import FlyinManager
from src.obj.node import Node
from src.parsing.parsing import parsing_data
from src.utils.error import exit_error

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

    print(flyinManager.to_string_detail())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        os.system("clear")
        file = open("src/utils/interrupt.txt", "r", encoding='utf-8')
        content = file.read()
        print(content)
    except Exception as e:
        print(f"Error: {e}")
