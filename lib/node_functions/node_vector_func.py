from .node_three_dim_func import ThreeDimNodeFunction
from dataclasses import dataclass

node_name = "NodeVector"

@dataclass
class VectorNodeFunction(ThreeDimNodeFunction):
    '''Vector Node Function Class'''