import os

__all__ = []
nodes_folder = os.path.dirname(__file__)

for filename in os.listdir(nodes_folder):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = filename[:-3]
        __all__.append(module_name)
