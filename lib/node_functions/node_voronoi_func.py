import numpy as np
from scipy.spatial import Voronoi
from .node_input import NodeInput
from .node_output import NodeOutput
from .node_base_func import BaseNodeFunction
from dataclasses import dataclass, field
import adsk.core, adsk.fusion


node_name = "Voronoi"
point_set_name = "_Point_set"
boundary_name = "_Boundary"

@dataclass
class VoronoiNodeFunction(BaseNodeFunction):

    point_set: NodeInput = field(default = None)

    boundary: NodeInput = field(default = None)

    def __post_init__(self):

        super().__post_init__()

        if self.point_set is None:

            self.point_set = self.add_input(point_set_name, required=True, ui_label="Point Set")

        if self.boundary is None:

            self.boundary = self.add_input(boundary_name, required=True, ui_label="Boundary")

    def compute(self, sender=None, app_data=None):

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

        brep = self.boundary.parameter[0]

        app = adsk.core.Application.get()

        self.design = adsk.fusion.Design.cast(app.activeProduct)
        
        rootcomp = self.design.rootComponent

        for pair in line_vertices:

            v1 = vertices[pair[0]]

            v2 = vertices[pair[1]]

            point1 = adsk.core.Point3D.create(v1[0] * 0.1, v1[1] * 0.1, v1[2] * 0.1) 

            point2 = adsk.core.Point3D.create(v2[0] * 0.1, v2[1] * 0.1, v2[2] * 0.1)

            containment1 = brep.pointContainment(point1)

            containment2 = brep.pointContainment(point2)

            if containment1 == 2 and containment2 == 2:

                continue

            elif containment1 == 2 and containment2 != 2:

                ori = adsk.core.Point3D.create(v2[0] * 0.1, v2[1] * 0.1, v2[2] * 0.1)

                x = (v1[0] - v2[0])
                y = (v1[1] - v2[1])
                z = (v1[2] - v2[2])

                ray = adsk.core.Vector3D.create(x, y, z)

                hitpoints = adsk.core.ObjectCollection.create()

                coll = rootcomp.findBRepUsingRay(ori, ray, 1, -1.0, True, hitpoints)

                if len(coll) > 0:

                    v1 = [hitpoints[0].x*10, hitpoints[0].y*10, hitpoints[0].z*10]

                    lines.append([v1, v2])

            elif containment1 != 2 and containment2 == 2:

                ori = adsk.core.Point3D.create(v1[0] * 0.1, v1[1] * 0.1, v1[2] * 0.1)

                x = (v2[0] - v1[0])
                y = (v2[1] - v1[1])
                z = (v2[2] - v1[2])

                ray = adsk.core.Vector3D.create(x, y, z)

                hitpoints = adsk.core.ObjectCollection.create()

                coll = rootcomp.findBRepUsingRay(ori, ray, 1, -1.0, True, hitpoints)

                if len(coll) > 0:

                    v2 = [hitpoints[0].x*10, hitpoints[0].y*10, hitpoints[0].z*10]

                    lines.append([v1, v2])

            else:

                lines.append([v1, v2])

        self.output.payload = np.array(lines)