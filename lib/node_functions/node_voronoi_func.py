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

        complex_boundary = self.boundary.parameter[0]

        # bounding_box = temp_brep_mgr.createBox(complex_boundary.orientedMinimumBoundingBox)

        #Initial Voronoi calculation

        # points = self.point_set.parameter

        points = np.array([[0, 0, 0], [0, 1, 0], [0, 2, 0], [1, 0, 0], [1, 1, 0], [1, 2, 0],
                        [2, 0, 0], [2, 1, 0], [2, 2, 0],
                        [0, 0, 1], [0, 1, 1], [0, 2, 1], [1, 0, 1], [1, 1, 1], [1, 2, 1],
                        [2, 0, 1], [2, 1, 1], [2, 2, 1],
                        [0, 0, 2], [0, 1, 2], [0, 2, 2], [1, 0, 2], [1, 1, 2], [1, 2, 2],
                        [2, 0, 2], [2, 1, 2], [2, 2, 2]])

        vor = Voronoi(points)

        vertices = vor.vertices

        regions = vor.regions

        ridge_vertices = vor.ridge_vertices

        ridge_points = vor.ridge_points

        voronoi_cells = []

        line_pairs = []

        #compute some stats on the generated points

        center = vor.points.mean(axis=0)

        # Map voronoi vertices to faces

        for region in regions:

            cell = VoronoiCell(region)

            if len(region) <= 2:

                continue

            else:

                for i in range(len(ridge_vertices)):
                    
                    ridge = ridge_vertices[i]

                    if all(v in region for v in ridge):

                        cell.ridges.append(ridge)

                        cell.ridge_indices.append(i)

                for k in range(len(cell.ridges)):

                    j = 0

                    face = VoronoiFace()

                    ridge = cell.ridges[k]
                    
                    edge_len = len(ridge)

                    ridge_point_indices = cell.ridge_indices[k]

                    has_infinity = any(v == -1 for v in ridge)

                    while j < edge_len:

                        if j == edge_len - 1:

                            t = 0

                        else:

                            t = j + 1
                            
                        if has_infinity == False:

                            v1 = ridge[j]

                            v2 = ridge[t]

                            pair = [v1, v2]

                            face.edges.append(pair)

                        else:

                            ridge_copy = [v for v in ridge if v != -1]  # Remove -1 from the list

                            l1_i = ridge_copy[0]

                            l2_i = ridge_copy[1]

                            l1 = vertices[l1_i]

                            l2 = vertices[l2_i]

                            a1 = l1

                            a2 = l2

                            # Compute a vector that represents the edge of the face running out to inifinity

                            l_vec = l2 - l1

                            point_indices = ridge_points[ridge_point_indices]

                            p1_i = point_indices[0]

                            p2_i = point_indices[1]

                            p1 = vor.points[p1_i]

                            p2 = vor.points[p2_i]

                            p_vec = p2 - p1

                            out_vec = np.cross(l_vec, p_vec) * 2 # multiply by 2 to space the point out a bit from the starting location

                            l1_a = l1 + out_vec

                            l1_b = l1 - out_vec

                            a_dist = np.linalg.norm(l1_a - center)

                            b_dist = np.linalg.norm(l1_b - center)

                            # determine which direction sets the vector in the right direction

                            if a_dist > b_dist:

                                out_vec = out_vec

                            else:

                                out_vec = -out_vec

                            l1_hit_points = adsk.core.ObjectCollection.create()

                            l2_hit_points = adsk.core.ObjectCollection.create()

                            l1_fusion = adsk.core.Point3D.create(l1[0] * 0.1, l1[1]*0.1, l1[2]*0.1)

                            l2_fusion = adsk.core.Point3D.create(l2[0] * 0.1, l2[1] * 0.1, l2[2] *0.1)

                            out_vec_fusion = adsk.core.Vector3D.create(out_vec[0],out_vec[1],out_vec[2])

                            coll=rootcomp.findBRepUsingRay(l1_fusion, out_vec_fusion, 1, -1.0, True, l1_hit_points)

                            coll=rootcomp.findBRepUsingRay(l2_fusion, out_vec_fusion, 1, -1.0, True, l2_hit_points)

                            l1_fusion = l1_hit_points.item(0)

                            l2_fusion = l2_hit_points.item(0)

                            l1 = np.array([l1_fusion.x, l1_fusion.y, l1_fusion.z])

                            l1 *= 10

                            l2 = np.array([l2_fusion.x, l2_fusion.y, l2_fusion.z])

                            l2 *= 10

                            line_pairs.append([a1, l1])

                            line_pairs.append([a2, l2])

                        j += 1

                    if has_infinity == False:

                        cell.faces.append(face)

                voronoi_cells.append(cell)

        #create finite faces

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

        self.output.payload = np.array(line_pairs)

class VoronoiCell:
    def __init__(self, vertex_indices):
        self.vertex_indices = vertex_indices
        self.ridges = []
        self.ridge_indices = []
        self.faces = []

class VoronoiFace:
    def __init__(self):
        self.edges = []