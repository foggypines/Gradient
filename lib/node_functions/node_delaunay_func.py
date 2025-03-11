import numpy as np
from scipy.spatial import Delaunay
from scipy.spatial import KDTree
from . node_input import NodeInput
from . node_output import NodeOutput
from . node_base_func import BaseNodeFunction
from dataclasses import dataclass, field

node_name = "Delaunay"
point_set_name = "_Point_set"
output2_name = "_Output2"

@dataclass
class DelaunayNodeFunction(BaseNodeFunction):

    point_set: NodeInput = field(default = None)

    output2: NodeOutput = field(default = None)

    def __post_init__(self):

        super().__post_init__()

        if self.point_set is None:

            self.point_set = self.add_input(point_set_name)

        if self.output2 is None:

            self.output2 = self.add_output(output2_name)

        self.outputs.append(self.output2)

    def compute(self, sender=None, app_data=None):

        tri = Delaunay(self.point_set.parameter)

        convex_hull = tri.convex_hull

        list1 = []

        list2 = []

        for i in range(0, len(convex_hull)):

            list1.extend([convex_hull[i][0], convex_hull[i][1], convex_hull[i][2]])

            list2.extend([convex_hull[i][1], convex_hull[i][2], convex_hull[i][0]])

        self.result = np.array([list1, list2])

        self.output.payload = list1
        self.output2.payload = list2