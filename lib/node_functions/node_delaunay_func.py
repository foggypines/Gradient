import numpy as np
from scipy.spatial import Delaunay
from scipy.spatial import KDTree
from . node_input import NodeInput
from . node_base_func import BaseNodeFunction
from dataclasses import dataclass, field

node_name = "Delaunay"
point_set_name = "_Point_set"

@dataclass
class DelaunayNodeFunction(BaseNodeFunction):

    point_set: NodeInput = field(default = None)

    def __post_init__(self):

        super().__post_init__()

        if self.point_set is None:

            self.point_set = self.add_input(point_set_name)

    def compute(self, sender=None, app_data=None):

        tri = Delaunay(self.point_set.parameter)

        self.output.payload = tri.simplices