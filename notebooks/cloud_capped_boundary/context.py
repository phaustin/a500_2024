"""
define the path to important folders without having
to install anything -- just do:

import contenxt

then the path for the data directory is

context.data_dir

"""
import sys
from pathlib import Path

path = Path(__file__).resolve()  # this file
this_dir = path.parent  # this folder
notebooks_dir = this_dir
root_dir = notebooks_dir.parents[1]  # a500_notebooks
data_dir = root_dir / Path("data")
test_dir = root_dir / Path("test_data")
map_dir = root_dir / Path("map_data")
print(f"add this: {root_dir}")
sys.path.insert(0, str(root_dir))
sep = "*" * 30
print(
    f"{sep}\ncontext imported. Front and back of path:\n{sys.path[0]}\n{sys.path[-1]}\n{sep}\n"
)


print(f"through {__file__} -- pha")
