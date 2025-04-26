import array
import numpy as np
from numpy.linalg import multi_dot
from scipy.spatial import Voronoi
from .node_input import NodeInput
from .node_output import NodeOutput
from .node_base_func import BaseNodeFunction
from dataclasses import dataclass, field
from itertools import combinations
import adsk.core, adsk.fusion


node_name = "Voronoi"
point_set_name = "_Point_set"
boundary_name = "_Boundary"

tolerance=1e-6

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

        #Get resources for generating faces

        app = adsk.core.Application.get()

        self.design = adsk.fusion.Design.cast(app.activeProduct)
        
        temp_brep_mgr = adsk.fusion.TemporaryBRepManager.get()

        rootcomp = self.design.rootComponent

        base_feature_attr_name = "gradient_base_feature"

        base_feature_attr_group = "gradient"

        attributes = self.design.findAttributes(groupName=base_feature_attr_group, 
                                        attributeName=base_feature_attr_name)

        base_feature = attributes[0].parent

        bodies = rootcomp.bRepBodies

        boundary = self.boundary.parameter

        #Getting starting values and do initial voroi calculation

        points = self.point_set.parameter

        vor = Voronoi(points)

        vertices = vor.vertices

        regions = vor.regions

        ridge_vertices = vor.ridge_vertices

        ridge_points = vor.ridge_points

        # Map voronoi vertices to faces

        voronoi_cells = []

        for region in regions:

            cell = VoronoiCell(region)

            if region == [] or -1 in region:
                continue

            else:

                for ridge in ridge_vertices:

                    if all(v in region for v in ridge):

                        cell.ridges.append(ridge)

                for ridge in cell.ridges:

                    j = 0

                    face = VoronoiFace()
                    
                    edge_len = len(ridge)

                    while j < edge_len:

                        if j == edge_len - 1:

                            t = 0

                        else:

                            t = j + 1

                        v1 = ridge[j]

                        v2 = ridge[t]

                        pair = [v1, v2]

                        j += 1

                        face.edges.append(pair)

                    cell.faces.append(face)

                voronoi_cells.append(cell)

        #create the faces

        for cell in voronoi_cells:

            for face in cell.faces:

                curves = []

                for edge in face.edges:

                    start = vertices[edge[0]]

                    end = vertices[edge[1]]

                    start_point = adsk.core.Point3D.create(start[0]*0.1, start[1]*0.1, start[2]*0.1)

                    end_point = adsk.core.Point3D.create(end[0]*0.1, end[1]*0.1, end[2]*0.1)

                    line_segment = adsk.core.Line3D.create(start_point, end_point)

                    curves.append(line_segment)

                wirebody, edgeMap = temp_brep_mgr.createWireFromCurves(curves)

                wire_bodies = []

                wire_bodies.append(wirebody)

                brep_face = temp_brep_mgr.createFaceFromPlanarWires(wire_bodies)

                body = bodies.add(brep_face, base_feature)

        adsk.doEvents()

class VoronoiCell:
    def __init__(self, vertex_indices):
        self.vertex_indices = vertex_indices
        self.ridges = []
        self.faces = []

class VoronoiFace:
    def __init__(self):
        self.edges = []

class Plane:
    
    def __init__(self, vec1, vec2, point):
        
        self.normal = np.cross(vec1, vec2)
        
        self.a, self.b, self.c = self.normal

        self.d = -np.dot(self.normal, point)
        

    def distance_to_point(self, point):

        x, y, z = point

        distance = np.abs(self.a * x + self.b * y + self.c * z + self.d) / np.sqrt(self.a**2 + self.b**2 + self.c**2)

        return distance