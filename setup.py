# setup.py
import sys

def load():
    paths = ['/path1/','/path2/','/path3/']
    for p in paths:
        sys.path.insert(0, p)

# entrypoint.py
from setup import load
load()
# continue with program