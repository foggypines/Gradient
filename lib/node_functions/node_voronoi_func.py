import numpy as np
from scipy.spatial import Voronoi
from .node_input import NodeInput
from .node_output import NodeOutput
from .node_base_func import BaseNodeFunction
from dataclasses import dataclass, field

node_name = "Voronoi"
point_set_name = "_Point_set"
output2_name = "_Output2"

@dataclass
class VoronoiNodeFunction(BaseNodeFunction):

    point_set: NodeInput = field(default = None)

    def __post_init__(self):

        super().__post_init__()

        if self.point_set is None:

            self.point_set = self.add_input(point_set_name)

    def compute(self, sender=None, app_data=None):

        # points = np.array([[0, 0, 0], [0, 1, 0], [0, 2, 0], [1, 0, 0], [1, 1, 0], [1, 2, 0],
        #                 [2, 0, 0], [2, 1, 0], [2, 2, 0],
        #                 [0, 0, 1], [0, 1, 1], [0, 2, 1], [1, 0, 1], [1, 1, 1], [1, 2, 1],
        #                 [2, 0, 1], [2, 1, 1], [2, 2, 1],
        #                 [0, 0, 2], [0, 1, 2], [0, 2, 2], [1, 0, 2], [1, 1, 2], [1, 2, 2],
        #                 [2, 0, 2], [2, 1, 2], [2, 2, 2]])

        points = self.point_set.parameter

        vor = Voronoi(points)

        vertices = vor.vertices

        ridge_vertices = vor.ridge_vertices

        lines = []

        line_vertices = []

        for i in range(len(ridge_vertices)):

            ridge = ridge_vertices[i]

            if -1 in ridge or len(ridge) == 0:

                continue

            else:

                ridge_len = len(ridge)

                j = 0

                while j < ridge_len:

                    if j == ridge_len - 1:

                        t = 0

                    else:

                        t = j + 1

                    v1 = ridge[j]

                    v2 = ridge[t]

                    pair = [v1, v2]

                    pair.sort()

                    line_vertices.append(pair)

                    j += 1

        line_vertices = np.array(line_vertices)

        line_vertices = np.unique(line_vertices, axis=0)

        for pair in line_vertices:

            v1 = vertices[pair[0]]

            v2 = vertices[pair[1]]

            lines.append([v1, v2])

        self.output.payload = np.array(lines)