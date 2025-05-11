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
        
        stitch_features = rootcomp.features.stitchFeatures

        base_feature = attributes[0].parent

        bodies = rootcomp.bRepBodies

        complex_boundary = self.boundary.parameter[0]

        bounding_box = complex_boundary.boundingBox

        #use this to detemine how much to offset clipped faces

        bounding_box_radii = (bounding_box.minPoint.distanceTo(bounding_box.maxPoint) / 2) * 10

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

        clipped_faces = [] #for storing finite clipped faces

        clipped_cells = []

        #compute some stats on the generated points

        input_points_center = vor.points.mean(axis=0)

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

                cell_infinity = any(v == -1 for v in cell.vertex_indices)

                for k in range(len(cell.ridges)):

                    j = 0

                    face = VoronoiFace()

                    ridge = cell.ridges[k]
                    
                    edge_len = len(ridge)

                    ridge_point_indices = cell.ridge_indices[k]

                    face_infinity = any(v == -1 for v in ridge)

                    while j < edge_len:

                        if j == edge_len - 1:

                            t = 0

                        else:

                            t = j + 1
                            
                        if cell_infinity == False:

                            v1_index = ridge[j]

                            v2_index = ridge[t]

                            v1 = vertices[v1_index]

                            v2 = vertices[v2_index]

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

                            a_dist = np.linalg.norm(l1_a - input_points_center)

                            b_dist = np.linalg.norm(l1_b - input_points_center)

                            # determine which direction sets the vector in the right direction

                            if a_dist > b_dist:

                                out_vec = out_vec

                            else:

                                out_vec = -out_vec

                            out_vec_unit = out_vec / np.linalg.norm(out_vec) #Get the out vector in unit vector form

                            l1 = l1 + out_vec_unit * bounding_box_radii

                            l2 = l2 + out_vec_unit * bounding_box_radii

                            line_pairs.append([a1, l1])

                            line_pairs.append([a2, l2])

                            #Add to clipped faces

                            voro_face = VoronoiFace()

                            voro_face.edges.append([a1, a2])

                            voro_face.edges.append([a2, l2])

                            voro_face.edges.append([l2, l1])

                            voro_face.edges.append([l1, a1])

                            clipped_faces.append(voro_face)

                        j += 1

                        cell.faces.append(face)

                if cell_infinity == False:

                    voronoi_cells.append(cell)

        #create finite cells

        for cell in voronoi_cells:

            #create the brep

            cell_brep_def = adsk.fusion.BRepBodyDefinition.create()

            cell_points = []

            for vertex_index in cell.vertex_indices:

                if vertex_index != -1:

                    cell_points.append(vertices[vertex_index])

            cell_points = np.array(cell_points)

            cell_center = cell_points.mean(axis=0) # find the center of the cell

            for face in cell.faces:

                edge_defs = []

                face_vec1 = None

                face_vec2 = None

                face_normal = None

                face_point = None

                for edge in face.edges:

                    #get the edge vertices and convert to fusion points

                    start = edge[0]

                    end = edge[1]

                    start_point = adsk.core.Point3D.create(start[0]*0.1, start[1]*0.1, start[2]*0.1)

                    end_point = adsk.core.Point3D.create(end[0]*0.1, end[1]*0.1, end[2]*0.1)

                    #construct the face normal and point

                    if face_vec1 is None:

                        face_vec1 = start - end
                        
                    elif face_vec2 is None:

                        face_vec2 = start - end

                    elif face_normal is None:

                        face_normal = np.cross(face_vec1, face_vec2) * 2

                        if not np.any(face_normal):

                            face_normal = None

                        else:

                            face_point = adsk.core.Point3D.create(start[0]*0.1, start[1]*0.1, start[2]*0.1)

                            face_offset1 = start + face_normal

                            face_offset2 = start - face_normal

                            offset_dist1 = np.linalg.norm(face_offset1 - cell_center)

                            offset_dist2 = np.linalg.norm(face_offset2 - cell_center)

                            if offset_dist2 > offset_dist1:

                                face_normal = -face_normal

                            face_normal = adsk.core.Vector3D.create(face_normal[0], face_normal[1], face_normal[2])

                    #create the edge definition

                    edge_defs.append(create_edge_def(cell_brep_def, start_point, end_point))

                face_plane = adsk.core.Plane.create(face_point, face_normal)

                create_face_for_body_def(cell_brep_def, face_plane, edge_defs)

            cell_brep = cell_brep_def.createBody()

            body = bodies.add(cell_brep, base_feature)

            body_coll = adsk.core.ObjectCollection.create()

            body_coll.add(body)

            val_input = adsk.core.ValueInput.createByString("0.25 mm")

            stitch_input = stitch_features.createInput(body_coll, val_input, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

            stitch_input.targetBaseFeature = base_feature

            stitch_features.add(stitch_input)

            base_bodies = base_feature.bodies

            b_count = base_bodies.count

            cell_body = base_bodies.item(b_count - 1)

            cell_body_copy = temp_brep_mgr.copy(cell_body)

            tool = temp_brep_mgr.copy(complex_boundary)

            temp_brep_mgr.booleanOperation(cell_body_copy, tool, adsk.fusion.BooleanTypes.IntersectionBooleanType)

            base_feature.updateBody(cell_body, cell_body_copy)

        adsk.doEvents()

        for face in clipped_faces:

            curves = []

            for edge in face.edges:

                start = edge[0]

                end = edge[1]

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

def create_edge_def(brep_def, start_point, end_point):

    # Create edge definition

    edgeDef = adsk.fusion.BRepEdgeDefinition.cast(None)

    # Create vertex definition

    start_vertex_def = brep_def.createVertexDefinition(start_point)

    end_vertex_def = brep_def.createVertexDefinition(end_point)  

    curve = adsk.core.Line3D.create(start_point, end_point)

    # Create edge definition by curve

    edgeDef = brep_def.createEdgeDefinitionByCurve(start_vertex_def, end_vertex_def, curve)
    
    return edgeDef   

def create_face_for_body_def(brep_def, surface, edge_defs):

    # Create face definition

    faceDef = adsk.fusion.BRepFaceDefinition.cast(None)
    
    # Create lump definition

    lumpDefs = brep_def.lumpDefinitions

    lumpDef = lumpDefs.add()

    # Create shell definition

    shellDefs = lumpDef.shellDefinitions

    shellDef = shellDefs.add()

    # Create face definition

    faceDefs = shellDef.faceDefinitions

    faceDef = faceDefs.add(surface, True)

    # Create loop definition

    loopDefs = faceDef.loopDefinitions

    loopdef = loopDefs.add()
    
    # Create coEdge definitions

    brepCoEdgeDefs = loopdef.bRepCoEdgeDefinitions   

    for edgeDef in edge_defs:

        brepCoEdgeDefs.add(edgeDef, True)

    return faceDef 